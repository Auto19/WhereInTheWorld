
#someone did the hard work for us
from FlightRadar24.api import FlightRadar24API

from PIL import Image, ImageDraw
import os

fr_api = FlightRadar24API()

flights = fr_api.get_flights()

#                  a   b      c   d
# I need to shift -180,180 to 0,4096
def shiftlong(long):
    return 0 + ((4096 - 0)/(180 + 180)) * (long + 180)

#        a   b    c   d
# shift -90,90 to 2048,0
def shiftlat(lat):
    return 2048 + ((0 - 2048)/(90 + 90)) * (lat + 90)



FlightImg = Image.new("RGBA", (4096,2048), (255, 255, 255, 0))#(4096,2048), (255, 255, 255, 0))
FlightDraw = ImageDraw.Draw(FlightImg)

for flight in flights:
    x1 = shiftlong(flight.longitude)
    y1 = shiftlat(flight.latitude)

    FlightDraw.rectangle([(x1, y1), (x1+6, y1+6)], fill=(255, 255, 255, 255))


FlightImg.save(os.path.join(os.getcwd(),'../imgs/flights/') + 'Flights.png')
