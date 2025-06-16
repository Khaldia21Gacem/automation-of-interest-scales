import pandas as pd
import numpy as np
import re

pd.options.display.float_format = '{:.2f}'.format

# Lecture brute
df = pd.read_excel(r'Exemple à envoyer_ Edition echelle Client X.xlsx', header=None, dtype=str, sheet_name="Brut")


# Nettoyage du séparateur "!"
df[0] = df[0].str.replace(r"\s*!\s*", "!", regex=True)

# Séparation en colonnes
df = df[0].str.split("!", expand=True)

# Renommer les colonnes (ordre corrigé pour correspondre à l'usage plus tard)
df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

# Remplacer les vides et propagation
df['a'] = df['a'].replace('', pd.NA).fillna(method='ffill')

# Nettoyage de la première colonne
df['a'] = df['a'].str.strip().str.replace(r'\*', '', regex=True)

# Nettoyage général (évite suppression des points numériques)
def nettoyer_colonne(col):
    return col.str.strip().str.replace(r'\s+', ' ', regex=True).str.replace(r'-+\s*', '', regex=True)

df = df.apply(lambda x: nettoyer_colonne(x) if x.dtype == "object" else x)

# Conversion de la première colonne en date
df['a'] = pd.to_datetime(df['a'], dayfirst=True, errors='coerce')
df = df[df['a'].notna()]

# Renommage des colonnes finales
df.columns = ['JJ/MM/AA', 'Debit1', 'Credit1', 'Debit2', 'Credit2', 'NBJ', 'Debit3', 'Credit3', 'Decouvert']

# # Nettoyage et conversion des données numériques
# for col in df.columns[1:]:
#     df[col] = df[col].str.replace('.', '', regex=False)#.replace('', np.nan).astype(float)

#***************
for col in df.columns[1:]:
    df[col] = df[col].str.replace(r'[^\d,.-]', '', regex=True)  # garde uniquement chiffres, virgules, etc.
    df[col] = df[col].str.replace('.', '', regex=False)         # supprime points de milliers
    df[col] = df[col].str.replace(',', '.', regex=False)        # remplace virgules décimales
    df[col] = df[col].replace('', np.nan).astype(float)         # convertit en float
#************


# Calcul de l'intérêt
df['Int'] = df['Decouvert'] * df['Debit3'] / 36000

# Ajout du MultiIndex
df.columns = pd.MultiIndex.from_tuples([
    ("Valeur", "JJ/MM/AA"),
    ("Capitaux", "Debit"), ("Capitaux", "Credit"),
    ("Soldes", "Debit"), ("Soldes", "Credit"),
    ("Nbj", "NBJ"),
    ("Nombres", "Debit"), ("Nombres", "Credit"),
    ("Taux", "Decouvert"),
    ("Int", "Int")
])
print(df.head(25))
# # Export Excel
# df.to_excel(r'_vf.xlsx')
