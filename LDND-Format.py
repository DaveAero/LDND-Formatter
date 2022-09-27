# Importing
import re
import pandas as pd
import numpy as np

# Loading data from excel
SnP = pd.read_excel('data\mpdsup.xls', "SYSTEMS AND POWERPLANT MAINTENA", skiprows=6, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "CAT", "TASK", "INTERVAL THRES.", "INTERVAL REPEAT", "ZONE", "ACCESS", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Str = pd.read_excel('data\mpdsup.xls', "STRUCTURAL MAINTENANCE PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "PGM", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])
Zon = pd.read_excel('data\mpdsup.xls', "ZONAL INSPECTION PROGRAM", skiprows=5, names=["Revision", "Index", "MPD ITEM NUMBER", "AMM REFERENCE", "ZONE", "ACCESS", "INTERVAL THRES.", "INTERVAL REPEAT", "APPLICABILITY APL", "APPLICABILITY ENG", "MAN-HOURS", "TASK DESCRIPTION"])

############################ Functions ############################
def formatter(mpd, path):
    # Inserting a blank row for the extracted notes
    colNames = ('THRES. Flight Hours', 'THRES. Flight Cycles', 'THRES. Calendar Days', 'REPEAT Flight Hours', 'REPEAT Flight Cycles', 'REPEAT Calendar Days')
    
    for name in colNames:
        mpd.insert(column = name, loc = int(len(mpd.columns)), value = np.nan)

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= FH| AH)')
        result = re.search(pattern, str(row['INTERVAL THRES.']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Flight Hours'] = int(result.group(0))

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= FC)')
        result = re.search(pattern, str(row['INTERVAL THRES.']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Flight Cycles'] = int(result.group(0))

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+ (HR|DY|MO|YR)')
        result = re.search(pattern, str(row['INTERVAL THRES.']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Calendar Days'] = result.group(0)

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= FH| AH)')
        result = re.search(pattern, str(row['INTERVAL REPEAT']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Flight Hours'] = int(result.group(0))

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= FC)')
        result = re.search(pattern, str(row['INTERVAL REPEAT']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Flight Cycles'] = int(result.group(0))

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+ (HR|DY|MO|YR)')
        result = re.search(pattern, str(row['INTERVAL REPEAT']))
        # if the result is not None
        if result != None:
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Calendar Days'] = result.group(0)

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= HR)')
        result = re.search(pattern, str(row['THRES. Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))/24
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= HR)')
        result = re.search(pattern, str(row['REPEAT Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))/24
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= MO)')
        result = re.search(pattern, str(row['THRES. Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*30.437
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= MO)')
        result = re.search(pattern, str(row['REPEAT Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*30.437
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= YR)')
        result = re.search(pattern, str(row['THRES. Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*365.25
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= YR)')
        result = re.search(pattern, str(row['REPEAT Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))*365.25
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= DY)')
        result = re.search(pattern, str(row['THRES. Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))
            # Print the extracted text to the new column
            mpd.loc[index, 'THRES. Calendar Days'] = days

    for index, row in mpd.iterrows():
        # On each row check the Taks Description for a match with Airplane Note
        pattern = re.compile(r'\d+(?= DY)')
        result = re.search(pattern, str(row['REPEAT Calendar Days']))
        # if the result is not None
        if result != None:
            days = int(result.group(0))
            # Print the extracted text to the new column
            mpd.loc[index, 'REPEAT Calendar Days'] = days
    mpd.to_excel(path)


formatter(SnP, "SnP.xlsx")