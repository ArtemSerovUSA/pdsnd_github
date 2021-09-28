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
    print('-'*40)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = (input('Please select a city from a list ("chicago", "new york city", "washington") to analyze ')).casefold()
        print('-'*40)
        if city not in ('chicago', 'new york city', 'washington'):
            print('Sorry, but "{}" not in the list of cities.\nPlease enter correct city name from a list'.format(city))
        else:
            print('You selected {} to analyze'.format(city))
            break

    # get user input for month (all, january, february, ... , june)
    while True:
            month = (input('Please select a month from a list ("all", "january", "february", "march", "april", "may", "june") to analyze ')).casefold()
            print('-'*40)
            if month not in ("all", "january", "february", "march", "april", "may", "june"):
                print('Sorry, but "{}" not in the list of months.\nPlease enter correct month from a list'.format(month))
            else:
                print('You selected {} to analyze'.format(month))
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = (input('Please select a weekday from a list ("all", "monday", "tuesday", "wednesday", "thursday", "saturday", "sunday") to analyze ')).casefold()
            print('-'*40)
            if day not in ("all", "monday", "tuesday", "wednesday", "thursday", "saturday", "sunday"):
                print('Sorry, but "{}" not in the list of weekdays.\nPlease enter correct weekday from a list'.format(day))
            else:
                print('You selected {} to analyze'.format(day))
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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv("C:\\Users\\p2966282\\Udacity\\bikeshare-2\\{}".format(CITY_DATA[city]))

    # extract month and day of week from Start Time to create new columns
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek

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
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['day_of_week'] == days.index(day)]

    return df


def raw_data_scroll(df):
    """ Enables interactive raw data scrolling by 5 lines at once """
    min_i = 0
    max_i = 5

    valid = False
    answer = None
    while not valid:
        valid = True
        answer = (input("Please type (yes) if you want to see 5 lines of raw data or (no) if you want go to the statistics")).casefold()
        # Validating the input
        if answer not in ('yes', 'no'):
            valid = False
            print('Please type only (yes) or (no)')
        # If answer is 'yes' then printing out 5 lines of dataframe
        if answer == "yes" and max_i <= df.iloc[-1][0]:
            valid = False
            print(df.iloc[[min_i]].to_string())
            for i in range(min_i + 1, max_i):
                print(df.iloc[[i]].to_string(header=None))
            min_i += 5
            max_i += 5
        # If answer is no then print a message
        if answer == 'no':
            print("Let's go to statistics!")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months_dict = {
        "1" : "January",
        "2" : "February",
        "3" : "March",
        "4" : "April",
        "5" : "May",
        "6" : "June"
    }
    print("The most common month of travel is *{}*".format(months_dict[str(df['month'].mode()[0])]))

    # display the most common day of week
    days_dict = {
        "0" : "Monday",
        "1" : "Tuesday",
        "2" : "Wednesday",
        "3" : "Thursday",
        "4" : "Friday",
        "5" : "Saturday",
        "6" : "Sunday"
    }
    print("The most common day of week of travel is *{}*".format(days_dict[str(df['day_of_week'].mode()[0])]))

    # display the most common start hour

    print("The most common hour of travel is *{}*".format(str(df['hour'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is *{}*".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is *{}*".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['combined'] = df['Start Station'] + ' - ' + df['End Station']
    print("The most frequent combination of start station and end station is *{}*".format(df['combined'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is {} minutes".format(df['Trip Duration'].sum()/60))

    # display mean travel time
    print("Mean travel time is {} minutes".format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays basic statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type count: ")
    print((df['User Type'].value_counts()).to_string())
    # Handling an exception if we have missing columns in files
    try:
        # Display counts of gender
        print("\nGender count:\n",(df['Gender'].value_counts()).to_string())
        # Display earliest, most recent, and most common year of birth
        print("\nCustomer's earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("\nCustomer's most recent year of birth is {}".format(int(df['Birth Year'].max())))
        print("\nCustomer's most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("\nThere is no additional data about users in current city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def secret_function():
    """
    Creates insanely high quality graphics
    """
    print('     _________')
    print('    / ======= \\')
    print('   / __________\\')
    print('  | ___________ |')
    print('  | |         | |')
    print('  | | UDACITY | |')
    print('  | |_________| |________________________')
    print('  \\*____________/      Artem Serov      )')
    print('  / """"""""""" \\                      /')
    print(" / ::::::::::::: \\                 =D-'")
    print('(_________________)')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data_scroll(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            secret_function()
            break


if __name__ == "__main__":
	main()
