import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
import plotly.graph_objects as go


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#table
tb = pd.read_csv('table.csv')

#time series
df = pd.read_csv('9_state_yearly.csv',index_col=0)

#scatter plot
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

#time series
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

app.layout = html.Div([
    html.Div(
        className="app-header",
        children = [
            html.H1('US Gas Price From Past to Today') 
        ] 
    ),
    html.Div(
        className='app-map-us'
    ),
    html.Div(
        className='app-map-state'
    ),
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

@app.callback(Output('state-line', 'figure'),
              Input('state_dropdown', 'value'))


def update_graph(state):
    if state is None:
        state = 'California'

    fig = px.line(df, x=df.index, y=df[state])

    fig.update_xaxes(rangeslider_visible = True)

    fig.update_layout(
        title={
            'text': state + ' Yearly Average Gas Price (2003-2021)',
            'font_size': 30,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)









