import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from stateAbriviation import abbreviation_to_full  # Ensure this module is available

# Load and prepare the data
with open('Data.json') as f:
    data = json.load(f)

with open('cities_to_map.json') as f:
    cities_to_map = json.load(f)

df = pd.DataFrame(data)
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

cities_df = pd.DataFrame(cities_to_map)
cities_df['State'] = cities_df['State'].map(abbreviation_to_full)

city_jobs = cities_df.groupby(['City', 'State'])['Job'].agg(list).reset_index()
job_counts = cities_df.groupby(['City', 'State']).size().reset_index(name='JobCount')

merged_df = pd.merge(df, job_counts, on=['City', 'State'], how='inner')
merged_df = pd.merge(merged_df, city_jobs, on=['City', 'State'], how='inner')

# Setup the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='search-input',
        type='text',
        placeholder='Enter a job keyword...',
        style={'width': '50%', 'padding': '10px'}  # Adjust width percentage as needed
    ),
    dcc.Graph(
        id='job-map',
        config={'displayModeBar': False}
    )
], style={'width': '80%', 'margin': 'auto'})


@app.callback(
    Output('job-map', 'figure'),
    Input('search-input', 'value')
)
def update_map(search_value):
    # Create a copy of the dataframe to modify
    dynamic_df = merged_df.copy()

    # Apply filter based on the search input
    if search_value:
        # Lowercase the search value for case insensitive matching
        search_value = search_value.lower()
        # Filter and count jobs dynamically based on the input
        dynamic_df['JobCount'] = dynamic_df['Job'].apply(
            lambda jobs: sum(search_value in job.lower() for job in jobs)
        )
        # Keep only rows where JobCount is greater than 0
        dynamic_df = dynamic_df[dynamic_df['JobCount'] > 0]
    else:
        # Calculate JobCount as the length of the Job list if no search query
        dynamic_df['JobCount'] = dynamic_df['Job'].apply(len)

    # Generate the map figure
    fig = px.scatter_geo(
        dynamic_df,
        lat='Latitude',
        lon='Longitude',
        size='JobCount',
        size_max=10,
        opacity=0.5,
        color='JobCount',
        scope='north america',
        hover_data={'City': True, 'State': True, 'Job': True, 'JobCount': True, 'Longitude': False, 'Latitude': False}
    )
    fig.update_geos(
        landcolor='black',
        countrycolor='gray',
        bgcolor='gray',
        coastlinecolor='gray',
        lakecolor='gray',
        oceancolor='gray',
        fitbounds="locations"
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        width=1300,
        height=600
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)