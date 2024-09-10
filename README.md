# qgis_utils
Python scripts to use with qgis

Three things are needed to use the scripts:
1. QGIS
2. Connect Google Earth with QGIS, I followed this tutorial:
https://gis.stackexchange.com/questions/439936/adding-google-satellite-imagery-to-qgis
3. And then you need geographical coordinates.
   * If the geographical coordiantes are on EPSG 4326 (lat and long), export the layer in EPSG 3857 and add that exported layer, so the units are in meters
