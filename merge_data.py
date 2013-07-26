""" Match the CPS data with BLS data based on MSA"""

import pandas as pd
import numpy as np

def read_cps():
    """ Read CPS data
     Must convert .sav file to .csv first """
    #cps = pd.read_csv('cdc_open211/cdc.csv', sep=' ', error_bad_lines = False, warn_bad_lines = False)
    cps = pd.read_csv('cdc.csv', sep=' ', error_bad_lines = False, warn_bad_lines = False)
    print cps.columns
    print cps.head(1)
    print "Shape:", cps.shape
    print
    
    # Only need certain columns
    cps = cps[['gtcbsa', 'income']]
    
    # Print the first region entry
    print cps['gtcbsa'].iloc[0]
    return cps

def read_occ():
    """ Read the Occupation data, just one part for now"""
    
    #Need new pandas .12 to do this
    #occ = pd.read_excel('cdc_open211/oesm12ma/aMSA_M2012_dl.xls', 'AMSA_dl') # Magic!
    occ = pd.read_excel('oesm12ma/aMSA_M2012_dl.xls', 'AMSA_dl') # Magic!
    
    print occ.columns
    print occ.head(1)
    return occ


# Check for match
cps = read_cps()
occ = read_occ()
print occ[occ['AREA_NAME'] == "San Francisco-Oakland-Fremont, CA"]['AREA_NAME'].head(1)
print cps[cps['gtcbsa'] == "San Francisco-Oakland-Fremont, CA"]['gtcbsa'].head(1)
# Yes it matches!

# Narrow the data
tot_pop = occ[occ['OCC_TITLE'] == "All Occupations"][['TOT_EMP','AREA_NAME','A_MEDIAN']]

occ = occ[occ['OCC_TITLE'] == "Community and Social Service Occupations"][['TOT_EMP','AREA_NAME','A_MEDIAN']]
occ = occ.rename(columns={'TOT_EMP':'SS Employed', 'A_MEDIAN':'SS Med Salary'})
# Includes Clery for now (Use 21-1___ to exclude later)
# Output is one line per MSA

# Narrow it down for now
#cps = cps[cps['gtcbsa'] == "San Francisco-Oakland-Fremont, CA"]
#occ = occ[occ['AREA_NAME'] == "San Francisco-Oakland-Fremont, CA"]
cps_income = pd.DataFrame(pd.pivot_table(cps, values ='income', rows = 'gtcbsa', aggfunc = 'median'))
m = pd.merge(occ, cps_income, how='left', left_on='AREA_NAME', right_index = True ) # right_on = 'index')
m = pd.merge(m, tot_pop, how = 'left', on='AREA_NAME')
#m = m[['AREA_NAME','A_MEDIAN', 'TOT_EMP','income']]
m.to_csv('merged_cps.csv')
#print cps['income'].head()
