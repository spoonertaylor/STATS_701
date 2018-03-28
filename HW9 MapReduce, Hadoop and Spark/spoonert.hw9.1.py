# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 10:14:45 2018

@author: spoonertaylor

This file is to answer #1 in STATS 701 HW9
Count the word frequency of a file.
"""

from mrjob.job import MRJob
import re

# Regex to only get words
# Decided to keep apostophes, however, hyphened words will be split up.
word_re = re.compile(r'[a-zA-Z_\']+')
# Each MR Job makes you make a class that extends MRJob
class MRWordFrequencyCount(MRJob):
    # Mapper. For each word in the line, yield that word and a count of 1
    def mapper(self, _, line):
        for word in word_re.findall(line):
            yield word.lower(), 1
    # Combine all the same words together by counting how many times they occued
    def combiner(self, word, count):
        yield word, sum(count)
    # Reduce over all nodes to get word count.
    def reducer(self, word, count):
        yield word, sum(count)

### YOU MUST HAVE THESE LINES!!!
if __name__ == '__main__':
    MRWordFrequencyCount.run()
