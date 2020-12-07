from config import host, database, user, password
from sqlalchemy import create_engine
import geoalchemy2
import geopandas as gpd

'''
Basic script to read in geometry data from postgres as geopandas geodataframe
'''

# create sqlalchemy engine to connect to db, note you will need to enter personal credentials in config.py
conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str, echo=True)
connection = engine.connect()

# enter SQL query, ensure geometry column is included in query
sql = """SELECT site_summary."UID", geometry FROM site_summary"""

# read as geodataframe using geopandas library
gdf = gpd.read_postgis(sql, connection, geom_col='geometry', crs='EPSG:27700')

# remove empty geometries to avoid key error
gdf = gdf[~gdf.geometry.is_empty]

# test plot of spatial data
gdf.plot(color="blue", figsize=(15, 15))
