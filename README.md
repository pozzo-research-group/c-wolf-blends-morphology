# c-wolf-blends-morphology

[![DOI](https://zenodo.org/badge/293610449.svg)](https://zenodo.org/badge/latestdoi/293610449)

This directory contains all required Python scripts and Jupyter notebooks to analyze the data and reproduce the results presented in the following work:

> <a name="pub"></a> **Wolf, C. M.; Guio, L., Scheiwiller, S. C., O’Hara, R., Luscombe, C., Pozzo, L. D. *Blend Morphology in Polythiophene-Polystyrene Composites from Neutron and X-ray Scattering* 2020 (*submitted*).**

All raw data, fitting results and figures can be found as supporting information for the above publication. By providing this material, we hope to increase transparency and reproducibility of our results. We encourage the use of the included material for new analysis methods in the future or to apply this analysis to new data. If you reference or utilize any of the provided material, we ask that you please acknowledge the [publication](#pub) (if using the data provided in the supporting information) and this repo.

## Introduction

In this work, we explore the molecular morphology and self-assembly behavior of conjugted and non-conjugated polymer blends. We utilize methods of small-angle and ultra-small-angle neutron scattering (SANS and USANS, respectively), wide-angle X-ray scattering (WAXS), ultraviolet-visible spectroscopy (UV-Vis), electrochemical impedance spectroscopy (EIS) and visual inspection to qualitatively and quantitatively explore these systems. 

There are six primary sub-directories: `dsc`, `conductivity`, `photos`, `sans`, `uv_vis`, and `waxs` that include all of the required Python scripts and Jupyter notebooks to complete the analysis presented in the publication cited above. An additional `data` directory is also referenced, but is not provided in this repo. This directory includes all of the raw data and meta-data required for the analyses, fitting results, and generated figures. It is provided as supporting information to the [publication](#pub) above. High-level overviews for each of these primary components are discussed later in this README, but the general structure of this directory follows:

    cp-ps-blends/
        |- README.md
        |- environment.yml
        |- conductivity/
            |- TO BE COMPLETED
        |- dsc/
            |- Plotting_DSC_Data.ipynb
        |- photos/
            |- Image_Cropping.ipynb
            |- Image_Plotting.ipynb
        |- sans/
            |- Plotting_SANS_Data_with_Fits.ipynb
            |- Plotting_SANS_Data.ipynb
            |- Smeared_Data_Reduction.ipynb
            |- Liquid_Samples/
                |- ...
            |- Porod_analysis/
                |- Plotting_Porod_Results.ipynb
                |- Porod_Analysis.ipynb  
            |- PS_Fitting/
                |- Plotting_PS_Fits.ipynb
                |- Polystyrene_Fits.ipynb
            |- Sample_Fitting/
                |- TO BE COMPLETED
                |-
        |- uv_vis/
            |- UV-Vis_Analysis.ipynb
        |- waxs/
            |- TO BE COMPLETED
        |- data/
            |- conductivity/
                |- TO BE COMPLETED
            |- dsc/
                |- ...
            |- photos/
                |- photo_figures/
                    |- ...
                |- photo_files/
                    |- ...
            |- sans/
                |- Fit_Finals.csv
                |- Fit_Truths.csv
                |- Sample_Info.csv
                |- Aug2019_SANS/
                    |- ...
                |- Liquid_Samples/
                    |- ...
                |- Dec2019_SANS/
                    |- ...
                |- Porod_analysis/
                    |- porod_figures/
                        |- fits/
                            |- ...
                        |- sv_plots/
                            |- ...
                    |- porod_results/
                        |- ...    
                |- PS_Fitting/
                    |- ps_fit_results/
                        |- figures/
                            |- ...
                        |- guinier_porod_rg/
                            |- ...
                        |- guinier_porod_s_scale/
                            |- ...
                        |- power_law_background/
                            |- ...
                        |- power_law_porod_exp_scale/
                            |- ...
                |- Sample_Fitting/
                    |- TO BE COMPLETED
                    |- 
                |- SANS_Figures/
                    |- ...
                |- SANS_Figures_with_Fits/
                    |- ...
                |- Smeared_Data_20200629/
                    |- ...
                |- USANS_smeared/
                    |- ...
            |- uv_vis/
                |- Corrected_wtPercents.csv
                |- CalCurveAssign.csv
                |- Cal_Curve_wtPercents/
                    |- ...
                |- correction_figures/
                    |- ...
                |- calibration_figures/
                    |- ...
                |- sample_figures/
                    |- ...
                |- uv_vis_data/
                    |- ...
            |- waxs/
                |- TO BE COMPLETED

## Installation

### Python 3

All scripts and Jupyter notebooks require the use of Python 3. If you don't already have Python 3 installed on your computer, you can recommend installing the latest version of Anaconda, which includes the `conda` package manager. You can find the install files for your operating system at <https://www.anaconda.com/products/individual>.

### Creating the Environment 

We recommend creating a new Python environment with the required pacakges. More information about managing python environments with `conda` can be found at <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>. 

We have included an `environment.yml` file created from the environment that we currently use when running all scripts and notebooks. A new environment can be created from this file by running:

    conda env create -f environment.yml

Alternatively, you can create the environment and manually install the required packages. First, create a new Python 3 environment named `sasmodels` with the following command, changing the environment name if needed:

    conda create -n sasmodels python=3.8

Then 'activate' the environment by utilizing either:

    source activate sasmodels  

or  

    conda activate sasmodels
    
Next, install most of the required packages with the following command:

    conda install -c conda-forge numpy pandas matplotlib jupyter pyopencl scipy pillow lxml h5py ipykernel nb_conda_kernels pip
    
### Installing `sasview` and `sasmodels`

Two additional packages must be installed using `pip`, which should be installed with the Anaconda package or with the previous command. If you still need to install pip, please follow the installation instructions found online. After ensuring `pip` is installed, run the following commands to install the `sasmodels` and `bumps` packages required for SANS data modelling:

    pip install sasmodels
    pip install bumps
    
You will also need to download the source code for both the `sasmodels` and `sasview` packages from their GitHub repositories. The `sasmodels` package can be found at <https://github.com/SasView/sasmodels> and the `sasview` package can be found at <https://github.com/SasView/sasview>. You can either download the source code directly from online, or you can clone the repositories using the following commands, being sure to run these commands from within the directory you would like to store the code on your computer:

    git clone https://github.com/sasview/sasmodels.git
    git clone https://github.com/sasview/sasview.git
    
#### Adding `sasview` to your python path variable

Many of the `sasmodels` functions require the use of the `sasview` source code. After downloading the source code in the previous step, this can be achieved in one of two ways.

1. (Recommended) Add `/path/to/sasview/src` to your `PYTHONPATH` as needed within each Python script or Jupyter notebook. To do this, utilize the following lines at the beginning of your script where the import statements are made:

	    import sys
	    sys.path.append("/path/to/sasview/src")
	    import sas
	    
2. Permanently add `/path/to/sasview/src` to your operating system's `PYTHONPATH` variable. You can find instructions for your OS at <https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html>. 

## Usage

### Python scripts

The Python scripts (`.py` files) can be viewed with a text editor, and ran with the following command:

    python script_name.py

Some text editors can be particularly advantageous for increasing readibility of these scripts as they can dectect the programming language and provide helpful color-coding of comments, functions, variables, etc. Our favorites include [Atom](https://atom.io/), [Sublime](https://www.sublimetext.com/), or [Visual Studio Code](https://code.visualstudio.com/).

### Parallel Python scripts

Some of our sans modeling scripts were designed to run in parallel on the supercomputing cluster at the University of Washington, enabling us to fit SANS/USANS data for multiple samples simultaneously. These scripts are all named in the form `parallel_xxx.py` and utilize the `multiprocessing` Python package. More information can be found in the Python documentation [here](https://docs.python.org/3/library/multiprocessing.html) about this package. If running these specific scripts, please modify these functions within the script to reflect the available cores on your machine or uncomment the block of code that enables these files to run in serial. However, we caution the reader that these parallel scripts required 3 - 10 days of computational time on the cluster running on one node and using 27 of its cores (27 simultaneous fits). Therefore, running these scripts serially on one machine could require a large computational expense depending on the number of samples that are being fit.

### Jupyter notebooks

Jupyter notebooks (`.ipynb` files) can be described as a more interactive Python script, with blocks of code separated by additional material and resources formatted with Markdown. You can launch Jupyter from the command line and access all notebooks in that directory with:

    jupyter notebook
    
Alternatively, you can launch a specific jupyter notebook with the command:

    jupyter notebook notebook_name.ipynb

    
    
    
