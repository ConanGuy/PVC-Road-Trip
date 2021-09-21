from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='myapplication')

################################

class City:

    def __init__(self, city, location=None):
        self.nom = city
        self.ville = city.split(', ')[0]
        self.pays = city.split(', ')[1]

        self.location = geolocator.geocode(city, timeout=10) if location == None else location
        self.city = self.location.raw["display_name"].split(",")[0]
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude

    def copy(self):
        return City(self.nom, self.location)