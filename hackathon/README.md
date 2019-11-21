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

