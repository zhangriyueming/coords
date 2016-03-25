# -*- coding: utf-8 -*-
from math import *

pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323

def gcj02_encrypt(gps84_lat, gps84_lon):
    if (outOfChina(gps84_lat, gps84_lon)):
    	return gps84_lat, gps84_lon
    lat = gps84_lat
    lon = gps84_lon
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = lat + dLat
    mgLon = lon + dLon
    return mgLat, mgLon

def gcj02_decrypt(gcj02_lat, gcj02_lon):
    lat, lon = gcj02_encrypt(gcj02_lat, gcj02_lon)
    lon = gcj02_lon * 2 - lon
    lat = gcj02_lat * 2 - lat
    return lat, lon

def outOfChina(lat, lon):
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret

x_pi = 3.14159265358979324 * 3000.0 / 180.0

def bd09_encrypt(gg_lat, gg_lon):
	x = gg_lon
	y = gg_lat
	z = sqrt(x * x + y * y) + 0.00002 * sin(y * x_pi) # y * pi
	theta = atan2(y, x) + 0.000003 * cos(x * x_pi) # x * pi
	bd_lon = z * cos(theta) + 0.0065
	bd_lat = z * sin(theta) + 0.006
	return bd_lon, bd_lat

def bd09_decrypt(bd_lat, bd_lon):
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = sqrt(x * x + y * y) - 0.00002 * sin(y * x_pi) # y * pi
    theta = atan2(y, x) - 0.000003 * cos(x * x_pi) # x * pi
    gg_lon = z * cos(theta)
    gg_lat = z * sin(theta)
    return gg_lon, gg_lat


