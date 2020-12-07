# postgres_read_write
Read/write spatial data to/from postgres database using python. Utilises pandas, geopandas, geoalchemy2 and sqlalchemy libraries.

## Motivation
Following the creation of a Peatland ACTION spatial database, there is a need to add existing project data, much of which is contained in spreadsheets. This project includes a simple framework to utilise the commonly used pandas and geopandas libraries to read/write from/to spatially enabled (PostGIS) PostgreSQL database.

## Requirements
The following libraries are required:
* Geopandads 0.8.0+
* Geoalchemy2
* sqlalchemy
Additional task specific libraries include:
* osgb

## Example code
Create connection engine using<br />
```
conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str, echo=True)]
connection = engine.connect()
```

Using this engine you can then use geopandas to read:
```
gdf = gpd.read_postgis(sql, connection, geom_col='geometry', crs='EPSG:27700')
```
and write:
```
gdf.to_postgis(name='test_table', schema='public', con=engine, if_exists:'replace')
```
to postgres database.
