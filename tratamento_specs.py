import pandas as pd

# Definindo limites com base nos tamanhos informados
colspecs = [(0, 3), (3, 50), (50, 58), (58, 108), (108, 109), (109, 159), (159, 171), (171, 185), (185, 186)]

# Definindo nome das colunas
col_names = ["PlanoScaf", "FSS", "data", "cod_fundo", "cod_origem", "UM", "valor_moeda", "valor_indice", "natureza"]

# Lendo o arquivo de largura fixa
ar1 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_1.txt', colspecs=colspecs, header=None, names=col_names)
ar2 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_2.txt', colspecs=colspecs, header=None, names=col_names)
ar3 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_3_999_250319_1928.txt', colspecs=colspecs, header=None, names=col_names)
ar4 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_4_999_250319_2142.txt', colspecs=colspecs, header=None, names=col_names)
ar5 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_5.txt', colspecs=colspecs, header=None, names=col_names)
ar6 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_6_999_250320_0333.txt', colspecs=colspecs, header=None, names=col_names)
ar7 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_7.txt', colspecs=colspecs, header=None, names=col_names)
ar8 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_8.txt', colspecs=colspecs, header=None, names=col_names)
ar9 = pd.read_fwf('7.2_RES_HistSaldoAtivo_Arq_9.txt', colspecs=colspecs, header=None, names=col_names)

# Concatenando os dataframes
df = pd.concat([ar1, ar2, ar3, ar4, ar5, ar6, ar7, ar8, ar9], ignore_index=True)
df.head()
df.tail()
df.info()

# Transformando em datetime
df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')

# Transformando valor_moeda e valor_indice em float
df['valor_moeda'] = df['valor_moeda'].astype(float).round(2) / 100
df['valor_indice'] = df['valor_indice'].astype(float).round(4) / 10000

# Selecionando apenas as colunas necessárias
df = df[['FSS', 'data', 'cod_fundo', 'UM', 'natureza', 'valor_moeda', 'valor_indice']]
df.shape

# Separando os planos do arquivo
fca = df[df['UM'].isin([16, 91, 92])]

mosaic_mais = df[df['UM'].isin([20, 157, 158, 159, 160, 165, 285])]
mosaic_mais = mosaic_mais[mosaic_mais['cod_fundo']!= 109]

mosaic_i = df[df['UM'].isin([68, 290, 291, 292, 293, 339, 340, 341, 342, 343, 344, 346])]
mosaic_i = mosaic_i[~mosaic_i['cod_fundo'].isin([105, 205, 411])]

mosaic_ii = df[df['UM'].isin([294, 295, 296, 297, 345])]

prevaler = df[df['UM'].isin([200, 201, 202, 203, 204])]

vale_fertilizantes = df[df['UM'].isin([68, 122])]
vale_fertilizantes = vale_fertilizantes[~vale_fertilizantes['cod_fundo'].isin([105, 205, 3022])]

vale_mais = df[df['UM'].isin([17, 20, 68, 88, 89, 90, 150, 205, 206, 207, 208, 209, 210, 211, 212, 282, 283])]
vale_mais = vale_mais[~vale_mais['cod_fundo'].isin([205, 411, 509, 3022])]

valiaprev = df[df['UM'].isin([18, 68, 94, 95, 96, 151, 213, 214, 215, 216, 217, 218, 219, 220, 284])]
valiaprev = valiaprev[~valiaprev['cod_fundo'].isin([105, 411, 3022])]

# Atualizando valores
fca.loc[fca['natureza']== 'D', 'valor_indice'] *= -1
mosaic_mais.loc[mosaic_mais['natureza']== 'D', 'valor_indice'] *= -1
mosaic_i.loc[mosaic_i['natureza']== 'D', 'valor_indice'] *= -1
mosaic_ii.loc[mosaic_ii['natureza']== 'D', 'valor_indice'] *= -1
prevaler.loc[prevaler['natureza']== 'D', 'valor_indice'] *= -1
vale_fertilizantes.loc[vale_fertilizantes['natureza']== 'D', 'valor_indice'] *= -1
vale_mais.loc[vale_mais['natureza']== 'D', 'valor_indice'] *= -1
valiaprev.loc[valiaprev['natureza']== 'D', 'valor_indice'] *= -1

# Exportando o arquivo para CSV
fca.to_csv('fca_sinqia.csv', decimal=',', index=False)
mosaic_mais.to_csv('mosaic_mais.csv', decimal=',', index=False)
mosaic_i.to_csv('mosaic_i.csv', decimal=',', index=False)
mosaic_ii.to_csv('mosaic_ii.csv', decimal=',', index=False)
prevaler.to_csv('prevaler.csv', decimal=',', index=False)
vale_fertilizantes.to_csv('vale_fertilizantes.csv', decimal=',', index=False)
vale_mais.to_csv('vale_mais.csv', decimal=',', index=False)
valiaprev.to_csv('valiaprev.csv', decimal=',', index=False)