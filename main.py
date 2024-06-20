import dash
import os

import dash_bootstrap_components as dbc
from flask import Flask, render_template, redirect, url_for

from layout import create_layout

app = Flask(__name__)

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/graficos/', external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_app.layout = create_layout()

diretorio=os.getcwd()
print(diretorio)
@app.route('/')
@app.route('/index')
def index(name=None):
    return render_template('index.html',name=name)


@app.route('/graficos/')
def graficos():
    return dash_app.index()


@app.route('/matriz-curricular')
def matriz_curricular():
    return render_template('matriz_curricular.html')


if __name__ == '__main__':
    app.run(debug=True)
