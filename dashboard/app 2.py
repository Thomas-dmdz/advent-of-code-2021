# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

app = dash.Dash(__name__)

file = 'data.csv'
file = 'advent-of-code-2021/dashboard/data.csv'
df = pd.read_csv(file)
temp = df.groupby('name')['score'].sum().sort_values(ascending=True).reset_index()
fig = px.bar(temp, x="score", y="name", orientation='h', text='score')
fig.update_layout(
    font_size=15
)

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.scripts.config.serve_locally = False

app.layout = html.Div(children=[
    html.H1(children='Advent of code 2021'),
    
    dcc.RadioItems(
    id='weekend_data',
    options=[
        {'label': 'Ignore weekend', 'value': 'true'},
        {'label': 'Include weekend', 'value': 'false'}
    ],
    value='true'
    ),
    
    
    dcc.Graph(
        id='scores',
        figure=fig
    ),
    
    generate_table(df),
    
    """
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
"""
])


# Callbacks
@app.callback(
    Output('scores', 'figure'),
    [Input('weekend_data', 'value')])
def update_graph(weekend_data):
    dff = df.copy()
    if weekend_data == 'true': # then ignore weekend
        print('true')
        dff = dff[dff['weekend'] == False]
    dff = dff.groupby('name')['score'].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(dff, x="score", y="name", orientation='h', text='score')
    fig.update_layout(font_size=15)


    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
