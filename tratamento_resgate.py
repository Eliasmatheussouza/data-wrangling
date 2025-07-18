import pandas as pd

df = pd.read_excel('regaste_valia.xlsx', decimal=',')
#d2 = pd.read_excel('resgatesdemais.xlsx', decimal=',')
#df = pd.concat([d1, d2], ignore_index=True)
#df['mes'] = df['data'].dt.month
#df['ano'] = df['data'].dt.year

#df = df[(df['ano']== 2024) &  (df['mes']== 7)]

# De-para código de evento do amadeus x extração
df.loc[df['cod_beneficio'].isin([27, 56, 73]), "beneficio"] = "PORTABILIDADE"
df.loc[df['cod_beneficio']== 50, "beneficio"] = "RESGATE PARCIAL"
df.loc[df['cod_beneficio'].isin([1, 61]), "beneficio"] = "RESGATE"
df.loc[df['cod_beneficio']== 3, "beneficio"] = "RESGATE DE HERDEIRO LEGAL"
#
df.loc[df['beneficio']== "PORTABILIDADE", "cod_beneficio"] = 405
df.loc[df['beneficio']== "RESGATE", "cod_beneficio"] = 407
df.loc[df['beneficio']== "RESGATE PARCIAL", "cod_beneficio"] = 408
df.loc[df['beneficio']== "RESGATE DE HERDEIRO LEGAL", "cod_beneficio"] = 413

df_melted = df.melt(id_vars=["FSS", "cod_plano", "plano", "cod_beneficio", "beneficio"], value_vars=["debito", "credito"], var_name="natureza", value_name="valor")

df_melted["natureza"] = df_melted["natureza"].map({"debito":"D", "credito":"C"})
df_melted.head()
df_final = df_melted[df_melted["valor"] != 0].reset_index(drop=True)
df_final

df_final.to_excel('resgates_valia_mesbase.xlsx', index=False)