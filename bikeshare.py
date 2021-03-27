import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington).
    city = input("\nWould you like data for chicago, new york city, or washington? \n")
    while (city.lower() not in CITY_DATA.keys()):
        cityp = input("\n Incorrect input. Would you like data for chicago, new york city, or washington? \n")

    # TO DO: get user input for month (all, january, february, ... , june)
    months = {'all':0, 'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
    month = input("\nWhich month would you like data for (type 'all' for all year)?\n")
    while (month.lower() not in months.keys()):
        month = input("\n Incorrect input. Which month would you like data for? \n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day would you like data for (type 'all' for all week)?\n")
    days = {'all':0, 'sunday':1, 'monday':2, 'tuesday':3, 'wednesday':4, 'thursday':5, 'friday':6, 'saturday':7}
    while(day.lower() not in days.keys()):
        day = input("\n Incorrect input. Which day would you like data for? \n")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
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

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Popular Month: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(' Popular Day: ', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(' Popular Hour: ', popular_hour, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('Popular Start Station: ', pop_start_station)

    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('Popular End Station: ', pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    pop_start = df.groupby('Start Station')
    pop_start_end = pop_start['End Station'].agg(lambda column: "".join(column))
    pop_start_end = pop_start_end.reset_index(name = 'End Station')
    pop_station_combo = pop_start_end['End Station'].mode()[0]
    
    print('Popular Station Combo: ', pop_station_combo, '\n')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: ",total_travel_time,'\n')

    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("Average Travel Time: ", avg_travel_time,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    
    if city == 'washington':
        return
    else: 
        print('\nCalculating User Stats...\n')
        start_time = time.time()

    # TO DO: Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types, ' ')
    # TO DO: Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print(gender_counts, '\n')


    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        latest_birth = df['Birth Year'].max()
        popular_birth = df['Birth Year'].mode()[0]
        print('Earliest Birth: ', earliest_birth, '\nLatest Birth: ', latest_birth, '\nPopular Birth: ', popular_birth, '\n')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        raw_data = input('\nWould you like five rows of raw data? Enter yes or no. \n')
        start_loc = 0
        while (raw_data.lower() == 'yes'):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            raw_data = input('\nWould you like five more rows of raw data? Enter yes or no. \n')
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
