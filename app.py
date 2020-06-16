# Import required libraries
import os
from random import randint

import plotly as py

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import plotly.graph_objects as go
import joblib
import pickle
import pandas as pd
import numpy as np
import plotly.express as px


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


# Put your Dash code here
test_model_data = pd.read_csv('https://raw.githubusercontent.com/popkdodge/Unit-2-Build/master/Test_Car.csv',index_col=[0])
test_model_data = test_model_data.T
df = pd.read_csv('https://raw.githubusercontent.com/popkdodge/Unit-2-Build/master/Carrera_911_1_2.csv',index_col=[0])

# VIS 1
number = [2015]
np.random.seed(1)
mean = df.Price[df.Year==number[0]].mean()
std = df.Price[df.Year==number[0]].std()
x = np.random.randn(10000)
model = joblib.load('911_Price.pkl')
price = model.predict(test_model_data)
spot = (mean-price[0])/std
hist_data = [x]
fair = round(price[0],0)
group_labels = ['911 Carrera'] # name of the dataset
fig = ff.create_distplot(hist_data, group_labels)
fig.update_layout(
    title={
        'text': f"{number[0]} Carrera Price Distribution",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f")
    )
fig.add_trace(go.Scatter(
    x=[0,2.13,-2.11],
    y=[0.45,0.3,0.3],
    text=[f"Mean:{mean:,.0f}",f'1 STD:{(mean+std):,.0f}',f'-1 STD:{mean-std:,.0f}'],
    mode="text",
)) 

fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=0,
            y0=0,
            x1=0,
            y1=0.4,
            line=dict(
                color="Yellow",
                width=3
            )))
fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=1,
            y0=0,
            x1=1,
            y1=0.23,
            line=dict(
                color="Red",
                width=3
            )))
fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=-1,
            y0=0,
            x1=-1,
            y1=0.23,
            line=dict(
                color="red",
                width=3
            )))
fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=spot,
            y0=0,
            x1=spot,
            y1=0.4,
            line=dict(
                color="Green",
                width=3
            )))
graph = fig.to_dict()
#VIS2
import plotly.graph_objects as go

fig1 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 3456,
    mode = "gauge+number+delta",
    title = {'text': "Price"},
    delta = {'reference': 0},
    gauge = {'axis': {'range': [-10000, 10000]},
            'bar': {'color': "#402306"},
             'steps' : [
                 {'range': [-10000, -3333], 'color': "#C29049"},
                 {'range': [-3333, 3333], 'color': "#464C47"},
                 {'range': [3333, 10000], 'color': "#A43131"}],
             'threshold' : {'line': {'color': "Black", 'width': 4}, 'thickness': 0.75, 'value': 300}}))
graph1 = fig1.to_dict()
#VIS3
fig2 = px.scatter(df, x="Year", y="Price", color="Transmission", trendline="lowess")
fig2.update_layout(
    title="The 991.1 and 991.2",
    xaxis_title="Model Year",
    yaxis_title="Price",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"),
        xaxis=dict(
        range=[2011.5, 2019.5]),
    yaxis=dict(
        range=[30000, 150000]),)
graph2 = fig2.to_dict()



external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
# Boostrap CSS.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(
                        children='Porsche 911 Carrera',
                        className='nine columns',
                        style={
                        'height': '15%',
                        'width': '30%',
                        'float': 'left',
                        'position': 'relative',
                        'top': 10,
                        'margin-top': 30,
                        'text-align': 'center',
                        'background-color': 'white',
                        'font-size': 70 ,
                        },
                        ),    
                html.Img(
                    src="https://di-uploads-pod3.dealerinspire.com/porscheoffremont/uploads/2018/09/porsche-logo.jpg",
                    className='three columns',
                    style={
                        'height': '50%',
                        'width': '20%',
                        'float': 'right',
                        'position': 'right',
                        'margin-top': 10,
                    },
                ),
            ], className="row",
            style={
                'background-color':'white',
            }
            
        ),
        html.Div(className='row',children='.',
        style={'background-color':'#EFF0F1',
                'color':'#EFF0F1',},
                ),
        html.Div(
            [
                dcc.Input(
                    id="Milage",
                    type='number',
                    placeholder="Milage",
                    className='one columns offset-by-two',
                    value=30000   
                ),
                dcc.Dropdown(
                    id='condition',
                    placeholder='CPO/Used',
                    options=[
                    {'label': 'Used', 'value': 'Used'},
                    {'label': 'CPO', 'value': 'CPO'},
                            ],
                    className='one columns offset-by-one-haft',
                    value="Used",
                    
                            ), 
                dcc.Dropdown(
                    id='Year',
                    placeholder='Year',
                    options=[
                    {'label': '2012', 'value': 2012},
                    {'label': '2013', 'value': 2013},
                    {'label': '2014', 'value': 2014},
                    {'label': '2015', 'value': 2015},
                    {'label': '2016', 'value': 2016},
                    {'label': '2017', 'value': 2017},
                    {'label': '2018', 'value': 2018},
                    {'label': '2019', 'value': 2019},
                            ],value='2013',
                    className='one columns offset-by-one-haft'
                            ),
                dcc.Dropdown(
                    id='Color',
                    placeholder='Color',
                    options=[
                    {'label': 'Black', 'value': 'Black'},
                    {'label': 'White', 'value': 'White'},
                    {'label': 'Gray', 'value': 'Gray'},
                    {'label': 'Silver', 'value': 'Silver'},
                    {'label': 'Blue', 'value': 'Blue'},
                    {'label': 'Red', 'value': 'Red'},
                    {'label': 'Other', 'value': 'Other'},
                            ],
                    className='one columns offset-by-one-haft',
                    value='Black',
                            ),
                dcc.Dropdown(
                    id='Transmission',
                    placeholder='Transmission',
                    options=[
                    {'label': 'Automatic', 'value': 'Automatic'},
                    {'label': 'Manual', 'value': 'Manual'},
                            ],
                    className='one columns offset-by-one-haft',
                    value='Automatic'
                            ),
                dcc.Dropdown(
                    id='Cabriolet',
                    placeholder='Cabriolet?',
                    options=[
                    {'label': 'Cabriolet', 'value': 'Cabriolet'},
                    {'label': 'Hardtop', 'value': 'Hardtop'},
                            ],
                    value='Cabriolet',
                    className='one columns offset-by-one-haft'
                ),
                dcc.Dropdown(
                    id='S_RS',
                    placeholder='Model',
                    options=[
                    {'label': 'Base', 'value': 'Base'},
                    {'label': '4', 'value': '4'},
                    {'label': 'S', 'value': 'S'},
                    {'label': '4S', 'value': '4S'},
                    {'label': 'GTS', 'value': 'GTS'},
                    {'label': 'GTS4', 'value': 'GTS4'},
                    {'label': 'T', 'value': 'T'},
                    {'label': 'Black Edition', 'value': 'Black'},
                            ],
                    value='Base',
                    className='one columns offset-by-one-haft'
                ),
            ], className="row",
                style={'background-color':'#EFF0F1'}
        ),
        html.Div(className='row',children='.',
        style={'background-color':'#EFF0F1',
                'color':'#EFF0F1',},
                ),
        html.Div(
            [
                html.H1(id='result', 
                        children='',
                        className='nine columns offset-by-three',
                        style={
                        'color':'#959899'
                        })
            ], className="row",
                style={
                    'background-color':'#313639',
                }
        ), 
        html.Div(className='row',children='.',
        style={'background-color':'#EFF0F1',
                'color':'#EFF0F1',},
                ),
        html.Div(
            [
                html.Div(
                    [   
                    dcc.Graph(figure=graph, id='fig1'),
                    ],className='six columns'
                ),
                html.Div(
                    [   
                    dcc.Graph(figure=graph1, id='fig2')
                    ],className='six columns'
                ),
            ], className="row",
        ),
        html.Div(
            [
                html.Div(
                    [   
                    dcc.Graph(figure=graph2, id='fig3')
                    ],className='ten columns offset-by-one',
                    style={
                    'background-clor':'gray',},
                ),
               
            ], className="row",
            
        ),
                    
    ],style={
            'background-clor':'EFF0F1',
            #'background-image': 'https://www.motortrend.com/uploads/sites/5/2020/02/2019-Porsche-Panamera-GTS-29.jpg',
            'background-size': 'cover',
            'background-position': 'center',
            },),
)
@app.callback(
    Output(component_id='result', component_property='children'),
    [Input (component_id='Milage', component_property='value'),
    Input (component_id='condition', component_property='value'),
    Input (component_id='Year', component_property='value'),
    Input (component_id='Color', component_property='value'),
    Input (component_id='Transmission', component_property='value'),
    Input (component_id='Cabriolet', component_property='value'),
    Input (component_id='S_RS', component_property='value'),
    ])
def update_price_input(Milage, condition, Year, Color, Transmission, Cabriolet, S_RS):
    test_model_data.milage = Milage
    test_model_data.condition = condition
    test_model_data.Year = Year
    test_model_data.Color = Color
    test_model_data.Transmission = Transmission
    test_model_data.Cabriolet = Cabriolet
    test_model_data.S_RS = S_RS
    price = model.predict(test_model_data)
    fair = round(price[0],0)
    high = round(price[0]+(price[0]*.05),0)
    low = round(price[0]-(price[0]*.05),0)
    return (f"High: ${high:,.0f}  Fair:  ${fair:,.0f}  Low: ${low:,.0f}")

@app.callback(
    Output(component_id='fig1', component_property='figure'),
    [Input (component_id='Milage', component_property='value'),
    Input (component_id='condition', component_property='value'),
    Input (component_id='Year', component_property='value'),
    Input (component_id='Color', component_property='value'),
    Input (component_id='Transmission', component_property='value'),
    Input (component_id='Cabriolet', component_property='value'),
    Input (component_id='S_RS', component_property='value'),
    ])        
def update_year_and_std(Milage, condition, Year, Color, Transmission, Cabriolet, S_RS):
    test_model_data.milage = Milage
    test_model_data.condition = condition
    test_model_data.Year = Year
    test_model_data.Color = Color
    test_model_data.Transmission = Transmission
    test_model_data.Cabriolet = Cabriolet
    test_model_data.S_RS = S_RS
    number = Year
    np.random.seed(1)
    mean = df.Price[df.Year==number].mean()
    std = df.Price[df.Year==number].std()
    x = np.random.randn(10000)
    model = joblib.load('911_Price.pkl')
    price = model.predict(test_model_data)
    spot = (mean-price[0])/-std
    hist_data = [x]
    group_labels = ['911 Carrera'] # name of the dataset
    fig = ff.create_distplot(hist_data, group_labels)
    fig.update_layout(
        title={
            'text': f"{number} Carrera Price Distribution",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f")
        )
    fig.add_trace(go.Scatter(
        x=[0,2.13,-2.11],
        y=[0.45,0.3,0.3],
        text=[f"Mean:{mean:,.0f}",f'1 STD:{(mean+std):,.0f}',f'-1 STD:{mean-std:,.0f}'],
        mode="text",
    )) 

    fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=0,
                y0=0,
                x1=0,
                y1=0.4,
                line=dict(
                    color="Yellow",
                    width=3
                )))
    fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=1,
                y0=0,
                x1=1,
                y1=0.23,
                line=dict(
                    color="Red",
                    width=3
                )))
    fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=-1,
                y0=0,
                x1=-1,
                y1=0.23,
                line=dict(
                    color="red",
                    width=3
                )))
    fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=spot,
                y0=0,
                x1=spot,
                y1=0.4,
                line=dict(
                    color="Green",
                    width=3
                )))
    graph = fig.to_dict()
    return graph
@app.callback(
    Output(component_id='fig2', component_property='figure'),
    [Input (component_id='Milage', component_property='value'),
    Input (component_id='condition', component_property='value'),
    Input (component_id='Year', component_property='value'),
    Input (component_id='Color', component_property='value'),
    Input (component_id='Transmission', component_property='value'),
    Input (component_id='Cabriolet', component_property='value'),
    Input (component_id='S_RS', component_property='value'),
    ])        
def update_graph2(Milage, condition, Year, Color, Transmission, Cabriolet, S_RS):
    test_model_data.milage = Milage
    test_model_data.condition = condition
    test_model_data.Year = Year
    test_model_data.Color = Color
    test_model_data.Transmission = Transmission
    test_model_data.Cabriolet = Cabriolet
    test_model_data.S_RS = S_RS
    price = model.predict(test_model_data)
    mean = df.Price[df.Year==Year].mean()
    fig1 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = price[0],
    mode = "gauge+number+delta",
    title = {'text': "Price"},
    delta = {'reference': mean},
    gauge = {'axis': {'range': [mean-15000, mean+15000]},
            'bar': {'color': "#402306"},
             'steps' : [
                 {'range': [mean-15000, mean-5000], 'color': "#C29049"},
                 {'range': [mean-5000, mean+5000], 'color': "#464C47"},
                 {'range': [mean+5000, mean+15000], 'color': "#A43131"}],
             'threshold' : {'line': {'color': "Black", 'width': 4}, 'thickness': 0.75, 'value': 300}}))
    graph1 = fig1.to_dict()
    return graph1
@app.callback(
    Output(component_id='fig3', component_property='figure'),
    [Input (component_id='Milage', component_property='value'),
    Input (component_id='condition', component_property='value'),
    Input (component_id='Year', component_property='value'),
    Input (component_id='Color', component_property='value'),
    Input (component_id='Transmission', component_property='value'),
    Input (component_id='Cabriolet', component_property='value'),
    Input (component_id='S_RS', component_property='value'),
    ])        
def update_graph3(Milage, condition, Year, Color, Transmission, Cabriolet, S_RS):
    test_model_data.milage = Milage
    test_model_data.condition = condition
    test_model_data.Year = Year
    test_model_data.Color = Color
    test_model_data.Transmission = Transmission
    test_model_data.Cabriolet = Cabriolet
    test_model_data.S_RS = S_RS
    price = model.predict(test_model_data)
    fig2 = px.scatter(df, x="Year", y="Price", color="Transmission", trendline="lowess")
    fig2.update_layout(
        title="The 991.1 and 991.2",
        xaxis_title="Model Year",
        yaxis_title="Price",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"),
            xaxis=dict(
            range=[2011.5, 2019.5]),
        yaxis=dict(
            range=[30000, 150000]),)
    fig2.add_annotation(
        x=Year,
        y=price[0],
        xref="x",
        yref="y",
        text="Your Car Here",
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=50,
        ay=-50,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
        )

    graph2 = fig2.to_dict()
    return graph2
@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'favicon.ico')
# Run the Dash app
if __name__ == '__main__':
    model = joblib.load('911_Price.pkl')
    app.server.run(debug=True, threaded=True)
