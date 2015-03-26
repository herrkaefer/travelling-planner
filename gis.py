#!/usr/local/bin/python
#-*- coding: utf-8 -*-

# import googlemaps
import logging
from util import distance_by_latlng


def get_roadmap(points, point_type, dist_type):
	n = len(points)
	roadmap = [[0 for x in range(n)] for x in range(n)]
	for i, p1 in enumerate(points):
		for j, p2 in enumerate(points):
			if j <= i: 
				continue
			if point_type == "latlng" and dist_type == "Euclidean":
				# print i, j, distance_by_latlng(p1[0], p1[1], p2[0], p2[1])
				roadmap[i][j] = roadmap[j][i] = distance_by_latlng(p1[0], p1[1], p2[0], p2[1])
			elif point_type == "latlng" and dist_type == "Driving":
				# use google api
				pass
			else:
				logging.WARNING("unknown point type or distance type")
				return None

	return tuple(map(tuple, roadmap))
