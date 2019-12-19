import re

post_string = "Park Central New York to Broadway Street"
locations = re.search(r'(.+?)\sto\s(.+)', post_string)
origin = locations.group(1)
destination = locations.group(2)

print(origin)
print(destination)