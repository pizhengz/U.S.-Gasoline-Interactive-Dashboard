import pandas as pd
import numpy as np
import plotly.express as px
import dash 
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash import dash_table



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
################
final = pd.read_excel('Final_Scatter.xlsx')
option_labels = ['Gas Tax','Median Income',
                 'Vehicle Registration Number', 
                 'Sales Tax', 'Population',
                 'Oil_Production','Gas Sales' ]
option_values = [ 'Gas_Tax','Median_Income',
                 'Auto', 'Sales_Tax', 
                 'Population','Oil_Production','Gas_Sales']
xaxis_labels = {'Auto':'# of Registered Vehicle',
                   'Sales_Tax' : 'Sales Tax (%/$)',
                    'Gas_Tax' : 'Gas Tax ($/ gallon)',
                    'Population' : 'Population',
                    'Median_Income' : 'Median Income ($)',
               'Oil_Production': 'Crude Oil Production (Thousand Barrels)',
               'Gas_Sales':'Total Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)'}
title_labels = {'Auto':'Number of Registered Vehicle',
                   'Sales_Tax' : 'Sales Tax',
                    'Gas_Tax' : 'Gas Tax',
                    'Population' : 'Population',
                    'Median_Income' : 'Median Income',
                   'Oil_Production': 'Crude Oil Production',
               'Gas_Sales':'Gasoline Sales'}


################
df_map = pd.read_csv('priceFIPS.csv')
df_map['FIPS'] = df_map['FIPS'].apply(lambda x: str(x).zfill(5))
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig_us = px.choropleth(df_map, geojson=counties, locations='FIPS', color='price',
                                   color_continuous_scale="jet",
                            hover_name="county",
                                   range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                                   scope="usa",
                            title = 'USA gas price by county'
                                  )
fig_us.update_traces(marker_line_width=0.1, marker_opacity=0.8)
fig_us.update_geos(showsubunits=True, subunitcolor="black")
fig_us.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})

fig_ca = px.choropleth(df_map[df_map['state']=='CA'], geojson=counties, locations='FIPS', color='price',
                                color_continuous_scale="jet",
                        hover_name="county",
                                range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                        title ='gas price by county in State CA' 
                                )
fig_ca.update_geos(fitbounds='locations', visible=False)
fig_ca.update_traces(marker_line_width=0.3)


app.layout = html.Div([
    dcc.Graph(id = 'Scatter_Plots'),

    dcc.Dropdown(
    id = 'my-dropdown',
    options = [{'label':i,'value':j} for i ,j in zip(option_labels,option_values)],
    searchable=False,
    value = 'Gas_Tax'),
    
    html.Hr(),
    
    dcc.Checklist(
    id = 'my-checklist',
    options = [{'label':'Party Affliation','value': 'party'}],
    value = []),
    
    dcc.RadioItems(
        id='xaxis-type',
        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
        value='Linear',
        labelStyle={'display': 'inline-block'}
    ),

    dcc.Dropdown(id='state_dropdown',
                 options=[{'label': state, 'value': state}
                          for state in df_map.state.unique()]),

    # dcc.Graph(id= 'map',figure = fig_us),
    dcc.Graph(id='graph',figure = fig_ca)
])


@app.callback(
    [Output('Scatter_Plots', 'figure'),Output('graph', 'figure')],
    [Input('my-dropdown', 'value'),
    Input('my-checklist', 'value'),
    Input('xaxis-type', 'value'),
    Input('state_dropdown', 'value')]
)
def update_output(x_value,par,mode,state):
    m = None
    if x_value is None:
        x_value == 'Gas Tax'
    if mode == 'Log':
        m = True
    p = None
    if par:
        p = 'Party'
    fig1 = px.scatter(data_frame=final,x=x_value,y='Gas_Price', color = p,
                     color_discrete_map = {'Democrat':'blue','Republic':'red'},
                     labels= {'Gas_Price':'Price ($)',
                             x_value: xaxis_labels[x_value]},
                     text = 'ST',
           hover_data=['State','Gas_Price', 'Auto', 'Population'],
           trendline="ols",
            width=750, height=600,
                    title=f'Average Retail Gasoline Price vs. {title_labels[x_value]} By State',
                    log_x=m)
    fig1.update_traces(textposition = 'bottom right',marker = dict(size = 8))
    fig1.update_layout(legend_traceorder="reversed")

    if state is None:
        df2 = df_map[df_map['state']=='CA']
    else:
        df2 = df_map[df_map['state']==state]
    fig2 = px.choropleth(df2, geojson=counties, locations='FIPS', color='price',
                                color_continuous_scale="jet",
                        hover_name="county",
                                range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                        title ='gas price by county in State ' + state
                                )
    fig2.update_geos(fitbounds='locations', visible=False)
    fig2.update_traces(marker_line_width=0.3)
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)

