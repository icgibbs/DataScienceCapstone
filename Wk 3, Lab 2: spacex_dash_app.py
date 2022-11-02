# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#not here originally - get unique list of Launch Sites
LaunchSites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                #dcc.Dropdown(id='site-dropdown', [LaunchSites])
                                dcc.Dropdown(id='site-dropdown',
                                    options = [
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site or All Launch Sites',
                                    searchable=True),
                                html.Br(),
                                html.Div(id='TestMessage'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                #new dropdown for new pie to show success of booster version category
                                dcc.Dropdown(id='boostercategory-dropdown',
                                    options = [
                                        {'label': 'All Version Categories', 'value': 'ALL'},
                                        {'label': 'B4', 'value': 'B4'},
                                        {'label': 'B5', 'value': 'B5'},
                                        {'label': 'FT', 'value': 'FT'},
                                        {'label': 'v1.0', 'value':'v1.0'},
                                        {'label': 'v1.1', 'value': 'v1.1'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a booster version category',
                                    searchable=True),
                                html.Br(),
                                html.Div(dcc.Graph(id='booster_version_pie')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step = 1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(
    Output(component_id='TestMessage', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_testmessage(value):
    return 'Output: {}'.format(value)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df


    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names = 'Launch Site',
        title = 'Of all the successful launches, how many were at each site?')
        return fig
    else:
        FilteredLaunchDF = spacex_df[spacex_df['Launch Site'] == entered_site]
        singlesitegroup_df = FilteredLaunchDF.groupby(['Launch Site', 'class']).size().reset_index(name = 'qty')

        fig = px.pie(singlesitegroup_df, values='qty', names='class', title=f"Total success launches for site {entered_site}")

        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value'),
            Input(component_id='boostercategory-dropdown', component_property='value'))

def get_scatter(entered_site, entered_range, entered_booster):
    scattered_df = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_range[0]]
    scattered_df = scattered_df[scattered_df['Payload Mass (kg)'] <= entered_range[1]]

    if entered_booster == 'ALL':
        scattered_df = scattered_df #essentially, don't modify the dataset
    else:
        scattered_df = scattered_df[scattered_df['Booster Version Category'] == entered_booster]



    if entered_site == 'ALL':
        fig = px.scatter(scattered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        singlesitescatter_df = scattered_df[scattered_df['Launch Site'] == entered_site]
        fig = px.scatter(singlesitescatter_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig



# New pie - for showing success by Booster Version Category
@app.callback(
    Output(component_id='booster_version_pie', component_property='figure'),
    Input(component_id='boostercategory-dropdown', component_property='value'))

def get_booster_pie(entered_category):
    booster_df = spacex_df


    if entered_category == 'ALL':
        fig = px.pie(booster_df, values='class',
        names = 'Booster Version Category',
        title = 'Of all the successful launches, how many were with each booster version category?')
        return fig
    else:
        FilteredLaunchPieDF = spacex_df[spacex_df['Booster Version Category'] == entered_category]
        singlecategorygroup_df = FilteredLaunchPieDF.groupby(['Booster Version Category', 'class']).size().reset_index(name = 'qty')

        fig = px.pie(singlecategorygroup_df, values='qty', names='class', title=f"Total success launches for site {entered_category}")

        return fig




# Run the app
if __name__ == '__main__':
    app.run_server()

"""
Which site has the largest succesfful launches?  (I assume this means "most succesfful launches")
    Pie chart for "all sites" shows KSC LC-39A as having the largest slice of the pie (41.7%), but that's really showing us 
    "of all the successful launches, which site had the highest % of success.  It may be that KSC LC-39A has
    the biggst slice of pie here because it also had the most launches.

    If the question means to ask "which site has the hgihest % success rate", then looking through each of the individual
    sites one by one reveals that KSC LC-39A has the highest success rate at 76.9%

Which site has the highest launch success rate?
    See above

Which payload ranges(s) has the highest launch success rate?
    Not sure how granular "range" should be here.  There were 7 successful launches and 3 failures in the 3000 - 4000 range (70% success)

Which payload range(s) has the lowest launch success rate?
    There were 4 failures and 0 successes in the 6000 - 7000 range (0% success)

Which F9 Booster version has the highest launch success rate?
    Created new pie chart to determine
    66.7% of the successful launches used the "FT" boosters
    But ... 100% of the launches with "B5" boosters were successful.
    However, there was only 1 launch with the B5 booster, so might have just been "luck"
    Of the booster categories that had been used in multiple launches, "FT" is the most successful at 66.7% - I'd try to use that one if I could

So ... I'd rather be in charge of launching a 3000 - 4000 kg payload from the KSC LC-39A site using FT boosters if I had a choice.
(There are two such launches already, and both = success.)

"""

