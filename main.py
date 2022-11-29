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

larcenies_data = df.groupby(['householdsize']).agg({"larcenies": 'mean'}).reset_index()
larcenies = px.line(larcenies_data, x='householdsize', y='larcenies')
larcenies.update_layout(xaxis_title="Размер домохозяйства",
                        yaxis_title="Среднее количество краж",
                        title="Зависимость краж со взломом от размера домохозяйства",
                        plot_bgcolor=colors['plot_bgcolor_1'],
                        paper_bgcolor=colors['paper_bgcolor_1'],
                        font_color=colors['white']
                        )

df['medFamInc_with_step'] = df['medFamInc'] - df['medFamInc'] % 1000
murders_data = df.groupby(['medFamInc_with_step']).agg({"murders": 'mean'}).reset_index()
murders = px.line(murders_data, x='medFamInc_with_step', y='murders')
murders.update_layout(xaxis_title="Доход (с шагом 1000)",
                      yaxis_title="Среднее количество убийств", title="Зависимость убийств от уровня дохода семьи",
                      plot_bgcolor=colors['plot_bgcolor_2'],
                      paper_bgcolor=colors['paper_bgcolor_2'],
                      font_color=colors['white']
                      )

rapes_data = df.groupby(['pctUrban']).agg({"rapes": 'mean'}).reset_index()
rapes = px.line(rapes_data, x='pctUrban', y='rapes')
rapes.update_layout(xaxis_title="Процент городского населения",
                    yaxis_title="Среднее количество изнасилований", title="Зависимость изнасилований от соотношения "
                                                                          "городского и сельского населения",
                    plot_bgcolor=colors['plot_bgcolor_1'],
                    paper_bgcolor=colors['paper_bgcolor_1'],
                    font_color=colors['white']
                    )

app.layout = html.Div([
    dcc.Graph(id='autoThefts', figure=autoThefts),
    dcc.Graph(id='burglaries', figure=burglaries),
    dcc.Graph(id='larcenies', figure=larcenies),
    dcc.Graph(id='murders', figure=murders),
    dcc.Graph(id='rapes', figure=rapes)
])

if __name__ == '__main__':
    app.run_server(debug=True)
