
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class TrainData(object):
    def __init__(self, dataframe):
        self.numerical_mapping = buildNumericalMapping(dataframe)
        self.df = dataframe.fillna(dataframe.mean())
        self.cat_mapping = buildCatMapping(self.df)


# Build category mapping for each column
def buildCatMapping(train):
    categorical_only = train.select_dtypes(['object'])
    cat_mapping = {} # key = (column, value), value = (rank, avg_price)
    for col, val in categorical_only.iteritems():
        unique = set(val.values)
        for unique_value in unique:
            if unique_value is np.nan:
                cat_mapping[(col, unique_value)] = train[train[col].isnull()]["SalePrice"].mean()
            else:
                cat_mapping[(col, unique_value)] = train[train[col] == unique_value]["SalePrice"].mean()

        # Set rankings
        sorted = []
        for unique_value in unique:
            sorted.append((cat_mapping[(col, unique_value)], unique_value))

        sorted.sort()
        rank = 1
        for element in sorted:
            cat_mapping[(col, element[1])] = (rank, cat_mapping[(col, element[1])])
            rank += 1

    return cat_mapping


# Build numerical mapping for each column
def buildNumericalMapping(train):
    numerical = train.select_dtypes(['int64', 'float64'])
    numerical_mapping = {}
    for col, val in numerical.iteritems():
        numerical_mapping[col] = val.mean()
    return numerical_mapping
