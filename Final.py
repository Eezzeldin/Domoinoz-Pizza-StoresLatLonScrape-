# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 06:06:03 2016

@author: emadezzeldin
"""

from bs4 import BeautifulSoup
import requests
import re


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
Dict = {}
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
==============================PART 2 : DATABASE INSERTION======================
'''
import sqlite3



#==============================================================================
# CREATTING A TABLE
#==============================================================================

# connect to the database and create a cursor
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()
# create SQL statement that creates table
sqlString =         """
                    CREATE TABLE DominosStores (
    URL           VARCHAR,
    city          VARCHAR ,
    state         VARCHAR,
    storeNum      VARCHAR 
);
                    """
# execute the string
myCursor.execute(sqlString)
# commit the change
myConnection.commit() 
# close the connection; clean up memory
myConnection.close() 

#==============================================================================
# #INSERTING DATA: 7613 ENTRY 
#==============================================================================
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()

sqlString =          """
                    INSERT INTO DominosStores VALUES (?,?,?,?) 
                    """

URL = []
for y in range (0,len(states)):
    URL = Dict [states[y]]
    Cities = []
    Storenum = []
    for x in range (0,len(URL)):
        city_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
        stornum_pattern = re.compile("\d.*\d", re.IGNORECASE)
        CitySearch = re.search(city_pattern, URL[x])
        stornumSearch = re.search(stornum_pattern, URL[x] )
        Cities.append (CitySearch.group())
        Storenum.append (stornumSearch.group())  
        Entry = [URL[x],Cities[x],states[y],Storenum[x]]
        myCursor.execute(sqlString,Entry)
    
    
myConnection.commit()
myCursor.close()
myConnection.close()

