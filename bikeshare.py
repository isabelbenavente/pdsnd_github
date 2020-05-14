import time
import pandas as pd
import numpy as np

CITY_DATA = { 'CHI': 'chicago.csv',
              'NYC': 'new_york_city.csv',
              'DC': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    cities = ('CHI', 'NYC', 'DC')
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    while True:
        city = (input("What city would you like to explore? Choose from: CHI, NYC, DC. ")).upper()
        if city not in cities:
            print('Sorry, this is not an option. Try again:' )
        else:
            break

    while True:
        month = (input("Are you interested in all data or filtered by month? Choose from all, january, february, march, april, may, june. ")).lower()
        if month not in months:
            print('Sorry, this is not an option. Try again:' )
        else:
            break

    while True:
        day = (input("Are you interested in all data or filtered by day? Choose from all, monday, tuesday, wednesday, thursday, friday. ")).lower()
        if day not in days:
            print('Sorry, this is not an option. Try again:' )
        else:
            break

    print('-'*40)
    print('Here we go!!')
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

    # DONE: display the most common month
    # DONE: display the most common day of week
    # DONE: display the most common start hour

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('Most Common Start Month:', common_month)

    df['day'] = df['Start Time'].dt.weekday_name
    common_day = df['day'].mode()[0]
    print('Most Common Start Day:', common_day)

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and route."""

    print('\nCalculating The Most Popular Stations and Route...\n')
    start_time = time.time()

    # DONE: display most commonly used start station
    # DONE: display most commonly used end station
    # DONE: display most frequent combination of start station and end station

    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station is:', popular_start)

    popular_end = df['End Station'].mode()[0]
    print('The most popular end station is:', popular_end)

    # create new Route column
    df['Route'] = df['Start Station'] + "  ...TO...  " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('The most popular route is:', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # DONE: display total travel time
    # DONE: display mean travel time

    total_travel = df['Trip Duration'].sum()
    print('The total travel time was:')
    print('...in minutes: ', total_travel/60)
    print('...in hours: ', total_travel/3600)
    print()
    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time was:')
    print('...in minutes: ', mean_travel/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # DONE: Display counts of user types
    # DONE: Display counts of gender
    # DONE: Display earliest, most recent, and most common year of birth

    user_types = df['User Type'].value_counts()
    print('These are our users:\n', user_types)

    print()
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('This is the gender distribution:\n', gender)
    else:
        print('No Gender info available for DC')

    print()
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        print('Our oldest user was born in:', oldest)
        youngest = df['Birth Year'].max()
        print('Our youngest user was born in:', youngest)
        common_year = df['Birth Year'].mode()[0]
        print('Most users were born in:', common_year)
    else:
        print('No Birth Year info available for DC')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw(df):
    """Asks if interested in raw data"""

    lower_bound = 0
    upper_bound = 5

    while True:
        show_raw = input('Would you like to see 5 or more rows of raw data? Enter yes or no.\n')
        if show_raw.lower() != 'yes':
            break
        else:
            print(df[df.columns[0:]].iloc[lower_bound:upper_bound])
            lower_bound += 5
            upper_bound += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
