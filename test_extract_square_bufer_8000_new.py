"""
    Extract google earth raster of each merge-big buffer from from previous script 'test_square_buffer'
    Save the rasters in a local directory
    
"""
#'output' is the merge-big buffer layer from the previuos script
layer = QgsProject.instance().mapLayersByName("output")[0]
feats = [ feat for feat in layer.getFeatures() ]
# 'google satellite' is XYZ tiles added to QGIS and to the project
layer = QgsProject.instance().mapLayersByName("google satellite")[0]
renderer = layer.renderer()
provider = layer.dataProvider()
crs = layer.crs().toWkt()
pipe = QgsRasterPipe()
pipe.set(provider.clone())
pipe.set(renderer.clone())
# each raster file is 8000 x 8000 pixels
width, height = 8000, 8000
# From each buffer, it have now an irregular shape due to the merge, create a rectangular shape
# extract rasters/images from google satellite layer within that new reactangular shape
for k, feat in enumerate(feats[1:]):
    extent_big = feat.geometry().boundingBox()
    xmax = extent_big.xMaximum()
    h = extent_big.height()
    w = extent_big.width()
    print(h, w)
    iter_w = int(round((w/0.1)/width,0))
    iter_h = int(round((h/0.1)/height,0))
    print("iterw")
    print(iter_w, iter_h)
    # pixel size is 0.1m
    sy = 8000 * 0.1 #h / iter_h
    sx = 8000 * 0.1 #w / iter_w
    print(sy, sx, xmax)
    xmin = xmax - sx
    for i in range(iter_w):
        ymax = extent_big.yMaximum()
        ymin = ymax - sy
        for j in range(iter_h):
            extent = QgsRectangle(xmin, ymin, xmax, ymax)
            # location to save raster files
            file_writer = QgsRasterFileWriter(f'/data/correct_data/delta/delta_{k}{i}{j}.tif')
            file_writer.writeRaster(pipe,
                                    width,
                                    height,
                                    extent,
                                    layer.crs())
            ymax = ymin
            ymin = ymax - sy
        xmax = xmin
        xmin = xmax - sx
# 363192.0,812001.5
# 361577.2,809442.0
# 359406.2,809992.0



