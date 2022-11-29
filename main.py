from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('crimedata.csv')

colors = {
    'black': '#111111',
    'white': '#FFFFFF',
    'text': '#7FDBFF',
    'paper_bgcolor_1': '#008B92',
    'plot_bgcolor_1': '#B7D5FE',
    'paper_bgcolor_2': '#D01120',
    'plot_bgcolor_2': '#E7C5C6'
}

app = Dash(__name__)

autoThefts_data = df.groupby(['state']).agg({"autoTheft": 'sum'}).reset_index()
autoThefts = px.histogram(autoThefts_data, x='state', y='autoTheft')
autoThefts.update_layout(xaxis_title="Штат",
                         yaxis_title="Количество угонов", title="Количество угонов по штатам",
                         plot_bgcolor=colors['plot_bgcolor_1'],
                         paper_bgcolor=colors['paper_bgcolor_1'],
                         font_color=colors['white']
                         )

df = df.sort_values('population')
burglaries = px.line(df, x='population', y='burglaries')
burglaries.update_layout(xaxis_title="Население",
                         yaxis_title="Количество краж со взломом", title="Зависимость краж со взломом от населения",
                         xaxis_range=[0, 1000000],
                         plot_bgcolor=colors['plot_bgcolor_2'],
                         paper_bgcolor=colors['paper_bgcolor_2'],
                         font_color=colors['white']
                         )



app.layout = html.Div([
    dcc.Graph(id='autoThefts', figure=autoThefts),
    dcc.Graph(id='burglaries', figure=burglaries),
])

if __name__ == '__main__':
    app.run_server(debug=True)
