import requests
from PIL import Image, ImageDraw
import os



# need this to get around their blocking methods, recommend getting your own
headers = {

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1'
}

req = requests.get("https://www.vesselfinder.com/api/pub/sfl?bbox=-107994000%2C-41830681%2C107994000%2C50833394&zoom=2", headers=headers, allow_redirects=True)

bytecode = req.content
ships = []

CF = 600000

l = len(bytecode)
o = 4

#if you want more info you need to decode their algorithm in the min-cs file, I only decoded enough of the api to get ship location and type data.
while(o < l):
    r = int.from_bytes(bytecode[o:o + 4], "big", signed=True) / CF
    o+= 4
    g = int.from_bytes(bytecode[o:o + 4], "big", signed=True) / CF
    o += 4
    p = int.from_bytes(bytecode[o:o + 1], "big", signed=True)
    o += 1
    if((p & 128) > 0):
        q = 1
    else:
        q = 0
    f = int.from_bytes(bytecode[o:o + 1], "big",  signed=True)
    o += 1
    k = f & 63
    n = int.from_bytes(bytecode[o:o + 1], "big",  signed=True) & 15
    o += 1

    ships.append({'lat': r, 'lon': g, 'tstamp': p, 'isOLD': q, 'flags': n, 'iconNumber': k })


""" for i in ships:
    print(i)
"""

# image size 4096x2048

# meanings (there are alot more than just this though)
# flag = 4   ->   cargo ship
# flag = 5   ->   fishing vessel
# flag = 7   ->   military
# flag = 6   ->   tanker
#
# icon has to do with orientation/type but that is a lot of work and ships are currently rendered as dots so it doesn't matter that much

# typical ship
# {'lat': -0.21198333333333333, 'lon': 179.8613, 'tstamp': 20, 'isOLD': 0, 'flags': 5, 'iconNumber': 14}

#                  a   b      c   d
# I need to shift -180,180 to 0,4096
def shiftlong(long):
    return 0 + ((4096 - 0)/(180 + 180)) * (long + 180)

#        a   b    c   d
# shift -90,90 to 2048,0
def shiftlat(lat):
    return 2048 + ((0 - 2048)/(90 + 90)) * (lat + 90)


#open, write, close
CargoImg = Image.new("RGBA", (4096,2048), (255, 255, 255, 0))
CargoDraw = ImageDraw.Draw(CargoImg)

FishingImg = Image.new("RGBA", (4096,2048), (255, 255, 255, 0))
FishingDraw = ImageDraw.Draw(FishingImg)

MilitaryImg = Image.new("RGBA", (4096,2048), (255, 255, 255, 0))
MilitaryDraw = ImageDraw.Draw(MilitaryImg)

OtherImg = Image.new("RGBA", (4096,2048), (255, 255, 255, 0))
OtherDraw = ImageDraw.Draw(OtherImg)

for ship in ships:
    x1 = shiftlong(float(ship.get('lon')))
    y1 = shiftlat(float(ship.get('lat')))

    #print(ship)

    if(ship.get('isOLD') == 0):
        if(ship.get('flags') == 4 or ship.get('flags') == 6):
            CargoDraw.rectangle([(x1, y1), (x1+6, y1+6)], fill=(255, 0, 0, 255))

        elif(ship.get('flags') == 5):
            FishingDraw.rectangle([(x1, y1), (x1+6,y1+6)], fill=(255, 191, 0, 255))

        elif(ship.get('flags') == 7):
            MilitaryDraw.rectangle([(x1, y1), (x1+6,y1+6)], fill=(128, 0, 128, 255))

        else:
            OtherDraw.rectangle([(x1, y1), (x1+6,y1+6)], fill=(15, 255, 15, 255))


OtherImg.save(os.path.join(os.getcwd(),'../imgs/boats/') + 'Other.png')
MilitaryImg.save(os.path.join(os.getcwd(),'../imgs/boats/') + 'Military.png')
FishingImg.save(os.path.join(os.getcwd(),'../imgs/boats/') + 'Fishing.png')
CargoImg.save(os.path.join(os.getcwd(),'../imgs/boats/') + 'Cargo.png')
