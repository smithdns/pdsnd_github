import time
import pandas as pd
import numpy as np
import datetime as dt
import math

citydata = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
dir='C:\\Users\\dlind\\OneDrive - Research Triangle Institute\\Documents\\PythonData\\'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # city = input("Enter city in small letters(chicago, new york city, washington): ")
    city = ''
    while (city != 'chicago') or (city !='new york city') or (city !='washington'):
        city = input("Enter city in small letters(chicago, new york city, washington): ")
        if (city == 'chicago') or (city == 'new york city') or (city =='washington'):
            break

    # get user input for month 
    month = -1
    while month < 0 or month > 6:
        month = int(input("Enter integer month(0=all, january=1, february=2, ... , june=6): "))
        if month >= 1 and month <= 6:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while (day != 'all') or (day != 'monday') or (day != 'tuesday') or (day != 'wednesday') or (day != 'thursday') or (day != 'friday') or (day != 'saturday')  or (day != 'sunday'):
        day = input("Enter day of week(all, monday, tuesday, ... sunday): ")
        if (day == 'all') or (day == 'monday') or (day == 'tuesday') or (day == 'wednesday') or (day == 'thursday') or (day == 'friday') or ( day == 'saturday')  or (day == 'sunday' ):
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(dir + citydata[city])

    df["City"] = city   
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Total Time'] = df['End Time']-df['Start Time']

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    
    months = df['month'].value_counts()
    print('months',months)
    
    days = df['day_of_week'].value_counts()
    print('days',days)
    
    if 'Gender' not in df.columns:
        df['Gender'] = 'Unknown'
        
    if 'Birth Year' not in df.columns:
        df['Birth Year'] = np.nan
    
    # filter by month if applicable
    
    if month != 0:     
     
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe        
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most popular day:', popular_day)

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]  
    print('Most popular start station:',  popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]  
    print('Most popular end station:',  popular_end_station)


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' from ' + df['End Station']
    print ('Most frequent combination of start station and end station', df['Trip'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time ", np.sum(df['Total Time']))

    # display mean travel time
    print("Mean travel time ", np.mean(df['Total Time']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)

    # Display counts of gender
    genders = df['Gender'].value_counts()

    print(genders)   
    
    #df["Birth Year"] = int(df["Birth Year"])

    # Display earliest, most recent, and most common year of birth
    minyob = np.min(df["Birth Year"]);
    maxyob = np.max(df["Birth Year"]);
    print('Earliest year of birth:',  minyob)
    print('Most recent year of birth:',  maxyob)  
    if ((math.isnan(minyob)) and ( math.isnan(maxyob))):    
        print('Most common year of birth: cannot be determined')
    else:
        print('Most common year of birth:',  df["Birth Year"].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = ''
    start_loc = 0
    end_loc = 5
    while (start_loc <= len(df.index)) and (end_loc <= len(df.index)):
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')        
        if (view_data == 'no'):
            break            
        print(df[start_loc:end_loc])
        start_loc += 5 
        end_loc += 5 
        if (end_loc > len(df.index)):
            end_loc = len(df.index)


def main():
    while True:
        city, month, day = get_filters()
        print (city,' ', month,' ', day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()