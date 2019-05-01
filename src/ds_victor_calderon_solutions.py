#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Victor Calderon
# Created      : 2019-04-30
# Last Modified: 2019-04-30
# Vanderbilt University
from __future__ import absolute_import, division, print_function 
__author__     = ['Victor Calderon']
__copyright__  = ["Copyright 2018 Victor Calderon, "]
__email__      = ['victor.calderon@vanderbilt.edu']
__maintainer__ = ['Victor Calderon']
"""
Solutions to the Data Science Problems
"""
# Importing modules
import numpy as np
import pandas as pd
from tqdm import tqdm

# Extra-modules
import argparse
from argparse import ArgumentParser
from argparse import HelpFormatter
from operator import attrgetter

## Functions

###############################################################################

def data_extract_clean():
    """
    This function extracts the data and cleans it in order to make it
    ready for the data analysis.

    Returns
    -----------
    df : `pandas.DataFrame`
        Clean DataFrame containing information about each type of DRG
    """
    # Path to the main file
    filepath = '../data/CMS_Medicare_OpenSource_Data.zip'

    # Reading in data
    df = pd.read_pickle(filepath, compression='zip')

    # Fixing columns by deleting unnecessary spaces
    cols_dict = dict([[x, '_'.join(x.split()).lower()] for x in df.columns.values])
    df.rename(columns=cols_dict, inplace=True)

    # Removing odd dollar symbols
    avg_cols = ['average_covered_charges', 'average_total_payments',
                'average_medicare_payments']
    for avg_ii in avg_cols:
        df.loc[:, avg_ii] = (df[avg_ii]
                                .replace( '[\$,)]','', regex=True )
                                .replace( '[(]','-',   regex=True )
                                .astype(float))

    return df

###############################################################################

# Question 1
# Which types of DRGs ("DRG.Definition") account for most of the patient
# population across all facilities?

def question_1(df, ntop=10):
    """
    Determines the top `ntop` DRGs that account for most of the patient
    population across all facilities

    Parameters
    ------------
    df : `pandas.DataFrame`
        DataFrame containing the original information about DRG.

    ntop : `int`, optional
        Number of top DRG elements to show. This variable is set to ``10``
        by default.
    """
    # Checking input parameters
    if not (ntop > 0):
        msg = '`ntop` ({0}) must be larger than `0`!'.format(ntop)
        raise ValueError(msg)
    # Column names to keep
    colnames = ['drg_definition', 'total_discharges']

    # First I need to group each DRG by the total number of patient
    # discharges.
    drg_patient_top = (df.loc[:, colnames].groupby('drg_definition')
                        .count()
                        .sort_values('total_discharges', ascending=False)
                        .reset_index())
    # Printing out the top `ntop` values
    for ii in range(ntop):
        msg = '{0}. - DRG: {1} - Discharges: {2}'.format(ii + 1,
            *drg_patient_top.iloc[ii].values)
        print(msg)

###############################################################################

# Question 2
# For each facility ("Provider.Name"), which DRGs form the largest portion
# of the patient population?

def question_2(df):
    """
    This function determines which DRGs form the largest portion of the
    patient population for each facility.

    Parameters
    ------------
    df : `pandas.DataFrame`
        DataFrame containing the original information about DRG.

    Returns
    ---------
    prov_dict : `dict`
        Dictionary containing 
    """









###############################################################################








###############################################################################












###############################################################################


def main(args):
    """
    Main Function to answer the questions
    """
    # Extracting and cleaning data
    df = data_extract_clean()
    # Question 1
    # Question 2
    # Question 3
    # Question 4

# Main function
if __name__=='__main__':
    # Main Function
    main(args)
