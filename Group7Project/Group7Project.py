# Group 7 
# Closed Horizontal Traverse Calculations
# Last Edited December 7, 2023

import csv
import math
import os
import arcpy

#Getting the current working directory
cwd = os.getcwd()

#NAME: titleScreen
#PARAMETERS: None
#ARGUMENTS: None
#RETURNS: None
#DESCRIPTION: Displays a fancy title screen for the user to enjoy 
#By Eofor I
def titleScreen():
    print("")
    print("*****************************************************************************************")
    print("*                                                                                       *")
    print("*                            Horizontal Traverse Calculator                             *")
    print("*                                                                                       *")
    print("*****************************************************************************************")
    print("*This application will read a .csv file and then calculate the following:               *")
    print("*Angular Misclosure, Latitude and Departure, Error of Closure, Precision, and Perimeter *")
    print("*****************************************************************************************")
    print("*Assumes the user knows the filepath of their .csv file and formatted the .csv correctly*")
    print("*Angular Misclosure, Latitude and Departure, Error of Closure, Precision, and Perimeter *")
    print("*****************************************************************************************")
    print("*****************************************************************************************")
    print("*                                                                                       *")
    print("*              Created by April M, Venus H, Ashish S, Prateek K, Eofor I                *")
    print("*                                                                                       *")
    print("*****************************************************************************************")
       
#NAME: misclosure
#PARAMETERS: length, angles
#ARGUMENTS: lengths, forwardangs
#DESCRIPTION: Calculates angle of misclosure, using length and forward angles 
#CREATOR: April McBay
def misclosure(length, angles):
    error = ((len(length)-2) * 180)
    rerror = sum(angles)
    angmisclosure = error - rerror
    return angmisclosure

#NAME: latitude
#NAME: departure
#PARAMETERS: length, radian
#ARGUMENTS: lengths[-1], radianvalues[-1]
#DESCRIPTION: Caclulates Latitude and Departure, using length and the calculacted radians
#April McBay    
def latitude(length,radian):
    lat = length * (math.cos(radian))
    return lat
def departure(length,radian):
    dep = length * (math.sin(radian)) 
    return dep

#NAME: errorclosure
#PARAMETERS: latcalc, depcalc
#ARGUMENTS: finallat, finaldep
#RETURNS: fperimeter
#DESCRIPTION: Calculates error of closure, using the already calculated latitude and departure
#Ashish
def errorclosure(latcalc, depcalc):
    x = pow(latcalc,2) + pow(depcalc,2)
    closure = math.sqrt(x)
    return closure

#NAME: perimeter
#PARAMETERS: length
#ARGUMENTS: lengths
#RETURNS: fperimeter
#DESCRIPTION: Calculates the preimter of the entire traverse, using the lengths
#Ashish
def perimeter(length):
    fperimeter = sum(length)
    return fperimeter

#NAME: precision
#PARAMETERS: closure, perimeter
#ARGUMENTS: error_of_closure, perimeter_of_traverse
#RETURNS: fprecision
#DESCRIPTION: Calculates the prescion of accuracy using the already calculated closure and perimeter
#Ashish
def precision(closure, perimeter):
    fprecision = closure/perimeter
    return fprecision

#NAME: dataImport
#PARAMETERS: None
#ARGUMENTS: None
#RETURNS: stations, lengths, forwardangs, latitiude, longitide
#DESCRIPTION: Reads the input file, processes the data
#Code by April M, Modularized by Eofor I 
def dataImport():
    try:
        #Importing data from a csv file and assinging the data by rows to list variables

        #Get the location of the CSV file  
        file_path = cwd + r"\Datafiles\TestValues.csv"

        #creating the list which various values will be assinged too
        stations = []
        lengths = []
        forwardangs = []
        latitiude = []
        longitide = []

        #Opening/reading the file
        with open(file_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

        #assinging the rows into each o the matching empty lists
            for row in readCSV:
            
                station = row[0]
                length = row[1]
                forwardang = row[2]
                lat = row[3]
                long = row[4]

                stations.append(station)
                lengths.append(length)
                forwardangs.append(forwardang)
                latitiude.append(lat)
                longitide.append(long)

        return stations, lengths, forwardangs, latitiude, longitide
    except(RuntimeError, TypeError, NameError):
        pass

#NAME: conversions
#PARAMETERS: latitiude, longitide, lengths, forwardangs
#ARGUMENTS: latitiude, longitide, lengths, forwardangs
#RETURNS: latitiude_t, longitide_t, lat_long, lengths, forwardangs, radianvalues
#DESCRIPTION: Converts some of the data so it may be useable for later calculations
#Code by April M, Modularized by Eofor I 
def conversions(latitiude, longitide, lengths, forwardangs):
    #Changing the list to a tuple
    latitiude_t = tuple(latitiude)
    longitide_t = tuple(longitide)
    #Combines both tuples using the zip() function
    zipped_lat_long = zip(latitiude_t, longitide_t)
    #Converting that zip back to tuple
    lat_long = tuple(zipped_lat_long)

    #Converting the numerical data into a workable format, lengths = floats and angles = floats 
    #by April Mcbay
    lengths = [float(l) for (l) in lengths]
    forwardangs = [float(d) for d in forwardangs]

    #Converts degrees to radians and assigning the new values to radianvalues list
    #by april m
    radianvalues = []
    for d in forwardangs:
        r = math.radians(d)
        radianvalues.append(r)

    return latitiude_t, longitide_t, lat_long, lengths, forwardangs, radianvalues

#NAME: export
#PARAMETERS: anglemisclosure, finallat ,finaldep,error_of_closure,perimeter_of_traverse,fprecision
#ARGUMENTS: anglemisclosure, finallat ,finaldep,error_of_closure,perimeter_of_traverse,fprecision
#RETURNS: none
#DESCRIPTION: Exports the data and final calculations to a .txt file  
#Code by Prateek, Modularized by Eofor I 
def export(anglemisclosure, finallat ,finaldep,error_of_closure,perimeter_of_traverse,fprecision):
 
    txt_location = cwd + r"\Output\Report.txt"

    data = [[anglemisclosure, finallat ,finaldep,error_of_closure,perimeter_of_traverse,fprecision]]
    with open(txt_location,"w") as file:
        for item in data:
            file.write(f"Angle of misclosure is {item[0]}\n"f"Final latitude is {item[1]}\n"f"Final departure is {item[2]}\n"f"Error of Closure is {item[3]}\n"f"Perimeter of Traverse is {item[4]}\n"f"Final precision is {item[5]}\n" )
    print("Data exported. Be happy!")

#NAME: calculateAndAppend
#PARAMETERS: lengths, forwardangs, radianvalues
#ARGUMENTS: lengths, forwardangs, radianvalues
#RETURNS: none
#DESCRIPTION: Starts to run the different calculation functions as well as appending thecalculations to a list so it may be displayed later  
#Code by Prateek, Modularized by Eofor I
def calculateAndAppend(lengths, forwardangs, radianvalues):
    Answers = []

    anglemisclosure = misclosure(lengths, forwardangs)
    answer = "The angle of misclosure in this traverse is", anglemisclosure
    Answers.append(answer)

    finallat = latitude(lengths[-1], radianvalues[-1])
    answer = "The final latitude for this traverse is", finallat
    Answers.append(answer)   

    finaldep = departure(lengths[-1], radianvalues[-1])
    answer = "The final departure for this traverse is", finaldep
    Answers.append(answer)

    error_of_closure = errorclosure(finallat, finaldep)
    answer = "The error of closure in this traverse is:", error_of_closure 
    Answers.append(answer)

    perimeter_of_traverse= perimeter(lengths)
    answer = "The perimeter of the traverse is:", perimeter_of_traverse
    Answers.append(answer)

    fprecision= precision(error_of_closure, perimeter_of_traverse)
    answer = "Precision of the traverse is:", fprecision
    Answers.append(answer)

    #Calls the export function
    export(anglemisclosure, finallat ,finaldep,error_of_closure,perimeter_of_traverse,fprecision)

#NAME: arcpyFunction
#PARAMETERS: none
#ARGUMENTS: none
#RETURNS: none
#DESCRIPTION: The arcpy. Creates the final .aprx and all the components needed to make it work  
#Code mostly by Venus with assistance from April, Eofor
#Modularized by Eofor 
def arcpyFunction(lat_long):
    # Set the workspace environment
    arcpy.env.workspace = cwd + r"\HorizontalSurvey" 

    # Specify a name (for the points shapefile)
    shapefile_name = "Total_Station_points.shp"
    # Create a shapefile with point geometry
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, shapefile_name, "POINT")

    # Add fields for x and y
    arcpy.AddField_management(shapefile_name, "X_Field", "DOUBLE")
    arcpy.AddField_management(shapefile_name, "Y_Field", "DOUBLE")

    # Create an InsertCursor
    with arcpy.da.InsertCursor(shapefile_name, ["SHAPE@", "X_Field", "Y_Field"]) as cursor:
    # Iterate through the data and insert rows
        for xy in lat_long:
            point = arcpy.Point(xy[0], xy[1])
            row = (arcpy.PointGeometry(point), xy[0], xy[1])
            cursor.insertRow(row)


    aprx = arcpy.mp.ArcGISProject(cwd + r"\HorizontalSurvey\HorizontalSurvey.aprx")
    # feature class to feature class (add .shp into .gdb)
    in_feature = "Total_Station_points.shp"
    out_location = (cwd + r"\HorizontalSurvey\HorizontalSurvey.gdb")
    out_feature = "Total_Station_point.shp"
    arcpy.conversion.FeatureClassToFeatureClass(in_feature,out_location,out_feature)

    # Refer the map name (Points) in ArcGIS Pro
    Map = aprx.listMaps("Points")[0]
    # Add layer (path) to map
    data_path = (cwd + r"\HorizontalSurvey\HorizontalSurvey.gdb\Total_Station_point")
    Map.addDataFromPath(data_path)

    # Zoom to layer
    layer = Map.listLayers()[0]
    layout = aprx.listLayouts()[0]
    mapframe = layout.listElements('MAPFRAME_ELEMENT','*')[0]
    mapframe.camera.setExtent(mapframe.getLayerExtent(layer))

    # Change symbology
    layer = Map.listLayers("Total_Station_point")[0]
    sym = layer.symbology
    # set a color
    orange = {"RGB": [255,211,127,100]}
    if layer.isFeatureLayer and hasattr(sym, "renderer"):
        sym.renderer.symbol.color = orange
        layer.symbology = sym # apply to layer

    # Save a copy
    aprx.saveACopy(cwd + r"\Output\Group7Project.aprx")
    del aprx # free up memory


#Main function!
def main():

    #Activates our title screen
    titleScreen()

    #Calls the dataImport function
    stations, lengths, forwardangs, latitiude, longitide = dataImport()

    #Calls the concversions function
    latitiude_t, longitide_t, lat_long, lengths, forwardangs, radianvalues = conversions(latitiude, longitide, lengths, forwardangs)

    #Calls the calculateAndAppend function
    calculateAndAppend(lengths, forwardangs, radianvalues)

    #Calls the arcpyFunction function
    arcpyFunction(lat_long)

#This is mandatory we need this <3 
if __name__ == "__main__":
    main()

