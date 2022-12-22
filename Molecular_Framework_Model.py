#!/usr/bin/env python
# coding: utf-8

# # **_Molecular Framework Database Building_**

# ## Environment Setting Up and Packages Importing:
#         !conda activate env-framework 
#         Please create the conda environment from the .yml file: framework.yml

import sys
import time

import pandas as pd
from tqdm import tqdm 
import pickle
import numpy as np

#RDKit:
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdchem
from rdkit.Chem.rdmolops import *
from rdkit.Chem import PandasTools
from rdkit.Chem.Draw import MolsToGridImage


# ### 1. Input the Data (usually for multiple-input-file cases):

# To check the time running the code:
start_time = time.time()


scr_path = sys.argv[1]
filename = (scr_path.split('/')[-1]).split('.')[0]

df_input = pd.read_csv(scr_path,  sep = ' ', header = None, names = ['SMILES'])



# #### (3) Clean the Raw Database:


# Remove the duplicates in the original dataset:
df_input.drop_duplicates(subset = "SMILES", keep = 'last', inplace = True)
df_input = df_input.reset_index(drop = True)
df_input


# To check the size of the database:
len(df_input)


output1 = 'This databse', filename, 'contains', len(df_input), 'compounds'


# ### 2. Create a Data Output Dataframe:


df_output = pd.DataFrame({'Input_Smiles':df_input['SMILES']}) 
df_output['Framework'] = 'framework'
df_output


# ### 3. Break Molecules from All SMILES:
# 
# 

# #### (1) Remove All the Non-Bond Ions:
#         Remove all the dissociation parts in the SMILES

# #### (2) Simplify All Bonds:
#         Convert all bonds into single bonds

# #### (3) Simplify All Atoms:
#         Convert all atoms into carbon atoms​

# #### (4) Remove All the Terminal Atoms​:
#         Get rid of all side chains, preserve only the main scaffold​


count = 0
my_list_invaild = []

for q in tqdm(range(0, len(df_output)), desc = 'Loop 1'):
    try:  
        # 1.remove all the non-bond ions:
        qsmiles = df_output['Input_Smiles'][q]
        qsmiles = qsmiles.replace('.[Li+]', '')
        qsmiles = qsmiles.replace('.[Na+]', '')
        qsmiles = qsmiles.replace('.[K+]', '')
        qsmiles = qsmiles.replace('.[F-]', '')
        qsmiles = qsmiles.replace('.[Cl-]', '')
        qsmiles = qsmiles.replace('.[Br-]', '')
        qsmiles = qsmiles.replace('.[I-]', '')
        #print(qsmiles)

        qmol = Chem.MolFromSmiles(qsmiles)
        qmolw = Chem.RWMol(qmol)

        # 2.make sure there is no more dissociation 
        if '.' not in qsmiles:
            
            if qmol and qmolw: 

                # 3.convert all bonds into single bonds:
                for bond in qmol.GetBonds():
                    bondtype = bond.GetBondType()

                    if bondtype != 'SINGLE':
                        qmol_begin = bond.GetBeginAtomIdx()
                        qmol_end = bond.GetEndAtomIdx()
                        qmolw.RemoveBond(qmol_begin, qmol_end)
                        qmolw.AddBond(qmol_begin, qmol_end, Chem.BondType.SINGLE)
    
                        new_mol = qmolw.GetMol()
                        new_smiles = Chem.MolToSmiles(new_mol)
                        qmol = new_mol
                        qmolw = Chem.RWMol(qmol)

                # 4.convert all atoms into carbon atoms:
                for atom in qmol.GetAtoms():
                    if atom != Chem.Atom(6):
                        i_non_carbon = atom.GetIdx()
                        qmolw.ReplaceAtom(i_non_carbon, Chem.Atom(6))
            
                        new_mol = qmolw.GetMol()
                        new_smiles = Chem.MolToSmiles(new_mol)
                        qmol = new_mol
                        qmolw = Chem.RWMol(qmol)
                        # print(new_smiles)

                # 5.remove all the terminal atoms:

                result_list = []

                while len(result_list) == len(set(result_list)):

                    for atom in qmol.GetAtoms():
                        
                        if atom.GetDegree() == 1:
                            result_list = list(set(result_list))
                            i = atom.GetIdx()
                            qmolw.RemoveAtom(i)
                            new_mol = qmolw.GetMol()   
                            new_smiles = Chem.MolToSmiles(new_mol)
                            qmol = Chem.MolFromSmiles(new_smiles)
                            qmolw = Chem.RWMol(qmol)
                            result_list.append(new_smiles)
                            # print('this is a terminal')
                            # print(result_list)
                            break

                        else:
                            # print('not a terminal')
                            result_list.append(new_smiles)
                            continue

                    # if len(result_list) != len(set(result_list)):
                        # print('Finish:', result_list)
                        # print(new_smiles)

                df_output['Framework'][q] = new_smiles
        
        else:
            count += 1
            my_list_invaild.append(q)
            continue

    except:
        count += 1
        my_list_invaild.append(q)
        continue

print(count, 'invalids')


# ### 4. Wrangling the Data Obtained :


# 1.Remove the invalid data: 
new_df = df_output.drop(my_list_invaild)

# Reset the index:
new_df = new_df.reset_index(drop = True)

print('After remove invalid data:', len(new_df))


# 2.Save the pickle file:
with open (filename + '-each-framework-without-ROMol.pickle','wb') as f:
    pickle.dump(new_df,f)

# 3.Add the frequencies and sort all the molecular frameworks:
new_df['Frequency'] = 1
df_result = new_df.groupby(['Framework'],as_index = False).agg({'Frequency': 'sum'})
df_result = df_result.sort_values(by=['Frequency'], ascending = False)

# Reset the index:
df_result = df_result.reset_index(drop = True)
df_result.head(10)


output2 = 'The number of frameworks obtained is:', len(df_result)-1



# 5.Save the pickle file:
with open (filename + '-frameworks-sorted-without-ROMol.pickle','wb') as f:
    pickle.dump(df_result,f)


# 5.Finish all the code running and print the key outputs:
end_time = time.time()
duration = round((end_time - start_time)/60)
output3 = 'This programme took', duration, 'minutes'

print(output1, output2, output3)


# ### 5. Display the Frameworks (ony for single-input-file cases, for multiple-input-file cases please use the 'merge' code):


# 1.Add ROMol to each framework:
PandasTools.AddMoleculeColumnToFrame(df_result, smilesCol = "Framework")
df_result.head(3)

# If the ROMols already have been added before, to display them again:
# PandasTools.RenderImagesInAllDataFrames(images=True)



# 2. Display the results (all or top 10000 frequent frameworks) in a .html file
df_result_top=df_result.head(10000)

fmolport = open(filename+'-top10000-frameworks-with-ROMol.html','w')
h = df_result.to_html()
fmolport.write(h)
fmolport.close()

