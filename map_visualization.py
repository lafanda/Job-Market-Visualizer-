import pandas as pd
import plotly.express as px
import json
from stateAbriviation import state_abbreviations

# Load the data from the JSON file
with open("USA.json") as f:
    data = json.load(f)

with open('cities_to_map.json') as f:
    cities_to_map = json.load(f)

df = pd.DataFrame(data)

df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

cities_df = pd.DataFrame(cities_to_map)
cities_df['State'] = cities_df['State'].map(state_abbreviations)
filtered_df = df[df[['City', 'State']].apply(tuple, axis=1).isin(cities_df.apply(tuple, axis=1))]

# Create the map
fig = px.scatter_mapbox(
    filtered_df,
    lat='Latitude',
    lon='Longitude',
    hover_name='City',
    zoom=3,
    height=1000,
    title='Job Sectors in North America',
    mapbox_style='carto-darkmatter',  # Dark map style
    opacity=1  # Set marker opacity
)

# Set map background to black
fig.update_layout(
    plot_bgcolor='#262626',  # Set the plot background color to black
    paper_bgcolor='#262626',  # Set the paper background color to black
)

# Save the map to an HTML file
fig.write_html('job_map.html')

print("Map has been created and saved as 'job_map.html'.")