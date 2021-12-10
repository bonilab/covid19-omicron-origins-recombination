#!/usr/bin/python3 -tO
# -*- coding: utf-8 -*-

# -O compiles to PYC files which are faster
# -t gives you whitespace warnings
# if this happens to select-all in emacs and "reindent"

# -t -t issues an error 

import os
import sys
import re
import glob
import random


#from basic_tools import *

if len( sys.argv ) != 2:
    print("\n\tUSAGE: rename.py   infile \n")
    sys.exit(-1)
    
infile = open( sys.argv[1], 'r' )

s = infile.readline()
while len(s) > 0:
    
    if s[0] != ">":
        print(s[:-1])
        s = infile.readline()
        continue
    
    ll = s.split('|')
    if len(ll) == 4:
        
        print( ll[0][:-1] + "_" + ll[2] + "_" + ll[3][:-1] )
    
    else:
        
        print(s[:-1])

    s = infile.readline()    
    
    
infile.close()
