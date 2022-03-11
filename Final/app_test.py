import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# from datetime import date
import plotly.graph_objects as go
# from urllib.request import urlopen
# import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#################### MAP ########################
df_map = pd.read_csv('priceFIPS.csv')
df_map['FIPS'] = df_map['FIPS'].apply(lambda x: str(x).zfill(5))
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig_us = px.choropleth(df_map, geojson=counties, locations='FIPS', color='price',
                        color_continuous_scale="jet", hover_name="county",
                        range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                        scope="usa",
                        title = 'USA gas price by county'
                        )
fig_us.update_traces(marker_line_width=0.1, marker_opacity=0.8)
fig_us.update_geos(showsubunits=True, subunitcolor="black")
fig_us.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})

fig_ca = px.choropleth(df_map[df_map['state']=='CA'], geojson=counties, locations='FIPS', color='price',
                        color_continuous_scale="jet", hover_name="county",
                        range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                        title ='gas price by county in State CA' 
                        )
fig_ca.update_geos(fitbounds='locations', visible=False)
fig_ca.update_traces(marker_line_width=0.3)

#################### table #########################
tb = pd.read_csv('table.csv')

################ scatter plot #######################
dt=pd.read_excel("Today's gas price by country(11.17).xlsx", sheet_name='9state')
ca=dt[dt['state']=='CA']['price']
co=dt[dt['state']=='CO']['price']
fl=dt[dt['state']=='FL']['price']
ma=dt[dt['state']=='MA']['price']
mn=dt[dt['state']=='MN']['price']
ny=dt[dt['state']=='NY']['price']
oh=dt[dt['state']=='OH']['price']
tx=dt[dt['state']=='TX']['price']
wa=dt[dt['state']=='WA']['price']

fig1 = go.Figure()
fig1.add_trace(go.Box(y=ca, name='California',
                marker_color = 'red'))
fig1.add_trace(go.Box(y=co, name='Colorado',
                marker_color = 'orange'))
fig1.add_trace(go.Box(y=fl, name='Florida',
                marker_color = 'yellow'))
fig1.add_trace(go.Box(y=ma, name='Massachusetts',
                marker_color = 'green'))
fig1.add_trace(go.Box(y=mn, name='Minnesota',
                marker_color = 'lightgreen'))
fig1.add_trace(go.Box(y=ny, name='NeW York',
                marker_color = 'blue'))
fig1.add_trace(go.Box(y=oh, name='Ohio',
                marker_color = 'navy'))
fig1.add_trace(go.Box(y=tx, name='Texas',
                marker_color = 'purple'))
fig1.add_trace(go.Box(y=wa, name='Washington',
                marker_color = 'grey'))

fig1.update_yaxes(nticks=18)

fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)'
)

fig1.update_layout(
    title={
        'text': "Today's gas price",
        'font_size': 30,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

################# time series ##########################
df = pd.read_csv('9_state_yearly.csv',index_col=0)
fig = px.line(df, x=df.index, y=df['California'])

fig.update_xaxes(rangeslider_visible = True)

fig.update_layout(
    title={
        'text': 'California Yearly Average Gas Price (2003-2021)',
        'font_size': 30,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        # 'pad_b':50
    }
)

################### Layout #########################
app.layout = html.Div([
    html.Div(
        className="app-header",
        children = [
            html.H1('US Gas Price From Past to Today') 
        ] 
    ),

    html.Div(className='app-map-us',
        children=[
            dcc.Graph(
                className= 'map-us-plot',
                id= 'usmap',
                figure = fig_us)]
        ),

    html.Div(className='app-map-state',
        children=[
            dcc.Dropdown(id='map_state_dropdown',
                    options=[{'label': j, 'value': j}
                            for j in df_map.state.unique()]),
            dcc.Graph(
                className= 'map-state-plot',
                id= 'statemap',
                figure = fig_ca)
        ]),

    html.Div(
        className='app-table',
        children= [
            html.H2('Gas Price Summary By Region'),
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in tb.columns],
            data=tb.to_dict('records'),
            style_table={
                'overflowX': 'auto'
            },
            style_cell={
                'height': '70px',
                'width': '85px', 
                'whiteSpace': 'normal',
                'text-align':'center',
                'font-size': '20px ',
                'font-family': 'Arial, Helvetica, sans-serif'
            },
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(58, 117, 194)',
                    'color': 'white'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(58, 117, 194)',
                'color': 'black',
                'fontWeight': 'bold',
                'text-align':'center',
                'font-size': '20px',
                'color':'white',
                'font-family': 'Arial, Helvetica, sans-serif'
            }
        )
        ]
    ),
    html.Div(
        className='app-scatter'
    ),
    html.Div(
        className='app-box',
        children = [
            dcc.Graph(
            className= 'app-box-plot',
            id='box',
            figure=fig1)]
        ),
    html.Div(className='app-time',
        children=[
            dcc.Graph(
                className= 'app-time-plot',
                id='state-line',
                figure=fig),
            html.H3('Please select the state you are interested in'),
            dcc.Dropdown(
                id='state_dropdown',
                className= 'app-time-drop',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='California',
                style = {
                    'width': '60%', 
                    'padding': '20 20',
                    'float':'right'
                })  
            ], style={
                    'width': '60%', 
                    'display': 'inline-block',
                    'padding': '10 5',
                    'margin':'auto' 
            }),
    html.Div(
        className= 'app-footer',
        children= [
            html.Hr(className='hr'),
            html.H6('DSO545 Final Project (Fall 2021) - Zihang Li, Freda Lin, Zihan Ling, Jingchen Liu, Yafan Zeng, Pizheng Zhang')
        ]
        )
])

# @app.callback([Output('statemap', 'figure'),Output('state-line', 'figure')],
#             [Input('map_state_dropdown', 'value'),Input('state_dropdown', 'value')])

# def update_figure(state_map,state_line):
#     if state_map is None:
#         df2 = df_map[df_map['state']=='CA']
#     else:
#         df2 = df_map[df_map['state']==state_map]
#     fig1 = px.choropleth(df2, geojson=counties, locations='FIPS', color='price',
#                             color_continuous_scale="jet", hover_name="county",
#                             range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
#                             title =f'gas price by county in State {state_map}' 
#                             )
#     fig1.update_geos(fitbounds='locations', visible=False)
#     fig1.update_traces(marker_line_width=0.3)

#     if state_line is None:
#         state_line = 'California'
#     fig2 = px.line(df, x=df.index, y=df[state_line])
#     fig2.update_xaxes(rangeslider_visible = True)
#     fig2.update_layout(
#         title={
#             'text': state_line + ' Yearly Average Gas Price (2003-2021)',
#             'font_size': 30,
#             'x':0.5,
#             'xanchor': 'center',
#             'yanchor': 'top'
#         }
#     )
#     return fig1,fig2

if __name__ == '__main__':
    app.run_server(debug=True)









