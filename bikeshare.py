import time
import pandas as pd
from datetime import timedelta as td

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

cities_with_gender_data=['chicago', 'new york']
cities_with_birth_year_data=['chicago', 'new york']

# used for viewing data by n-rows (see display_data() function below); columns to include are specified here
CITY_DATA_COLUMNS = { 'chicago': ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'],
                'new york': ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'],
                'washington': ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type']}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "" (empty string) to apply no month filter
        (str) day - name of the day of week to filter by, or "" (empty string) to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA:
        city = str(input('Would you like to see data for Chicago, New York, or Washington? ')).lower()
    print('\n\t ==> You chose to see data for city: {}!\n'.format(city.title()))
    
    # get user input for month (all, january, february, ... , june)
    month = ''
    is_filter_by_month = str(input('Would you like to filter by month? ([y] YES or [any key] NO): ')).lower()
    if is_filter_by_month == 'yes' or is_filter_by_month == 'y':
        while month not in months:
            month = str(input('Which month - January, February, March, April, May, or June?: ')).lower()
        print('\n\t ==> Data will be analyzed for month of: {}\n'.format(month.title()))
    
    if month == '':
        print('\n\t ==> No filter applied for month; All months will be analyzed.\n')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    is_filter_by_day = str(input('Would you like to filter by day? ([y] YES or [any key] NO): ')).lower()
    if is_filter_by_day == 'yes' or is_filter_by_day == 'y':
        while day not in days:
            day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?: ')).lower()
        print('\n\t ==> Data will only focus for day of the week: {}\n'.format(day.title()))

    if day == '':
        print('\n\t ==> No filter applied for day; All days of the week will be analyzed.\n')
 
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "" (empty string) to apply no month filter
        (str) day - name of the day of week to filter by, or "" (empty string) to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time(Converted)'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time(Converted)'].dt.month
    #df['day_of_week'] = df['Start Time(Converted)'].dt.weekday_name #python 1 and below
    df['day_of_week'] = df['Start Time(Converted)'].dt.day_of_week 
    df['hour'] = df['Start Time(Converted)'].dt.hour

    # filter by month if applicable
    if month != '':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != '':
        #df = df[df['day_of_week'] == day.title()] #low version of pandas (v1.0 below)
        df = df[df['day_of_week'] == days.index(day)]

    return df

def display_data(df, city, rowcount):
    """
    Displays every n rows of data.
    
    Args:
        (pandas.DataFrame) df - the DataFrame to refer the statistics.
        (int) rowcount - number of rows to display
    """
    
    view_df = df[CITY_DATA_COLUMNS[city]]

    answer = str(input("Would you like to view every {} rows of individual trip data? Enter [y] yes or [n] no: ".format(rowcount))).lower()
    start_loc = 0
    end_loc = rowcount
    while (answer == 'yes' or answer == 'y') and end_loc < len(view_df): 
        print(view_df.iloc[start_loc:end_loc].to_json(orient='records', lines=True))
        start_loc = end_loc
        end_loc += rowcount
        answer = str(input("Do you wish to continue displaying rows of data? Enter [y] yes or [n] no: ")).lower()

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (pandas.DataFrame) df - the DataFrame to refer the statistics.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #popular_month = df['month'].value_counts().idxmax()
    popular_month = df['month'].value_counts().idxmax()
    print('What is the most popular month for traveling? Answer: {}'.format(months[popular_month-1].title()))
    
    # display the most common day of week
    popular_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('What is the most popular day for traveling? Answer: {}'.format(popular_day_of_week))

    # display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('What is the most popular hour of the day to start traveling? Answer: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (pandas.DataFrame) df - the DataFrame to refer the statistics.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()

    # display most frequent combination of start station and end station trip
    print('The most popular start station is: {}'.format(popular_start_station))
    print('The most popular end station is: {}'.format(popular_end_station))
    
    gs = df.groupby(['Start Station', 'End Station']).size().reset_index()
    gs.columns = ['Start Station', 'End Station', 'Count']
    # print('The most popular trip is from {} to {}'.format(gs.iloc[gs['Count'].idxmax()][0], gs.iloc[gs['Count'].idxmax()][1]))
    print('The most popular trip is from {} to {}'.format(gs.iloc[gs['Count'].idxmax()]["Start Station"], gs.iloc[gs['Count'].idxmax()]["End Station"]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_timedelta(timedelta_input):
    """
    Formats the timedelta object into a string: '<%> days, <%> hours, <%> minutes, <%> seconds'
    
    Args:
        (datetime.timedelta) timedelta_input - the timedelta object
    """
    days = timedelta_input.days
    hours, remainder = divmod(timedelta_input.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return_str = ''
    if days > 0:
        return_str += ('{} days, ').format(days)
    if hours > 0:
        return_str += ('{} hours, ').format(hours)
    if minutes > 0:
        return_str += ('{} minutes, ').format(minutes)

    return_str += ('{} seconds').format(seconds)
    
    return return_str
    
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (pandas.DataFrame) df - the DataFrame to refer the statistics.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_td = td(seconds=float(total_travel_time))
    print('Travel time total: {}'.format(format_timedelta(total_travel_time_td)))
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_td = td(seconds=float(mean_travel_time))
    print('Travel time average: {}'.format(format_timedelta(mean_travel_time_td)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (pandas.DataFrame) df - the DataFrame to refer the statistics.
        (str) city - name of the city to analyze the user stats.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].unique()
    user_types = user_types[~pd.isnull(user_types)]
    print('[User Type]  [Count]')
    for ut in user_types:
        print('{}: {}'.format(ut, df['User Type'].value_counts()[ut]))

    # Display counts of gender
    if city in cities_with_gender_data:
        genders = df['Gender'].unique()
        genders = genders[~pd.isnull(genders)]
        print('\n[Gender]\t[Count]')
        for g in genders:
            print('{}:\t{}'.format(g, df['Gender'].value_counts()[g]))
    else:
        print('No Gender data for city: {}'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if city in cities_with_birth_year_data:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('\nWhat is the oldest, youngest, and most popular year of birth, respectively?')
        print('{}, {}, {}'.format(earliest_birth_year, most_recent_birth_year, common_birth_year))
    else:
        print('No Birth Year data for city: {}'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df, city, 5)

        restart = input('\nWould you like to restart? Enter [y] YES or [any key] NO.\n')
        if restart.lower() != 'y' and restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
