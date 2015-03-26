#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import googlemaps
from itertools import combinations


# all_waypoints = ["Beijing, China",
#                  "Shijiazhuang, Hebei, China",
#                  "Jinan, Shandong, China",
#                  "Chengdu, Sichuan, China",
#                  "Guangzhou, Guangdong, China",
#                  "Hefei, Anhui, China",
#                  "Zhengzhou, Henan, China"]

all_waypoints = ["北京",
                 "石家庄",
                 "济南",
                 "成都",
                 "广州",
                 "合肥",
                 "郑州"]

gmaps = googlemaps.Client(key="AIzaSyBjlzNKt3fYpYbxtEgwbdVXheMGK3mPYqI")


waypoint_distances = {}
waypoint_durations = {}

for (waypoint1, waypoint2) in combinations(all_waypoints, 2):
    try:
        print (waypoint1, waypoint2)
        route = gmaps.distance_matrix(origins=[waypoint1],
                                      destinations=[waypoint2],
                                      mode="driving",
                                      language="Chinese",
                                      units="metric")

        # "distance" is in meters
        distance = route["rows"][0]["elements"][0]["distance"]["value"]

        # "duration" is in seconds
        duration = route["rows"][0]["elements"][0]["duration"]["value"]

        waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
        waypoint_durations[frozenset([waypoint1, waypoint2])] = duration
    
    except Exception as e:
        print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))


with open("my-waypoints-dist-dur.tsv", "wb") as out_file:
    out_file.write("\t".join(["waypoint1",
                              "waypoint2",
                              "distance_m",
                              "duration_s"]))
    
    for (waypoint1, waypoint2) in waypoint_distances.keys():
        out_file.write("\n" +
                       "\t".join([waypoint1,
                                  waypoint2,
                                  str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                  str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))
