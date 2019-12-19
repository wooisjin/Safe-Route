from generate import return_arrays
from search import binarySearch
from datetime import date, datetime
from models import dict_database
day = date.today().weekday()
hour = datetime.now().hour


def return_avg(path_array):
    location_key = return_arrays()
    path_length = len(path_array)
    total_danger = 0
    for i in range(path_length):
        location = path_array[i]
        long_index = binarySearch(location_key[0], 0, len(location_key[0]), location[0])
        lat_index = binarySearch(location_key[1], 0, len(location_key[1]), location[1])
        total_danger += grid[day][hour][long_index][lat_index]
    return total_danger/path_length