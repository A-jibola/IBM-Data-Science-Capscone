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
launch_sites = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites = launch_sites[['Launch Site']]
siteOptions = [{'label': s['Launch Site'], 'value':s['Launch Site']} for i, s in launch_sites.iterrows()]
siteOptions.append({'label': 'All Sites', 'value': 'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=siteOptions, value='ALL', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=100, marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500'}, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        sum_site = spacex_df.groupby(['Launch Site'], as_index=False).sum()
        sum_site = sum_site[['Launch Site', 'class']]
        fig = px.pie(sum_site, values='class', names='Launch Site', title='Ratio of Successes')
        return fig
    else:
        sum_site = spacex_df[spacex_df['Launch Site']== entered_site]
        sum_site = sum_site.groupby(['class'], as_index=False).count()
        sum_site['Status'] = ['Failure', 'Success']
        fig = px.pie(sum_site, values='Launch Site', names='Status', title='Ratio of Successes to Failures')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(sitename, payload):
    if sitename == 'ALL':
        site_df = spacex_df[(spacex_df['Payload Mass (kg)']>= payload[0]) & (spacex_df['Payload Mass (kg)']<= payload[1])]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site']== sitename] 
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
