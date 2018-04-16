# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:04:15 2018

@author: spoonertaylor
This file is to answer #3 in STATS 701 HW9
Count triangles in a tree
"""

from pyspark import SparkConf, SparkContext
import sys
from itertools import combinations

if(len(sys.argv) != 3):
    print('Usage' + sys.argv[0] + ' <in> <out>')
    sys.exit(1)

# Input file, output file
inputLocation = sys.argv[1]
outputLocation = sys.argv[2]

# Set up spark
conf = SparkConf().setAppName("CountTri")
sc = SparkContext(conf=conf)

# Reads in the entire directory.
data = sc.textFile(inputLocation)

# Define the mapper to be used
def mapper(data):
    keys = []
    # Split the space seperated line into a list
    data = data.split()
    # Head friend is friends with the people in this line
    head_friend = int(data[0])
    # The friends of the head friend
    rest_friends = data[1:]
    rest_friends = [int(x) for x in rest_friends] # Change all to ints
    # Get all of the two combinations of the rest of the list
    combos = combinations(rest_friends, 2)
    for c in combos:
        # Add the head friend to the combination
        # c_list = [head_friend, *c] Doesn't work because python 3
        c_list = [head_friend, c[0], c[1]]
        c_list.sort() # Sort so smallest number is first
        # Key: (tuple of three friends)
        # Value: 1
        keys.append((tuple(c_list), 1))
    
    return keys

# Map the data into key-value paris
data2 = data.flatMap(mapper)
# Sum up how many times this appears and then filter for the ones more than 2
# For their to be a triangle, tuple must 
data3 = data2.reduceByKey(lambda x,y: x+y).filter(lambda x: x[1] >= 2)

tris = data3.keys().sortBy(lambda x: x)
tris = tris.map(lambda t: str(t[0]) + " " + str(t[1]) + " " + str(t[2]))
tris.saveAsTextFile(outputLocation)