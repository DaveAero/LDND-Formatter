# Importing
import re
import pandas as pd
import numpy as np

# Loading data from excel
SnP = pd.read_excel('data\mpdsup.xls', "SYSTEMS AND POWERPLANT MAINTENA", skiprows=6, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "CAT", "TASK", "INTERVAL THRES.", "INTERVAL REPEAT", "ZONE", "ACCESS", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Str = pd.read_excel('data\mpdsup.xls', "STRUCTURAL MAINTENANCE PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "PGM", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Zon = pd.read_excel('data\mpdsup.xls', "ZONAL INSPECTION PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])

############################ Functions ############################
def extracter(mpd, compilecheck, columnFrom, columnTo, factor):
    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(compilecheck)
        result = re.search(pattern, str(row[columnFrom]))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*factor
            # Print the extracted text to the new column
            mpd.loc[index, columnTo] = days
        
        # Sorting out string entries in intervals that will remain the same
        if str(row[columnFrom]) == 'LIF LIM':
            mpd.loc[index,columnTo] = str('LLP')
        
        if str(row[columnFrom]) == 'APU CNG':
            mpd.loc[index,columnTo] = str('APU CNG')

        if str(row[columnFrom]) == 'ENG CNG':
            mpd.loc[index,columnTo] = str('ENG CNG')

        if str(row[columnFrom]) == 'VEN REC':
            mpd.loc[index,columnTo] = str('VEN REC')

############################ Functions ############################
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

    # Print to Excel
    mpd.to_excel(path)

############################ Main Code ############################
formatter(SnP, "SnP.xlsx")
formatter(Str, "Str.xlsx")
formatter(Zon, "Zon.xlsx")