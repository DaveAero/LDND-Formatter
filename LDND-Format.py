# Importing
import re
import pandas as pd
import numpy as np

# Loading data from excel
SnP = pd.read_excel('data\mpdsup.xls', "SYSTEMS AND POWERPLANT MAINTENA", skiprows=6, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "CAT", "TASK", "INTERVAL THRES.", "INTERVAL REPEAT", "ZONE", "ACCESS", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Str = pd.read_excel('data\mpdsup.xls', "STRUCTURAL MAINTENANCE PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "PGM", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Zon = pd.read_excel('data\mpdsup.xls', "ZONAL INSPECTION PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])

############################ Functions ############################
# A function to extract the core items such as FC / FH / Days
# Loads in:
# mpd - the current working MPD tab
# compilecheck - the Regex pattern to be searched
# columnFrom - the colum to be searched
# columnTo - the column for the extracted text to be placed into
# factor - the multiplying factor for calendar items like years or months
def extracter(mpd, compilecheck, columnFrom, columnTo, factor):
    # working through the whole MPD sheet one row at a time iterativly
    for index, row in mpd.iterrows():
        # loading pattern to be searched into Regex
        pattern = re.compile(compilecheck)
        # Searching the pattern in the working row in the selected column to be searched
        result = re.search(pattern, str(row[columnFrom]))
        # if the result is not None continue
        if result != None:
            # Using the factor to correct months and years
            days = int(result.group(0))*factor
            # Print the extracted number to the chosen column
            mpd.loc[index, columnTo] = days

# A function to extract items such as Life Lim and Ven Rec
# Loads in:
# mpd - the current working MPD tab
def textExtracter(mpd):
    # Loading the columns to be filled into a list, to use in a for loop
    columnTo = ['THRES. Flight Hours', 'THRES. Flight Cycles', 'THRES. Calendar Days', 'REPEAT Flight Hours', 'REPEAT Flight Cycles', 'REPEAT Calendar Days']
    # Loading the possible matched and results into a dictionary, to use in a for loop
    textToExtract = {'LIF LIM':'LLP', 'APU CNG':'APU CNG', 'ENG CNG':'ENG CNG', 'VEN REC':'Hard Time'}

    # working through the whole MPD sheet one row at a time iterativly
    for index, row in mpd.iterrows():
        # Searching each possible match in a for loop
        for textType in textToExtract:
            # searching in the THRES columns as both columns are the same for text items. If there is a match to the searching text continue.
            if str(row['INTERVAL THRES.']) == textType:
                # using a for loop for each of the columns to be filled
                for columns in columnTo:
                    # using the dictionary key pairs to fill each of the columns
                    mpd.loc[index,columns] = str(textToExtract[textType])

############################ A function for FLS Tasks ############################
def slope(x1, y1, x2, y2):
  if (x2-x1) == 0:
    return 0
  s = (y2-y1)/(x2-x1)
  return s

# Line 1, Aircraft Utilisation
#starting Utilization
x1 = 0
y1 = 0
# Current Utilization
x2 = 55517.62
y2 = 21739
m1 = slope(x1, y1, x2, y2)
c1 = y1-(m1*x1)

# Line 2, Flight Cycle limit
x3 = 0
y3 = 75000

x4 = 45000
y4 = 75000
# m2 = 0
# c2 = 75000

# Line 3, Sloped limit
# Starts at the end of line 2
x5 = 100000
y5 = 30000
m3 = slope(x4, y4, x5, y5)
c3 = y4-(m3*x4)

# Line 4, Flight Hour limit
# Starting at the end of line 3
x6 = 100000
y6 = 0
# m4 = 0
# c4 = 30000


# line 1 / line 2 intersection
x12 = (((m1*-x2)+y2) - (y3))/(-m1)
y12 = 75000

# line 1 / line 3 intersection
x13 = (((m1*-x2)+y2) - ((m3*-x4)+y4))/(m3-m1)
y13 = (m3*x13) + ((m3*-x4)+y4)

# line 1 / line 4 intersection
x14 = 100000
y14 = (m1*x14) + y1 - (m1*x1)

# finding x intersection
if x13 < x4:
    x = x12
elif x13 > x5:
    x = x14
else:
    x = x13

if y13 > y4:
    y = y12
elif y13 < y5:
    y = y14
else:
    y = y13


############################ Functions ############################
# Loads in:
# mpd - the current working MPD tab
# path - the location where the file will be saved
def formatter(mpd, path):
    # Inserting a blank row for the extracted notes
    colNames = ('THRES. Flight Hours', 'THRES. Flight Cycles', 'THRES. Calendar Days', 'REPEAT Flight Hours', 'REPEAT Flight Cycles', 'REPEAT Calendar Days')
    
    for name in colNames:
        mpd.insert(column = name, loc = int(len(mpd.columns)), value = np.nan)

    extracter(mpd,r'\d+(?= FH| AH)','INTERVAL THRES.','THRES. Flight Hours',1)
    extracter(mpd,r'\d+(?= FC)','INTERVAL THRES.','THRES. Flight Cycles',1)
    extracter(mpd,r'\d+(?= FH| AH)','INTERVAL REPEAT','REPEAT Flight Hours',1)
    extracter(mpd,r'\d+(?= FC)','INTERVAL REPEAT','REPEAT Flight Cycles',1)
    
    extracter(mpd,r'\d+(?= HR)','INTERVAL THRES.','THRES. Calendar Days',(1/24))
    extracter(mpd,r'\d+(?= HR)','INTERVAL REPEAT','REPEAT Calendar Days',(1/24))
    extracter(mpd,r'\d+(?= MO)','INTERVAL THRES.','THRES. Calendar Days',30.437)
    extracter(mpd,r'\d+(?= MO)','INTERVAL REPEAT','REPEAT Calendar Days',30.437)
    extracter(mpd,r'\d+(?= YR)','INTERVAL THRES.','THRES. Calendar Days',365.25)
    extracter(mpd,r'\d+(?= YR)','INTERVAL REPEAT','REPEAT Calendar Days',365.25)
    extracter(mpd,r'\d+(?= DY)','INTERVAL THRES.','THRES. Calendar Days',1)
    extracter(mpd,r'\d+(?= DY)','INTERVAL REPEAT','REPEAT Calendar Days',1)

    #textExtracter
    textExtracter(mpd)

    # Print to Excel
    mpd.to_excel(path)

############################ Main Code ############################
formatter(SnP, "SnP.xlsx")
formatter(Str, "Str.xlsx")
formatter(Zon, "Zon.xlsx")