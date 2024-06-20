# dashboard.py

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
from layout import create_layout

# Inicialize o Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir o layout do Dash app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Função para obter o conteúdo da página do Flask
def fetch_flask_page(url):
    response = requests.get(url)
    return response.content.decode('utf-8')

# Callback para atualizar o conteúdo da página
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/graficos/':
        return create_layout()
    elif pathname == '/matriz-curricular':
        return html.Div(fetch_flask_page('http://localhost:5000/matriz-curricular'))
    else:
        return '404 - Página não encontrada'

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Executar o Dash na porta 8050




