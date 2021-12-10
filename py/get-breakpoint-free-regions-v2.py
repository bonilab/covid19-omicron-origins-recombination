#!/usr/bin/python3 -tO
# -*- coding: utf-8 -*-

# -O compiles to PYC files which are faster
# -t gives you whitespace warnings
# if this happens to select-all in emacs and "reindent"

# -t -t issues an error 

import os
import sys
import re
#from basic_tools import *

from operator import itemgetter

# alignment length should be 29903 here (3/18/2021)
if len( sys.argv ) != 3:
    print("\n\tUSAGE: get-breakpoint-free-regions.py    3s.rec.csv   alignment_length\n")
    sys.exit(-1)


infile1  = open( sys.argv[1], 'r' )
strHeader = infile1.readline()	# this is the header line 

alignment_length = int( sys.argv[2] ) # 29901 for set1 , 29903 for set3

lst_all_breakpoints = []

s = infile1.readline()
while len(s) > 0:
    l = s.split(',')

    # this loops through all the end-cells for each line that contain all of the breakpoint-range combinations
    for i in range(12,len(l)):
        
        # bppair has two elements "a-b" and "c-d"
        bppair = l[i].split('&')
        
        if len(bppair)==2:
            
            range_ends_1 = bppair[0].split('-')
            range_ends_2 = bppair[1].split('-')
            
            leftbp1 = int(range_ends_1[0])
            rightbp1 = int(range_ends_1[1])
            leftbp2 = int(range_ends_2[0])
            rightbp2 = int(range_ends_2[1])
            
            # if the breakpoints are b1 and b2 (these are spaces between nucleotides)
            # then it's nucleotides b1+1 to b2 (inclusive) that have to be excluded from 
            # the breakpoint-free regions
            
            # all the js below are "breakpoint nucleotide positions", which have to
            # be complemented to get the BFR
            
            for j in range(leftbp1+1,rightbp1+1):
                lst_all_breakpoints.append(j)
                
            for j in range(leftbp2+1,rightbp2+1):
                lst_all_breakpoints.append(j)
                
            #bp1 = int( ( int(range_ends_1[0]) + int(range_ends_1[1]) ) / 2.0 )
            #bp2 = int( ( int(range_ends_2[0]) + int(range_ends_2[1]) ) / 2.0 )
            
            #lst_all_breakpoints.append(bp1)
            #lst_all_breakpoints.append(bp2)
            #print bp1, bp2
        #print bppair



    s = infile1.readline()

#print( "\n" )
##print( lst_all_breakpoints  )
#print( "\n" )
#print( "\n" )
#print( len( lst_all_breakpoints ) )
#print( "\n" )
#print( len( set(lst_all_breakpoints) ) )

infile1.close()

lst_sorted_nucleotides_nonBFR = sorted( set ( lst_all_breakpoints) ) 

LL = []
current_bfr_pair=[]

if 1 in lst_sorted_nucleotides_nonBFR:
    inside_bfr = False
    outside_bfr = True
else:
    inside_bfr = True
    outside_bfr = False
    current_bfr_pair.append(1)


for ntpos in range(2,alignment_length+1):

    if inside_bfr:
        
        if ntpos in lst_sorted_nucleotides_nonBFR:
        
            current_bfr_pair.append(ntpos-1)
            if len(current_bfr_pair)==2:
                LL.append( current_bfr_pair )
                current_bfr_pair = []
            inside_bfr = False
            outside_bfr = True
            continue
        
        else:
            
            continue    
        
        
    if outside_bfr:
        
        if ntpos in lst_sorted_nucleotides_nonBFR:
        
            continue
        
        else:
            
            current_bfr_pair.append(ntpos)
            if len(current_bfr_pair) != 1:
                print("\n\tERROR 1")
                #LL.append( current_bfr_pair )
                #current_bfr_pair = []
            inside_bfr = True 
            outside_bfr = False
            continue
#end loop through ntpos of entire alignment

if inside_bfr:
    if len(current_bfr_pair) != 1:
        print("\n\tERROR 2")
    current_bfr_pair.append(alignment_length)
    LL.append( current_bfr_pair )
    
# LL is the list that holds the start points and end points of all the BFRs

#print( LL )
        

for l in LL:
    l.append( l[1]-l[0]+1 )
    

#print(LL)

LL_sorted = sorted(LL, key=itemgetter(2), reverse=True)

for l in LL_sorted:
    print(l[0], ", ", l[1], ", ", l[2])









