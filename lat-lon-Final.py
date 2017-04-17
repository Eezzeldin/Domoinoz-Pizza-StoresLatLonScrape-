# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 20:51:06 2016

@author: emadezzeldin
"""


from bs4 import BeautifulSoup
import requests
import re

'''
OUTLINE
=======
PART 1 : Making a Dictionary (key value : states) of lists containing "URLs" of every store in every state
PART 2 : Making a csv file with the address of every store
    
'''

'''
=================================PART 1========================================
'''

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#Make all states in "states" lower case          
for x in range (0 , len(states)):
         states[x] = states [x].lower()

rootURL = 'http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us/'
statesFindAlllist =[]
for x in range (0 , len(states)):
    state = states[x] 
    state_String =  rootURL + state
    state_HTML = requests.get(state_String)
    state_Soup = BeautifulSoup(state_HTML.content)
    pattern = re.compile('<a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title', re.IGNORECASE)
    statesFindAll = re.findall(pattern, str(state_Soup))
    statesFindAlllist.append (statesFindAll)# List of tuples: 51 state each with its pattern matching cases.



storenumcity =[]

Dict = {} # State : URL 
#For loop for the complete URL which includes city and store num         
for n in range (0,len(statesFindAlllist)):
    Dict[states[n]] = ""
    storenumcity =[]
    for y in range (0,len(statesFindAlllist[n])):
        storenumcity_pattern = re.compile('(?<=")(.*?)(?=")', re.IGNORECASE)
        storenumcitySearch = re.search(storenumcity_pattern, str(statesFindAlllist[n][y]))
        storenumcity.append (storenumcitySearch.group())
        Dict[states[n]]=storenumcity
       

'''
=================================PART 2========================================
'''

lonlatDict = {}
for state in states:
    for link in Dict[state]:
        URL = link
        lon_lat_HTML = requests.get(URL)
        lon_lat_Soup = BeautifulSoup(lon_lat_HTML.content)
        
        stornum_pattern = re.compile("\d.*\d", re.IGNORECASE)        
        stornumSearch = re.search(stornum_pattern, URL)
        
        lonpattern = '(?=lat=)(.*?)(?=\d&)'
        latpattern = '(?=lng=)(.*?)(?=\d&)'
        
        lonpattern_1 = re.compile(lonpattern, re.IGNORECASE)
        lon_Search = re.search(lonpattern, str(lon_lat_Soup))
                
        
        latpattern_1 = re.compile(latpattern, re.IGNORECASE)
        lat_Search = re.search(latpattern, str(lon_lat_Soup))

        if  stornumSearch and lon_Search and lat_Search is not None:
            lonlatDict [stornumSearch.group()] = [lon_Search.group(),lat_Search.group()]
          
            
import csv
with open('mycsvfile.csv','wb') as f:
    w = csv.writer(f)
    w.writerows(lonlatDict.items())