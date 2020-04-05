# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 01:20:16 2020

@author: ahmed

Generating Maps with Python
"""
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library

# conda install folium -c conda-forge

import folium

# define the world map
world_map = folium.Map()

# display world map
world_map
iraq_map = folium.Map(location=[33.312805, 44.361488])
# define the world map centered around Baghdad with a higher zoom level
Baghdad_map = folium.Map(location=[33.312805, 44.361488], zoom_start=11)

# display world map
Baghdad_map
Baghdad_map.save('maps/Baghdad_map.html')

# define Mexico's geolocation coordinates
mexico_latitude = 23.6345 
mexico_longitude = -102.5528

mexico_map = folium.Map(location=[mexico_latitude, mexico_longitude], zoom_start=4)
mexico_map

""" ############################# A. Stamen Toner Maps ######################
These are high-contrast B+W (black and white) maps. 
They are perfect for data mashups and exploring river meanders and coastal zones.
"""

# create a Stamen Toner map of the world centered around Middle East
world_map = folium.Map(location=[33.312805, 44.361488], zoom_start=4, tiles='Stamen Toner')
# display map
world_map
world_map.save('maps/Stamen-Toner.html')

""" ############################ B. Stamen Terrain Maps ######################
These are maps that feature hill shading and natural vegetation colors. 
They showcase advanced labeling and linework generalization of dual-carriageway roads."""

# create a Stamen Toner map of the world centered around Middle East
world_map = folium.Map(location=[33.312805, 44.361488], zoom_start=4, tiles='Stamen Terrain')

# display map
world_map
world_map.save('maps/Stamen-Terrain.html')


""" ############################ C. Mapbox Bright Maps ############################
These are maps that quite similar to the default style, except that the borders 
are not visible with a low zoom level. Furthermore, unlike the default style where 
country names are displayed in each country's native language, 
Mapbox Bright style displays all country names in English."""
# create a world map with a Mapbox Bright style.
world_map = folium.Map(location=[33.312805, 44.361488],tiles='Mapbox Bright')

# display the map
world_map
world_map.save('maps/Mapbox-Bright.html')


""" ############################ Maps with Markers ############################ """

df_incidents = pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Police_Department_Incidents_-_Previous_Year__2016_.csv')

print('Dataset downloaded and read into a pandas dataframe!')
df_incidents.head()
"""So each row consists of 13 features:
> 1. **IncidntNum**: Incident Number
> 2. **Category**: Category of crime or incident
> 3. **Descript**: Description of the crime or incident
> 4. **DayOfWeek**: The day of week on which the incident occurred
> 5. **Date**: The Date on which the incident occurred
> 6. **Time**: The time of day on which the incident occurred
> 7. **PdDistrict**: The police department district
> 8. **Resolution**: The resolution of the crime in terms whether the perpetrator was arrested or not
> 9. **Address**: The closest address to where the incident took place
> 10. **X**: The longitude value of the crime location 
> 11. **Y**: The latitude value of the crime location
> 12. **Location**: A tuple of the latitude and the longitude values
> 13. **PdId**: The police department ID"""
# Let's find out how many entries there are in our dataset.
df_incidents.shape
"""df_incidents.shape
So the dataframe consists of 150,500 crimes, which took place in the year 2016. 
In order to reduce computational cost, let's just work with the first 100 incidents in this dataset."""
# get the first 100 crimes in the df_incidents dataframe
limit = 100
df_incidents = df_incidents.iloc[0:limit, :]
"""Now that we reduced the data a little bit, let's visualize where these crimes took place in the city of San Francisco. We will use the default style and we will initialize the zoom level to 12."""
# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42
# create map and display it
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# display the map of San Francisco
sanfran_map.save('maps/sanfran_map.html')

"""
Now let's superimpose the locations of the crimes onto the map. 
The way to do that in Folium is to create a feature group with its own features 
and style and then add it to the sanfran_map.
"""
# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through the 100 crimes and add each to the incidents feature group
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        #folium.features.CircleMarker(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add incidents to map
sanfran_map.add_child(incidents)

"""
You can also add some pop-up text that would get displayed when you hover over a marker. 
Let's make each marker display the category of the crime when hovered over."""
# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through the 100 crimes and add each to the incidents feature group
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add pop-up text to each marker on the map
latitudes = list(df_incidents.Y)
longitudes = list(df_incidents.X)
labels = list(df_incidents.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(sanfran_map)    
    
# add incidents to map
sanfran_map.add_child(incidents)


"""If you find the map to be so congested will all these markers, 
there are two remedies to this problem. The simpler solution is to remove these 
location markers and just add the text to the circle markers themselves as follows:"""

# create map and display it
sanfran_map2 = folium.Map(location=[latitude, longitude], zoom_start=12)

# loop through the 100 crimes and add each to the map
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.vector_layers.CircleMarker(
        [lat, lng],
        radius=5, # define how big you want the circle markers to be
        color='yellow',
        fill=True,
        popup=label,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(sanfran_map2)

# show map
sanfran_map2
sanfran_map2.save('maps/sanfran_map2.html')

""" The other proper remedy is to group the markers into different clusters. 
Each cluster is then represented by the number of crimes in each neighborhood. 
These clusters can be thought of as pockets of San Francisco which you can then analyze separately.

To implement this, we start off by instantiating a MarkerCluster object and 
adding all the data points in the dataframe to this object."""
from folium import plugins

# let's start again with a clean copy of the map of San Francisco
sanfran_map3 = folium.Map(location = [latitude, longitude], zoom_start = 12)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(sanfran_map3)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# display map
sanfran_map3
sanfran_map3.save('maps/sanfran_map3.html')




""" ###########################  Choropleth Maps ###############################
A Choropleth map is a thematic map in which areas are shaded or patterned in 
proportion to the measurement of the statistical variable being displayed on the map, 
such as population density or per-capita income. The choropleth map provides an 
easy way to visualize how a measurement varies across a geographic area or it 
shows the level of variability within a region. Below is a Choropleth map of the US 
 depicting the population by square mile per state."""


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                     sheet_name='Canada by Citizenship',
                     skiprows=range(20),
                     skipfooter=2)

print('Data downloaded and read into a dataframe!')

# print the dimensions of the dataframe
print(df_can.shape)
# clean up the dataset to remove unnecessary columns (eg. REG) 
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)

# let's rename the columns so that they make sense
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

# for sake of consistency, let's also make all column labels of type string
df_can.columns = list(map(str, df_can.columns))

# add total column
df_can['Total'] = df_can.sum(axis=1)

# years that we will be using in this lesson - useful for plotting later on
years = list(map(str, range(1980, 2014)))
print ('data dimensions:', df_can.shape)

"""In order to create a Choropleth map, we need a GeoJSON file that defines 
the areas/boundaries of the state, county, or country that we are interested in. 
In our case, since we are endeavoring to create a world map, we want a GeoJSON 
that defines the boundaries of all world countries. For your convenience, 
we will be providing you with this file, so let's go ahead and download it. 
Let's name it world_countries.json."""

# download countries geojson file
# !wget --quiet https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/world_countries.json -O world_countries.json
    
print('GeoJSON file downloaded!')
"""Now that we have the GeoJSON file, let's create a world map, centered around [0, 0] 
 latitude and longitude values, with an intial zoom level of 2, and using Mapbox Bright style."""

world_geo = r'files/world_countries.json' # geojson file

# create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2, tiles='Mapbox Bright')


# generate choropleth map using the total immigration of each country to Canada from 1980 to 2013
folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada'
).add_to(world_map)

# display map
world_map
world_map.save('maps/Choropleth1.html')

"""Notice how the legend is displaying a negative boundary or threshold. 
Let's fix that by defining our own thresholds and starting with 0 instead of -6,918!"""

world_geo = r'files/world_countries.json'

# create a numpy array of length 6 and has linear spacing from the minium total immigration to the maximum total immigration
threshold_scale = np.linspace(df_can['Total'].min(),
                              df_can['Total'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # make sure that the last value of the list is greater than the maximum immigration

# let Folium determine the scale.
world_map = folium.Map(location=[0, 0], zoom_start=2, tiles='Mapbox Bright')
folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
).add_to(world_map)
world_map.save('maps/Choropleth12.html')

#-----------------------------------------------------------------------------------------
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'
state_unemployment = f'{url}/US_Unemployment_Oct2012.csv'
state_data = pd.read_csv(state_unemployment)

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['State', 'Unemployment'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Unemployment Rate (%)'
).add_to(m)

folium.LayerControl().add_to(m)

m.save('maps/Choropleth2.html')


# https://python-visualization.github.io/folium/quickstart.html



