import json
import os
from collections import namedtuple
import sys
from math import log, tan, pi, radians
import time

# globals
Pt = namedtuple('Pt', 'x,y')
Edge = namedtuple('Edge', 'a,b')
Poly = namedtuple('Poly', 'name,edges')
_eps = 1e-5
_huge = sys.float_info.max
_tiny = sys.float_info.min


def load_json():
    file_in = open(os.getcwd() + "/Neighborhoods_2012_polygons.json")
    d = json.load(file_in)
    return d


def spherical_mercator_projection(longitude, latitude):
    # http://en.wikipedia.org/wiki/Mercator_projection <- invented in 1569!
    # http://stackoverflow.com/questions/4287780/detecting-whether-a-gps-coordinate-falls-within-a-polygon-on-a-map
    x = -longitude
    y = log(tan(radians(pi / 4 + latitude / 2)))
    return (x, y)


def rayintersectseg(p, edge):
    # http://rosettacode.org/wiki/Ray-casting_algorithm#Python
    # takes a point p=Pt() and an edge of two endpoints a,b=Pt() of a line segment returns boolean
    a, b = edge
    if a.y > b.y:
        a, b = b, a
    if p.y == a.y or p.y == b.y:
        p = Pt(p.x, p.y + _eps)
    intersect = False

    if (p.y > b.y or p.y < a.y) or (
            p.x > max(a.x, b.x)):
        return False

    if p.x < min(a.x, b.x):
        intersect = True
    else:
        if abs(a.x - b.x) > _tiny:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _huge
        if abs(a.x - p.x) > _tiny:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _huge

        intersect = m_blue >= m_red
    return intersect


def is_odd(x):
    return x % 2 == 1


def ispointinside(p, poly):
    ln = len(poly)
    return is_odd(sum(rayintersectseg(p, edge)
                      for edge in poly.edges))


def get_all_neighborhoods():
    d = load_json()
    shape_list = []
    area_list = []
    for shape_idx in range(len(d['features'])):
        name = d['features'][shape_idx]['properties']['PRI_NEIGH']
        area = d['features'][shape_idx]['properties']['SHAPE_AREA']

        edges = []
        for coordinate_idx in range(len(d['features'][shape_idx]['geometry']['coordinates'][0]) - 1):
            lon_1 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx][0]
            lat_1 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx][1]

            lon_2 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx + 1][0]
            lat_2 = d['features'][shape_idx]['geometry']['coordinates'][0][coordinate_idx + 1][1]

            x1, y1 = spherical_mercator_projection(lon_1, lat_1)
            x2, y2 = spherical_mercator_projection(lon_2, lat_2)
            edges.append(Edge(a=Pt(x=x1, y=y1), b=Pt(x=x2, y=y2)))

        shape_list.append(Poly(name=name, edges=tuple(edges)))
        area_list.append(area)

    return (shape_list, area_list)


def find_neighborhood(test_long, test_lat, all_neighborhoods):
    shape_list = all_neighborhoods[0]
    area_list = all_neighborhoods[1]
    x, y = spherical_mercator_projection(test_long, test_lat)
    for i in range(0, len(shape_list)):
    # for neighborhood in all_neighborhoods:
        correct_neighborhood = ispointinside(Pt(x=x, y=y), shape_list[i])
        if correct_neighborhood:
            return (shape_list[i].name, area_list[i])
			
#all_neighborhoods = get_all_neighborhoods()
#42.0116333	-87.8301961

#test_long = -87.688448576
#test_lat = 41.910760821

#beg = time.time()
#neighborhood = find_neighborhood(test_long,test_lat,all_neighborhoods)
#print(neighborhood[0])
#print(neighborhood[1])
#print(time.time() - beg)