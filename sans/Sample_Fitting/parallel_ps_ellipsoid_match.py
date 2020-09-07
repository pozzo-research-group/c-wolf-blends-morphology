import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

from bumps.names import *
from bumps.fitters import fit

import sasmodels

from sasmodels.core import load_model
from sasmodels.bumps_model import Model, Experiment
from sasmodels.data import load_data, plot_data, empty_data1D
from sasmodels.direct_model import DirectModel

import bumps

sys.path.append('/gscratch/stf/caitwolf/sans_fitting/python_install/sasview/src')
import sas

import multiprocessing as mp

# sample meta-data
sample_info = pd.read_csv('../Sample_Info.csv')

# helpful meta-data dictionaries
names = dict(zip(sample_info['Sample'], sample_info['Name']))
cps = dict(zip(sample_info['Sample'], sample_info['Conjugated Polymer']))
matrix = dict(zip(sample_info['Sample'], sample_info['Commodity Polymer']))
solvent_names = dict(zip(sample_info['Sample'], sample_info['Solvent']))

# target weight percents of conjugated polymer
target = dict(zip(sample_info['Sample'], sample_info['Target Fraction']*100))

# fixing 401/402 and 403/404 sample pair target values for plotting colors only
target[401] = 0.5
target[402] = 0.1
target[403] = 5
target[404] = 1

# actual volume percentages
data = np.loadtxt('../../uv_vis/Corrected_wtPercents.csv', delimiter=',', skiprows=1)
actual_vol = {}
actual_stdev_vol = {}
for key, tar, act, stdev, act_vol, stdev_vol in data:
    actual_vol[key] = act_vol
    actual_stdev_vol[key] = stdev_vol
    
slds = {'RRe-P3HT':0.676,
       'RRa-P3HT':0.676,
       'P3DDT':0.316,
       'PQT-12':0.676,
       #'Polystyrene-D8':6.407,
       'Polystyrene-D8':6.464, # density of 1.13 g/mL
       'Polystyrene-H8':1.426}

data_dir = '../Smeared_Data_20200629/'
files = os.listdir(data_dir)
sans_data = {}
usans_data = {}
for file in files:
    if 'USANS' in file:
        key = int(file.split('_')[0][3:])
        usans_data[key] = load_data(data_dir + file)
    elif 'SANS' in file:
        key = int(file.split('_')[0][3:])
        sans_data[key] = load_data(data_dir + file)
        
true_keys = []

true_reads = pd.read_csv('../Fit_Truths.csv')
true_reads = true_reads.to_numpy()
mask = true_reads[:,2].astype(bool)

ellipsoid_keys = true_reads[mask,0]

run_keys = list(ellipsoid_keys)

background_files = [file for file in os.listdir('../PS_Fitting/ps_fit_results/power_law_background') if 'json' in file]
backgrounds = {} # key is sample key, value is ('best', '95% confidence interval')
for file in background_files:
    data_read = pd.read_json('../PS_Fitting/ps_fit_results/power_law_background/' + file)
    key = int(file.split('_')[0][3:])
    p95 = data_read.loc['p95',str(key) + ' background']
    backgrounds[key] = (data_read.loc['best',str(key) + ' background'], p95)
    
power_law_fit_info = pd.read_json('../PS_Fitting/ps_fit_results/power_law_porod_exp_scale/PS_porod_exp_scale-err.json')
ps_scales = {}

for key, value in power_law_fit_info.items():
    if 'porod_exp' in key:
        ps_porod_exp = value['best']
        ps_porod_exp_95 = value['p95']
    else:
        key = int(key.split()[0])
        ps_scales[key] = (value['best'], value['p95'])
        
guinier_porod_fit = pd.read_json('../PS_Fitting/ps_fit_results/guinier_porod_s_scale/PS_s_scale-err.json')
rgs = {}
adjusted_scales = {}
for key, value in guinier_porod_fit.items():
    if key == 'ps s':
        ps_s = value['best']
        ps_s_95 = value['p95']
    elif 'rg' in key:
        key = int(key.split()[0])
        rgs[key] = (value['best'], value['p95'])
    elif 'scale' in key:
        key = int(key.split()[0])
        ps_scales[key] = (value['best'], value['p95'])
        
for key in rgs.keys():
    q1 = (1/rgs[key][0]) * np.sqrt((ps_porod_exp - ps_s)*(3-ps_s)/2)
    new_scale = ps_scales[key][0] * np.exp(-1*q1**2*rgs[key][0]**2/(3-ps_s)) * q1**(ps_porod_exp - ps_s)
    new_95p = np.array(ps_scales[key][1]) * np.exp(-1*q1**2*rgs[key][0]**2/(3-ps_s)) * q1**(ps_porod_exp - ps_s)
    adjusted_scales[key] = (new_scale, list(new_95p))

    
avg_rg = np.average([x[0] for x in rgs.values()])
max_rg = np.max([x[1][1] for x in rgs.values()])
min_rg = np.min([x[1][0] for x in rgs.values()])

avg_scale = np.average([x[0] for y, x in ps_scales.items() if y in rgs.keys()])
max_scale = np.average([x[1][1] for y, x in ps_scales.items() if y in rgs.keys()])
min_scale = np.average([x[1][0] for y, x in ps_scales.items() if y in rgs.keys()])

porod_files = [file for file in os.listdir('../Porod_analysis/porod_results') if 'json' in file]

for file in porod_files:
    data_read = pd.read_json('../Porod_analysis/porod_results/' + file)
    key = int(file.split('_')[0][3:])
    for column, value in data_read.items():
        if 'background' in column:
            backgrounds[key] = (value['best'], value['p95']) 
            
os.makedirs('fitting_results/ps_ellipsoid_match', exist_ok=True)
run_keys = [key for key in run_keys if key in actual_vol.keys() and key in usans_data.keys()]
            
def fit_function(
    key,
    sans_data,
    usans_data,
    actual_vol,
    actual_stdev_vol,
    backgrounds,
    avg_scale,
    avg_rg,
    ps_s,
    ps_porod_exp,
    slds,
    cps,
    matrix):

    #np.savetxt('Sample_'+str(key)+'.txt', np.array(['Fitting']), fmt='%s')
    kernel = load_model("guinier_porod+ellipsoid")


    # loading the data
    sans = sans_data[key]
    sans.dx = sans.dx-sans.dx # removing smearing from sans segment
    usans = usans_data[key]

    vol = actual_vol[key]/100 # cp volume fraction from uv-vis
    vol_stdev = actual_stdev_vol[key]/100

    # initial parameter values

    scale = Parameter(1, name=str(key) + 'scale')
    background = Parameter(backgrounds[key][0], name=str(key) + 'background')

    A_scale = Parameter(avg_scale*(1-vol), name=str(key) + ' PS scale')
    A_rg = Parameter(avg_rg, name=str(key) + ' PS rg')
    A_s = Parameter(ps_s, name=str(key) + ' PS s')
    A_porod_exp = Parameter(ps_porod_exp, name=str(key) + ' PS porod_exp')

    B_scale_normal = bumps.bounds.Normal(mean=vol, std=vol_stdev)
    B_scale = Parameter(vol, name=str(key) + ' sphere scale', bounds=B_scale_normal)

    B_sld = Parameter(slds[cps[key]], name=str(key) + ' PS sld')
    B_sld_solvent = Parameter(slds[matrix[key]], name=str(key) + ' PS solvent')

    B_radius_polar = Parameter(1000, limits=[0,inf], name=str(key) + ' ellipsoid polar radius')
    B_radius_polar_pd = Parameter(0.5, name = str(key) + ' ellipsoid polar radius pd')
    B_radius_polar_pd_n = Parameter(200, name = str(key) + ' ellipsoid polar radius pd n')
    B_radius_polar_pd_nsigma = Parameter(8, name = str(key) + ' ellipsoid polar radius pd nsigma') 

    B_radius_equatorial = Parameter(1000, limits=[0,inf], name=str(key) + ' ellipsoid equatorial radius')
    B_radius_equatorial_pd = Parameter(0.5, name = str(key) + ' ellipsoid equatorial radius pd')
    B_radius_equatorial_pd_n = Parameter(200, name = str(key) + ' ellipsoid equatorial radius pd n')
    B_radius_equatorial_pd_nsigma = Parameter(8, name = str(key) + ' ellipsoid equatorial radius pd nsigma') 

    # setting up the combined model for fitting
    sans_model = Model(
        model=kernel,
        scale=scale,
        background=background,
        A_scale=A_scale,
        A_rg=A_rg,
        A_s=A_s,
        A_porod_exp=A_porod_exp,
        B_scale=B_scale,
        B_sld=B_sld,
        B_sld_solvent=B_sld_solvent,
        B_radius_polar=B_radius_polar,
        B_radius_polar_pd_type='lognormal',
        B_radius_polar_pd=B_radius_polar_pd,
        B_radius_polar_pd_n=B_radius_polar_pd_n,
        B_radius_polar_pd_nsigma=B_radius_polar_pd_nsigma,
        B_radius_equatorial=B_radius_equatorial,
        B_radius_equatorial_pd_type='lognormal',
        B_radius_equatorial_pd=B_radius_equatorial_pd,
        B_radius_equatorial_pd_n=B_radius_equatorial_pd_n,
        B_radius_equatorial_pd_nsigma=B_radius_equatorial_pd_nsigma,
    )

    # setting parameter ranges as needed

    sans_model.B_radius_polar.range(0,200000)
    sans_model.B_radius_equatorial.range(0,200000)

    sans_experiment=Experiment(data=sans, model=sans_model)
    usans_experiment=Experiment(data=usans, model=sans_model)

    usans_smearing = sasmodels.resolution.Slit1D(usans.x, 0.117)
    usans_experiment.resolution = usans_smearing

    experiment = [sans_experiment, usans_experiment]

    problem=FitProblem(experiment)
    
    result=fit(problem, method='dream', samples=1e6, steps=1000, verbose=True)
    result.state.save('fitting_results/ps_ellipsoid_match/CMW' + str(key) + '_ps_ellipsoid_state')
    #result.state.show(figfile='fitting_results/ps_ellipsoid/CMW' + str(key) + '_ps_ellipsoid')
    #plt.close()
    #print_array = np.array(['Sample ' + str(key)])
    #np.savetxt('fitting_results/ps_ellipsoid/CMW' + str(key) + '.txt', print_array, fmt='%s')

pool = mp.Pool(27)
results = pool.starmap(fit_function, [(key,
    sans_data,
    usans_data,
    actual_vol,
    actual_stdev_vol,
    backgrounds,
    avg_scale,
    avg_rg,
    ps_s,
    ps_porod_exp,
    slds,
    cps,
    matrix) for key in run_keys])

pool.close()

