###Created by Molly Marks, GIS Specialist for OHM Advisors
### The purpose of this tool is to define projections and mosaic tiles extracted from Nearmap.com


import arcpy


### Create parameters for Workspace and coordinate system

arcpy.env.workspace = arcpy.GetParameter(0) #workspace
CoordSys = arcpy.GetParameter(1) #coordinate system


### Create List of Tiles so you can do multiple define projections at once,
### this will list ALL rasters in the workspace folder, so make sure you extract your tiles into a folder made specifically to use this tool

Tiles = arcpy.ListRasters()



### perform define projection on each tile in TileList

for tile in Tiles:
    arcpy.management.DefineProjection(tile, CoordSys)




### run mosaic to new raster on Tiles

arcpy.management.MosaicToNewRaster(Tiles,arcpy.env.workspace, r"NearmapMosaic.jpg", "", '8_BIT_UNSIGNED',"", "3", "","")


