#!/usr/local/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 10:01:17 2015

@author: annacurrey, naszka, fatalinha

Executable file for statistical language modeling assignment 2

Reads in UTF-8 sentences from stdin
Outputs log10 probabilities of each word to stdout
Allows for arbitrary length n-grams
Required command-line argument: name of ARPA file

TO DOs (improvements):
    1. more checking of input
    2. store arpa model as a trie instead of a dictionary
    3. make the reading in of the arpa model more portable 
        (ex. check highest n against n-gram counts)
    4. what to do about highest order (no back-off)? -- dummy value?
    5. check that the highest order we get is what is expected when reading in model
    6. speed up reading in of model
"""

## will need to read in command line arguments
import sys

## strings containing relevant meta info
CURRENT_VERSION = "1.3"
USAGE_INFO = "Usage: ./lm-query.py lm.arpa\n"
USAGE_INFO +="version\t--v\tDisplay version of QueLMy and exit.\n"
USAGE_INFO += "-help\t--h\tPrint this help.\n"
USAGE_INFO +="-lm.arpa\tName of the ARPA file\n"
USAGE_INFO +="exit\t\tType to exit "
REPO_URL = "https://github.com/fatalinha/LM_Assignment2"
COPYRIGHT = "Copyright (C), 2015, Currey A., Naszadi K., Karakanta A.\n""This is free software: you are free to change and redistribute it.\n""There is NO WARRANTY, to the extent permitted by law."

def prob(seq, model):
    """ calculates probability for the last element in seq
     n-gram order is the length of seq"""
    if seq in model:

        return (model[seq][0], len(seq))
    elif len(seq) == 1:   #this is an OOV, it isn't in the model, and is one long
        return (model[("<unk>",)][0],0) #return 0 for order if OOV
    elif seq[:len(seq)-1] in model:

        pr=prob(seq[1:], model)
        return (model[seq[:len(seq)-1]][1] + pr[0], pr[1])
    else:

        return prob(seq[1:], model)

def prob_sentence(sentence, order, model):
    total=0
    OOVs=0
    
    for i in range(1,len(sentence)):

        if i < order:
            pr=prob(sentence[:i+1], model)

        else:
            pr=prob(sentence[i-order+1:i+1],model)
        s=sentence[i]+" "+str(pr[1])+" "+str(pr[0])+"\t"
        sys.stdout.write(s)
        total+=pr[0]
        if pr[1] == 0:
            OOVs+=1
    sys.stdout.write("Total: "+str(total)+"\t"+"OOVS:"+str(OOVs)+"\n")
    return total
    
def read_arpa(arpa_file):
	## read in and store arpa model -- currently dictionary {ngram:(prob, backoff)}
	arpa_model = {}

	# open the arpa file
	with open(arpa_file, 'r') as file:
		# keep track of where we are 
		# -1 is before any n-grams, 0 is n-gram counts, 1 is 1-grams, etc.
		position = -1
		
		# read in line by line
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
							arpa_model[tuple(split_line[1].split())] = (float(split_line[0]), float(split_line[2]))
						# careful -- highest order doesn't have back-off!
						elif len(split_line) == 2:
							# use dummy value (100) instead
							arpa_model[tuple(split_line[1].split())] = (float(split_line[0]), 100.0)
						else:
							print("Unexpected number of arguments in a line!")
	return arpa_model, position

def main():
	## argument checking
	# check number of arguments (need exactly 1)
	if len(sys.argv) != 2:
		print(USAGE_INFO)
		print("Enter --help for more information")
		sys.exit(1)

	# check argument
	elif sys.argv[1] in ("--version", "-v"):
		## Version info
		print("QueLMy version " + CURRENT_VERSION)
		print(COPYRIGHT)
		sys.exit(0)
	elif sys.argv[1] in ("--help", "-h"):
		## print out help info
		print("Language model querying software\n")
		print(USAGE_INFO)
		print("Reads in UTF-8 sentences (one per line) from stdin")
		print("Outputs log10 probabilities of each word based on lm.arpa\n")
		print("See " + REPO_URL + " for more information")
		sys.exit(0)
	else:
		arpa_file = sys.argv[1]
		arpa_model, order=read_arpa(arpa_file)
		
	## read in test sentence(s) from stdin and process it
	to_process="" # variable holding the text waiting to be processed
	total=0 #variable holding total of log10 probs
	num_of_words=0 #number of all words
	while True:
		line=sys.stdin.readline()
		if line == "":
			break # exit for reading a file
		if line.strip("\n") =="exit":
			break  #exit for console input
		else:
			to_process+=line.replace("\n"," ")
			#processing is done sentence by sentence
			s, punct, rest = to_process.partition(".")  # TO DO should be done with regex for all end of sentence punct
			if punct=="":  #there was no end of sentence in this line
					continue
			while rest != "": #processing all sentences in buffer
				sentence="<s> "+s+" "+punct+" </s>"
				sentence=sentence.lower()
				sentence=sentence.split()
				num_of_words+=len(sentence)-1 #substract 1, because <s> doesn't have prob
				to_process=rest
				total+=prob_sentence(tuple(sentence),order,arpa_model)
				print(total)
				s, punct, rest = to_process.partition(".")

	#process what is left in buffer
	if to_process !=" ":
		sentence="<s> "+to_process
		sentence=sentence.lower()
		sentence=sentence.split()
		num_of_words+=len(sentence)-1 #substract 1, because <s> doesn't have prob
		total+=prob_sentence(tuple(sentence),order,arpa_model)


	#calculate perplexity and write to stderr

	perplexity=2**(total/num_of_words)
	sys.stderr.write("perplexity: "+str(perplexity)+"\n")
	return 0
	
if __name__ == '__main__':
	main()


## TESTING (SANITY CHECKS)
#print("probability of the:", arpa_model["the"][0])
#print("backoff of i am at:", arpa_model["i am at"][1])
#print("highest order:", position)
#print("probabiblity of compared:",  prob(("<s>","that","number", "compared"),arpa_model))
#print(prob_sentence(tuple("<s> that number compared with about".split()),position,arpa_model))

