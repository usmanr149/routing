#!/usr/bin/python
#----------------------------------------------------------------
# routeAsCSV - routes with OSM data, and generates a
# CSV file containing the result
#
#------------------------------------------------------
#------------------------------------------------------
# Copyright 2007-2008, Oliver White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------
from route import Router
from loadOsm import LoadOsm
import gpxpy.geo
import geopy.distance

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


def routeToCSV(lat1,lon1,lat2,lon2, transport):
  """Format a route (as list of nodes)"""
  data = LoadOsm(transport)

  node1 = data.findNode(lat1,lon1)
  node2 = data.findNode(lat2,lon2)

  router = Router(data)
  result, route = router.doRoute(node1, node2)
  if result != 'success':
    return("Fail")

  output = ''
  distance = 0
  for i in route:
    try:
      old_node = new_node
      new_node = data.rnodes[i]
      distance+=geopy.distance.vincenty((new_node[0], new_node[1]), (old_node[0], old_node[1])).km
      print(distance)
    except UnboundLocalError:
      new_node = data.rnodes[i]
    """output = output + "%d,%f,%f\n" % ( \
                  i,
                  node[0],
                  node[1])"""
  return(distance)

def routeToCSVFile(lat1,lon1,lat2,lon2, transport, filename):
  f = open(filename,'w')
  f.write(routeToCSV(lat1,lon1,lat2,lon2, transport))
  f.close()

if __name__ == "__main__":
  print (routeToCSV(
    52.2181,
    0.1162,
    52.2184,
    0.1427,
    "cycle"))
