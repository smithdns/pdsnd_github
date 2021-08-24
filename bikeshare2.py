import time
import pandas as pd
import numpy as np
import datetime as dt
import sys
import matplotlib
import matplotlib.pyplot as plt

citydata = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
dir='C:\\Users\\dlind\\OneDrive - Research Triangle Institute\\Documents\\PythonData\\'

def load_data2(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
     
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(dir + citydata[city])

    df["city"] = city 
    df['duration'] = df['Trip Duration']
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Total Time'] = df['End Time']-df['Start Time']

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")   
   
    df['day_of_week']=df['day_of_week'].astype('category').cat.codes
    df['city']=df['city'].astype('category').cat.codes
    
    if 'Gender' not in df:
        df['Gender'] = 'unknown'    
       
    print(df.info())
    
    df.corr()  
    
    return df

df1 = load_data2('chicago')
df1["cityindex"] = 1
df1.plot(kind = 'scatter', x = 'month', y = 'duration')   
plt.savefig(dir + 'chicago' + ".png")
df1.corr()

df2 = load_data2('new york city')
df2["cityindex"] = 2
df2.plot(kind = 'scatter', x = 'month', y = 'duration')   
plt.savefig(dir + 'newyork' + ".png")
df2.corr()

df3 = load_data2('washington')
df3["cityindex"] = 3
df3.plot(kind = 'scatter', x = 'month', y = 'duration')   
plt.savefig(dir + 'washington' + ".png")
df3.corr()

frames = [df1, df2, df3]

result = pd.concat(frames)

result = pd.concat(frames)
result.plot(kind = 'scatter', x = 'month', y = 'duration') 
plt.savefig(dir + 'month' + ".png")
result.plot(kind = 'scatter', x = 'cityindex', y = 'duration') 
plt.savefig(dir + 'city' + ".png")

result['Gender']=result['Gender'].astype('category').cat.codes

result.corr()

#work in progress here
months = result["month"]
durations = result["duration"]
plt.plot(months,durations)
plt.savefig(dir + 'all' + ".png")