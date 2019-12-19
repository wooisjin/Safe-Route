min_long = -74.23152410599994
max_long = -73.70967520399995
inc_long = 0.0012668507

min_lat = 40.502384488000075
max_lat = 40.898595640000046
inc_lat = 0.00068913125899999999


def generate_long(min_long, max_long, increment):
	values = []
	while min_long <= max_long:
		min_long = min_long + increment
		values.append(min_long)
	return values


def generate_lat(min_lat, max_lat, increment):
	values = []
	while min_lat <= max_lat:
		min_lat = min_lat + increment
		values.append(min_lat)
	return values


def return_arrays():
	return [generate_long(-74.23152410599994, -73.70967520399995, 0.0012668507),
			generate_lat(40.502384488000075, 40.898595640000046, 0.00068913125899999999)]

