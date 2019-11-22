# Hackathon

This directory is for placing useful inputs and outputs from our hackathon
projects.

## Starting Point for "Creating an Operator"

The notebook `generic.ipynb` can be used as a stub for creating a new operator.

## Workflow

We'll develop the projects using a common fork/pull request workflow.

1. Every project will fork https://github.com/hpc4cmb/toast-workshop-trieste-2019 to create their own copy of the repository. Use the "Fork" button at the upper right hand corner of the github window.

2. Rename your remote to `upstream`:
```
cd toast-workshop-trieste-2019
git remote rename origin upstream
```

3. Setup your fork as the `origin` remote:

```
git remote add origin git checkout https://github.com/<YOUR GITHUB USERNAME>/toast-workshop-trieste-2019

```

Fetch all the branches of that remote into remote-tracking branches,
such as upstream/master:

```
git fetch upstream
```

Create a new `hackathon` branch:

```
git checkout -b hackathon
```

## Setup on laptop

### Install TOAST

You can install TOAST easily on your laptop using the conda package, [see the documentation](https://toast-cmb.readthedocs.io/en/latest/install.html#conda-packages)

### Checkout a copy of the workshop notebooks

Checkout a copy of your fork on your laptop

    export GITHUBUSERNAME='your-github-username`
    git clone git@github.com:$GITHUBUSERNAME/toast-workshop-trieste-2019

### Execute notebooks locally

Activate the conda environment where you installed TOAST:

    conda activate toast

Install the required packages (from root folder of the repository):

    conda install --file requirements.txt

Install JupyterLab in the environment:

    conda install jupyterlab
    jupyter lab
