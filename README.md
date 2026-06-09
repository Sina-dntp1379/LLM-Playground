# DDOM Lab repository template
Template repo for DDOM Lab repositories.

Use this template to create new repositories for DDOM Lab projects. Doing this will ensure that the repository is properly configured with the necessary files and settings.

Once you've created your repo from the template, you should do the following on the local machine:
1. Clone the repository to your local machine.
2. Edit `environment.yml` to add the environment name, Python version, and any necessary packages.
3. Create a new conda environment using the `environment.yml` file: `conda env create -f environment.yml`.
4. Activate the new environment: `conda activate <environment_name>`.
5. Install `pre-commit` hooks: `pre-commit install`.

## `.gitignore`
The `.gitignore` file is configured to ignore common files and directories that should not be committed to the repository. The file is based on the `Python.gitignore` template provided by GitHub. Ignore statements for IDE files and directories are also included, as well as the `.DS_Store` file that macOS creates.

## `.pre-commit-config.yaml`
Pre-commits are run automatically on the local machine when a commit is made. They ensure that code is properly formatted and that there are no errors. We use `ruff` for linting and code formatting.

## `environment.yml`
The `environment.yml` file is used to create a new conda environment with the necessary packages for the project. The file should be edited to include the environment name, Python version, and any necessary packages.

## `LICENSE`
By default, our code is provided under the MIT License, but can be modified if necessary.

## `README.md`
This file provides a brief overview of the repository and should be updated to include information about the project, installation instructions, usage, etc.