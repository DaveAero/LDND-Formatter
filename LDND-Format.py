# Importing
import re
import pandas as pd
import numpy as np

# Loading data from excel
SnP = pd.read_excel('data\mpdsup.xls', "SYSTEMS AND POWERPLANT MAINTENA", skiprows=6, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "CAT", "TASK", "INTERVAL THRES.", "INTERVAL REPEAT", "ZONE", "ACCESS", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Str = pd.read_excel('data\mpdsup.xls', "STRUCTURAL MAINTENANCE PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "PGM", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Zon = pd.read_excel('data\mpdsup.xls', "ZONAL INSPECTION PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])

############################ Functions ############################
def daysSorter(mpd, compilecheck, columnFrom, columnTo, factor):
    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(compilecheck)
        result = re.search(pattern, str(row[columnFrom]))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*factor
            # Print the extracted text to the new column
            mpd.loc[index, columnTo] = days

def extracter(mpd,extraction,columnFrom,columnTo):
        for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
            pattern = re.compile(extraction)
            result = re.search(pattern, str(row[columnFrom]))
            # if the result is not None
            if result != None:
                # Print the extracted text to the new column
                mpd.loc[index,columnTo] = int(result.group(0))

############################ Functions ############################
def formatter(mpd, path):
    # Inserting a blank row for the extracted notes
    colNames = ('THRES. Flight Hours', 'THRES. Flight Cycles', 'THRES. Calendar Days', 'REPEAT Flight Hours', 'REPEAT Flight Cycles', 'REPEAT Calendar Days')
    
    for name in colNames:
        mpd.insert(column = name, loc = int(len(mpd.columns)), value = np.nan)

    extracter(mpd,r'\d+(?= FH| AH)','INTERVAL THRES.','THRES. Flight Hours')
    extracter(mpd,r'\d+(?= FC)','INTERVAL THRES.','THRES. Flight Cycles')
    extracter(mpd,r'\d+(?= FH| AH)','INTERVAL REPEAT','REPEAT Flight Hours')
    extracter(mpd,r'\d+(?= FC)','INTERVAL REPEAT','REPEAT Flight Cycles')
    
    daysSorter(mpd,r'\d+(?= HR)','INTERVAL THRES.','THRES. Calendar Days',(1/24))
    daysSorter(mpd,r'\d+(?= HR)','INTERVAL REPEAT','REPEAT Calendar Days',(1/24))
    daysSorter(mpd,r'\d+(?= MO)','INTERVAL THRES.','THRES. Calendar Days',30.437)
    daysSorter(mpd,r'\d+(?= MO)','INTERVAL REPEAT','REPEAT Calendar Days',30.437)
    daysSorter(mpd,r'\d+(?= YR)','INTERVAL THRES.','THRES. Calendar Days',365.25)
    daysSorter(mpd,r'\d+(?= YR)','INTERVAL REPEAT','REPEAT Calendar Days',365.25)
    daysSorter(mpd,r'\d+(?= DY)','INTERVAL THRES.','THRES. Calendar Days',1)
    daysSorter(mpd,r'\d+(?= DY)','INTERVAL REPEAT','REPEAT Calendar Days',1)

    # Print to Excel
    mpd.to_excel(path)

formatter(SnP, "SnP.xlsx")