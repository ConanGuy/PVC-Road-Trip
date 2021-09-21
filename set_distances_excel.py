from City import City

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='myapplication')

import googlemaps
key = 'AIzaSyB7_RmWxVF0dU9xaJ_ZQ5JCriaUpr_bBlo'
gmaps = googlemaps.Client(key=key)

import pickle
import pandas as pd

################################

def get_distance(src, dst):
    c1 = (src.latitude,src.longitude)
    c2 = (dst.latitude,dst.longitude)

    g = gmaps.directions(c1,c2,mode="driving")
    distance = g[0]["legs"][0]["distance"]["value"]
    duration = g[0]["legs"][0]["duration"]["value"]

    return distance, duration

################################

df_dist = pd.read_excel("cities_distances.xlsx", index_col=0, sheet_name="Distances")
df_dur = pd.read_excel("cities_distances.xlsx", index_col=0, sheet_name="Durations")

###

allCitiesLoc = {}

cities_file = open("cities.pkl", "rb")
allCitiesLoc = pickle.load(cities_file)
cities_file.close()

for c in df_dur.columns:
    if c not in allCitiesLoc:
        print(c, end = ' ')
        city = City(c)
        allCitiesLoc[c] = city
        print(city.city)

cities_file = open("cities.pkl", "wb")
pickle.dump(allCitiesLoc, cities_file, pickle.HIGHEST_PROTOCOL)
cities_file.close()

###

for col in df_dur.columns:
    if df_dur[col].hasnans or df_dist[col].hasnans:
        for row in df_dur.index:
            if pd.isna(df_dur[col][row]) or pd.isna(df_dist[col][row]):
                try:
                    dd = get_distance(allCitiesLoc[col], allCitiesLoc[row]) 
                except :
                    dd = (999999999,999999999)
                dist, dur = dd
                
                print(col, row, dd)

                df_dur[col][row] = dur
                df_dur[row][col] = dur

                df_dist[col][row] = dist
                df_dist[row][col] = dist

with pd.ExcelWriter("cities_distances.xlsx", mode="w") as writer:
    df_dist.to_excel(writer, sheet_name="Distances")
    df_dur.to_excel(writer, sheet_name="Durations")