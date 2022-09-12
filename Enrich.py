#import necessary packages
import pandas as pd 
import numpy as np
from tableone import TableOne as t1 #make sure to have T and O upercase for import
import researchpy as rp #needed to pip3 install researchpy but was already installed and after being already installed, used import command which then weridly enough worked
#setting data 
sparcs = pd.read_csv('dataset/SPARCS.csv')
blt = pd.read_csv('dataset/Childhood_blood_lead_testing_Testing.csv')
#cleaning data
blt.columns = blt.columns.str.replace('[^A-Za-z0-9]+', '_')
sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_')
list(sparcs)
list(blt)

#choosing columns and a name for subvariable
blt_zip = blt[['Zip', 'Tests']]
print(blt_zip.head(5).to_markdown())
sparcs_enrich = sparcs['Zip_Code_3_digits', 'Hospital_County']
print(sparcs_enrich.sample(10).to_markdown())

# need to change dtype to int for both zip & #of tests
print(sparcs_enrich[sparcs_enrich['Zip_Code_3_digits'].isnull()])
sparcs_enrich['Zip_Code_3_digits']= pd.to_numeric(sparcs_enrich['Zip_Code_3_digits'], errors='coerce')
sparcs_enrich = sparcs_enrich.dropna(subset=['Zip_Code_3_digits'])
sparcs_enrich['Zip_Code_3_digits'] = sparcs_enrich['Zip_Code_3_digits'].astype(int)

print(blt_zip[blt_zip['Tests'].isnull()])
blt_zip['Tests']= pd.to_numeric(blt_zip['Tests'], errors='coerce')
blt_zip = blt_zip.dropna(subset=['Tests'])
blt_zip['Tests'] = blt_zip['Tests'].astype(str).astype(int)

# Merges the data we are looking for 
enriched = sparcs_enrich.merge(blt_zip, how='left', left_on='Zip_Code_3_digits', right_on='Zip')
enriched.shape 
enriched
#same number of rows from sparcs_enrich but now two more columns
# from the blt_zip set
# problem with NAN still being their
enriched.to_csv('dataset/enriched.csv')
#saved csv however numbers are still in NAN and cannot change probably due 
# potentiall not being able to correlate both zips with each other
# used concat function but still coming up with NAN 
combined = pd.concat([sparcs_enrich, blt_zip])
combined
combined.to_csv('dataset/combined.csv')