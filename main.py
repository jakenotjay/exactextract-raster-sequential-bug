# /// script
# dependencies = [
#   "exactextract",
#   "rioxarray",
#   "xarray",
#   "geopandas",
#   "rasterio",
# ]
# ///

import exactextract
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
import rasterio

gdf = gpd.read_file("./biodiversity_Polygon_86681e4dfffffff.geojson")

with rasterio.open("./biodiversity_Polygon_86681e4dfffffff.tif") as src:
    descriptions = src.descriptions

statistic_stack_masked_read = rxr.open_rasterio(
    "./biodiversity_Polygon_86681e4dfffffff.tif",
    masked=True,
    band_as_variable=True,
    parse_coordinates=True,
)
print(statistic_stack_masked_read)

# rename the bands to the descriptions
statistic_stack_masked_read = statistic_stack_masked_read.rename({band: description for band, description in zip(statistic_stack_masked_read.keys(), descriptions)})

feature_source = exactextract.feature.GeoPandasFeatureSource(gdf)

ops = ["mean", "sum", "stdev"]

results_feature_sequential = exactextract.exact_extract(
    statistic_stack_masked_read,
    feature_source,
    ops=ops,
    strategy="feature-sequential",
    include_geom=True,
    output="pandas"
)

results_raster_sequential = exactextract.exact_extract(
    statistic_stack_masked_read,
    feature_source,
    ops=ops,
    strategy="raster-sequential",
    include_geom=True,
    output="pandas"
)

results_feature_sequential.to_file(f"./biodiversity_86681e4dfffffff_outputs_feature_sequential.geojson", driver="GeoJSON")
results_raster_sequential.to_file(f"./biodiversity_86681e4dfffffff_outputs_raster_sequential.geojson", driver="GeoJSON")