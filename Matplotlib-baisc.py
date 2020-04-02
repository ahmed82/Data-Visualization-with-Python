# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:28:51 2020

@author: ahmed
"""


import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library

"""Let's download and import our primary Canadian Immigration dataset using pandas read_excel() method. Normally,
 before we can do that, we would need to download a module which pandas requires to read in excel files.
 This module is xlrd. For your convenience, we have pre-installed this module, 
 so you would not have to worry about that. Otherwise, you would need to run the following
 line of code to install the xlrd module:

!conda install -c anaconda xlrd --yes
Now we are ready to read in our data."""


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)

print ('Data read into a pandas dataframe!')

df_can.head()
# tip: You can specify the number of rows you'd like to see as follows: df_can.head(10) 

#We can also veiw the bottom 5 rows of the dataset using the tail() function.
df_can.tail()

#When analyzing a dataset, it's always a good idea to start by getting basic information about your dataframe. We can do this by using the info() method.
df_can.info()

# To get the list of column headers we can call upon the dataframe's .columns parameter.
df_can.columns.values 
# Similarly, to get the list of indicies we use the `.index` parameter.
df_can.index.values

# Note: The default type of index and columns is NOT list.
print(type(df_can.columns))
print(type(df_can.index))

# To get the index and columns as lists, we can use the tolist() method.
df_can.columns.tolist()
df_can.index.tolist()

print (type(df_can.columns.tolist()))
print (type(df_can.index.tolist()))

# To view the dimensions of the dataframe, we use the .shape parameter.
# size of dataframe (rows, columns)
df_can.shape

# Note: The main types stored in pandas objects are float, int, bool, 
# datetime64[ns] and datetime64[ns, tz] (in >= 0.17.0), timedelta[ns], 
# category (in >= 0.15.0), and object (string). In addition these dtypes have 
# item sizes, e.g. int64 and int32.

"""Let's clean the data set to remove a few unnecessary columns. 
We can use pandas drop() method as follows:"""
# in pandas axis=0 represents rows (default) and axis=1 represents columns.
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)
df_can.head(2)


"""Let's rename the columns so that they make sense. We can use rename() 
method by passing in a dictionary of old and new names as follows:"""
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region'}, inplace=True)
df_can.columns

# We will also add a 'Total' column that sums up the total immigrants 
# by country over the entire period 1980 - 2013, as follows:
df_can['Total'] = df_can.sum(axis=1)
    
# We can check to see how many null objects we have in the dataset as follows:
df_can.isnull().sum()
    
# Finally, let's view a quick summary of each column in our dataframe using the describe() method.
df_can.describe()
    
"""pandas Intermediate: Indexing and Selection (slicing)

Select Column
There are two ways to filter on a column name:

Method 1: Quick and easy, but only works if the column name does NOT have spaces or special characters.

    df.column_name 
        (returns series)
Method 2: More robust, and can filter on multiple columns.

    df['column']  
        (returns series)
    df[['column 1', 'column 2']] 
        (returns dataframe)
Example: Let's try filtering on the list of countries ('Country')."""
df_can.Country  # returns a series
    
# Let's try filtering on the list of countries ('OdName') and the data for years: 1980 - 1985.
df_can[['Country', 1980, 1981, 1982, 1983, 1984, 1985]] # returns a dataframe
# notice that 'Country' is string, and the years are integers. 
# for the sake of consistency, we will convert all column names to string later on.

"""Select Row
There are main 3 ways to select rows:

    df.loc[label]        
        #filters by the labels of the index/column
    df.iloc[index]       
        #filters by the positions of the index/column
Before we proceed, notice that the defaul index of the dataset is a numeric range from 0 to 194. 
This makes it very difficult to do a query by a specific country. 
For example to search for data on Japan, we need to know the corressponding index value.

This can be fixed very easily by setting the 'Country' column as the index using set_index() method."""

df_can.set_index('Country', inplace=True)
# tip: The opposite of set is reset. So to reset the index, we can use df_can.reset_index()

# optional: to remove the name of the index
df_can.index.name = None

"""Example: Let's view the number of immigrants from Japan (row 87) for the following scenarios: 
    1. The full row data (all columns) 
    2. For year 2013 
    3. For years 1980 to 1985"""

# 1. the full row data (all columns)
print(df_can.loc['Japan'])

# alternate methods
print(df_can.iloc[87])
print(df_can[df_can.index == 'Japan'].T.squeeze())

# 2. for year 2013
print(df_can.loc['Japan', 2013])

# alternate method
print(df_can.iloc[87, 36]) # year 2013 is the last column, with a positional index of 36


# 3. for years 1980 to 1985
print(df_can.loc['Japan', [1980, 1981, 1982, 1983, 1984, 1984]])
print(df_can.iloc[87, [3, 4, 5, 6, 7, 8]])

"""Column names that are integers (such as the years) might introduce some confusion. 
For example, when we are referencing the year 2013, one might confuse that when the 2013th positional index.

To avoid this ambuigity, let's convert the column names into strings: '1980' to '2013'."""

df_can.columns = list(map(str, df_can.columns))
# [print (type(x)) for x in df_can.columns.values] #<-- uncomment to check type of column headers






















