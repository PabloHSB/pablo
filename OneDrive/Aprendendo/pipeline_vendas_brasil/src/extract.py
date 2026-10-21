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
print(df_reduzido)
