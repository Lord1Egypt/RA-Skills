---
name: worldclim-extract
description: Extract bioclimatic variables (BIO1-BIO19) from WorldClim GeoTIFF rasters using sample coordinates (longitude/latitude). Supports automatic download of WorldClim 2.1 data, batch extraction from Excel/CSV, and output to Excel or CSV. Use when matching geographic sample points to climate data like annual temperature or precipitation.
metadata:
  {"openclaw": {"requires": {"bins": ["python3"]}, "emoji": "🌍"}}
---

## Version Compatibility

Reference examples tested with: Python 3.10+, rasterio 1.4+, pandas 2.0+

Before using code patterns, verify installed versions match. If versions differ:
- `pip show rasterio pandas openpyxl`

If code throws ImportError, install missing packages:
```bash
pip install rasterio pandas openpyxl
```

## Overview

WorldClim provides global climate data as GeoTIFF raster files. Each `.tif` file is a grid covering the entire Earth, where each grid cell stores a climate value (e.g., temperature in °C or precipitation in mm). This skill automates the process of extracting climate values for specific geographic coordinates.

### How It Works

1. **Input**: Excel or CSV file containing sample coordinates (longitude, latitude)
2. **Data**: WorldClim 2.1 bioclimatic GeoTIFF files (19 BIO variables, 1970-2000 average)
3. **Process**: For each coordinate, find the corresponding grid cell and read its value
4. **Output**: Original data plus extracted climate columns appended

### Grid Resolution

| Resolution | Cell Size | Approx. Area | File Size |
|------------|-----------|--------------|-----------|
| `10m` | 0.167° | ~18.5 km² | ~48 MB zip |
| `5m` | 0.083° | ~9.3 km² | ~170 MB zip |
| `2.5m` | 0.042° | ~4.6 km² | ~650 MB zip |

**Default**: `10m` — sufficient for most ecological/population genetics studies.

## Quick Start

### Using the CLI Script

A reusable Python script is provided at `{baseDir}/extract_worldclim.py`:

```bash
# Extract BIO1 (annual mean temp) and BIO12 (annual precipitation) — default
python3 {baseDir}/extract_worldclim.py \
  -i samples.xlsx \
  -o samples_with_climate.xlsx

# Extract all 19 bioclimatic variables
python3 {baseDir}/extract_worldclim.py \
  -i samples.xlsx \
  -o samples_all_bio.xlsx \
  --bios 1-19

# Extract specific variables with custom column names
python3 {baseDir}/extract_worldclim.py \
  -i coords.csv \
  -o result.xlsx \
  --bios 1,5,6,12,13 \
  --res 2.5m \
  --lon longitude \
  --lat latitude
```

### Using Python Directly

For custom integration or programmatic use:

```python
import pandas as pd
import rasterio

def extract_bio(tif_path, lon, lat):
    """Extract a single value from a GeoTIFF at given coordinates."""
    with rasterio.open(tif_path) as src:
        value = next(src.sample([(lon, lat)]))[0]
    return value

# Read sample coordinates
df = pd.read_excel("samples.xlsx")
coords = list(zip(df["经度"], df["纬度"]))

# Extract BIO1 (Annual Mean Temperature)
with rasterio.open("wc2.1_10m_bio_1.tif") as src:
    df["年均温度_C"] = [v[0] for v in src.sample(coords)]

# Extract BIO12 (Annual Precipitation)
with rasterio.open("wc2.1_10m_bio_12.tif") as src:
    df["年降水量_mm"] = [v[0] for v in src.sample(coords)]

df.to_excel("samples_with_climate.xlsx", index=False)
```

## WorldClim Data Download

### Automatic (script handles it)

The CLI script auto-downloads data on first run to the `--cache` directory (default: `./worldclim_data`).

### Manual Download

If automatic download fails (e.g., network issues):

```bash
# 10m resolution (~48 MB)
curl -O https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_10m_bio.zip
unzip wc2.1_10m_bio.zip -d ./worldclim_data/

# 2.5m resolution (~650 MB)
curl -O https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_2.5m_bio.zip
unzip wc2.1_2.5m_bio.zip -d ./worldclim_data/
```

## BIO Variable Reference

| BIO | Name | Unit | Description |
|-----|------|------|-------------|
| BIO1 | Annual Mean Temperature | °C | 年均温度 |
| BIO2 | Mean Diurnal Range | °C | 昼夜温差月均值 |
| BIO3 | Isothermality | % | 等温性 (BIO2/BIO7 × 100) |
| BIO4 | Temperature Seasonality | SD × 100 | 温度季节性 |
| BIO5 | Max Temp of Warmest Month | °C | 最暖月最高温 |
| BIO6 | Min Temp of Coldest Month | °C | 最冷月最低温 |
| BIO7 | Temperature Annual Range | °C | 年温度范围 (BIO5−BIO6) |
| BIO8 | Mean Temp of Wettest Quarter | °C | 最湿季均温 |
| BIO9 | Mean Temp of Driest Quarter | °C | 最干季均温 |
| BIO10 | Mean Temp of Warmest Quarter | °C | 最暖季均温 |
| BIO11 | Mean Temp of Coldest Quarter | °C | 最冷季均温 |
| BIO12 | Annual Precipitation | mm | 年降水量 |
| BIO13 | Precipitation of Wettest Month | mm | 最湿月降水量 |
| BIO14 | Precipitation of Driest Month | mm | 最干月降水量 |
| BIO15 | Precipitation Seasonality | CV | 降水季节性 |
| BIO16 | Precipitation of Wettest Quarter | mm | 最湿季降水量 |
| BIO17 | Precipitation of Driest Quarter | mm | 最干季降水量 |
| BIO18 | Precipitation of Warmest Quarter | mm | 最暖季降水量 |
| BIO19 | Precipitation of Coldest Quarter | mm | 最冷季降水量 |

**Data Source**: WorldClim 2.1 (1970-2000, 30-year average)

## Input Format Requirements

### Required Columns

- **Longitude column**: Decimal degrees, range [-180, 180]. Default column name: `经度` (override with `--lon`)
- **Latitude column**: Decimal degrees, range [-90, 90]. Default column name: `纬度` (override with `--lat`)

### Supported Input Formats

- `.xlsx` — Excel workbook (recommended, handles Chinese headers well)
- `.csv` — Comma-separated values

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Coordinates read as text | Hidden special characters (e.g., `\xa0` non-breaking space) | Script auto-cleans with `pd.to_numeric(errors='coerce')`; check for NA after conversion |
| Negative longitudes rejected | Using East/West format instead of decimal | Convert to decimal: 东经 117° → 117.0; 西经 117° → -117.0 |
| Missing extracted values | Coordinate falls in ocean or outside raster bounds | Check coordinate validity; WorldClim covers land globally |

## Output Format

The output file contains **all original columns** plus extracted BIO columns:

```
名称    经度        纬度        年均温度_C    年降水量_mm
NFAL10  117.214052  31.270421   16.15        1325.0
NFBJ1   116.591445  40.032115   11.88        542.0
```

## Using R (terra) for Cross-Validation

If you need to validate results with R:

```r
library(terra)

# Read raster stack
bio <- rast(list.files("./worldclim_data", pattern = "\\.tif$", full.names = TRUE))

# Read and clean coordinates
pts <- readxl::read_excel("samples.xlsx")
pts$经度 <- as.numeric(gsub("\\s+", "", pts$经度))  # Remove hidden spaces
pts$纬度 <- as.numeric(pts$纬度)
pts <- pts[!is.na(pts$经度) & !is.na(pts$纬度), ]

# Extract
v <- vect(pts, geom = c("经度", "纬度"), crs = "EPSG:4326")
result <- extract(bio, v)
write.csv(cbind(pts, result[, -1]), "output.csv", row.names = FALSE)
```

**Note**: R's `as.numeric()` is stricter than Python's pandas and may fail on hidden whitespace. Always clean coordinates before conversion.

## Decision Tree

```
Need to extract climate data for sample coordinates?
├── Have coordinates in Excel/CSV?
│   └── Use the CLI script: python3 extract_worldclim.py -i input.xlsx -o output.xlsx
├── Need only temperature and precipitation?
│   └── Default: --bios 1,12 (no need to specify)
├── Need all 19 bioclimatic variables?
│   └── Use: --bios 1-19
├── Need higher spatial resolution?
│   ├── ~9 km cells → --res 5m
│   └── ~4.6 km cells → --res 2.5m
└── Need to integrate into a Python pipeline?
    └── Use the direct Python code pattern with rasterio.sample()
```

## Related Skills

- bio-geo-data — For general geospatial data operations
- bio-read-sequences — For biological sequence file parsing
- bio-batch-processing — For processing multiple files in batch
