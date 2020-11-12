# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import time
import plotly.graph_objects as go
import dash_table
import pandas as pd
from lib import*

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Twitter Data Analyze In Car Brand Topic'),
    html.H2('CS-226 Group2 Final Project'),
    html.H4('Support Function:'),
    dcc.Link('Search Content', href='/page-1'),
    html.Br(),
    dcc.Link('Car Brand Popularity in the City', href='/page-2'),
    html.Br(),
    dcc.Link('Brand Popularity in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('WordCloud Analyze', href='/page-4'),
])

##################Page-1#######################
page_1_layout = html.Div([
    html.H1('Search the Database'),
    html.H2('Brands'),
    dcc.Checklist(
        id='brand_checklist',
        options=[
            {'label': 'Ford', 'value': 'ford'},
            {'label': 'Toyota', 'value': 'toyota'},
            {'label': 'Chevrolet', 'value': 'chevrolet'},
            {'label': 'Honda', 'value': 'honda'},
            {'label': 'Nissan', 'value': 'nissan'},
            {'label': 'Jeep', 'value': 'jeep'},
            {'label': 'Ram Trucks', 'value': 'ramtrucks'},
            {'label': 'Hyundai', 'value': 'hyundai'},
            {'label': 'Subaru', 'value': 'subaru'},
            {'label': 'Kia', 'value': 'kia'},
            {'label': 'GMC', 'value': 'gmc'},
            {'label': 'Dodge', 'value': 'dodge'},
            {'label': 'Volkswagen', 'value': 'volkswagen'},
            {'label': 'BMW', 'value': 'bmw'},
            {'label': 'Mercedes Benz', 'value': 'mercedesbenz'}
        ],
        value = ['ford'],
        labelStyle={'display': 'inline-block'}
    ),
    html.H2('City'),
    dcc.Dropdown(
        id='city_dropdown',
        options=[
            {'label': 'Birmingham', 'value': 'Birmingham'},
            {'label': 'Anchorage', 'value': 'Anchorage'},
            {'label': 'Phoenix', 'value': 'Phoenix'},
            {'label': 'Little Rock', 'value': 'LittleRock'},
            {'label': 'Los Angeles', 'value': 'LosAngeles'},
            {'label': 'Denver', 'value': 'Denver'},
            {'label': 'Billings', 'value': 'Billings'},
            {'label': 'Omaha', 'value': 'Omaha'},
            {'label': 'Las Vegas', 'value': 'LasVegas'},
            {'label': 'Manchester', 'value': 'Manchester'},
            {'label': 'Newark', 'value': 'Newark'},
            {'label': 'Albuquerque', 'value': 'Albuquerque'},
            {'label': 'New York', 'value': 'NYC'},
            {'label': 'Charlotte', 'value': 'Charlotte'},
            {'label': 'Fargo', 'value': 'Fargo'},
            {'label': 'Columbus', 'value': 'Columbus'},
            {'label': 'OklahomaCity', 'value': 'OklahomaCity'},
            {'label': 'Portland', 'value': 'Portland'},
            {'label': 'Philadelphia', 'value': 'Philadelphia'},
            {'label': 'Providence', 'value': 'Providence'},
            {'label': 'Columbia', 'value': 'Columbia'},
            {'label': 'SiouxFalls', 'value': 'SiouxFalls'},
            {'label': 'Memphis', 'value': 'Memphis'},
            {'label': 'Houston', 'value': 'Houston'},
            {'label': 'Salt Lake City', 'value': 'SaltLakeCity'},
            {'label': 'Burlington', 'value': 'Burlington'},
            {'label': 'Virginia Beach', 'value': 'VirginiaBeach'},
            {'label': 'Seattle', 'value': 'Seattle'},
            {'label': 'Charleston', 'value': 'Charleston'},
            {'label': 'Milwaukee', 'value': 'Milwaukee'},
            {'label': 'Cheyenne', 'value': 'Cheyenne'},
            {'label': 'Riverside', 'value': 'Riverside'}
        ],
        multi = True,
        value = ['Phoenix']
    ),
    html.H2('Select Time Range'),
    dcc.RangeSlider(
        id='time-range-slider',
        min=1,
        max=61,
        step=1,
        value=[1, 61],
        updatemode='drag',
        dots=True
    ),
    html.Div(id='output-container-range-slider', style={'margin-top': 20, 'fontSize': 20}),

    html.Div('Please wait a moment to generate graph due to large amounts of data !', style={'margin-top': 20, 'fontSize': 16, 'color':'Red'}),
    
    #table
    dash_table.DataTable(
        id='search_table',
        data=[],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_table={
        'maxHeight': 'auto',
        'overflowY': 'scroll',
        },

        style_header={
        'backgroundColor': 'lightblue',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'font_size': '20px',
        },

        style_cell={
        # all three widths are needed
        'minWidth': '20px', 'width': '180px', 'maxWidth': '300px',
        'overflow': 'hidden',
        'whiteSpace': 'normal',
        'textAlign': 'left',
        },

        style_cell_conditional=[
        {'if': {'column_id': 'datetime'},'width':'10%',}
        ]
        ),

    html.Br(),
    dcc.Link('Car Brand Popularity in the City', href='/page-2'),
    html.Br(),
    dcc.Link('Brand Popularity in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('WordCloud Analyze', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('time-range-slider', 'value')])
def update_output(value):
    result = []
    for v in value:
        if v <= 31:
            result.append('10/' + str(v))
        else:
            v = v - 31
            result.append('11/' + str(v))

    return '=== Start time: {}, End Time: {} ==='.format(
        result[0],
        result[1]
    )

@app.callback(
    [dash.dependencies.Output('search_table', 'data'),dash.dependencies.Output('search_table', 'columns')],
    [dash.dependencies.Input('brand_checklist', 'value'),dash.dependencies.Input('city_dropdown', 'value'),dash.dependencies.Input('time-range-slider', 'value')])
def renew_table(brand_list,city_list,timerange):
    brand_list = [brand.encode("utf-8") for brand in brand_list]
    city_list = [city.encode("utf-8") for city in city_list]
    time_result = []
    for v in timerange:
        if v <= 31:
            time_result.append([10,v])
        else:
            v = v - 31
            time_result.append([11,v])
    select_data = select_from_DB(city_list,time_result[0][0],time_result[0][1],time_result[1][0],time_result[1][1])
    select_data = select_from_content(select_data,brand_list)
    df = pd.DataFrame.from_dict(select_data)

    columns=[{"name": i, "id": i} for i in df.columns]
    data=df.to_dict('records')

    return data,columns



##################Page-1#######################

##################Page-2#######################
page_2_layout = html.Div([
    html.H1('Car Brand Popularity in the City'),
    html.H2('Brands'),
    html.H5('Brand list includes:'),
    html.H6('[Ford,Toyota,Chevrolet,Honda,Nissan,Jeep,Ram Trucks,Hyundai,Subaru,Kia,GMC,Dodge,Volkswagen,BMW,Mercedes Benz]'),
    html.H2('City'),
    dcc.Dropdown(
        id='city_dropdown',
        options=[
            {'label': 'Birmingham', 'value': 'Birmingham'},
            {'label': 'Anchorage', 'value': 'Anchorage'},
            {'label': 'Phoenix', 'value': 'Phoenix'},
            {'label': 'Little Rock', 'value': 'LittleRock'},
            {'label': 'Los Angeles', 'value': 'LosAngeles'},
            {'label': 'Denver', 'value': 'Denver'},
            {'label': 'Billings', 'value': 'Billings'},
            {'label': 'Omaha', 'value': 'Omaha'},
            {'label': 'Las Vegas', 'value': 'LasVegas'},
            {'label': 'Manchester', 'value': 'Manchester'},
            {'label': 'Newark', 'value': 'Newark'},
            {'label': 'Albuquerque', 'value': 'Albuquerque'},
            {'label': 'New York', 'value': 'NewYork'},
            {'label': 'Charlotte', 'value': 'Charlotte'},
            {'label': 'Fargo', 'value': 'Fargo'},
            {'label': 'Columbus', 'value': 'Columbus'},
            {'label': 'OklahomaCity', 'value': 'OklahomaCity'},
            {'label': 'Portland', 'value': 'Portland'},
            {'label': 'Philadelphia', 'value': 'Philadelphia'},
            {'label': 'Providence', 'value': 'Providence'},
            {'label': 'Columbia', 'value': 'Columbia'},
            {'label': 'SiouxFalls', 'value': 'SiouxFalls'},
            {'label': 'Memphis', 'value': 'Memphis'},
            {'label': 'Houston', 'value': 'Houston'},
            {'label': 'Salt Lake City', 'value': 'SaltLakeCity'},
            {'label': 'Burlington', 'value': 'Burlington'},
            {'label': 'Virginia Beach', 'value': 'VirginiaBeach'},
            {'label': 'Seattle', 'value': 'Seattle'},
            {'label': 'Charleston', 'value': 'Charleston'},
            {'label': 'Milwaukee', 'value': 'Milwaukee'},
            {'label': 'Cheyenne', 'value': 'Cheyenne'},
            {'label': 'Riverside', 'value': 'Riverside'}
        ],
        multi = False,
        value = 'Phoenix'
    ),
    html.H2('Select Time Range'),
    dcc.RangeSlider(
        id='time-range-slider',
        min=1,
        max=61,
        step=1,
        value=[1, 61],
        updatemode='drag',
        dots=True
    ),
    html.Div(id='output-container-range-slider', style={'margin-top': 20, 'fontSize': 20}),

    html.Div('Please wait a moment to generate graph due to large amounts of data !', style={'margin-top': 20, 'fontSize': 16, 'color':'Red'}),
    
    #bar chart
    dcc.Graph(id='bar_char'),

    html.Br(),
    dcc.Link('Search Content', href='/page-1'),
    html.Br(),
    dcc.Link('Brand Popularity in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('WordCloud Analyze', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    dash.dependencies.Output('bar_char', 'figure'),
    [dash.dependencies.Input('city_dropdown', 'value'),dash.dependencies.Input('time-range-slider', 'value')])
def bar_char(city,timerange):
    brand_list = ['ford','toyota','chevrolet','honda','nissan','jeep','ramtrucks','hyundai','subaru','kia','gmc','dodge','volkswagen','bmw','mercedesbenz']
    city_list = []
    time_result = []
    city_list.append(city.encode('utf-8'))
    for v in timerange:
        if v <= 31:
            time_result.append([10,v])
        else:
            v = v - 31
            time_result.append([11,v])
    select_data = select_from_DB(city_list,time_result[0][0],time_result[0][1],time_result[1][0],time_result[1][1])
    x,y = brand_count(select_data,brand_list)
    y,x = zip(*sorted(zip(y, x), reverse=True))
    return{
        'data': [
            {'x': x, 'y': y, 'type': 'bar'},
        ],
        'layout': {
            'title': 'Popularity',     
        }
    }
##################Page-2#######################

##################Page-3#######################
page_3_layout = html.Div([
    html.H1('Specific Car Brand Popularity in Each State'),
    html.H2('Brands'),
    dcc.Dropdown(
        id='brand_dropdown',
        options=[
            {'label': 'Ford', 'value': 'ford'},
            {'label': 'Toyota', 'value': 'toyota'},
            {'label': 'Chevrolet', 'value': 'chevrolet'},
            {'label': 'Honda', 'value': 'honda'},
            {'label': 'Nissan', 'value': 'nissan'},
            {'label': 'Jeep', 'value': 'jeep'},
            {'label': 'Ram Trucks', 'value': 'ramtrucks'},
            {'label': 'Hyundai', 'value': 'hyundai'},
            {'label': 'Subaru', 'value': 'subaru'},
            {'label': 'Kia', 'value': 'kia'},
            {'label': 'GMC', 'value': 'gmc'},
            {'label': 'Dodge', 'value': 'dodge'},
            {'label': 'Volkswagen', 'value': 'volkswagen'},
            {'label': 'BMW', 'value': 'bmw'},
            {'label': 'Mercedes Benz', 'value': 'mercedesbenz'}
        ],
        value = 'ford'
    ),
    html.H2('Select Time Range'),
    dcc.RangeSlider(
        id='time-range-slider',
        min=1,
        max=61,
        step=1,
        value=[1, 61],
        updatemode='drag',
        dots=True
    ),
    html.Div(id='output-container-range-slider', style={'margin-top': 20, 'fontSize': 20}),

    html.Div('Please wait a moment to generate graph due to large amounts of data !', style={'margin-top': 20, 'fontSize': 16, 'color':'Red'}),

    dcc.Graph(id='hotmap', style={"height": "600px", "width":"1000px"}),

    html.Br(),
    dcc.Link('Search Content', href='/page-1'),
    html.Br(),
    dcc.Link('Car Brand Popularity in the City', href='/page-2'),
    html.Br(),
    dcc.Link('WordCloud Analyze', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('hotmap', 'figure'),
              [dash.dependencies.Input('brand_dropdown', 'value'),dash.dependencies.Input('time-range-slider', 'value')])
def draw_map(brand_list,timerange):

    brand_list = [brand.encode("utf-8") for brand in [brand_list]]

    code = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY'
            ,'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ'
            ,'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA'
            ,'VT','WA','WI','WV','WY']

    city_code = ['AL','AK','AZ','CA','CO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','IN','SD','TN','TX','UT','NJ','VA','WA','SC','WI','WY',]

    time_result = []
    for v in timerange:
        if v <= 31:
            time_result.append([10,v])
        else:
            v = v - 31
            time_result.append([11,v])

    value = generate_hotmap_data(brand_list,time_result[0][0],time_result[0][1],time_result[1][0],time_result[1][1])

    fig = go.Figure( data = go.Choropleth(
        locations = city_code,
        z=value,
        locationmode='USA-states',
        colorscale = 'Reds',
        autocolorscale=False,
        marker_line_color='White', # line markers between states
        #marker_line_width=1,
        colorbar = go.choropleth.ColorBar(
        title = str(brand_list[0])),
        geo = 'geo2'
        ), 

        layout =go.Layout(
        geo2 = dict(
        scope='usa',
        showframe=False,
        showland=True,
        showcountries=False,       
        bgcolor='rgba(235, 50, 255, 0.0)',),
        showlegend=True,
        font=dict(
        size=20
        )
        )
    )
    
    fig.add_trace(go.Scattergeo(
        locations = code,
        text = code,
        mode = 'text',

        textfont=dict(
        family="sans serif",
        size=12,
        color="crimson"
        ),
        
        locationmode='USA-states',
        showlegend = False,
        geo = 'geo2'
        )
    )

    return fig

##################Page-3#######################

##################Page-4#######################
page_4_layout = html.Div([
    html.H1('WordCloud Analyze'),
    html.H2('Brands'),
    dcc.Checklist(
        id='brand_checklist',
        options=[
            {'label': 'Ford', 'value': 'ford'},
            {'label': 'Toyota', 'value': 'toyota'},
            {'label': 'Chevrolet', 'value': 'chevrolet'},
            {'label': 'Honda', 'value': 'honda'},
            {'label': 'Nissan', 'value': 'nissan'},
            {'label': 'Jeep', 'value': 'jeep'},
            {'label': 'Ram Trucks', 'value': 'ramtrucks'},
            {'label': 'Hyundai', 'value': 'hyundai'},
            {'label': 'Subaru', 'value': 'subaru'},
            {'label': 'Kia', 'value': 'kia'},
            {'label': 'GMC', 'value': 'gmc'},
            {'label': 'Dodge', 'value': 'dodge'},
            {'label': 'Volkswagen', 'value': 'volkswagen'},
            {'label': 'BMW', 'value': 'bmw'},
            {'label': 'Mercedes Benz', 'value': 'mercedesbenz'}
        ],
        value = ['ford'],
        labelStyle={'display': 'inline-block'}
    ),
    html.H2('City'),
    dcc.Dropdown(
        id='city_dropdown',
        options=[
            {'label': 'Birmingham', 'value': 'Birmingham'},
            {'label': 'Anchorage', 'value': 'Anchorage'},
            {'label': 'Phoenix', 'value': 'Phoenix'},
            {'label': 'Little Rock', 'value': 'LittleRock'},
            {'label': 'Los Angeles', 'value': 'LosAngeles'},
            {'label': 'Denver', 'value': 'Denver'},
            {'label': 'Billings', 'value': 'Billings'},
            {'label': 'Omaha', 'value': 'Omaha'},
            {'label': 'Las Vegas', 'value': 'LasVegas'},
            {'label': 'Manchester', 'value': 'Manchester'},
            {'label': 'Newark', 'value': 'Newark'},
            {'label': 'Albuquerque', 'value': 'Albuquerque'},
            {'label': 'New York', 'value': 'NewYork'},
            {'label': 'Charlotte', 'value': 'Charlotte'},
            {'label': 'Fargo', 'value': 'Fargo'},
            {'label': 'Columbus', 'value': 'Columbus'},
            {'label': 'OklahomaCity', 'value': 'OklahomaCity'},
            {'label': 'Portland', 'value': 'Portland'},
            {'label': 'Philadelphia', 'value': 'Philadelphia'},
            {'label': 'Providence', 'value': 'Providence'},
            {'label': 'Columbia', 'value': 'Columbia'},
            {'label': 'SiouxFalls', 'value': 'SiouxFalls'},
            {'label': 'Memphis', 'value': 'Memphis'},
            {'label': 'Houston', 'value': 'Houston'},
            {'label': 'Salt Lake City', 'value': 'SaltLakeCity'},
            {'label': 'Burlington', 'value': 'Burlington'},
            {'label': 'Virginia Beach', 'value': 'VirginiaBeach'},
            {'label': 'Seattle', 'value': 'Seattle'},
            {'label': 'Charleston', 'value': 'Charleston'},
            {'label': 'Milwaukee', 'value': 'Milwaukee'},
            {'label': 'Cheyenne', 'value': 'Cheyenne'},
            {'label': 'Riverside', 'value': 'Riverside'}
        ],
        multi = True,
        value = ['Phoenix']
    ),
    html.H2('Select Time Range'),
    dcc.RangeSlider(
        id='time-range-slider',
        min=1,
        max=61,
        step=1,
        value=[1, 61],
        updatemode='drag',
        dots=True
    ),
    html.H2('N-grams'),
    dcc.Dropdown(
        id='ngram',
        options=[
            {'label': 'Uni-gram', 'value': '1'},
            {'label': 'Bi-grams', 'value': '2'},
            {'label': 'Tri-grams', 'value': '3'}
        ],
        multi = False,
        value = 'unigram'
    ),
    html.Div(id='output-container-range-slider', style={'margin-top': 20, 'fontSize': 20}),

    html.Div('Please wait a moment to generate graph due to large amounts of data !', style={'margin-top': 20, 'fontSize': 16, 'color':'Red'}),

    # Word freq
    dcc.Graph(id='word_freq_bar_char'),

    html.Br(),
    dcc.Link('Search Content', href='/page-1'),
    html.Br(),
    dcc.Link('Car Brand Popularity in the City', href='/page-2'),
    html.Br(),
    dcc.Link('Brand Popularity in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(
    dash.dependencies.Output('word_freq_bar_char', 'figure'),
    [dash.dependencies.Input('brand_checklist', 'value'),dash.dependencies.Input('city_dropdown', 'value'),dash.dependencies.Input('time-range-slider', 'value'),dash.dependencies.Input('ngram', 'value')])
def update_wordfreq(brand_list,city_list,timerange,ngram):
    brand_list = [brand.encode("utf-8") for brand in brand_list]
    city_list = [city.encode("utf-8") for city in city_list]
    time_result = []
    for v in timerange:
        if v <= 31:
            time_result.append([10,v])
        else:
            v = v - 31
            time_result.append([11,v])
    select_data = select_from_DB(city_list,time_result[0][0],time_result[0][1],time_result[1][0],time_result[1][1])
    select_data = select_from_content(select_data,brand_list)
    dd = data_preprocess(select_data)
    if ngram == '2':
        dd = generate_ngrams(dd, 2)
    if ngram == '3':
        dd = generate_ngrams(dd, 3)

    if len(dd) >=1:
        # plot word cloud in images
        wordcloud_generator(dd)
        
        word_list,freq_list = word_freq(dd)
        #cut_point = int(round(len(word_list)*0.05))
        cut_point = 10
        word_list = word_list[:cut_point]
        freq_list = freq_list[:cut_point]
        return{
            'data': [
                {'x': freq_list[::-1], 'y': word_list[::-1], 'type': 'bar', 'orientation':'h'},
            ],
            'layout': {
                'title': 'Top 10 of the Word Freqeuncy  ',     
            }
        }

    else:
        return{}
##################Page-4#######################

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True)