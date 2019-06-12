import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import re
import csv
import matplotlib 

cameras = 'https://redshiftzero.github.io/policesurveillance/pod.html'
data = requests.get(cameras)
soup = BeautifulSoup(data.content, 'html.parser')

# print(soup)
right_table = soup.find_all('script')
what_we_need = right_table[6]

pattern = re.compile(".*var marker_.* = L.marker\(\[.*\n.*\n")
all_patterns = pattern.findall(what_we_need.string)

with open('lat_long.csv', mode='w') as camera_file:
    camera_file = csv.writer(camera_file, delimiter=',', lineterminator = '\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    camera_file.writerow(["Latitude", "Longitude"])
    for each in all_patterns:
        each = each.strip()
        each = ' '.join(each.split())
        each = each[each.find('[') + 1:each.find(']')]
        (lat, long) = each.split(',')
        lat = lat.strip()
        long = long.strip()
        camera_file.writerow([lat, long])

    # print(float(lat))
    # print(float(long))


