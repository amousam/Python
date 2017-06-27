
#The purpose of this code is to quickly estimate the boundaries of a floodplain behind a levee based on a uniform value of an elevation
list = [835.687998,837.257842,836.223039,845.940659,844.685716,848.890725,848.802865,850.841569,847.214562,845.407858,840.000707,851.19067,853.694535,845.092557,848.326824,850.636869,849.437666,854.444576,
881.304831,852.687633,852.701773,	835.342538,838.526644,841.35895,837.245701,838.147643,838.394704,840.426508,833.143693,832.957923,826.141742,837.993461,833.015793,833.123693] #minimum elevation of each levee segment. 
for i in range(0,34): # number of levee segments
	number = i 
	low_point = list[i]
	raster = "P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/StructuralBasedInundation/Raster/levee{}".format(number) #raster with the uniform value 
	extent = "P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/StructuralBasedInundation/shapefiles/{}.shp".format(number) #extent of processing for each levee segment (created previously in arcGIS)
	dem = "P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/04_Modeling/DEMs/DEM_FromTerrain/dem_prj_ft" #5ft DEM from Terrain
	raster_rs ="P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/StructuralBasedInundation/Raster/rs_levee{}".format(number) #results of raster calculator 
	raw_levee="P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/StructuralBasedInundation/shapefiles/raw_levee{}.shp".format(number) #raw floodplain from raster
	merge_levee= "P:/02/NY/Broome_Co_36007C/LAMP/TECHNICAL/StructuralBasedInundation/shapefiles/merge_levee{}.shp".format(number) #dissolved floodplain
	arcpy.gp.CreateConstantRaster_sa(raster, low_point, "FLOAT", "5", extent) #create constant raster based on the list
	arcpy.gp.RasterCalculator_sa("""Int(SetNull("{0}" <= "{1}", "{0}"-"{1}")*1000)""".format(raster,dem),raster_rs) #use raster calculator to remove negative values and convert to integer 
	arcpy.RasterToPolygon_conversion(in_raster=raster_rs, out_polygon_features=raw_levee, raster_field="COUNT") #convert from raster to polygon
	arcpy.Dissolve_management(in_features=raw_levee, out_feature_class=merge_levee, dissolve_field="", statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES") #dissolve raw polygon 


