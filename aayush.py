

import xlsxwriter
import re
import logging
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data



def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        
        if gps_latitude and gps_latitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

           

    return lat
def get_lon(exif_data):
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
		
        if gps_longitude and gps_longitude_ref:
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lon

import os
import numpy as np

w=[]
for root, dirs, files in os.walk('images'):
    for filename in files:
        w.append([filename])
       
#print(w)
import csv
data=[]
data1=[]
data2=[]
path = 'images' 
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
print('done')
for imagePath in imagePaths:
        image = Image.open(imagePath)
        exif_data = get_exif_data(image)
        data.append(get_lat(exif_data))
        data1.append(get_lon(exif_data))
        data2.append(imagePath)
import os
a=[]
a.append(os.listdir("images"))   
import xlsxwriter  
  
import csv
import pandas as pd
data_tuples = list(zip(data,data1,data2))
print(data_tuples)



with open('file.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(w)
    writer.writerow(data)
    writer.writerow(data1)

