#!/usr/local/bin/python
#-*- coding: utf-8 -*-

# simple TSP solver

import random
import logging
import gis


def get_random_route(n, start, end):
	r = range(n)
	try:
		r.remove(start)
		if start != end:
			r.remove(end)
	except ValueError:
		logging.ERROR("start or end point error.")

	random.shuffle(r)
	r.insert(0, start)
	r.append(end)
	return r


def tsp_2_opt(route, roadmap):
	reduced_cost = 0.0
	improved = True;
	epsilon = 1e-6;
	start = 0
	end = len(route) - 1

	while (improved):
		improved = False
		for i in range(start, end-1):
			for j in range(i+1, end):
				delta_cost = roadmap[route[i-1]][route[j]] + roadmap[route[i]][route[j+1]] \
						- roadmap[route[i-1]][route[i]] - roadmap[route[j]][route[j+1]]
				# todo: for directed graph, to add more to delta_cost ...

				if delta_cost < -epsilon:
					route[i:j+1] = reversed(route[i:j+1])
					reduced_cost += delta_cost
					improved = True
					print "improved: %f" % delta_cost

	return route, reduced_cost


def solve_tsp(points, start=0, end=0, point_type="latlng", dist_type="Euclidean"):
	
	roadmap = gis.get_roadmap(points, point_type, dist_type)
	if not roadmap:
		logging.ERROR("can't get roadmap")
		return
	# print roadmap
	print points

	route = get_random_route(len(points), start, end)
	print "init route: "
	print route

	route, reduced_cost = tsp_2_opt(route, roadmap)
	print "optimal route:"
	print route
	print reduced_cost
	return route


def test():
	pass

if __name__ == '__main__':
	test()
	