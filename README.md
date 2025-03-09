import pandas as pd
import re
import numpy as np
pd.options.display.float_format = '{:.2f}'.format

df = pd.read_excel(r'******\Exemple à envoyer_ Edition echelle Client X.xlsx', header=None, dtype=str, sheet_name="Brut")
df[0] = df[0].str.replace(r"\s*!\s*", "!", regex=True)
df = df[0].str.split("!", expand=True)
df.columns= ['a', 'b', 'c','d', 'e','f', 'j','h','i']
df['a'].replace('',pd.NA,inplace=True)
df['a'] = df['a'].fillna(method='ffill')

df['a'] = df['a'].str.strip().str.replace('*','', regex=True)
df = df.apply(lambda x: x.str.strip().str.replace(r'\s+',' ', regex=True).str.replace('-+ ','', regex=True).str.replace('.','', regex=True)
              if x.dtype == "object" else x)

df['a'] = pd.to_datetime(df['a'], dayfirst=True, errors='coerce')
df = df[df['a'].notna()]
df.columns = ['JJ/MM/AA','Debit1','Credit1','Debit2','Credit2','NBJ','Debit3','Credit4','Decouvert'] 
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace (',','.',regex=True))
df.iloc[:, 1:] = df.iloc[:,1:].replace('',np.nan).replace('',np.nan).astype(float)
df['Int'] = df['Decouvert']* df['Debit3']/3600
df.columns = pd.MultiIndex.from_tuples([
    ("Valuer", "JJ/MM/AA"),
    ("Capitaux","Debit1"),("Capitaux","Credit1"),
    ("Soldes","Debit2"),("Soldes","Credit2"),
    ("Nbj","Nbj"),
    ("Nombres","Debit3"),("Nombres","Credit3"),
    ("Taux","Decouvert"),
    ("Int","Int")])
df.to_excel('******\db_vf.xlsx')
