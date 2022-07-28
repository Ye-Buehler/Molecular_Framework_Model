# Molecular Framework Model

Thank you for your interest in this repo complementing the "[Molecular Framework Analysis of the Drug-like Chemical Space](https:)" publication.

## Requirements
### You have installed anaconda or miniconda with python 3.6 - 3.9
### Install conda environment

The requirements for the environment are given in the framework.yml file
<Br/>`conda env create -f framework.yml`

Specific packages used are also listed below:
  - ipykernel >= 6.4.1
  - numpy >= 1.21.2
  - pandas >= 1.4.1
  - pickleshare >= 0.7.5
  - rdkit >= 2021.09.4
  - tqdm >= 4.63.0
  
### Conda environment activation
 `conda activate env-framework`
 
## Quickstart

### Example

*example1.smi* and *example2.smi* files in folder *example* are provided for the Molecular Framework Model demonstration.

  - The model can be executed by using the following command and the python script *Molecular_Framework_Model.py*
<Br/>`python Molecular_Framework_Model.py example1.smi`

  - The model can also be carried out by appying the script *Molecular_Framework_Model.ipynb* in the Jupyter Notebook

The two approaches above will both yield two .pickle files containining the framework for each molecule in the sample pool (you can find these data in folder *example/results_of_each_example*) and the final framework dataset after combining the duplicates and sorting their frequency (you can find these final framework datasets for two examples in folder *results_merging/results/* for further steps of merging, etc.). 

A .html file elaborating the final framework results can be also obtained for each approach.

### Results Merging

For very large databases, we usually have to split the databases or even using high performance computer clusters to treat them parallely. 

Therefore, an efficient script for merging all the results for each sub-databases is necessary. 

In folder *results_merging* you can see the file down below which will realize this merging process.

<Br/>`Molecular_Framework_Results_Merge.ipynb`

<Br/>Then all or top 10000 sorted frameworks for the entire database can be displayed in a .html file. 

<Br/>You can also save the SMILES of frameworks on your own or utlize the *results_merged.pickle* file, and then display them with softwares like ChemDraw or Marvin.*top-10000-results-with-ROMol.html* in the same folder shows the framework dataset built from the two combined expamles.

## Contributing

We welcome contributions, in the form of issues or pull requests.

If you have a question or want to report a bug, please submit an issue.

To contribute with code to the project, follow these steps:
1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the remote branch: `git push`
5. Create the pull request.

## Contributors

* [@Ye-Buehler](https://github.com/Ye-Buehler)

The contributors have limited time for support questions, but please do not hesitate to submit an issue (see above).
 
## Citation 

## License

The software is licensed under the MIT license (see LICENSE file), and is free and provided as-is.
