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
























