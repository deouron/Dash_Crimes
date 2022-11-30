from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('crimedata.csv')
df['medFamInc_with_step'] = df['medFamInc'] - df['medFamInc'] % 1000

states_df = df.groupby(['state']).agg({"racepctblack": 'mean', 'racePctWhite': 'mean',
    'racePctAsian': 'mean', 'racePctHisp': 'mean', 'murders': 'sum', 'rapes': 'sum', 'robberies': 'sum',
    'assaults': 'sum', 'burglaries': 'sum', 'larcenies': 'sum', 'autoTheft': 'sum', 'arsons': 'sum'}).reset_index()

autoThefts_incomes_state_df = df.groupby(['state', 'medFamInc_with_step']).agg({"autoTheft": 'mean'}).reset_index()

colors = {
    'black': '#111111',
    'white': '#FFFFFF',
    'text': '#7FDBFF',
    'paper_bgcolor_1': '#008B92',
    'plot_bgcolor_1': '#B7D5FE',
    'paper_bgcolor_2': '#D01120',
    'plot_bgcolor_2': '#E7C5C6',
    'plot_bgcolor_3': '#E9F4FF',
    'plot_bgcolor_4': '#FFF1FA'
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

    html.Br(),
    dcc.Graph(id='burglaries', figure=burglaries),

    html.Br(),
    dcc.Graph(id='larcenies', figure=larcenies),

    html.Br(),
    dcc.Graph(id='murders', figure=murders),

    html.Br(),
    dcc.Graph(id='rapes', figure=rapes),

    html.Br(),
    html.Label(['Город:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(df['communityName'], df['communityName'][0], id='communityName_races'),
    dcc.Graph(id='races'),

    html.Br(),
    html.Label(['Штат:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(states_df['state'], states_df['state'][0], id='state_races'),
    dcc.Graph(id='races_states'),

    html.Br(),
    html.Label(['Город:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(df['communityName'], df['communityName'][0], id='communityName_crimes'),
    dcc.Graph(id='crimes'),

    html.Br(),
    html.Label(['Штат:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(states_df['state'], states_df['state'][0], id='states_crimes'),
    dcc.Graph(id='crimes_states'),

    html.Br(),
    html.Label(['Штат:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(states_df['state'], states_df['state'][0], id='states_autoThefts'),
    dcc.Graph(id='autoThefts_states')
])


@app.callback(
    Output(component_id='races', component_property='figure'),
    [Input(component_id='communityName_races', component_property='value')]
)
def update_output(selected_community):
    community_df = df[df.communityName == selected_community]
    community_df = community_df.iloc[0]
    fig = px.pie(community_df, names=['Чёрные', 'Белые', 'Азиаты', 'Латиноамериканцы'],
                 values=[community_df['racepctblack'], community_df['racePctWhite'],
                         community_df['racePctAsian'], community_df['racePctHisp']])

    fig.update_layout(title=f"Соотношение рас в {selected_community}",
                      plot_bgcolor=colors['plot_bgcolor_3'],
                      paper_bgcolor=colors['plot_bgcolor_3'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='races_states', component_property='figure'),
    [Input(component_id='state_races', component_property='value')]
)
def update_output(selected_state):
    state_df = states_df[states_df.state == selected_state]
    state_df = state_df.iloc[0]
    fig = px.pie(state_df, names=['Чёрные', 'Белые', 'Азиаты', 'Латиноамериканцы'],
                 values=[state_df['racepctblack'], state_df['racePctWhite'],
                         state_df['racePctAsian'], state_df['racePctHisp']])

    fig.update_layout(title=f"Соотношение рас в {selected_state}",
                      plot_bgcolor=colors['plot_bgcolor_4'],
                      paper_bgcolor=colors['plot_bgcolor_4'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='crimes', component_property='figure'),
    [Input(component_id='communityName_crimes', component_property='value')]
)
def update_output(selected_community):
    community_df = df[df.communityName == selected_community]
    community_df = community_df.iloc[0]
    fig = px.histogram(community_df,
                       x=['Убийства', 'Изнасилования', 'Грабежи', 'Нападения', 'Кражи со взломом', 'Кражи',
                          'Автокражи', 'Поджоги'],
                       y=[community_df['murders'], community_df['rapes'], community_df['robberies'],
                          community_df['assaults'], community_df['burglaries'], community_df['larcenies'],
                          community_df['autoTheft'], community_df['arsons']])

    fig.update_layout(yaxis_title="Количество преступлений",
                      xaxis_title="Преступления",
                      title=f"Соотношение преступлений в {selected_community}",
                      plot_bgcolor=colors['plot_bgcolor_3'],
                      paper_bgcolor=colors['plot_bgcolor_3'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='crimes_states', component_property='figure'),
    [Input(component_id='states_crimes', component_property='value')]
)
def update_output(selected_state):
    state_df = states_df[states_df.state == selected_state]
    state_df = state_df.iloc[0]
    fig = px.histogram(state_df,
                       x=['Убийства', 'Изнасилования', 'Грабежи', 'Нападения', 'Кражи со взломом', 'Кражи',
                          'Автокражи', 'Поджоги'],
                       y=[state_df['murders'], state_df['rapes'], state_df['robberies'],
                          state_df['assaults'], state_df['burglaries'], state_df['larcenies'],
                          state_df['autoTheft'], state_df['arsons']])

    fig.update_layout(title=f"Соотношение преступлений в {selected_state}",
                      plot_bgcolor=colors['plot_bgcolor_4'],
                      paper_bgcolor=colors['plot_bgcolor_4'],
                      font_color=colors['black'])
    return fig


@app.callback(
    Output(component_id='autoThefts_states', component_property='figure'),
    [Input(component_id='states_autoThefts', component_property='value')]
)
def update_output(selected_state):
    state_df = autoThefts_incomes_state_df[autoThefts_incomes_state_df.state == selected_state]
    state_df = state_df.sort_values(by='medFamInc_with_step')
    fig = px.line(state_df, x='medFamInc_with_step', y='autoTheft')

    fig.update_layout(xaxis_title="Доход (с шагом 1000)",
                      yaxis_title="Среднее количество автокраж",
                      title=f"Зависимость автокраж от дохода в {selected_state}",
                      plot_bgcolor=colors['plot_bgcolor_3'],
                      paper_bgcolor=colors['plot_bgcolor_3'],
                      font_color=colors['black'])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
