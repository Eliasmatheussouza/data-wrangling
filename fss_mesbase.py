## Importando os pacotes
import pandas as pd

# Criando o DataFrame principal
v1 = pd.read_excel('ficha_financeira_valia.xlsx', decimal=',')
v2 = pd.read_excel('resgates_valia_mesbase.xlsx', decimal=',')
valia = pd.concat([v1, v2], ignore_index=True)
filtro = pd.read_excel('filtro_plano.xlsx')
filtro.info()

# Tratando dataframe valia
valia = valia.applymap(lambda x: x.strip() if isinstance(x, str) else x)
valia.info()
valia.tail()

# Filtrando
extrat_merge = pd.merge(valia, filtro, on=('FSS', 'cod_plano'), how='left')

# Removendo NaN
extrat_merge = extrat_merge.dropna(subset=['Mrc_Migra'])

# Consultando se temos valores diferentes de "S" e removendo espaço extra
extrat_merge['Mrc_Migra'].unique()
extrat_merge = extrat_merge.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = extrat_merge[extrat_merge['Mrc_Migra'] == "S"]

# Visualizando os headers do DF
df.info()
df.tail()

# Verificar valores nulos
df.isnull().sum()

# Removendo espaços extras do DataFrame
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.loc[df['natureza'] == 'D', 'valor'] = df['valor'] * -1
#df.loc[df['natureza'] == 'D', 'valor'] = df['valor'] * -1
# Selecionando as colunas desejadas e agrupando por FSS, plano, beneficio e natureza
df_plano_natureza = df.groupby(['cod_plano', 'plano', 'natureza'], as_index=False)['valor'].sum()
df_plano_beneficio_natureza = df.groupby(['cod_plano', 'cod_beneficio', 'beneficio', 'plano', 'natureza'], as_index=False)['valor'].sum()

df_plano_natureza.to_excel('valia_agrupado.xlsx', index=False)
df_plano_beneficio_natureza.to_excel('valia_plano_beneficio_natureza.xlsx', index=False)

# Importando DF Sinqia
sinqia_plano = pd.read_excel('totalizador_plano.xlsx', decimal=',')
sinqia_plano.columns
sinqia_plano = sinqia_plano.applymap(lambda x: x.strip() if isinstance(x, str) else x)

sinqia_plano_beneficio = pd.read_excel('totalizador_plano_beneficio.xlsx', decimal=',')
sinqia_plano_beneficio.columns
sinqia_plano_beneficio = sinqia_plano_beneficio.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Mesclando os dataframes
merge_plano_natureza = pd.merge(sinqia_plano, df_plano_natureza, on=('cod_plano', 'natureza'), how='outer', suffixes=('_sinqia', '_valia'))
merge_plano_natureza.head()
merge_plano_natureza['valor_sinqia'] = merge_plano_natureza['valor_sinqia'].fillna(0)
merge_plano_natureza['valor_valia'] = merge_plano_natureza['valor_valia'].fillna(0)
merge_plano_natureza['dif_valor'] = merge_plano_natureza['valor_sinqia'] - merge_plano_natureza['valor_valia']
merge_plano_natureza.to_excel('validacao_plano_natureza.xlsx', index=False)

# merge_plano_natureza['plano'] = merge_plano_natureza['plano_valia'].combine_first(merge_plano_natureza['plano_sinqia'])
# merge_plano_natureza['beneficio'] = merge_plano_natureza['beneficio_valia'].combine_first(merge_plano_natureza['beneficio_sinqia'])

merge_beneficio_natureza = pd.merge(sinqia_plano_beneficio, df_plano_beneficio_natureza, on=('cod_plano', 'cod_beneficio', 'natureza'), how='outer', suffixes=('_sinqia', '_valia'))
merge_beneficio_natureza['valor_sinqia'] = merge_beneficio_natureza['valor_sinqia'].fillna(0)
merge_beneficio_natureza['valor_valia'] = merge_beneficio_natureza['valor_valia'].fillna(0)
merge_beneficio_natureza['dif_valor'] = merge_beneficio_natureza['valor_sinqia'] - merge_beneficio_natureza['valor_valia']
merge_beneficio_natureza.to_excel('validacao_beneficio_natureza.xlsx', index=False)

#df1 = pd.read_excel('plano_benef_natureza.xlsx', decimal=',')

#df = pd.merge(merge_beneficio_natureza, df1, on=('cod_plano', 'cod_beneficio', 'natureza'), how='left', suffixes=('_sinqia', '_df1'))
#df.columns
#df.tail()
#df.rename(columns={'plano_df1':'plano'}, inplace=True)
#df.rename(columns={'beneficio_df1':'beneficio'}, inplace=True)
#plano_map = df[df['plano'].notnull()][['cod_plano', 'plano']].drop_duplicates().set_index('cod_plano')['plano'].to_dict()
#beneficio_map = df[df['beneficio'].notnull()][['cod_beneficio', 'beneficio']].drop_duplicates().set_index('cod_beneficio')['beneficio'].to_dict()

#df['plano'] = df['plano'].fillna(df['cod_plano'].map(plano_map))
#df['beneficio'] = df['beneficio'].fillna(df['cod_beneficio'].map(beneficio_map))
#df['beneficio'].unique()
#df1.isnull().sum()
#df1 = df.dropna(subset=('FSS'))
#df1['beneficio'].unique()
#df2 = df1[['FSS', 'plano', 'cod_plano', 'beneficio', 'cod_beneficio', 'natureza', 'valor_sinqia', 'valor_valia', 'dif_valor']]
#df2.to_excel('validacao_ff_mesb_0506v2.xlsx', index=False)