import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

df = pd.read_excel(r'C:\Users\hp\Documents\Exemple à envoyer_ Edition echelle Client X.xlsx',
                   header=None, dtype=str, sheet_name="Brut")

df[0] = df[0].str.replace(r"\s*!\s*", "!", regex=True)
df = df[0].str.split("!", expand=True)
df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i']

df.loc[:, 'a'] = df['a'].replace('', pd.NA)
df['a'] = df['a'].ffill()

df['a'] = df['a'].str.strip().str.replace(r'\*', '', regex=True)

df = df.apply(lambda x: x.str.strip()
                        .str.replace(r'\s+', ' ', regex=True)
                        .str.replace(r'-+ ', '', regex=True)
                        .str.replace(r'\.', '', regex=True)
              if x.dtype == "object" else x)

df['a'] = pd.to_datetime(df['a'], dayfirst=True, errors='coerce')
df = df[df['a'].notna()]

df.columns = ['JJ/MM/AA', 'Debit1', 'Credit1', 'Debit2', 'Credit2', 'NBJ', 'Debit3', 'Credit4', 'Decouvert']

df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '.', regex=True))
df.iloc[:, 1:] = df.iloc[:, 1:].replace('', np.nan).astype(float)

df['Int'] = df['Decouvert'] * df['Debit3'] / 3600

df.columns = pd.MultiIndex.from_tuples([
    ("Valuer", "JJ/MM/AA"),
    ("Capitaux", "Debit1"), ("Capitaux", "Credit1"),
    ("Soldes", "Debit2"), ("Soldes", "Credit2"),
    ("Nbj", "Nbj"),
    ("Nombres", "Debit3"), ("Nombres", "Credit3"),
    ("Taux", "Decouvert"),
    ("Int", "Int")
])

output_path = r'C:\Users\hp\Documents\db_vf.xlsx'
try:
    df.to_excel(output_path, index=False)
    print(f"File saved successfully at {output_path}")
except Exception as e:
    print(f"Error saving file: {e}")
