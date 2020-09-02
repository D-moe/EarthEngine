import ee
import json

import numpy as np

ee.Initialize()
area = ee.Geometry.Polygon([[11.143450874999994, 47.835723546120256],\
                            [12.022357124999994, 47.835723546120256],\
                            [12.022357124999994, 48.42234523396127],\
                            [11.143450874999994, 48.42234523396127],\
                            [11.143450874999994, 47.835723546120256]])

def LatLonImg(img):
    img = img.addBands(ee.Image.pixelLonLat())
 
    img = img.reduceRegion(reducer=ee.Reducer.toList(),\
                                        geometry=area,\
                                        scale=100)
 
    data = np.array((ee.Array(img.get("AVE_DSM")).getInfo()))
    lats = np.array((ee.Array(img.get("latitude")).getInfo()))
    lons = np.array((ee.Array(img.get("longitude")).getInfo()))
    print("Num longs is "+str(len(lats)))
    print("Num lats is "+str(len(lons)))
    print("Size of data is"+str(len(data)))
    return lats, lons, data
# covert the lat, lon and array into an image
def toImage(lats,lons,data):
    print("Num longs is "+str(len(lats)))
    print("Num lats is "+str(len(lons)))
    print("Size of data is"+str(len(data)))
    # get the unique coordinates
    uniqueLats = np.unique(lats)
    uniqueLons = np.unique(lons)
 
    # get number of columns and rows from coordinates
    ncols = len(uniqueLons)
    nrows = len(uniqueLats)
 
    # determine pixelsizes
    ys = uniqueLats[1] - uniqueLats[0]
    xs = uniqueLons[1] - uniqueLons[0]
 
    # create an array with dimensions of image
    arr = np.zeros([nrows, ncols], np.float32) #-9999
 
    # fill the array with values
    counter =0
    for y in range(0,len(arr),1):
        for x in range(0,len(arr[0]),1):
            if lats[counter] == uniqueLats[y] and lons[counter] == uniqueLons[x] and counter < len(lats)-1:
                counter+=1
                arr[len(uniqueLats)-1-y,x] = data[counter] # we start from lower left corner
    return arr

#dataset = ee.Image('USGS/GMTED2010').clip(area)
dataset = ee.Image("JAXA/ALOS/AW3D30/V2_2").clip(area)
lat, lon, data = LatLonImg(dataset)
 
# 1d to 2d array
image  = toImage(lat,lon,data)
lists = data.tolist()
json_str = json.dumps(lists)
file = open("finalOutput.json", "w")
file.write(json_str)