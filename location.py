import geocoder

def getLocation():

    """
    :return: Lat and Long
    """
    try:
        g = geocoder.ip('me')
        my_string=g.latlng
        longitude=my_string[0]
        latitude=my_string[1]

        return longitude,latitude
    except:
        print('Error make sure you have Geo-Coder Installed ')

def buildLocation(lat, long):
    '''
    :return: {"latitude" : xxx, "longitude" : xxx}
    '''
    location = {"latitude" : lat, "longitude" : long}
    return location

if __name__ == '__main__':
    location = getLocation()
    print(f'Your current location is {location[0]} {location[1]}')