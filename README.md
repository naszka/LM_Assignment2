QueLMy 1.3
==========

Language model querying software.

How it works
============
QueLMy reads ARPA files, a file format used for N-gram back-off models.
It reads UTF-8 sentences from stdin and outputs the log10 probabilities to stdout.
The stdout format is word, length of history, log10probability.
The software allows for arbitrary n-gram lengths, depending on the n-gram length of the ARPA file.

Usage
=====
Run:  
        `bin/lm-query.py lm.arpa` where lm.arpa is the name of the ARPA file.

The query text can then be typed or read in from a file. 
In the first case, add a period (.) to the end of the sentence.  
Log10 probabilities for every word will then be displayed.
Enter "exit" to quit and display the total perplexity in stderr.


QueLMy
------
Version 1.3  
Contributions to QueLM are welcome.  
Hosted on https://github.com/fatalinha/LM_Assignment2/blob/master/lm-query.py
