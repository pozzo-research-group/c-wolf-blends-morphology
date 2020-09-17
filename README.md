# c-wolf-blends-morphology

[![DOI](https://zenodo.org/badge/293610449.svg)](https://zenodo.org/badge/latestdoi/293610449)

This directory contains all required Python scripts and Jupyter notebooks to analyze the data and reproduce the results presented in the following work:

> <a name="pub"></a> **Conformation of Polythiophene-Polystyrene Blends from Neutron and X-ray Scattering** (*in preparation*)

All raw data, fitting results and figures can be found as supplemental material for the above publication. By providing this material, we hope to increase transparency and reproducibility of our results. We encourage the use of the included material for new analysis methods in the future or to apply this analysis to new data. If you reference or utilize any of the provided material, we ask that you please acknowledge the [publication](#pub) (if using the supplemental data file) and this repo.

## Introduction

In this work, we explore the molecular morphology and self-assembly behavior of conjugted and non-conjugated polymer blends. We utilize methods of small-angle and ultra-small-angle neutron scattering (SANS and USANS, respectively), wide-angle X-ray scattering (WAXS), ultraviolet-visible spectroscopy (UV-Vis), electrochemical impedance spectroscopy (EIS) and visual inspection to qualitatively and quantitatively explore these systems. 

There are five primary sub-directories: `eis`, `photos`, `sans`, `uv_vis`, and `waxs` that include all of the required Python scripts and Jupyter notebooks to complete the analysis presented in the publication cited above. An additional `data` directory is also referenced, but is not provided in this repo. This directory includes all of the raw data and meta-data required for the analyses, fitting results, and generated figures. It is provided as a supplemental file to the [publication](#pub) above. High-level overviews for each of these primary components are discussed later in this README, but the general structure of this directory follows:

    cp-ps-blends/
        |- README.md
        |- environment.yml
        |- eis/
            |- TO BE COMPLETED
        |- photos/
            |- Image_Cropping.ipynb
            |- Image_Plotting.ipynb
        |- sans/
            |- Plotting_SANS_Data_with_Fits.ipynb
            |- Plotting_SANS_Data.ipynb
            |- Smeared_Data_Reduction.ipynb
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
            |- eis/
                |- TO BE COMPLETED
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
    
### `sasview` and `sasmodels`

Two additional packages must be installed using `pip`, which should be installed with the Anaconda package or with the previous command. If you still need to install pip, please follow the installation instructions found online. After ensuring `pip` is installed, run the following commands to install the `sasmodels` and `bumps` packages required for SANS data modelling:

    pip install sasmodels
    pip install bumps
    
You will also need to download the source code for both the `sasmodels` and `sasview` packages from their GitHub repositories. The `sasmodels` package can be found at <https://github.com/SasView/sasmodels> and the `sasview` package can be found at <https://github.com/SasView/sasview>. You can either download the source code directly from online, or you can clone the repositories using the following commands, being sure to run these commands from within the directory you would like to store the code on your computer:

    git clone https://github.com/sasview/sasmodels.git
    git clone https://github.com/sasview/sasview.git
    


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

<!--
## Sub-Directory Overviews

This section provides the user with high level descriptions of the five primary sub-directories, their contents, and the general analysis approach. The goal is to provide the user with enough information to help them find specific scripts, notebooks, or figures they may be interested in. However, we encourage the reader to explore the detailed comments and Markdown cells provided within each Python script or Jupyter ntoebook for step-by-step information.

### `photos`

Visual inspection of the samples was one of the first analyses performed after creating the solid films of conjugated polymer and polystyrene blends. The color provided the first clues of conformation changes within the conjugated phase. The original sample photos can be found at `data/photos/photo_files/`. The photos were then cropped using the `Image_Cropping.ipynb` notebook and arranged into the manuscript figures in `Image_Plotting.ipynb`. These figures can be found in the `data/photo_figures/` directory.

### `uv_vis`

Ultraviolet-visible spectroscopy, or UV-Vis, was performed to determine accurate concentrations in solid blends of a conjugated polymer and deuterated polystyrene. Three sections of each solid film were dissolved in chloroboenzene (replicates) and compared against a calibration curve created from solutions with known conjugated polymer and polystyrene amounts. This data was particularly important for modeling of the SANS data.

The raw UV-Vis data collected for both the solid sample replicates and the calibration curve solutions can be found at `data/uv_vis/uv_vis_data/`. Additional calibration curve data, including the known conjugated polymer concentration for each solution and the assignment of each sample to the appropriate calibration curve, is provided in the `data/Cal_Curve_wtPercents/` directory and `data/CalCurveAssign.csv` file, respectively. Finally, the complete analysis process can be found in the `UV-Vis_Analysis.ipynb` notebook. These results, including the calibrated wt% and vol% for each sample, are saved to the `data/Corrected_wtPercents.csv` file, which is referenced by the `sans`, `waxs`, and `eis` analyses.

### `sans`

Small-angle and ultra-small-angle neutron scattering data (SANS and USANS, respectively) were collected for solid blends of a conjugated polymer with deuterated polystyrene to quantitatively describe the phase interfaces as well as the shapes and sizes of formed 3D structures.

In the `data/sans` directory, the raw SANS and USANS can be found in `data/sans/Aug2019_SANS/`, `data/sans/Dec2019_SANS/` and `data/sans/USANS_smeared/` folders. The notebooks `Smeared_Data_Reduction.ipynb` compiles the SANS and USANS data for each sample, trims any noise from the data, and saves the final form in the folder `data/sans/Smeared_Data_20200629/`. Finally, the `Plotting_SANS_Data.ipynb` notebook plots this final data into concentration series of the conjugated polymer phase and saves them in the `SANS_Figures/` directory. The `data/sans/Sample_Info.csv` file is ued by these scripts (and many others) to define information about each sample, including the specific conjugated polymer and matrix polymer used as well as the assigned sample key. All scripts included here utilize these sample keys to easily track samples across all the different analyses. 

The Porod analysis was first performed to describe the interface between conjugated and non-conjugated components of the blend. This analysis can be found at `sans/Porod_analysis/`. Included are two notebooks, the first, `Porod_Analysis.ipynb`, automates the Porod fit for all samples and records that information in the `data/sans/Porod_analysis/porod_results/` directory. The second, `Plotting_Porod_Results.ipynb`, plots these fits (and the extracted data) and saves them in the `data/sans/Porod_analysis/porod_figures/` directory. 

A combined model was fit to all SANS/USANS profiles to account for both the polystyrene and conjugated polymer phases (more information can be found in the manuscript regarding these models). First, the polystyrene contribution was captured by performing simultaneous fits of the pure polystyrene control samples using the Guinier-Porod model. These results can be found in the `sans/PS_Fitting/` directory. The `Polystyrene_Fits.ipynb` notebook automates this fitting process, saving the results in sub-directories of the `data/sans/PS_Fitting/ps_fit_results/` directory. The fitting process was broken down into multiple steps, as discussed more thoroughly in the notebook. The `Plotting_PS_Fits.ipynb` notebook then plots these final fits, saving them to the `data/sans/PS_Fitting/ps_fit_results/figures` directory.

All combined fitting procedures can be found in the `sans/Sample_Fitting/` directory. In the `data/sans` directory, the `Fit_Truths.csv` file is referenced by these fitting scripts to determine which samples need to be fit with specific combined models. After the fits are completed and evaluated manually by the others, the final combined model for each sample was recorded in the `Fit_Finals.csv` file in the `data/sans` directory. [TO BE COMPLETED ONCE WE NARROW THESE DOWN].

### `waxs`


### `eis`
-->

    
    
    
