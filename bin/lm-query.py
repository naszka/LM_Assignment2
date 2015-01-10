#!/usr/local/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 10:01:17 2015

@author: annacurrey

Executable file for statistical language modeling assignment 2

Reads in UTF-8 sentences from stdin
Outputs log10 probabilities of each word to stdout
Allows for arbitrary length n-grams
Required command-line argument: name of ARPA file

TO DOs (must have):
    1. allow command-line arguments like -help, -version (AC)
    2. read in sentences from stdin (KN)
        a. process them (capitalization, punctuation, sentence markers, split words)
        b. output log10 probabilities to stdout (arbitrary length of n-gram)
    3. output total perplexity (2 -- seen and unseen) to stderr (AK)
    4. write the README.md file (AK)
    5. add this script to a bin file on github
    6. check this works on Python 3 (I used 2.7 to write it)

TO DOs (improvements):
    1. more checking of argv
    2. store arpa model as a trie instead of a dictionary
    3. make the reading in of the arpa model more portable
    4. what to do about highest order (no back-off)? -- dummy value?
    5. check that the highest order we get is what is expected when reading in model
    6. speed up reading in of model
"""

## read in command line arguments
import sys

# check number of arguments (need exactly 1)
if len(sys.argv) != 2:
    print "Usage: ./lm-query.py lm.arpa\nEnter -help for more information"
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

# TO DO check input a bit more


## read in and store arpa model -- currently dictionary {ngram:(prob, backoff)}
arpa_model = {}

# open the arpa file
with open(arpa_file, 'r') as file:
    # keep track of where we are 
    # -1 is before any n-grams, 0 is n-gram counts, 1 is 1-grams, etc.
    position = -1
    
    # read in line by line
    # TO DO implement as a trie later
    for line in file:
        # ignore blank lines
        if line.strip():
            # lines that start with backslashes don't have data
            if line[0] == "\\":
                # \data\ line lets us know we can start (n-gram counts)
                if line.strip() == "\\data\\":
                    position += 1
                # \end\ line tells us we are at end of file (don't increment)
                elif line.strip() == "\\end\\":
                    pass
                # otherwise we'll be at the n-grams
                # want to make sure we've actually seen the data line as well
                elif position >= 0:
                    position += 1
                # otherwise do nothing
            
           
            # other lines have data that we wanna keep
            else:
                # ignore if we haven't seen \data\ line, also ignore n-gram counts
                if position >= 1:
                    # split based on tab space
                    split_line = line.split("\t")
                    
                    # store n-grams and back-off in dictionary
                    if len(split_line) == 3:
                        arpa_model[split_line[1]] = (float(split_line[0]), float(split_line[2]))
                    # careful -- highest order doesn't have back-off!
                    elif len(split_line) == 2:
                        # use dummy value (100?) instead TO DO
                        arpa_model[split_line[1]] = (float(split_line[0]), 100.0)
                        # TO DO actually check that highest order
                    else:
                        print "Unexpected number of arguments in a line!"

## TESTING (SANITY CHECKS)
#print "probability of the:", arpa_model["the"][0]
#print "backoff of i am at:", arpa_model["i am at"][1]
#print "highest order:", position

## read in sentences from stdin
# assume 1 sentence per line
# insert the <s> and </s> markers
# also need to normalize (capitalization, punctuation, etc.)
#for line in sys.stdin:
    # word by word
    # calculate the log 10 probabilities
        # if n-gram exists, use that
        # otherwise, sum probability of the word + backoff weights
        # remember to  deal with OOV
        # remember to deal with end of sentence markers
    # write to stdout
        # format: word=index length-of-history log10-probability
#    pass

## calculate perplexity and write to std error

# TO DO note that position variable holds highest n-gram
