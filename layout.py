import dash_bootstrap_components as dbc
from dash import dcc, html
from graficos import generate_pie_chart, generate_plot, generate_bar_chart

def create_sidebar():
    return html.Div(
        [
            html.H2("Mapbib", className="display-4", style={"textAlign": "center", "marginBottom": "20px"}),
            html.H5("Navegação", className="display-5", style={"marginBottom": "10px"}),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Gráficos", href="/graficos/", active="exact"),
                    dbc.NavLink("Matriz Curricular", href="/matriz-curricular", active="exact"),
                ],
                vertical=True,
                pills=True,
                className="flex-column"
            ),
        ],
        style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "16rem", "padding": "1.5rem", "background-color": "#f8f9fa"}
    )

def create_layout():
    pie_chart_figure = generate_pie_chart()
    plot_figure = generate_plot()
    bar_chart_figure = generate_bar_chart()

    layout = dbc.Container([
        dbc.Row([
            dbc.Col(create_sidebar(), width=2, style={"paddingRight": 0}),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Gráfico de Tipos de Referência", style={"textAlign": "center"}),
                                dcc.Graph(figure=pie_chart_figure)
                            ]),
                            style={"marginBottom": "20px", "height": "100%"}
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Distribuição de Tipos de Referência", style={"textAlign": "center"}),
                                dcc.Graph(figure=plot_figure)
                            ]),
                            style={"marginBottom": "20px", "height": "100%"}
                        ),
                        width=6
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Referências por Década", style={"textAlign": "center"}),
                                dcc.Graph(figure=bar_chart_figure)
                            ]),
                            style={"marginBottom": "20px", "height": "100%"}
                        ),
                        width=12
                    )
                ])
            ], width=10, style={"paddingLeft": 0})
        ])
    ], fluid=True, style={"marginLeft": "18rem", "padding": "2rem 0"})
    return layout
