import pandas as pd
import plotly.express as px
import json
from stateAbriviation import abbreviation_to_full  # Import both mappings

# Load the larger data file
with open('Data.json') as f:
    data = json.load(f)

# Load the cities and states to map file
with open('cities_to_map.json') as f:
    cities_to_map = json.load(f)

df = pd.DataFrame(data)

# Convert Latitude and Longitude to float
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# Create a DataFrame from the cities to map list
cities_df = pd.DataFrame(cities_to_map)

# Convert the state abbreviations in cities_df to full names
cities_df['State'] = cities_df['State'].map(abbreviation_to_full)

# Print cities_df to verify conversion
print(cities_df)

# Merge the filtered DataFrame with the cities DataFrame to include Jobs
filtered_df = df[df[['City', 'State']].apply(tuple, axis=1).isin(cities_df[['City', 'State']].apply(tuple, axis=1))]

# Merge filtered_df with cities_df to bring in the Jobs data
merged_df = pd.merge(filtered_df, cities_df[['City', 'State', 'Jobs']], on=['City', 'State'], how='inner')

# Check the merged DataFrame
print(merged_df)

# Create the map using the filtered DataFrame
fig = px.scatter_geo(
    merged_df,
    lat='Latitude',
    lon='Longitude',
    size='Jobs',  # Use the Jobs column for the size of the dots
    size_max=10,  # Set the maximum size of the dots
    opacity=0.5,
    color='Jobs',  # Use the Jobs column for the color of the dots
    scope='north america',  # Limit the map to North America
    title='Jobs by City in North America',
    hover_data={'City': True, 'State': True, 'Jobs': True, 'Longitude': False,'Latitude': False}  # Include City, State, and Jobs in the hover data
)


fig.update_layout(
    width=1200,  # Set width in pixels
    height=1000,  # Set height in pixels
)

fig.update_geos(
    landcolor='black',  # Change to your preferred color
    countrycolor='gray',      # Optional: change the color of country borders
    bgcolor='gray',
    coastlinecolor='gray',    # Optional: change the color of coastline borders
    lakecolor='gray',        # Optional: change the color of lakes
    oceancolor='gray',       # Optional: change the color of oceans
)

fig.write_html('jobMap.html')

print("Map has been created and saved as 'filtered_job_map.html'.")
