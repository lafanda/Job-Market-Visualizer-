import pandas as pd
import plotly.express as px

# Sample Data with Coordinates
data = {
    'City': ['New York', 'Toronto', 'Mexico City'],
    'Jobs': [1000, 50, 75],
    'Latitude': [40.7128, 43.7, 19.4326],
    'Longitude': [-74.0060, -79.42, -99.1332],
}
df = pd.DataFrame(data)

# Create Scatter Geo Map
fig = px.scatter_geo(
    df,
    lat='Latitude',
    lon='Longitude',
    color='Jobs',
    size='Jobs',
    opacity=0.5,
    scope='north america',  # Limit the map to North America
    title='Jobs by City in North America',
)



fig.update_geos(
    landcolor='black',  # Change to your preferred color
    countrycolor='gray',      # Optional: change the color of country borders
    bgcolor='gray',
    coastlinecolor='gray',    # Optional: change the color of coastline borders
    lakecolor='gray',        # Optional: change the color of lakes
    oceancolor='gray',       # Optional: change the color of oceans
)

fig.show()
