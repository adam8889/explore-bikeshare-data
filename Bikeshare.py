import time
import re
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ['january', 'february', 'march', 'april', 'may', 'june']
days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the city for which you would like to see data. Choices are Chicago, New York City, or Washington.\n").lower()
        if city not in ["chicago", "new york city", "washington"]:
            print("Please enter a valid city. Choices are Chicago, New York City, or Washington.\n")
            continue
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        print("Enter the month or months for which you would like to see data. Choices are January through June, or all")
        months = input("Separate choices with a comma.\n").lower()
        if months.strip() == 'all':
            break
        months = re.split(', |,', months)
        months = [element.strip() for element in months]
        if invalid_month_input(months):
            print("Please enter a valid month. Choices are January through June, or all.\n")
            continue
        break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print("Enter the day or days for of the week for which you wouldl ike to see data, or enter all for all days.")
        days = input("Separate choices with a comma.\n").lower()
        if days.strip() == 'all':
            break
        days = re.split(', |,', days)
        days = [element.strip() for element in days]
        if invalid_day_input(days):
            print("Please enter a valid day of the week.\n")
            continue
        break

    print('-'*40)
    return city, months, days

def invalid_month_input(months):
    """Checks input to make sure months entered by user are in the months_list list"""
    for month in months:
        if month not in months_list:
            return True
    return False

def invalid_day_input(days):
    """Checks input to make sure days entered by user are in the days_list list"""
    for day in days:
        if day not in days_list:
            return True
    return False


def load_data(city, months, days):
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
    df['start_stop_combos'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    # filter by month if applicable
    if months != 'all':
        # use the index of the months list to get the corresponding int
        months = [months_list.index(element) + 1 for element in months]

        # filter by month to create the new dataframe
        df = df[df['month'].isin(months)]

    # filter by day of week if applicable
    if days != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].isin([element.title() for element in days])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = months_list[df['month'].mode()[0] - 1]
    print("The most common month for users to rent a bike is {}".format(common_month.title()))

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week to rent a bike is {}".format(common_day_of_week))

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common starting hour to rent a bike is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station = df['Start Station'].value_counts().index[0]
    num = df['Start Station'].value_counts()[0]
    print("The most commonly used start station is: {} with {} starts.".format(station, num))

    # display most commonly used end station
    station = df['End Station'].value_counts().index[0]
    num = df['End Station'].value_counts()[0]
    print("The most commonly used end station is: {} with {} stops.".format(station, num))

    # display most frequent combination of start station and end station trip
    station = df['start_stop_combos'].value_counts().index[0]
    num = df['start_stop_combos'].value_counts()[0]
    print("The most frequent combination of start station and end station trip is: {} with {} trips.".format(station, num))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("The total amount of time traveled is {:.2f} seconds, or {:.2f} hours.".format(travel_time, travel_time / (60 * 60)))

    # display mean travel time
    travel_time = df['Trip Duration'].mean()
    print("The mean amount of time traveled is {:.2f} seconds, or {:.2f} minutes.".format(travel_time, travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("These are the user types and number of each:\n{}\n".format(user_types.to_string()))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("These are the number of male and female users:\n{}\n".format(gender.to_string()))
    except KeyError:
        print("Gender data does not exist for this location.")

    # Display earliest, most recent, and most common year of birth
    #Surrounded in try/catch logic as Washington does not have data for this
    try:
        most_recent = df['Birth Year'].max()
        earliest = df['Birth Year'].min()
        most_common = df['Birth Year'].mode()[0]

        print("The earliest birth year of a user was {:.0f}.".format(earliest))
        print("The most recent birth year of a user was {:.0f}.".format(most_recent))
        print("The most common birth year of users was {:.0f}.".format(most_common))
    except KeyError:
        print("Birth year data does not exist for this location.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data from the DataFrame"""

    index = 0
    continue_flag = True
    raw_data = input("Would you like to see raw data?\n")
    if raw_data.lower() not in ['yes', 'y']:
        continue_flag = False
    while continue_flag:
        print(df.iloc[index : index + 5])
        index += 5
        raw_data = input("Would you like to see more?\n")
        if raw_data.lower() not in ['yes', 'y']:
            break


def main():
    while True:
        city, months, days = get_filters()
        df = load_data(city, months, days)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
