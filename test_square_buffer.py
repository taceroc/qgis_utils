"""
    Create square buffers around coordiante locations and add buffer layer to qgis project
    The buffers created here are temporal files, you need to modify this code or save the layer by hand
"""
# 'delta_state' is coordinate points
layer = QgsProject.instance().mapLayersByName("delta_state")[0]
feats = [ feat for feat in layer.getFeatures() ]
epsg = layer.crs().postgisSrid()
# store in a temporal file
uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer&field=x:real&field=y:real&field=point_id:integer""&index=yes"
mem_layer = QgsVectorLayer(uri,
                           'square_buffer',
                           'memory')
prov = mem_layer.dataProvider()

# loop over each point and create a buffer of 500 m around it (I believe the units change depending on the EPSG)
for i, feat in enumerate(feats):
    if feat.geometry().isNull():
        print(f'Geometry null {i}')
    else:
        point = feat.geometry().asPoint()
        new_feat = QgsFeature()
        new_feat.setAttributes([i, point[0], point[1], feat.id()])
        bbox = feat.geometry().buffer(500, -1).boundingBox()
        tmp_feat = bbox.asWktPolygon()
        xmin1,ymin1,xmax1,ymax1 = bbox.toRectF().getCoords()
        xmin2,ymin2,xmax2,ymax2 = feat.geometry().buffer(500, -1).boundingBox().toRectF().getCoords()
        #p1 = QgsPoint(xmin1, ymax2)
        #p2 = QgsPoint(xmax1, ymin2)
        new_ext = QgsRectangle(xmin1, ymin2, xmax1, ymax2)
        new_tmp_feat = new_ext.asWktPolygon()
        new_feat.setGeometry(QgsGeometry.fromWkt(new_tmp_feat))
        prov.addFeatures([new_feat])
# show the temporal file
QgsProject.instance().addMapLayer(mem_layer)
# This loop creates buffer for the individual points, there is going to be overlap, 
# merge/dissolve the buffers that have overlap to create a big (in some cases no square) buffer


layer = QgsProject.instance().mapLayersByName("square_buffer")[0]
layer_dissolve_shp = processing.run("native:dissolve", {'INPUT':layer,'FIELD':[],'SEPARATE_DISJOINT':True, 'OUTPUT':'memory:'})["OUTPUT"]
QgsProject.instance().addMapLayer(layer_dissolve_shp)