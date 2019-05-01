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

def question_2(df, return_all=False, ntop=10, return_type='dict'):
    """
    This function determines which DRGs form the largest portion of the
    patient population for each facility.

    Parameters
    ------------
    df : `pandas.DataFrame`
        DataFrame containing the original information about DRG.

    return_all : `bool`, optional
        If `True`, the function returns the complete dictionary for all of
        the facilities that includes ``all`` of the different DRGs treated
        at each facilities. This variable is set to `False` by default.

    ntop : `int`, optional
        Number of top DRGs to return. This variable is only used when
        ``return_all = False``. Otherwise, it is not used.
        This variable is set to ``10`` by default.

    return_type : {`pd`, `dict`}, optional
        Option for which type of element to return. This variable is set
        to `dict` by default.

        Options:
            - `dict` : A dictionary is returned with info on DRGs for each provider
            - `pd` : A DataFrame is returned with info on DRGs for each provider

    Returns
    ---------
    return_obj : {`dict`, `pandas.DataFrame`}
        Python dictionary or `pandas.DataFrame` with the information on
        DRGs for each of the different facilities. This variable depends
        on the value of `return_type`.
    """
    # Columns to keep
    disch_col = 'total_discharges'
    prov_col  = 'provider_name'
    drg_col   = 'drg_definition'
    cols_keep = [prov_col, disch_col, drg_col]
    # Creating sub-DataFrame
    prov_main_df = df.loc[:, cols_keep]
    # Unique set of providers
    prov_unq  = prov_main_df[prov_col].unique()
    # Unique facilities
    print('There are `{0}` unique facilities'.format(prov_unq.shape[0]))
    # Saving output file as dictionary
    # Initializing dictionary
    prov_dict = {}
    # Looping over each unique facility and sorting DRGs by number of patients
    tqdm_msg = 'Unique providers: '
    for prov_ii in tqdm(prov_unq, desc=tqdm_msg):
        if return_all:
            prov_dict[prov_ii] = (prov_main_df.loc[
                prov_main_df[prov_col] == prov_ii]
                .sort_values(by=disch_col, ascending=False)
                .reset_index(drop=True)
                .drop(prov_col, axis=1))
        else:
            prov_dict[prov_ii] = (prov_main_df.loc[
                prov_main_df[prov_col] == prov_ii]
                .sort_values(by=disch_col, ascending=False)
                .reset_index(drop=True)
                .drop(prov_col, axis=1)).head(ntop)
    # Creating DataFrame with the most common DRG per facility
    if (return_type == 'pd'):
        # Grouping by facilities and selecting the DRG with largest
        # number of discharge
        prov_grouped = [[] for x in range(prov_unq.shape[0])]
        # Looping over all unique facilities
        for ii, prov_ii in enumerate(tqdm(prov_unq)):
            prov_ii_pd = prov_dict[prov_ii].head(1)
            prov_grouped[ii] = prov_dict[prov_ii].head(1)
        # Concatenating list
        prov_max_grouped = pd.concat(prov_grouped).reset_index(drop=True)
        # Adding column
        prov_max_grouped.loc[:, prov_col] = prov_unq
        # Rearranging column order
        prov_max_grouped = (prov_max_grouped[[prov_col, drg_col, disch_col]]
                            .sort_values(prov_col).reset_index(drop=True))

    if (return_type == 'dict'):
        return_obj = prov_dict
    elif (return_type == 'pd'):
        return_obj = prov_max_grouped

    return return_obj

###############################################################################

# Question 3
# Calculate the average Medicare payments per DRG per facility.

def question_3(df):
    """
    This functions determines the average Medicare payments per DRG per
    facility.

    Parameters
    ------------
    df : `pandas.DataFrame`
        DataFrame containing the original information about DRG.

    Returns
    --------
    medicare_pd : `pandas.DataFrame`
        DataFrame containing information about the average Medicare
        payments per DRG per facility
    """
    # Columns to keep
    disch_col = 'total_discharges'
    prov_col  = 'provider_name'
    drg_col   = 'drg_definition'
    medi_col  = 'average_medicare_payments'
    cols_keep = [prov_col, disch_col, drg_col, medi_col]
    # Creating sub-DataFrame
    med_main_df = df.loc[:, cols_keep]
    # Grouping by DRG and facility
    medicare_pd = (med_main_df.groupby([drg_col, prov_col])
                    .mean()).drop(disch_col, axis=1)

    return medicare_pd

###############################################################################












###############################################################################


def main(args):
    """
    Main Function to answer the questions
    """
    # Extracting and cleaning data
    df = data_extract_clean()
    # Question 1
    question_1(df)
    # Question 2
    prov_obj = question_2(df, return_type='pd')
    # Question 3
    medicare_pd = question_3()
    # Question 4

# Main function
if __name__=='__main__':
    # Main Function
    main(args)
