# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:46:11 2018

@author: spoonertaylor

This file is to answer #2 in STATS 701 HW9
Obtain simple summery stats (sample size, mean and variance).
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from functools import reduce
import sys

# Each MR Job makes you make a class that extends MRJob
class MRWordFrequencyCount(MRJob):
    # Define the steps we are going to take to run this.
    def steps(self):
        return [
                MRStep(mapper=self.mapper, 
                       reducer=self.reducer_sums),
                MRStep(reducer=self.reducer_stats)]
    
    # Mapper. For each word in the line, yield that word and a count of 1
    def mapper(self, _, line):
        # Split each line
        l = line.split()
        if len(l) != 2:
            print(l)
            sys.exit(1)
        # Label is first
        label = int(l[0])
        # Get value and cast to int
        values = float(l[1])
        yield label, values

    # Value is of type generator.        
    def reducer_sums(self, label, values):
        # Reduce by making a tuple, first element is N,
        # Second is summing up the values and third is summing up the squared values
        v = reduce(lambda x, y: (x[0]+1, x[1]+y, x[2]+y**2), values, (0.0,0.0,0.0))
        yield (label, v)#(v[0], v[1]/v[0], v[2]/v[0]))

    def reducer_stats(self, label, values):
        # Our values, v, is now a generator but only of one thing since 
        # we have already reduced. make it a list.
        mn_v = reduce(lambda x,y: (y[0], y[1]/y[0], y[2]/y[0]-(y[1]/y[0])**2), values, (0,0,0))
        yield (label, mn_v)

### YOU MUST HAVE THESE LINES!!!
if __name__ == '__main__':
    MRWordFrequencyCount.run()

