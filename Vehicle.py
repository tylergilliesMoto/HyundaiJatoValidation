
# This is a Class to create vehicle objects
# Very basic, basically just using it make things a little simpler and easier to manage since now I can use instance variables
class Vehicle:

    def __init__(self, year, make, model, modelID, trimNames, trimIDs, manuCodes, exColors=None, intColors=None, colorNames=None):
        self.year = year
        self.make = make
        self.model = model
        self.trimNames = trimNames
        self.modelID = modelID
        self.trimIDs = trimIDs
        self.manuCodes = manuCodes
        self.exColors = exColors
        self.intColors = intColors

        self.colorNames = colorNames

    def __str__(self):
        return str(self.year) + " " + str(self.make) + " " + str(self.model) + " " + str(self.modelID) + " " + str(self.trimNames) + " " + str(self.trimIDs) + " " + str(self.manuCodes) + " " + str(self.exColors) + " " + str(self.intColors) + " " + str(self.colorNames)

    def setColors(self, exteriors, interiors):
        self.exColors = exteriors
        self.intColors = interiors


def findJatoID(jatodf, manuCode, year):
    for i in range(len(jatodf)):
        mCode = str(jatodf.loc[i, 'Manufacturer code']).split('/')
        if str(manuCode) in mCode:
            if str(jatodf.loc[i, 'Year']) == str(year):
                return jatodf.loc[i, 'Vehicle id']


