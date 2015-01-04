# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 10:01:17 2015

@author: annacurrey

Executable file for statistical language modeling assignment 2

Reads in UTF-8 sentences from stdin
Outputs log10 probabilities of each word to stdout
Allows for arbitrary length n-grams
Required command-line argument: name of ARPA file

NOTE: this file is just a skeleton and doesn't actually do anything!!
"""

# TO DO shebang

## read in command line arguments
import sys

# check number of arguments (need at least 1)
if len(sys.argv) < 2:
    print "usage: ./lm-query.py lm.arpa"
    print "enter -help for more information"
    sys.exit(1)

# check first argument
if sys.argv[1] == "-version":
    ## TO DO version info
    sys.exit(0)
elif sys.argv[1] == "-help":
    ## TO DO help info
    sys.exit(0)
else:
    arpa_file = sys.argv[1]

## TO DO should we have length of n-gram as optional command-line arg?

## read in and store arpa model -- dictionary (or multiple dictionaries?)
# unigrams in one array
# n-grams in one dictionary, n > 1
# {(n-gram, length):[prob, backoff]}?

# open the arpa file
with open(arpa_file, 'r') as arpa:
    # read in line by line
    # ignore lines before /data/
    # store n-gram counts
    # store 1-grams
    # store remaining n-grams
    # keep track of the highest n-gram available


## read in sentences from stdin
# assume 1 sentence per line
for line in sys.stdin:
    # word by word
    # calculate the log 10 probabilities
        # if n-gram exists, use that
        # otherwise, sum probability of the word + backoff weights
        # remember to  deal with OOV
        # remember to deal with end of sentence markers
    # write to stdout
        # format: word=index length-of-history log10-probability

## calculate perplexity and write to std error
