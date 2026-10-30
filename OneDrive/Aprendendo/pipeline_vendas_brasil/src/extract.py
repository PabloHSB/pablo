# ==========================================
# 1. IMPORTAÇÕES E CONFIGURAÇÕES
# ==========================================

import pandas as pd
import numpy as np
from pathlib import Path

caminho_onedrive = Path(r"C:\Users\pablo\OneDrive\Aprendendo\pipeline_vendas_brasil\data\vendas_brasil_sinteticas.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

# ==========================================
# 2. EXTRAÇÃO DOS DADOS
# ==========================================

df = pd.read_csv(caminho_onedrive)

# ==========================================
# 3. INVESTIGAÇÃO DA QUALIDADE
# ==========================================

linhas_com_ausentes = df[df['uf'].isna()]

pedidos_cancelados = ['Cancelado']
pedidos = len(df[df['status_pedido'].isin(pedidos_cancelados) & df['prazo_entrega_dias'].notna()])

#Ivestigando prazo de entrega ausentes com pedidos 
df_desejado = ['pedido_id', 'regiao', 'cliente_id', 'uf', 'prazo_entrega_dias']
df_reduzido = df[df['uf'].isna()][df_desejado]

clientes_s = ['C0027', 'C0094', 'C0163', 'C0191', 'C0229', 'C0245', 'C0361', 'C0400']
df_clientes_s = df[df['cliente_id'].isin(clientes_s)]
pedidos_por_cliente = df_clientes_s.groupby('cliente_id')
print(pedidos_por_cliente)


# Quantidade de linhas duplicadas no DF 7 linhas
# iremos fazer a remoção das duplicadas pois o pedido não sofreu alteração nos dados
linhas_dupli = df[df.duplicated(keep=False)]
linhas_dupli_j = len(linhas_dupli.sort_values(by='pedido_id'))
print(linhas_dupli_j)


#Investigando quantidade negativa
df_ins_q = ['pedido_id', 'regiao', 'cliente_id', 'produto', 'quantidade', 'status_pedido', 'canal_venda', 'qualidade_dados']
valores_N = df_tratado[df_tratado['quantidade'] <= 0 ][df_ins_q]
print(valores_N)
print('---------------------------------------------------')

#Investigando preço negativo
df_ins_preco = ['pedido_id', 'regiao', 'cliente_id', 'produto_id', 'quantidade', 'preco_unitario', 'status_pedido', 'canal_venda', 'qualidade_dados']
preco_negativo = df_tratado[df_tratado['preco_unitario'] <= 0][df_ins_preco]
print(preco_negativo)
print('---------------------------------------------------')

# #Verificando se os produtos com preço negativo são os mesmos que os produtos com preço positivo
Inv_p = ['P008', 'P011', 'P006', 'P011', 'P005']
filtro = df_tratado['produto_id'].isin(inv_p) & (df_tratado['preco_unitario'] > 0)
preco_positivo = df_tratado[filtro]
preco_positivo_unicos = preco_positivo.drop_duplicates(subset=['produto_id'])
print(preco_positivo_unicos.head(5))
print('---------------------------------------------------')

# #Investigando data dos pedidos negativos
df_tratado['data_pedido'] = pd.to_datetime(df_tratado['data_pedido'])
df_ins_data = ['pedido_id', 'regiao', 'cliente_id', 'produto', 'status_pedido', 'canal_venda', 'data_pedido']
data_negativa = df_tratado['data_pedido'] < '2025-01-01'
print(df_tratado[data_negativa][df_ins_data])
print('---------------------------------------------------')

##Investigando prazo de entrega negativo
df_ins_entrega = ['pedido_id', 'regiao', 'cliente_id', 'produto', 'status_pedido', 'canal_venda', 'prazo_entrega_dias']
entrega_negativa = df_tratado['prazo_entrega_dias'] < 0
print(df_tratado[entrega_negativa][df_ins_entrega])
print('---------------------------------------------------')

# ==========================================
# 4. TRANSFORMAÇÃO INICIAL
# ==========================================

df_tratado = df.copy()

# Remover duplicatas exatas
linhas_dupli = df[df.duplicated(keep=False)]

# Converter datas
df_tratado['data_pedido'] = pd.to_datetime(df_tratado['data_pedido'],errors='coerce')

# ==========================================
# 5. CLASSIFICAÇÃO DA QUALIDADE
# ==========================================

# 1. Define as regras em linhas separadas
regra_quantidade_ruim = df_tratado['quantidade'] <= 0
regra_preco_ruim = df_tratado['preco_unitario'] <= 0
regra_uf_aus = df_tratado['uf'].isna()

# 2. Junta tudo no np.where de forma limpa
df_tratado['qualidade_dados'] = np.select([regra_quantidade_ruim | regra_preco_ruim,regra_uf_aus],['Suspeito','OK, com ressalva'],default='OK')

# ==========================================
# 6. REGISTRO DOS MOTIVOS
# ==========================================

