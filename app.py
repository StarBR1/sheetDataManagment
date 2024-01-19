import pandas as pd
from google.oauth2 import service_account
import os
import gspread

currentDirectory = os.path.dirname(os.path.abspath(__file__))
filePath = os.path.join(currentDirectory, 'li.1_24_19.01_09h42.csv')

jsonFile = os.path.join(currentDirectory, 'gsheetsbot-411316-9067a6fa88ed.json')

df = pd.read_csv(filePath, sep=';', header=None)
df = df.fillna('')

credentials = service_account.Credentials.from_service_account_file(jsonFile, 
                                                                   scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'])

gc = gspread.authorize(credentials)
workSheetDestination = gc.open_by_key('1uOyoUHHCND-x_Gp2TNgWptLTpBPfEl9yCCrgrvK1Xz8')
sheetDestination = workSheetDestination.worksheet('Página1')

chunk_size = 1000
print('loading')
for i in range(0, len(df), chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    cell_list = sheetDestination.range(i+1, 1, i+len(chunk), df.shape[1])
    for j, value in enumerate(chunk.values.flatten()):
        cell_list[j].value = value
    sheetDestination.update_cells(cell_list)

print("done")
