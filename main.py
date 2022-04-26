import requests

import json

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font

import pandas as pd

from Vehicle import *

# grab the model years from text file
# MODEL_YEARS = ['2022', '2021']
f = open("Model Years.txt", "r")
line = f.readline()
MODEL_YEARS = line.split(', ')
print(MODEL_YEARS)


print('Please Stand By . . . ')

# Get all the model ids from API
r = requests.get('https://apps.hac.ca/Api/models/en/7').json()

modelData = r['ModelGroups']['ModelGroup']
modelIDs = []
for i in modelData:
    models = i['Models']['Model']
    for j in models:
        modelIDs.append(j['ModelId'])

# print("===> " + str(modelIDs))  # All model ids are in here


# Use those model IDs to get all the trim ids
#   Then we will use all that data to create a Vehicle() object to use later
vehicles = []
for modelID in modelIDs: # loop through each model id
    trimIDs = []
    trimNames = []
    manuCodes = []

    r = requests.get(f'https://apps.hac.ca/Api/trims/en/7/{modelID}').json()
    modelData = r['Models']['Model']

    # Get Model Info
    modelID = modelID  # redundant, I just like having them all together
    modelYear = modelData['ModelYear']
    modelName = modelData['ModelName']

    if modelYear in MODEL_YEARS:

        #Get trim info
        trimData = r['Models']['Model']['Trims']['Trim']
        for j in trimData:
            trimIDs.append(j['TrimId'])
            trimNames.append(j['TrimName'])
            manuCodes.append(j['HSCCodes']['HSCCode'][0]['LBT_SAC'])

        # Use all that to create a Vehicle Object and append that to a list of vehicles
        temp = Vehicle(modelYear, 'Hyundai', modelName, modelID, trimNames, trimIDs, manuCodes)  # see Vehicle.py, just a very basic class so I can use objects
        vehicles.append(temp)

# print("***********************************************")
# for i in vehicles:
#     print(i)
# print("***********************************************")


# Now use the model and trim ids to make requests to get the colors of each vehicle
# we will gather that color data and add them to each of the vehicle objects using the function at the bottom of this loop
colorNames = {}
for i in vehicles:
    exteriors, interiors = [], []
    model = str(i.modelID)
    trims = i.trimIDs

    # for each trim, get all its exterior and interior colors
    for trim in trims:
        r = requests.get(f'https://apps.hac.ca/API/colors/en/7/{model}/{str(trim)}').json()
        colorData = r['Trims']['Trim']['ExteriorColors']['ExteriorColor']

        temp1 = []
        temp2 = []
        trimInteriors = []

        name1 = []
        name2 = []

        for j in colorData:
            colorCode = j['ExtSAPColorCode'].upper()
            temp1.append(colorCode)
            temp2 = [x['IntSAPColorCode'].upper() for x in j['InteriorColors']['InteriorColor']]
            # print(temp2)
            # print()
            # grab the color names
            name1 = j['ExteriorColorName']
            name2 = [x['InteriorColorName'] for x in j['InteriorColors']['InteriorColor']]

            # get rid of duplicates
            if colorCode not in colorNames:
                #colorNames.append([colorCode, name1])
                colorNames[colorCode] = name1

            for k in range(len(temp2)):
                if temp2[k] not in colorNames:
                    #colorNames.append([temp2[k], name2[k]])
                    colorNames[temp2[k]] = name2[k]

            # Getting the interiors into a list and removing repeats, then that will be appended to the "interiors" variable
            for k in temp2:
                if k not in trimInteriors:
                    trimInteriors.append(k)



        exteriors.append(temp1)
        interiors.append(trimInteriors)

    # print("@@@@@===" + str(exteriors))
    # print("$$$$$===" + str(interiors))
    i.setColors(exteriors, interiors)
    # print(i)
print(colorNames)
# f = open("tester.txt", 'w')
# for i in vehicles:
#     f.write(str(i))
#     f.write('\n')

# Now lets use the manufacturer codes we have to get each vehicle's jato id from jato vehicle download
jatodf = pd.read_csv("Jato Hyundais.csv")  # This file is from here: https://motocommerce.ca/uh-adm/nvd/jatovehicle/


# Lets output this to excel
wb = Workbook()
ws = wb.active
ws.append(["Year", "Make", "Model", "Trim", "Manu Code", "Hyundai ModelID", "Hyundai TrimID", "JATO ID", "Hyundai Option Codes", "Hyundai Option Names"])
boldFont = Font(bold=True)
for cell in ws[1:1]:
    cell.font = boldFont

for v in vehicles:
    for i in range(len(v.trimIDs)):
        jatoID = findJatoID(jatodf, v.manuCodes[i], v.year)

        # get names of colors from our dictionary we made
        names = []
        for j in v.exColors[i] + v.intColors[i]:
            names.append(colorNames[j])


        ws.append([v.year, v.make, v.model, v.trimNames[i], v.manuCodes[i], v.modelID, v.trimIDs[i], jatoID, str(v.exColors[i] + v.intColors[i]), str(names)])

wb.save("Hyundai API Info.xlsx")


