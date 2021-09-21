import geocoder
from City import City

key = 'AIzaSyB7_RmWxVF0dU9xaJ_ZQ5JCriaUpr_bBlo'

import pickle

for c in allCitiesLoc:
    results = geocoder.google(c, key=key)
    print(c, results.current_result, results.current_result.country)