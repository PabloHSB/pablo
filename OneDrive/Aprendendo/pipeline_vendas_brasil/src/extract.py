import pandas as pd
from pathlib import Path

caminho_onedrive = Path("C:\\Users\\pablo\\OneDrive\\Aprendendo\\pipeline_vendas_brasil\\data\\vendas_brasil_sinteticas.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

df = pd.read_csv(caminho_onedrive)


linhas_com_ausentes = df[df['uf'].isna()]

pedidos_cancelados = ['Cancelado']
pedidos = len(df[df['status_pedido'].isin(pedidos_cancelados) & df['prazo_entrega_dias'].notna()])

df_desejado = ['pedido_id', 'regiao', 'cliente_id', 'uf', 'prazo_entrega_dias']
df_reduzido = df[df['uf'].isna()][df_desejado]

clientes_s = ['C0027', 'C0094', 'C0163', 'C0191', 'C0229', 'C0245', 'C0361', 'C0400']
df_clientes_s = df[df['cliente_id'].isin(clientes_s)]
pedidos_por_cliente = df_clientes_s.groupby('cliente_id')
print(pedidos_por_cliente)

# 1. Filtra duplicados olhando APENAS o ID do pedido (traz tudo)
#todos_duplicados = df[df.duplicated(subset=['pedido_id'], keep=False)]

# 2. Filtra duplicados olhando a LINHA INTEIRA (traz só os que são 100% idênticos)
# identicos = df[df.duplicated(keep=False)]

# 3. O que está no grupo 1 mas NÃO está no grupo 2 são os pedidos que mudaram!
# pedidos_com_alteracao = todos_duplicados[~todos_duplicados.index.isin(identicos.index)]

# Ordena para comparar lado a lado
# print(pedidos_com_alteracao.sort_values(by='pedido_id'))

# Quantidade de linhas duplicadas no DF 7 linhas
# iremos fazer a remoção das duplicadas pois o pedido não sofreu alteração nos dados
linhas_dupli = df[df.duplicated(keep=False)]
linhas_dupli_j = len(linhas_dupli.sort_values(by='pedido_id'))
print(linhas_dupli_j)

df_tratado = df.copy()

df_tratado = df_tratado.drop_duplicates()

print("Antes:", len(df))

print("Depois:", len(df_tratado))











