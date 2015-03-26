#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import math

def distance_by_latlng(lat1, lng1, lat2, lng2):
	"""
	Getting distance (km) between two points based on latitude/longitude
	"""
	
	R = 6373.0 # earth's radius

	lat1 = math.radians(lat1)
	lng1 = math.radians(lng1)
	lat2 = math.radians(lat2)
	lng2 = math.radians(lng2)

	dlng = lng2 - lng1
	dlat = lat2 - lat1
	a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlng/2))**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	return R * c

if __name__ == '__main__':
	lat1 = 52.2296756
	lng1 = 21.0122287
	lat2 = 52.406374
	lng2 = 16.9251681
	print points_distance_latlng(lat1, lng1, lat2, lng2)

