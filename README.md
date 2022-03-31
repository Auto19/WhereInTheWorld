## Description
A project that shows where in the world something is.  Ie where are current planes in the air.

## Controls
Use z and x to zoom

click and drag to move the globe

Select objects to have them rendered on the globe


## To Update Data
cd into the scripts folder (important that you are in there when running the scripts, the scripts use relative pathing)


no command arguments, just run the scripts as they are. Python3

ie 'python3 -i ScrapCropData.py'

## Start the server on localhost as otherwise the image pathing won't work
'servez'

## Potential features
Might come back to these later, but right now the project works as intended

 - county outlines
 - diasters
   - hurricane/tropical storms
   - Tornados
   - Floods
   - Wildfires
   - Earthquakes
 - temprature tracking  -> https://climatereanalyzer.org/
 - implement an update feature to track boat moves and planes (cron job and refresh right now)
 - add storm tracking -> https://gis.ipad.fas.usda.gov/arcgis/rest/services/TCM_Active_Storms/MapServer/export?bbox=-354.025,1.0088043478260431,205.32500000000013,337.4294565217392
 - fix scripts relative pathing
 - implement sprites for planes and boats
 - update event handlers from individual to top-down
