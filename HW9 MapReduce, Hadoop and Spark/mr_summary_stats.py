# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:46:11 2018

@author: spoonertaylor

This file is to answer #2 in STATS 701 HW9

"""
from mrjob.job import MRJob
from functools import reduce

# Each MR Job makes you make a class that extends MRJob
class MRWordFrequencyCount(MRJob):
    # Mapper. For each word in the line, yield that word and a count of 1
    def mapper(self, _, line):
        # Split each line
        l = line.split()
        # Label is first
        label = int(l[0])
        # Get value and cast to int
        value = int(l[1])
        #yield label, value
        yield label, (1, value)

    # Value is of type generator.        
    def reducer(self, label, value):
        #for v in value:
        #    print(v[0])
        N = 0.0
        s = 0.0
        s2 = 0.0
        for v in value:
            N += v[0]
            s += v[1]
            s2 += v[1]*v[1]
#        N = reduce(lambda x,y: x+1, value, 0.0) # Length of values
#        s = reduce(lambda x,y: x+y, value, 0.0) # Sum the values together
#        s2 = reduce(lambda x,y: x+y**2, value, 0.0) # Sum the squared values together
        m = s/N # Find mean
        v = s2/N - m**2 # Find variance
        yield label, (N, m, v)

### YOU MUST HAVE THESE LINES!!!
if __name__ == '__main__':
    MRWordFrequencyCount.run()

