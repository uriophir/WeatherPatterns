
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d50/0dafa7edc4fe5b664340ad4f14631d8451795bb7e92f4811c570a0dc.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Tel Aviv, Tel Aviv, Israel**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(50,'0dafa7edc4fe5b664340ad4f14631d8451795bb7e92f4811c570a0dc')


# In[2]:

get_ipython().magic('matplotlib notebook')


# In[3]:

# Read CSV file
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d50/0dafa7edc4fe5b664340ad4f14631d8451795bb7e92f4811c570a0dc.csv')


# In[ ]:




# In[5]:

# Create Maximun and Minimun Dataframes
df_min = df[(df['Element'] == 'TMIN') & (df['Date'] < '2015-01-01')].drop('Element',axis=1)

df_min['Date'] = pd.to_datetime(df_min['Date'],errors='coerce')
df_min['Date'] = df_min['Date'].dt.strftime('%d-%b')

df_max = df[(df['Element'] == 'TMAX') & (df['Date'] < '2015-01-01')].drop('Element',axis=1)
df_max['Date'] = pd.to_datetime(df_max['Date'],errors='coerce')
df_max['Date'] = df_max['Date'].dt.strftime('%d-%b')

df_min = df_min[['Date','Data_Value']].groupby('Date').agg(np.min).rename(columns = {'Data_Value':'Min'}).reset_index()
df_max = df_max[['Date','Data_Value']].groupby('Date').agg(np.max).rename(columns = {'Data_Value':'Max'}).reset_index()


# In[6]:

data = df_min.merge(df_max, how='outer',on='Date')


# In[7]:

#2. Overlay a scatter of the 2015 data for any points (highs and lows) 
#for which the ten year record (2005-2014) record high or record low was broken in 2015.

# Create Maximun and Minimun Dataframes
df_min_2015 = df[(df['Element'] == 'TMIN') & (df['Date'] >= '2015-01-01')].drop('Element',axis=1)

df_min_2015['Date'] = pd.to_datetime(df_min_2015['Date'],errors='coerce')
df_min_2015['Date'] = df_min_2015['Date'].dt.strftime('%d-%b')

df_max_2015 = df[(df['Element'] == 'TMAX') & (df['Date'] >= '2015-01-01')].drop('Element',axis=1)
df_max_2015['Date'] = pd.to_datetime(df_max_2015['Date'],errors='coerce')
df_max_2015['Date'] = df_max_2015['Date'].dt.strftime('%d-%b')

df_min_2015 = df_min_2015[['Date','Data_Value']].groupby('Date').agg(np.min).rename(columns = {'Data_Value':'Min_2015'}).reset_index()
df_max_2015 = df_max_2015[['Date','Data_Value']].groupby('Date').agg(np.max).rename(columns = {'Data_Value':'Max_2015'}).reset_index()

data_2015 = df_min_2015.merge(df_max_2015, how='outer',on='Date')

scatter_data = data.merge(data_2015, how='outer',on='Date')


# In[9]:

scatter_data['isMinScore'] = np.where(scatter_data['Min_2015'] < scatter_data['Min'], 1,0)
scatter_data['isMaxScore'] = np.where(scatter_data['Max_2015'] > scatter_data['Max'], 1,0)


# In[16]:

max_2015_data = scatter_data[(scatter_data['isMaxScore'] == 1)].drop(['Min','Max','Min_2015','isMaxScore','isMinScore'],axis=1)
min_2015_data = scatter_data[(scatter_data['isMinScore'] == 1)].drop(['Min','Max','Max_2015','isMaxScore','isMinScore'],axis=1)

data = data.merge(max_2015_data, how='left',on='Date').merge(min_2015_data, how='left',on='Date')


# In[21]:

Date = np.array(data.loc[:,'Date'].to_datetime(a,unit='D')).dt.month)
Max = np.array(data.loc[:,'Max'])
Min = np.array(data.loc[:,'Min'])
Max_2015 = np.array(data.loc[:,'Max_2015'])
Min_2015 = np.array(data.loc[:,'Min_2015'])


# In[119]:

plt.figure()

plt.plot(Date,Max,'-',Date,Min,'-',Date,Max_2015,'o',Date,Min_2015,'o')


# In[ ]:




# In[84]:

plt.fill_between(Day, Min, Max, color='grey', alpha='0.5')


# In[15]:

max_2015_data = scatter_data[(scatter_data['isMaxScore'] == 1)].drop(['Min','Max','Min_2015','isMaxScore','isMinScore'],axis=1)
min_2015_data = scatter_data[(scatter_data['isMinScore'] == 1)].drop(['Min','Max','Max_2015','isMaxScore','isMinScore'],axis=1)

data = data.merge(max_2015_data, how='left',on='Date').merge(min_2015_data, how='left',on='Date')
data['Date'] = data['Date'].dt.strptime('')

print(data)


# In[89]:




# In[ ]:



