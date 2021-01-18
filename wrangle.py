'''
Module for wrangling data: cleans and prepares all data sets for analysis 
'''

import numpy as np
import pandas as pd

POPS = ["data/pop_90-99.csv", "data/pop_00-10.csv", "data/pop_10-19.csv"]

def load_clean_pop(filepath):
    '''
    Imports and cleans a census estimates dataframe

    Inputs: 
        filepath (str): the string for the filepath

    Returns: 
        pop_df (pandas df): cleaned dataframe of population data
    '''

    df = pd.read_csv(filepath, header=3, thousands=",")
    df.columns = df.columns.str.lower()
    df = df.dropna()

    keep_cols = [col for col in df.columns if "-" not in col]
    df_yrs = df[keep_cols]

    states_mask = df_yrs.iloc[:, 0].str.startswith(".")
    df_states = df_yrs.loc[states_mask, :]
    df_states.reset_index(drop=True, inplace=True)
    
    if "unnamed" in df_states.columns[0]:
        df_states = df_states.rename(columns={"unnamed: 0": "geography"})

    return df_states


def merge_pop(files=POPS):
    '''
    Loads, cleans, and merges all three population data sets

    Inputs: 
        files (lst): list of filepaths for the three data sets (constant)

    Returns:
        pop_df (pandas df): a dataframe of population data from 1990-2019
    '''
    pop_df = load_clean_pop(files[0])

    for filename in files[1:]:
        df = load_clean_pop(filename)
        pop_df = pop_df.merge(df, how="inner", on="geography")

    drop_cols = [col for col in pop_df.columns if \
                 col != "geography" and len(col) > 4]
    pop_df.drop(columns=drop_cols, inplace=True)

    pop_df["geography"] = pop_df["geography"].str.lower().str.strip(".")

    return pop_df
    