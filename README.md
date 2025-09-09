# exactextract Bug Reproduction

This directory contains a minimal reproduction case for a bug in the `exactextract` library where the "raster-sequential" strategy produces null/zero results while "feature-sequential" strategy works correctly.

## Bug Description

In specific cases (conditions currently unknown), the `exactextract.exact_extract()` function with `strategy="raster-sequential"` returns:
- `null` values for mean and standard deviation statistics
- `0.0` values for sum statistics

The same operation with `strategy="feature-sequential"` returns correct non-null values. This is problematic because:
1. Both strategies should produce identical results
2. "raster-sequential" is preferred for efficiency with large chunk-wise dataset processing
3. The failure appears to be silent (no errors/warnings)

## Files

### Input Data
- `biodiversity_Polygon_86681e4dfffffff.geojson` - Vector polygons (3 features) for zonal statistics
- `biodiversity_Polygon_86681e4dfffffff.tif` - Multi-band raster with biodiversity metrics

### Script
- `main.py` - Bug reproduction script that runs both strategies and saves outputs

### Output Data (Generated)
- `biodiversity_86681e4dfffffff_outputs_feature_sequential.geojson` - Correct results with valid statistics
- `biodiversity_86681e4dfffffff_outputs_raster_sequential.geojson` - Buggy results with null/zero values

## Requirements

The script uses [uv](https://docs.astral.sh/uv/) with inline dependency specification (PEP 723). Required packages:
- exactextract
- rioxarray  
- xarray
- geopandas
- rasterio

## Usage

### Install uv (if not already installed)
```bash
pip install uv
```

### Run the reproduction script
```bash
uv run main.py
```

This will:
1. Load the input raster and vector data
2. Run `exactextract.exact_extract()` with both strategies
3. Save results to GeoJSON files for comparison

## Expected vs Actual Results

### Expected Behavior
Both strategies should produce identical statistical results like:
```json
{
  "diversity_score_mean": 0.042889822550238252,
  "chm_m_mean_2017_mean": 12.345276151534765,
  "diversity_score_sum": 4.0828066916384316,
  "diversity_score_stdev": 0.020008660946385613
}
```

### Actual Bug Behavior  
The "raster-sequential" strategy produces:
```json
{
  "diversity_score_mean": null,
  "chm_m_mean_2017_mean": null,
  "diversity_score_sum": 0.0,
  "diversity_score_stdev": null
}
```

## Investigation Notes

- The bug appears to be specific to certain raster/vector combinations
- No errors or warnings are raised during execution
- All sum statistics return 0.0 while mean/stdev return null
- The same geometries are present in both outputs (only statistics differ)

## Environment

This reproduction was tested on:
- Python with the dependencies listed in `main.py`
- Input data: Multi-band GeoTIFF with 22 bands covering biodiversity metrics
- Vector data: 3 polygon features in WGS84 (EPSG:4326)