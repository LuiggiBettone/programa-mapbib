import pandas as pd
import plotly.express as px

# Definição de uma sequência de cores azul
blue_colors = [
    '#1f77b4',  # Azul padrão do Plotly
    '#aec7e8',  # Azul claro
    '#6baed6',  # Azul intermediário
    '#3182bd',  # Azul escuro
    '#08519c'  # Azul muito escuro
]

# Carregando o arquivo CSV em um DataFrame
main_df = pd.read_csv('C:/Users/luiggi/PycharmProjects/pythonProject2/Dados/tabela.csv', sep=';')


# Função para gerar o gráfico de distribuição de tipos de referência
def generate_plot():
    quant = main_df['Tipo Referencia'].value_counts()
    type_names = quant.index
    fig = px.pie(
        names=type_names,
        values=quant.values,
        color_discrete_sequence=blue_colors,
        title='Distribuição de Tipos de Referência'
    )
    return fig


# Função para extrair letras de um texto
def extrair_letras(texto):
    letras = ''.join([caracter for caracter in str(texto) if caracter.isalpha()])
    return letras


def ler_departamentos(dataframe_obrigatorias):
    departamentos_df = pd.read_csv('C:/Users/luiggi/PycharmProjects/pythonProject2/Dados/departamentos.csv', sep=';')
    lista_obrigatorias_df = pd.read_csv('C:/Users/luiggi/PycharmProjects/pythonProject2/Dados/lista_obrigatorias.csv',
                                        sep=';')
    lista_optativas_df = pd.read_csv('C:/Users/luiggi/PycharmProjects/pythonProject2/Dados/lista_optativas.csv',
                                     sep=';')
    dataframe_obrigatorias = pd.merge(dataframe_obrigatorias, lista_obrigatorias_df, left_on='CODIGO', right_on='codigo', how='left')
    dataframe_obrigatorias = pd.merge(dataframe_obrigatorias, departamentos_df, left_on='id', right_on='id', how='left')
    dataframe_obrigatorias.drop(['id', 'codigo'], axis=1, inplace=True)
    dataframe_obrigatorias = dataframe_obrigatorias.dropna(subset=["departamento"])
    print(dataframe_obrigatorias.tail())

    return dataframe_obrigatorias

# Função para gerar o gráfico de porcentagem de exemplares por departamento
def generate_pie_chart():
    obrigatorias_df = pd.read_csv('C:/Users/luiggi/PycharmProjects/pythonProject2/Dados/obrigatorias.csv', sep=';')
    obrigatorias_df = ler_departamentos(obrigatorias_df)
    # obrigatorias_df['DEPARTAMENTO'] = obrigatorias_df['CODIGO'].apply(extrair_letras)
    total_por_departamento = obrigatorias_df.groupby('departamento')['TOTAL EXEMPLARES'].sum()
    total_geral = obrigatorias_df['TOTAL EXEMPLARES'].sum()
    total_por_departamento = total_por_departamento.to_frame()
    total_por_departamento['Porcentagem'] = (total_por_departamento['TOTAL EXEMPLARES'] / total_geral) * 100

    fig = px.pie(
        total_por_departamento,
        names=total_por_departamento.index,
        values='Porcentagem',
        color_discrete_sequence=blue_colors,
        title='Porcentagem de Exemplares por Departamento em Relação ao Total Geral'
    )
    return fig


# Função para gerar o gráfico de barras de referências por década
def generate_bar_chart():
    # Limpeza e manipulação dos dados
    dados = main_df.copy()
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace(':', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace(';', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace(',', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace('.', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace('—', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.replace('  ', ' ') if isinstance(x, str) else x)
    dados['TITULO'] = dados['TITULO'].apply(lambda x: x.split(' ') if isinstance(x, str) else x)

    # Função para extrair o ano do título
    def extrair_ano_condicional(valor):
        for item in valor:
            if len(item) == 4 and item.isdigit():
                ano = int(item)
                if 1900 <= ano <= 2024:
                    return ano
        return 'Ano não encontrado ou inválido'

    # Aplicando a função de extração de ano
    dados['Ano'] = dados['TITULO'].apply(extrair_ano_condicional)
    dados['Ano_Invalido'] = dados['Ano'] == 'Ano não encontrado ou inválido'

    # Contagem de anos inválidos
    contagem_ano_invalido = dados['Ano_Invalido'].sum()
    print(f"Número de 'Ano não encontrado ou inválido': {contagem_ano_invalido}")

    # Salvando referências em um arquivo CSV
    referencias = dados[['CODIGO', 'BIBLIOGRAFIA', 'Ano']]
    referencias.to_csv('referencias.csv', sep=';', index=False)

    # Convertendo coluna 'Ano' para numérico e criando coluna 'Decada'
    dados['Ano'] = pd.to_numeric(dados['Ano'], errors='coerce')
    dados['Decada'] = (dados['Ano'] // 10) * 10

    # Filtrando dados válidos e contando por década
    df_validos = dados.dropna(subset=['Ano'])
    contagem_por_decada = df_validos['Decada'].value_counts().sort_index()

    # Gerando gráfico de barras
    fig = px.bar(
        x=contagem_por_decada.index,
        y=contagem_por_decada.values,
        title='Número de Referências por Década',
        labels={'x': 'Década', 'y': 'Número de Referências'},
        color_discrete_sequence=blue_colors
    )
    return fig
def gerar_grafico_exemplares():
    # Leitura dos arquivos CSV relevantes
    df1 = pd.read_csv("obrigatorias_eng_carto.csv", sep=";")
    df2 = pd.read_csv("departamentos.csv", sep=";")
    df3 = pd.read_csv("lista_obrigatorias.csv", sep=";")

    # Realizando pesquisa por palavra nos DataFrames
    df1_online = df1.apply(lambda row: row.astype(str).str.contains("online", case=False).any(), axis=1)
    df1_https = df1.apply(lambda row: row.astype(str).str.contains("https", case=False).any(), axis=1)
    df1_offline = df1.apply(lambda row: row.astype(str).str.contains("offline", case=False).any(), axis=1)

    # Combinando os resultados da pesquisa "online" e "https"
    df1_online_https = df1[df1_online | df1_https]

    # Calculando a quantidade total de códigos e matérias antes do filtro
    quantidade_total_codigos_antes = len(df1['CODIGO'])
    quantidade_total_materias_antes = df1['CODIGO'].nunique()

    # Calculando a quantidade total de códigos e matérias após o filtro
    quantidade_total_codigos_depois = len(df1_online_https['CODIGO'])
    quantidade_total_materias_depois = df1_online_https['CODIGO'].nunique()

    # Gerando gráfico de barras com a contagem de exemplares online e offline
    fig = px.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    status_counts = [quantidade_total_codigos_depois, quantidade_total_codigos_antes - quantidade_total_codigos_depois]
    labels = ['Exemplares Online', 'Exemplares Offline']
    ax.bar(labels, status_counts, color=['blue', 'orange'])
    ax.set_title('Distribuição de Exemplares Online e Offline')
    ax.set_xlabel('Status dos Exemplares')
    ax.set_ylabel('Quantidade')
    px.xticks(rotation=45)
    px.tight_layout()

    # Salvando o gráfico como uma imagem
    px.savefig('static/grafico_exemplares.png')  # Salva o gráfico na pasta static do seu projeto

    # Convertendo o gráfico Plotly para HTML
    fig = px.bar(x=labels, y=status_counts, labels={'x': 'Status dos Exemplares', 'y': 'Quantidade'})
    fig.update_layout(title='Distribuição de Exemplares Online e Offline')
    grafico_html = fig.to_html(full_html=False)

    return grafico_html