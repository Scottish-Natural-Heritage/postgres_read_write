from config import host, database, user, password
from sqlalchemy import create_engine
import geoalchemy2
import pandas as pd
import geopandas as gpd
import osgb
import re
import numpy as np

"""
Outline script to add geometry column to dataframe from grid reference values,
convert to geodataframe and publish to postgres database.
"""

# create sqlalchemy engine to connect to db, note you will need to enter credentials in config.py
# With setting Echo=True, engine will log every query
conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str, echo=True)
connection = engine.connect()

# read in dataframe to be uploaded as pandas dataframe, no dtypes declared
df = pd.read_csv("sitesummary.csv", encoding='cp1252')

# drop 'Unnamed' columns and set column names to lower case for usability in postgres
df = df.drop([i for i in df.columns if 'Unnamed' in i], axis=1)
df = df.rename(columns=str.lower)
df.columns = df.columns.str.replace(' ', '_')

# convert gridref column to string, remove white space
df = df[~df['grid_reference'].isnull()]
df = df[~df['uid'].isnull()]
df = df.astype({'grid_reference': 'string'})
df['grid_reference'] = df['grid_reference'].str.replace(' ', '')

# use parse_grid to convert osgr to easting/northing, null for values that don't match regex
df['easting'] = df['grid_reference'].apply(lambda x: osgb.parse_grid(x)[0] if re.match(r'[a-zA-Z]{2}\d{6,10}', str(x)) is not None else np.nan)
df['northing'] = df['grid_reference'].apply(lambda x: osgb.parse_grid(x)[1] if re.match(r'[a-zA-Z]{2}\d{6,10}', str(x)) is not None else np.nan)

# convert dataframe to geodataframe with geom column
gdf = gpd.GeoDataFrame(df, geometry= gpd.points_from_xy(df.easting, df.northing), crs='EPSG:27700')
gdf = gdf[~gdf.geometry.is_empty]

# export to database using gpd.to_postgis, note this will drop existing table and replace
gdf.to_postgis(name='site_summary', schema='public', con=engine, if_exists='replace')
