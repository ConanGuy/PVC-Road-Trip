import pygame as pg
import pickle
from City import City

cities_file = open("cities.pkl", "rb")
allCitiesLoc = pickle.load(cities_file)
cities_file.close()

pg.init()
WIDTH, HEIGHT = 1580, 900
win = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("dont care")

shift = 30

minLat = min([l.latitude for l in allCitiesLoc.values()])
minLon = min([l.longitude for l in allCitiesLoc.values()])
print(minLon, minLat)

for c in allCitiesLoc.values():
    c.latitude -= minLat
    c.longitude -= minLon

maxLat = max([l.latitude for l in allCitiesLoc.values()])
maxLon = max([l.longitude for l in allCitiesLoc.values()])
print(maxLon, maxLat)

ratLat = (HEIGHT - shift*2) / maxLat
ratLon = (WIDTH - shift*2) / maxLon


while True:

    col = (235,235,235)
    win.fill((15, 15, 15))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)
    
    last = None
    for city in allCitiesLoc:
        pos = (allCitiesLoc[city].longitude*ratLon+shift, HEIGHT-allCitiesLoc[city].latitude*ratLat-shift)
        pg.draw.circle(win, (235,235,235), pos, 5)

        if last != None:
            pg.draw.line(win, col, last, pos, 3)
        last = pos

        font = pg.font.SysFont(None, 15)
        img = font.render(allCitiesLoc[city].ville, True, (235,15,15))
        win.blit(img, (allCitiesLoc[city].longitude*ratLon+shift+10, HEIGHT-allCitiesLoc[city].latitude*ratLat-shift+10))

        col = (col[0]*0.95, col[1]*0.95, col[2]*0.95)

    pg.display.update()