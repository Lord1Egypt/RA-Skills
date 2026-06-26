---
name: City of Toronto Open Data
description: "Access 537+ datasets from the City of Toronto open data portal. Search, fetch, and analyze city data on transit, traffic, housing, environment, and more via the CKAN API."
permissions: Bash
triggers:
  - toronto open data
  - city of toronto data
  - toronto dataset
  - open.toronto.ca
  - toronto transit
  - toronto housing
---

# City of Toronto Open Data

Access and analyze 537+ open datasets from the City of Toronto via the CKAN API. Data covers transit, traffic, housing, environment, budget, community services, and more.

**Portal:** https://open.toronto.ca
**Platform:** CKAN
**API:** https://ckan0.cf.opendata.inter.prod-toronto.ca

## Quick Start

```bash
# Search for datasets
python3 scripts/toronto_data.py search "traffic"

# List all datasets
python3 scripts/toronto_data.py list

# View dataset info
python3 scripts/toronto_data.py info 311-service-request-codes

# Fetch data from CKAN datastore
python3 scripts/toronto_data.py fetch traffic-volumes-at-intersections-for-all-modes --limit 5

# Fetch with filters
python3 scripts/toronto_data.py fetch traffic-volumes-at-intersections-for-all-modes --where "total_vehicle > 20000" --limit 10

# Export as CSV
python3 scripts/toronto_data.py fetch traffic-volumes-at-intersections-for-all-modes --limit 100 --csv > traffic.csv

# List datastore-enabled datasets
python3 scripts/toronto_data.py searchable
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword |
| `list` | List all datasets |
| `info <dataset-id>` | Show dataset metadata and resources |
| `fetch <dataset-id>` | Fetch data from datastore (opts: `--limit`, `--where`, `--select`, `--csv`) |
| `searchable` | List datasets with queryable datastore resources |

## Query Parameters

- `--limit N` — Max rows to return (default: 10)
- `--where "condition"` — SQL filter (e.g., `"total_vehicle > 20000"`)
- `--select "col1,col2"` — Choose specific columns
- `--csv` — Output as CSV instead of JSON
- `--resource-id ID` — Specify which resource to query

## Dataset IDs

Dataset IDs are URL-safe slugs (e.g., `traffic-volumes-at-intersections-for-all-modes`). Find them via `search` or `list`, or from the dataset URL: `open.toronto.ca/dataset/{id}`.

## Data Sources

All data is sourced from the City of Toronto's Open Data Portal (open.toronto.ca). See [references/datasets.md](references/datasets.md) for a curated list of popular datasets.
