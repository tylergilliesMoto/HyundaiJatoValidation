import http.client, urllib.request, urllib.parse, urllib.error, base64

import json

import pandas as pd
import openpyxl
from openpyxl import load_workbook

from Vehicle import Vehicle

import ast


# set up jato authorization
#token = "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6ImJjZGEyYTU4LWM1MmYtNDU3ZC1iMzk2LWZjMTE5MDM4NWI1ZCIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiJjYS51bmhhZ2dsZXZpbiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vYWNjZXNzY29udHJvbHNlcnZpY2UvMjAxMC8wNy9jbGFpbXMvaWRlbnRpdHlwcm92aWRlciI6IkFTUC5ORVQgSWRlbnRpdHkiLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IjU0MWQ3YzI4LTljNzItNDQ1NS04ZTI1LTgzZTM2YTZhNDU0NCIsImh0dHA6Ly9zY2hlbWFzLmphdG8uY29tL3dzLzIwMTUvMDYvaWRlbnRpdHkvY2xhaW1zL2NhL2FsbG93ZWRjdWx0dXJlcyI6WyJlbi1DQSIsImZyLUNBIl0sImh0dHA6Ly9zY2hlbWFzLmphdG8uY29tL3dzLzIwMTUvMDgvaWRlbnRpdHkvY2xhaW1zL2NhL2FsbG93ZWR2aW5kZWNvZGluZyI6InRydWUiLCJodHRwOi8vc2NoZW1hcy5qYXRvLmNvbS93cy8yMDE2LzA2L2lkZW50aXR5L2NsYWltcy9jYS9hbGxvd2VkaGlzdG9yaWNhbCI6InRydWUiLCJodHRwOi8vc2NoZW1hcy5qYXRvLmNvbS93cy8yMDE4LzEwL2lkZW50aXR5L2NsYWltcy9jYS9hbGxvd2Vkc3BlY3MiOiJ0cnVlIiwiaHR0cDovL3NjaGVtYXMuamF0by5jb20vd3MvMjAxNS8wNi9pZGVudGl0eS9jbGFpbXMvdXMvYWxsb3dlZGN1bHR1cmVzIjpbImVuLVVTIiwiZXMtVVMiXSwiaHR0cDovL3NjaGVtYXMuamF0by5jb20vd3MvMjAxNS8wOC9pZGVudGl0eS9jbGFpbXMvdXMvYWxsb3dlZHZpbmRlY29kaW5nIjoidHJ1ZSIsImh0dHA6Ly9zY2hlbWFzLmphdG8uY29tL3dzLzIwMTgvMTAvaWRlbnRpdHkvY2xhaW1zL3VzL2FsbG93ZWRzcGVjcyI6InRydWUiLCJodHRwOi8vc2NoZW1hcy5qYXRvLmNvbS93cy8yMDE2LzA2L2lkZW50aXR5L2NsYWltcy91cy9hbGxvd2VkaGlzdG9yaWNhbCI6InRydWUiLCJodHRwOi8vc2NoZW1hcy5qYXRvLmNvbS93cy8yMDE3LzA0L2lkZW50aXR5L2NsYWltcy9jYS9kaXNwbGF5aW52b2ljZXByaWNlIjoidHJ1ZSIsImh0dHA6Ly9zY2hlbWFzLmphdG8uY29tL3dzLzIwMTcvMDQvaWRlbnRpdHkvY2xhaW1zL214L3N1YnNjcmlwdGlvbmtleSI6IjFjYWQ3ZGVkYTE1MzRjOGM5ZjVhMDQyNDg2Yjg2NjQ2IiwiaHR0cDovL3NjaGVtYXMuamF0by5jb20vd3MvMjAxNy8wNC9pZGVudGl0eS9jbGFpbXMvdXMvc3Vic2NyaXB0aW9ua2V5IjoiMWNhZDdkZWRhMTUzNGM4YzlmNWEwNDI0ODZiODY2NDYiLCJodHRwOi8vc2NoZW1hcy5qYXRvLmNvbS93cy8yMDE3LzA0L2lkZW50aXR5L2NsYWltcy9jYS9zdWJzY3JpcHRpb25rZXkiOiIxY2FkN2RlZGExNTM0YzhjOWY1YTA0MjQ4NmI4NjY0NiIsImh0dHA6Ly9zY2hlbWFzLmphdG8uY29tL3dzLzIwMTcvMDQvaWRlbnRpdHkvY2xhaW1zL2JyL3N1YnNjcmlwdGlvbmtleSI6IjFjYWQ3ZGVkYTE1MzRjOGM5ZjVhMDQyNDg2Yjg2NjQ2IiwiaHR0cDovL3NjaGVtYXMuamF0by5jb20vd3MvMjAxOC8xMC9pZGVudGl0eS9jbGFpbXMvdXMvc2hvd3JlZ2lvbmFscyI6ImZhbHNlIiwibmJmIjoxNjUwNTE1NDkwLCJleHAiOjE2NTA2MDE4ODksImlzcyI6Imh0dHBzOi8vYXV0aC5qYXRvZmxleC5jb20iLCJhdWQiOiI0MTRlMTkyN2EzODg0ZjY4YWJjNzlmNzI4MzgzN2ZkMSJ9.UVzdtLeeccflMsRvRMAMk5SXq_0CSDiSQxsMyLaX5VQ"
token = input("Enter Token: ")

headers = {
    # Request headers
    'Subscription-Key': '1cad7deda1534c8c9f5a042486b86646',
    'Authorization': token
}
params = urllib.parse.urlencode({
})
print('Please Stand By . . . ')

# open the "Hyundai API Info.xlsx" we made and grab the JATO IDs
# will loop through each id and call the api for it
# will then grab the options/color info from that response

df = pd.read_excel("Hyundai API Info.xlsx")
optionCodes = []
optionNames = []
for i in df['JATO ID']:
    if str(i) != 'nan':
        jatoID = str(int(i))
        try:
            conn = http.client.HTTPSConnection('api.jatoflex.com')
            conn.request("GET", f"/api/en-ca/options/{jatoID}?%s" % params, "{body}", headers)
            response = conn.getresponse()

            encoding = response.info().get_content_charset('utf-8')  # JSON default
            raw_data = response.read()

            data = json.loads(raw_data.decode(encoding))
            #print(data)

            # Here is where we grab the options info
            optionsData = data['options']

            codes = [x['optionCode'].upper() for x in optionsData]
            optionCodes.append(codes)

            names = [x['optionName'] for x in optionsData]
            optionNames.append(names)

            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    else:
        optionCodes.append(['Missing JATO ID'])
        optionNames.append(['Missing JATO ID'])

# add a column for the jato option codes
df['JATO Codes'] = optionCodes
df['JATO Option Names'] = optionNames

#df = pd.read_excel("Hyundai vs JATO.xlsx")

# now lets create a column comparing the 2 sets of options
arr1 = []
arr2 = []
arr3 = []
arr4 = []

for i in range(len(df)):
    # Compare the codes from both sides
    codes1 = str(df.loc[i, 'Hyundai Option Codes'])
    codes1 = ast.literal_eval(codes1)

    codes2 = str(df.loc[i, 'JATO Codes'])
    codes2 = ast.literal_eval(codes2)

    names1 = str(df.loc[i, 'Hyundai Option Names'])
    names1 = ast.literal_eval(names1)

    names2 = str(df.loc[i, 'JATO Option Names'])
    names2 = ast.literal_eval(names2)


    # append the codes and names to these arrays if they are not present in the other api results
    inHyundai = []
    inJato = []

    inHyundai2 = []
    inJato2 = []
    for j in range(len(codes1)):
        # if codes2.count(codes1[j]) == 0:
        #     inHyundai.append(codes1[j])
        #     inHyundai2.append(names1[j])
        found = False
        for k in codes2:
            if codes1[j] == k or codes1[j] in k or k in codes1[j]:
                found = True
                break
        if not found:
            inHyundai.append(codes1[j])
            inHyundai2.append(names1[j])

    for j in range(len(codes2)):
        # if codes1.count(codes2[j]) == 0:
        #     inJato.append(codes2[j])
        #     inJato2.append(names2[j])
        found = False
        for k in codes1:
            if codes2[j] == k or codes2[j] in k or k in codes2[j]:
                found = True
                break
        if not found:
            inJato.append(codes2[j])
            inJato2.append(names2[j])

    arr1.append(inHyundai)
    arr2.append(inJato)
    arr3.append(inHyundai2)
    arr4.append(inJato2)



df['Not in JATO'] = arr1
df['Not in Hyundai'] = arr2
df['Names Not in JATO'] = arr3
df['Names Not in Hyundai'] = arr4


df.to_excel("Hyundai vs JATO.xlsx")



