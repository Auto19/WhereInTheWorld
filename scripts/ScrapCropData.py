import os
import time
from PIL import Image, ImageOps, ImageEnhance



items = ["Corn", "Barley", "Cotton", "Millet", "Palmoil", "Peanut", "Rapeseed", "Rice", "Sorghum", "Soybean", "Sunflower", "Wheat"]

# theoretically should get an image
TypicalUrl = "https://gis.ipad.fas.usda.gov/arcgis/rest/services/CommodityExplorerCorn/MapServer/export?bbox=-180.0000%2C+-90.0000%2C+180.0000%2C+90.0000&bboxSR=&layers=&layerDefs=&size=5400%2C2700&imageSR=&historicMoment=&format=png&transparent=true&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&rotation=&datumTransformations=&layerParameterValues=&mapRangeValues=&layerRangeValues=&f=image"


for i in range(len(items)):
    URL = "https://gis.ipad.fas.usda.gov/arcgis/rest/services/CommodityExplorer" + items[i] + "/MapServer/export"
    data = "bbox=-180.0000%2C+-90.0000%2C+180.0000%2C+90.0000&bboxSR=&layers=&layerDefs=&size=5400%2C2700&imageSR=&historicMoment=&format=png&transparent=true&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&rotation=&datumTransformations=&layerParameterValues=&mapRangeValues=&layerRangeValues=&f=image"
    os.system("cd ../imgs/crops/ && curl -X POST " + URL + " -H \"Content-Type: application/x-www-form-urlencoded\" -d \"bbox=-180.0000%2C+-90.0000%2C+180.0000%2C+90.0000&bboxSR=&layers=&layerDefs=&size=5400%2C2700&imageSR=&historicMoment=&format=png&transparent=true&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&rotation=&datumTransformations=&layerParameterValues=&mapRangeValues=&layerRangeValues=&f=image\"" + "> " + items[i] + "_original.png")

    time.sleep(7)



def invert(image):
    return image.point(lambda p: 255 - p)


for i in items:
    try:
        img = Image.open(os.path.join(os.getcwd(),'../imgs/crops/') + i + "_original.png").convert("RGBA") # opens image

        #thanks stack Overflow : https://stackoverflow.com/questions/11484204/python-invert-image-with-transparent-background-pil-gimp
        r, g, b, a = img.split()
        r, g, b = map(invert, (r, g, b))

        img = Image.merge(img.mode, (r, g, b, a))

        img = img.convert('LA') # converts to grayscale w/ alpha

        img = ImageEnhance.Brightness(img).enhance(3)  # the image we get isnt that bright, so we need to scale it so it contrasts properly on the map

        img.save(os.path.join(os.getcwd(),'../imgs/crops/') + i + '.png') # saves image result into new file
    except:
        print("Error on File: " + i + "_original.png, check if file is corrupted.");
