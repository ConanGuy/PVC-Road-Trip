import random
import pandas as pd
import pickle
from City import City
import pygame as pg

pg.init()
WIDTH, HEIGHT = 1580, 900
win = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("dont care")

key = 'AIzaSyB7_RmWxVF0dU9xaJ_ZQ5JCriaUpr_bBlo'

cities_file = open("cities.pkl", "rb")
allCitiesLoc = pickle.load(cities_file)
cities_file.close()
shift = 30

df_dist = pd.read_excel("cities_distances.xlsx", index_col=0, sheet_name="Distances")
df_dur = pd.read_excel("cities_distances.xlsx", index_col=0, sheet_name="Durations")

###

startCity = "Paris, France"
endCity = "Paris, France"

allCities = list(df_dur.columns)

try: allCities.remove(startCity)
except: pass
try: allCities.remove(endCity)
except: pass

random.shuffle(allCities)
#allCities = allCities[:10]
allCities = ["Stuttgart, Allemagne", "Munich, Allemagne", "Vienne, Autriche", "Graz, Autriche", "Venise, Italie", "Milan, Italie"]

acl = {c:allCitiesLoc[c].copy() for c in allCities+[startCity, endCity]}

minLat = min([l.latitude for l in acl.values()])
minLon = min([l.longitude for l in acl.values()])

for c in acl.values():
    c.latitude -= minLat
    c.longitude -= minLon

maxLat = max([l.latitude for l in acl.values()])
maxLon = max([l.longitude for l in acl.values()])

ratLat = (HEIGHT - shift*2) / maxLat
ratLon = (WIDTH - shift*2) / maxLon

def get_all_travel(lst):
    return [startCity] + lst + [endCity]

def total_distance(lst):
    s1 = 0
    s2 = 0
    for i in range(len(lst)-1):
        s1 += df_dist[lst[i]][lst[i+1]]
        s2 += df_dur[lst[i]][lst[i+1]]
    return s1,s2

#####################################

class Path:

    def __init__(self, path, distance):
        self.path = path
        self.distance = distance

        self.path_cities = list(map(lambda x: allCitiesLoc[x].ville.replace(' ', '+')+",+"+allCitiesLoc[x].pays.replace(' ', '+'), path))

        self.url = "https://www.google.fr/maps/dir/" + "/".join(self.path_cities)
        self.divided_url = []
        per_page = 10
        for i in range(0,len(path),per_page):
            st = i-1 if i > 0 else 0
            self.divided_url.append("https://www.google.fr/maps/dir/" + "/".join((self.path_cities[:-1])[st:i+per_page]))
        self.divided_url[-1] += "/"+allCitiesLoc[endCity].nom.replace(' ', ',+')

df = df_dur.copy()

def draw(path, col):
    return
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)
    
    last = None
    for city in path:
        pos = (acl[city].longitude*ratLon+shift, HEIGHT-acl[city].latitude*ratLat-shift)
        pg.draw.circle(win, (235,235,235), pos, 5)

        if last != None:
            pg.draw.line(win, col, last, pos, 3)
        last = pos

        font = pg.font.SysFont(None, 15)
        img = font.render(acl[city].ville, True, (235,15,15))
        win.blit(img, (acl[city].longitude*ratLon+shift+10, HEIGHT-acl[city].latitude*ratLat-shift+10))


def rec_get_fastest_path(current_path, current_dist, to_visit, min_dist = None):

    win.fill((15, 15, 15))
    if len(current_path) > 1:
        draw(current_path, (235,235,235))
    if min_dist != None:
        draw(min_dist.path, (235,15,15))
    pg.display.update()

    if len(to_visit) == 0:
        end_dist = current_dist+df[current_path[-1]][endCity]

        p = Path(current_path+[endCity], end_dist)

        if min_dist == None:
            print(p.path)
            print(p.distance)
            for u in p.divided_url:
                print(u)

            print()
            return p
        
        if end_dist < min_dist.distance:
            min_dist = p
            print(p.path)
            print(p.distance)
            for u in p.divided_url:
                print(u)

            print()
            print(p.url)
            print()

        return min_dist

    if min_dist != None:
        if current_dist > min_dist.distance:
            return min_dist

    d = current_dist
    last_visited = current_path[-1]
    to_visit = sorted(to_visit, key=lambda x: df[last_visited][x])
    for next_city in to_visit:
        c_to_visit = to_visit.copy()

        c_to_visit.remove(next_city)
        min_dist = rec_get_fastest_path(current_path+[next_city], d+df[last_visited][next_city], c_to_visit, min_dist)
    
    return min_dist

#####################################

allCities = sorted(allCities, key=lambda x: df[startCity][x])
p = rec_get_fastest_path([startCity], 0, allCities)
print()
print()
print("--------- END ---------")
print(p.path)
print(p.distance, p.distance)
for u in p.divided_url:
    print(u)
print()
print(p.url)