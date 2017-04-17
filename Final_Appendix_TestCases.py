# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:43:40 2016

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





'''
#==============================================================================
# ======================APPENDIX A: BEAUTIFUL SOUP=============================
#==============================================================================
'''
#==============================================================================
#Part1. Turning the contents of the dominos pizza united states webpage into beautiful Soup Object
#==============================================================================
urlString='http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us/'
myPage = requests.get(urlString)
USdominos = BeautifulSoup(myPage.content)
print USdominos.prettify()


#==============================================================================
#Part2. Turning the contents of the webpage of Virginia only into beautiful Soup Object
#==============================================================================
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#Make all states in "states" lower case          
for x in range (0 , len(states)):
         states[x] = states [x].lower()
   
# Convert the webpage of virginia dominos into beautiful soup object
rootURL = 'http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us/'
state = states[46] # states [46] : va (Virginia)
VA_String =  rootURL + state
VA_HTML = requests.get(urlString)
VA_Soup = BeautifulSoup(VA_HTML.content)

#==============================================================================
#Part.3 Replicating the experiment of Virginia for all states
#==============================================================================
#First Run all Part 2 until rootURL then run this part
state_soup =[]
for n in range (0,len(states)): 
    state = states[n] # states [46] : va (Virginia)
    state_String =  rootURL + state
    state_HTML = requests.get(state_String)
    state_soup.append( BeautifulSoup(state_HTML.content))


# Now we have all the HTML contents for all states stored in soup objects.
# They are stored inside the list state_soup
'''
===============================================================================
'''

'''
#==============================================================================
# ==========================APPENDIX B: REGULAR EXPRESSION=====================
'''
#==============================================================================
#PART1: implementing pattern on one case (VA)
#==============================================================================

pattern = re.compile('<a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title', re.IGNORECASE)
VAFindAll = re.findall(pattern, str(state_soup[46]))

#==============================================================================
#Part2: Extracting 1 city from VA (alexandria)
#==============================================================================
str2 = "'"
str1 = "'"
teststring = str1 + VAFindAll[1] + str2
cities_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
VACitiesSearch = re.search(cities_pattern, teststring  )
#print VACitiesSearch.group() 
Alex = VACitiesSearch.group()

#==============================================================================
# #Part2: Extracting All cities from VA 
#==============================================================================
str2 = "'"
str1 = "'"
VAstringlist = []
for n in range (0,len(VAFindAll)):
    VAstringlist.append (str1 + VAFindAll[n] + str2)

for n in range (0,len(VAFindAll)):
    VAstringlist.append (str( VAFindAll[n] ))


VAcities = []
for n in range (0,len(VAstringlist)):
    cities_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
    VACitiesSearch = re.search(cities_pattern, VAstringlist[n]  )
    VAcities.append (VACitiesSearch.group())
    
 
#==============================================================================
# #Part3: Extracting All store numbers from Dominos' VA Stores
#==============================================================================
#run the first for loop in part 2
VAstorenum = []
for n in range (0,len(VAstringlist)):
    VAstorenum_pattern = re.compile('\d.*\d', re.IGNORECASE)
    VAstorenumSearch = re.search(VAstorenum_pattern, VAstringlist[n]  )
    VAstorenum.append (VAstorenumSearch.group())
  
for n in range (0,len(VAstorenum)):
    VAstorenum [n] = int (VAstorenum[n])


#==============================================================================
# #Part4: Extracting All store numbers and city from Dominos' VA Stores
#==============================================================================
#run the first for loop in part 2
VAstorenumcity = []
for n in range (0,len(VAstringlist)):
    VAstorenumcity_pattern = re.compile('(?<=a-)(.*?)(?=")', re.IGNORECASE)
    VAstorenumcitySearch = re.search(VAstorenumcity_pattern, VAstringlist[n]  )
    VAstorenumcity.append (VAstorenumcitySearch.group())
    
VADict= {}
VADict= {'VA':VAstorenumcity}
   
   
   
   



'''   
===============================================================================
==================================APPENDIX C : DATABASE========================
'''

#==============================================================================
# Part1 : Deleting a table
#==============================================================================
# connect to the database and create a cursor
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()

# create SQL statement that creates table
sqlString =         """
                    DROP TABLE DominosStores;
                    """
# execute the string
myCursor.execute(sqlString)

# commit the change
myConnection.commit() 

# close the connection; clean up memory
myConnection.close() 



#==============================================================================
# Part 2.1: INSERTING URL of 1 entry in VA 
#==============================================================================
   
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()

web = Dict ['va'] [1]
sqlString = """
                    INSERT INTO DominosStores VALUES ('http://www.menuism.com/restaurants/dominos-pizza-alexandria-839934',0,0,0) 
                    """

myCursor.execute(sqlString)
myConnection.commit()

myCursor.close()
myConnection.close()

#------------------------------------------------------------------------------

myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()

URL = Dict ['va'] [1]
Entry = [URL,0,0,0]
sqlString = """
                    INSERT INTO DominosStores VALUES (?,?,?,?) 
                    """

myCursor.execute(sqlString,Entry)
myConnection.commit()

myCursor.close()
myConnection.close()

#==============================================================================
# Part 2.2: INSERTING URL and state of 1 entry in VA 
#==============================================================================
 
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()


stat = 'va'
URL = Dict [stat] [1]
city_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
VACitySearch = re.search(city_pattern, URL  )
City = VACitySearch.group()


Entry = [URL,City,'va',0]
sqlString = """
                    INSERT INTO DominosStores VALUES (?,?,?,?) 
                    """

myCursor.execute(sqlString,Entry)
myConnection.commit()

myCursor.close()
myConnection.close()

#==============================================================================
# Part 2.3: INSERTING URL state , city and store num of 1 entry in VA 
#==============================================================================
 
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()


stat = 'va'
URL = Dict [stat] [1]
city_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
VACitySearch = re.search(city_pattern, URL  )
City = VACitySearch.group()
stornum_pattern = re.compile("\d.*\d", re.IGNORECASE)
stornumSearch = re.search(stornum_pattern, URL  )
stornum = stornumSearch.group()

Entry = [URL,City,'va',stornum]
sqlString = """
                    INSERT INTO DominosStores VALUES (?,?,?,?) 
                    """

myCursor.execute(sqlString,Entry)
myConnection.commit()

myCursor.close()
myConnection.close()
 
 
#==============================================================================
# Part 2.4: INSERTING URL state , city and store num of all entries in VA 
#==============================================================================
#http://sebastianraschka.com/Articles/sqlite3_database.html
myConnection = sqlite3.connect('Dominos.db')
myCursor = myConnection.cursor()

stat = 'va'
VAURL = Dict [stat]
Cities = []
Storenum = []
for x in range (0,len(VAURL)):
    city_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
    stornum_pattern = re.compile("\d.*\d", re.IGNORECASE)
    VACitySearch = re.search(city_pattern, VAURL[x])
    stornumSearch = re.search(stornum_pattern, VAURL [x] )
    Cities.append (VACitySearch.group())
    Storenum.append (stornumSearch.group())  
    Entry = [VAURL[x],Cities[x],'va',Storenum[x]]
    myCursor.execute(sqlString,Entry)
    
    
myConnection.commit()

myCursor.close()
myConnection.close()




#==============================================================================
# Part 2.5: INSERTING URL state , city and store num of all entries in All states 
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

 
 
 
 
 
 
'''
===============================APPENDIXD: TEST CASES===========================
'''
#==============================================================================
#Test Case 1: Related to Appendix A P3 in the code.
#==============================================================================
#Test Case 1.1 : state_soup have the same length of states
#===============
# Operation : len (state_soup) == len (states)
# Expected O/P : True

# Execution:
#len (state_soup) == len (states)
#Out[34]: True

# Test Case Passed: state_soup holds all websites of stores in all USA states.

#------------------------------------------------------------------------------

#Test Case 1.2:state_soup have the same index of states .
#==============
#Given : states [46] : HTML of VA
#Expected : state_soup [46] : Soup object of VA

#Operation : 
#-----------
#1- Type state_soup [46] in the console.
#2- CNTRL + F 
#3- Search for the word "Virginia"

#Output:
#-------
#Expected: you should see in the console dominos pizza in VA cities.
#Actual : Yup

#Test Case Passed.
#------------------------------------------------------------------------------
#==============================================================================
# Test Case 2: Related to Appendix B P1 in the code
#==============================================================================
#Test Case 2.1:
#===============
# Objective: Making sure that the pattern is correct.
# Resources : 
#------------
#http://web-sniffer.net/    ,  
#http://regexr.com/
#http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us/va
#<a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title
#Safari books :Introducing Regular Expression in Python
    #Chapter : Boundaries
#Regular Expression _ V : Class PowerPoint

# Operation : 
#------------
#1- Open http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us/va
# and read the number of dominos store in virginia (263).
#2- Copy paste the URL into http://web-sniffer.net/
#3- Copy paste the HTML into http://regexr.com/
#4- Copy paste the pattern into regexr.


#Output :
#--------
#Expected output: 263 match
#Actual output : 263 match

# Test Case Passed: The pattern is correct.

#------------------------------------------------------------------------------

#Test Case 2.2: Make sure that the pattern works in python.
#==============
# Reousrces: 
#--------------
#1- The pattern : <a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title
#2- state_soup[46] is VA Soup Object (see test case 1.2)
#3- The number of matches of the pattern on regex is 263
#4- finall function : return a tuples of tuples of all the matches.

#Operation
#----------
#Run part 1 ,2 and 3 of Appendix A : Beautiful Soup
#Encoding Style 1 : Which Failed
#pattern =r' <a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title'
#myFindAll = re.findall(pattern, str(state_soup[46]))

#Encoding Style 2: Which Worked
#pattern = re.compile('<a href="http:\/\/www.menuism.com\/restaurants\/dominos-pizza.*title', re.IGNORECASE)
#myFindAll = re.findall(pattern, str(state_soup[46]))


#Output
#------
#Encoding Style 1
#Expected : The len(myFindAll) should be 263
#Actual : len (myFindAll) : Out[79] :  208
#!!!!!!Test Case Failed
 
 #Encoding Style 2
#Expected : The len(myFindAll) should be 263
#Actual : len (myFindAll) : Out[79] :  263
#!!!!!!Test Case Passed

#Test Case 2.3: Make sure that myFindAll contains tuples of matches of href.
#==============
#Resources
#---------
#Appendix B 
#myFindAll
#Console Veiw

#Operation
#---------
#1- Run appendix B code
#2- type myFindAll in console

#Output
#------
#Expected : something like that: [' <a href="http://www.menuism.com/restaurants/dominos-pizza-alexandria-839934" title'
#Actual : yup 

#Test Case Passed : myFindAll does contain tuples of matches.

#------------------------------------------------------------------------------
#Test Case 2.4
#==============
#Resources
#----------
#' <a href="http://www.menuism.com/restaurants/dominos-pizza-alexandria-839934" title'
#VACitiesFindAll = re.findall(pattern, teststring  )
#VACitiesSearch = re.search(pattern, teststring  )
#\-.*-
#(?<=a-)(.*?)(?=-)
#VAFindAll


#Operation
#---------
#str2 = "'"
#str1 = "'"
#teststring = str1 + VAFindAll[0] + str2
#cities_pattern = re.compile("(?<=a-)(.*?)(?=-)", re.IGNORECASE)
#VACitiesFindAll = re.findall(cities_pattern, teststring  )

#2nd Option
#VACitiesSearch = re.search(cities_pattern, teststring  )
#print VACitiesSearch.group() 


#Output
#------
#Expected : alexandria
#Actual : 
#VACitiesSearch.group()
#Out[164]: 'alexandria'

#Test Case Passed
#------------------------------------------------------------------------------
#==============================================================================
# Test Case 3 : Testing the validation of the main code Part 1
#==============================================================================
#length = 0
#for x in range (0,len(states)):
#    length = len(Dict [states[x]]) + length


#length
#Out[259]: 7613


#Test Case Passed
'''
===============================================================================
'''
