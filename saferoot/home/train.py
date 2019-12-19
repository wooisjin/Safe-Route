import pandas as pd
from generate import return_arrays
from search import binarySearch
import numpy as np

df_shooting = pd.read_csv("NYPD_Shooting_Incident_Data__Historic_.csv")
df_arrest = pd.read_csv("NYPD_Arrests_Data__Historic_ (1).csv")
df_arrest = df_arrest.sample(200000)

df_arrest_con = df_arrest.drop(columns=['ARREST_KEY',
                                        'PD_CD',
                                        'KY_CD',
                                        'LAW_CODE',
                                        'ARREST_BORO',
                                        'ARREST_PRECINCT',
                                        'JURISDICTION_CODE',
                                        'X_COORD_CD',
                                        'Y_COORD_CD',
                                        'PERP_RACE',
                                        'PERP_SEX',
                                        'PD_DESC',
                                        'OFNS_DESC']
                               )
df_shooting_con = df_shooting.drop(columns=['INCIDENT_KEY',
                                            'BORO',
                                            'PRECINCT',
                                            'JURISDICTION_CODE',
                                            'LOCATION_DESC',
                                            'PERP_SEX',
                                            'PERP_RACE',
                                            'VIC_AGE_GROUP',
                                            'VIC_SEX',
                                            'VIC_RACE',
                                            'X_COORD_CD',
                                            'Y_COORD_CD'])


def fill_age(age_group):
    if age_group == '<18':
        return 1.755
    elif age_group == '18-24':
        return 1.661
    elif age_group == '25-44':
        return 1.161
    elif age_group == '45-64':
        return 0.341
    elif age_group == '65+':
        return 0.083
    else:
        return 1


def fill_murder(murder):
    if murder:
        return 5
    else:
        return 3


def change_hour(time):
    return time[:-6]


def weekDay(timestamp):
    df = pd.Timestamp(timestamp)
    return df.dayofweek


def law_category(category):
    if category == 'F':
        return 2.0
    elif category == 'M':
        return 0.5
    elif category == 'V':
        return 0.25
    else:
        return 0


df_arrest_con['AGE_GROUP'] = df_arrest_con['AGE_GROUP'].apply(lambda val: fill_age(val))
df_arrest_con['ARREST_DATE'] = df_arrest_con['ARREST_DATE'].apply(lambda val: weekDay(val))
df_arrest_con['LAW_CAT_CD'] = df_arrest_con['LAW_CAT_CD'].apply(lambda val: law_category(val))

df_shooting_con['PERP_AGE_GROUP'] = df_shooting_con['PERP_AGE_GROUP'].apply(lambda val: fill_age(val))
df_shooting_con['STATISTICAL_MURDER_FLAG'] = df_shooting_con['STATISTICAL_MURDER_FLAG'].apply(
    lambda val: fill_murder(val))
df_shooting_con['OCCUR_TIME'] = df_shooting_con['OCCUR_TIME'].apply(lambda val: change_hour(val))
df_shooting_con['OCCUR_DATE'] = df_shooting_con['OCCUR_DATE'].apply(lambda val: weekDay(val))

location_array_key = return_arrays()
longitude_key = location_array_key[0]
latitude_key = location_array_key[1]
longitude_length = len(longitude_key)
latitude_length = len(latitude_key)

baseline_matrix = [[], [], [], [], [], [], []]

for day in range(7):
    for i in range(longitude_length):
        baseline_matrix[day].append([])
        for j in range(latitude_length):
            baseline_matrix[day][i].append([])

for index, row in df_arrest_con.iterrows():
    long_value = row['Longitude']
    lat_value = row['Latitude']
    day_of_week = int(row['ARREST_DATE'])
    long_index = int(binarySearch(longitude_key, 0, longitude_length, long_value))
    lat_index = int(binarySearch(latitude_key, 0, latitude_length, lat_value))

    baseline_matrix[day_of_week][long_index][lat_index].append((row['AGE_GROUP'], row['LAW_CAT_CD']))

grid = [[], [], [], [], [], [], []]
for day in range(7):
    for hour in range(24):
        grid[day].append(baseline_matrix[day])

for index, row in df_shooting_con.iterrows():
    long_value = row['Longitude']
    lat_value = row['Latitude']
    day_of_week = int(row['OCCUR_DATE'])
    hour = int(row['OCCUR_TIME'])
    long_index = int(binarySearch(longitude_key, 0, longitude_length, long_value))
    lat_index = int(binarySearch(latitude_key, 0, latitude_length, lat_value))
    grid[day_of_week][hour][long_index][lat_index].append((row['PERP_AGE_GROUP'], row['STATISTICAL_MURDER_FLAG']))


def populate_arrest_grid(grid_space_array):
    if type(grid_space_array) is None:
        return 0
    elif type(grid_space_array) == type(1):
        return grid_space_array
    elif type(grid_space_array) == type(np.float64(1.1)):
        return float(grid_space_array)
    total_aggregate = 0
    for age, crime in grid_space_array:
        total_aggregate += age * crime
    return total_aggregate


def find_variation_total():
    total_size = longitude_length * latitude_length
    total_of_aggregate = 0
    for day in range(7):
        for hour in range(24):
            for lon in range(longitude_length):
                for lat in range(latitude_length):
                    grid_total = populate_arrest_grid(grid[day][hour][lon][lat])
                    grid[day][hour][lon][lat] = grid_total
                    total_of_aggregate = grid_total
        avg_score = total_of_aggregate / (total_size)
        for hour in range(24):
            for lon in range(longitude_length):
                for lat in range(latitude_length):
                    value = grid[day][hour][lon][lat]
                    value = avg_score - value
                    if value <= 0:
                        value = value ** 2
                    else:
                        value = value
                    grid[day][hour][lon][lat] = value

def get_grid():
    find_variation_total()
    return grid


