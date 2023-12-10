import time
import pandas as pd
import numpy as np

# Creating a dictionary containing the data sources for the three cities
CITY_DATA = {'chicago': 'data/chicago.csv', 
             'new york city': 'data/new_york_city.csv',
             'washington': 'data/washington.csv'}

# Function to figure out the filtering requirements of the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Args:
        None.
       
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of the week to filter by, or "all" to apply nop day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # Initializing an empty city variable to store city choice from user
    # You will see this repeat throughout the program
    city = ''
    # Running this loop to ensure the correct user input gets selected otherwise repeat
    while city not in CITY_DATA.keys():
        print('Welcome to this program. Please choose your city:')
        print('\n1. Chicago 2. New York City 3. Washington')
        # Taking user input and converting into lowercase to standardize them 
        # You will find this happening at every stage of input throughout this program
        city = input().lower()

        if city not in CITY_DATA.keys():
            print('\nMaybe you made a typo. Please enter the correct city name.')
            print('\nRestarting...')

    print(f'You have chosen {city.title()} as your city.')

    # Creating a dictionary to store all the months including the 'all' option
    MONTH_DICT = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DICT.keys():
        print('\nWhich month data would you like to see - January, February, March, April, May, June?')
        print('\n(You may also opt to view data for all months, please type \'all\' or \'All\' or \'ALL\' for that.)')
        month = input().lower()

        if month not in MONTH_DICT.keys():
            print('Maybe you made a typo. Please try again\n')
            print('\nRestarting...')

    print(f'\nYou have chosen {month.title()} as your month.')

    # Creating a list to store all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print('\nWhich day would you like to see - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
        print('\n(You can also put \'all\' or \'All\' to view data for all days in a week.)')
        day = input().lower()

        if day not in DAY_LIST:
            print('Maybe you made a typo. Please try again\n')
            print('\nRestarting...')

    print(f'\nYou have chosen {day.title()} as your day.')
    print(f'\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()}, and day\s: {day.upper()}.')
    print('-'*80)
    # Returning the city, month and day selections
    return city, month, day

# Function to load data from .csv files
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or 'all' to apply no month filter
        param3 (str): name of the day of the week to filter by, or 'all' to apply no day filter

    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    # Load data for city
    print('\nLoading data...')
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Return the selected file as a dataframe (df) with relevant columns
    return df

# Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        param1 (df): The DataFrame you wish to work with.

    Returns:
        None.
    """
    
    print('\nCalculate The Most Frequent Times of Travel...')
    start_time = time.time()
    
    # This try clause is implemented to calculate the most frequent times of travel
    # However, some df may be empty hence...
    try:
        # Uses mode method to find the most popular month
        popular_month = df['month'].mode()[0]
        print(f'\nMost Popular Month (1 = January,..., 6 = June): {popular_month}')

        # Uses mode method to find the most popular day
        popular_day = df['day_of_week'].mode()[0]
        print(f'\nMost Popular Day: {popular_day}')

        # Extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour

        # Uses mode method to find the most popular hour
        popular_hour = df['hour'].mode()[0]
        print(f'\nMost Popular Start Hour: {popular_hour}')
    except:
        print('Oops!\nSeems to have encountered an empty DataFrame.')

    # Prints the time taken to perform the calculation
    # You will find this in all the functions involving any calculation throughout this program
    print(f'\nThis took {time.time() - start_time} seconds.')
    print('-'*80)

# Function to calculate station related statistics 
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        param1 (df): The DataFrame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating the Most Popular Stations and Trip...')
    start_time = time.time()

    # This try clause is implemented to calculate the most popular stations and trips
    # However, some df may be empty hence...
    try:

        # Uses the mode method to find the most common start station 
        common_start_station = df['Start Station'].mode()[0]

        print(f'\nThe most commonly used start station: {common_start_station}')

        # Uses mode method to find the most common end station
        common_end_station = df['End Station'].mode()[0]

        print(f'\nThe most commonly used end station: {common_end_station}')

        # Uses str.cat to combine two columns in the df
        # Assigns the result to a new column 'Start To End'
        # Uses mode on this new column to find out the most common combination of start and end stations
        df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
        combo = df['Start To End'].mode()[0]

        print(f'\nThe most frequent combination of trips are from {combo}.')

    except:
        print('Oops!\nSeems to have encountered an empty DataFrame.')

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('-'*80)

# Function for trip duration related statistics
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        param1 (df): The DataFrame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # This try clause is implemented to calculate trip duration...
    # However, some df may be empty hence...
    try: 
        # Uses sum method to find the total trip duration
        total_duration = df['Trip Duration'].sum()

        # Find the duration in minutes and seconds format
        minute, second = divmod(total_duration, 60)
        # Find the duration in hours and minutes format
        hour, minute = divmod(minute, 60)
        print(f'\nThe total trip duaration is {hour} hours, {minute} minutes and {second} seconds.')

    
        # Uses mean method to calculate the average trip duaration
        average_duration = round(df['Trip Duration'].mean())

        # Find the average duartion in minutes and seconds format
        mins, sec = divmod(average_duration, 60)
        # This filter prints the time in hours, mins, sec format if the mins exceed 60
        #if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f'\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.')
        #else:
            #print(f'\nThe average trip duration is {mins} minutes and {sec} seconds.')

    except:
        print('Oops!\nSeems to have encountered an empty DataFrame.')

    print(f'\nThis took {time.time() - start_time} seconds.')
    print('-'*80)

# Function to calculate user statistics
def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        param1 (df): The DataFrame you wish to work with.

    Returns:
        None.
    """

    print('\nCalculating User Stats...')
    start_time = time.time()

    # This try clause is implemented to display the number of users by Gender
    # However, not every df may have the Gender column, hence this...
    try:    
        # The total users are counted using value_counts method
        # They are then displayed by their types (e.g. Subscriber or Customer)
        user_type = df['User Type'].value_counts()

        print(f'\nThe types of users by number are given below:\n\n{user_type}')

    
        gender = df['Gender'].value_counts()
        print(f'\nThe types of users by gender are given below:\n\n{gender}')
    except:
        print('\nThere is no \'Gender\' column in this file.')

    # Similarly, this try cluase is there to ensure only df containing 'Birth Year' column are displayed
    # The earliest birth year, most recent birth year and the most common birth years are displayed

    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = df['Birth Year'].mode()[0]
        print(f'\nThe most earliest year of birth is: {earliest}\n\nThe most recent year of birth is: {recent}\n\nThe most common year of birth is: {common_year}')
    except:
        print('There are no birth year details in this file.')
    
    print(f'\nThis took {time.time() - start_time} seconds.')
    print('-'*80)

# Function to display the data frame itself depending on the user request
def display_data(df):
    """
    Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The DataFrame you wish to work with.

    Returns:
        None.
    """

    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    # counter variable is initialized as a tag to ensure only details from a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print('\nDo you wish to view the row data? Type \'Yes\' or \'No\'\n')
        rdata = input().lower()
        # The raw data from the df is displayed if user opts for it
        if rdata == 'yes':
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print('\nMaybe you made a typo. Please try again')
            print('\nRestarting...\n')

   # Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print('Do you wish to view more raw data?')
        counter += 5
        rdata = input().lower()
        # If user opts for it, this displays next 5 rows of data
        if rdata == 'yes':
            print(df[counter:counter+5])
        elif rdata != 'yes':
            break

    print('-'*80)

# Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()