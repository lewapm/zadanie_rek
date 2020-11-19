import pandas as pd

pd = pd.read_csv('./test.csv')

pdx = pd.loc[pd['data_urodzenia'].str[6] == '2']
print("Ilosc osob urodzonych po 31.12.1999: {}".format(pdx.count()['data_urodzenia']))
zenskie = pd.loc[pd['imie'].str[-1] =='a']['imie']
print("Lista imion zenskich {}".format(zenskie.unique()))