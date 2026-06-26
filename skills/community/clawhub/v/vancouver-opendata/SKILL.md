---
name: City of Vancouver Open Data
description: "Access 194+ datasets from the City of Vancouver open data portal. Search, fetch, and analyze city data on parking, transit, permits, demographics, and more via the Opendatasoft API."
permissions: Bash
triggers:
  - vancouver open data
  - city of vancouver data
  - vancouver dataset
  - opendata.vancouver.ca
  - vancouver transit
  - vancouver permits
---

# City of Vancouver Open Data

Access and analyze 194+ open datasets from the City of Vancouver via the Opendatasoft API. Data covers parking, transit, permits, demographics, environment, infrastructure, and more.

**Portal:** https://opendata.vancouver.ca
**Platform:** Opendatasoft

## Quick Start

```bash
# Search for datasets
python3 scripts/vancouver_data.py search "parking"

# List all datasets
python3 scripts/vancouver_data.py list

# View dataset info
python3 scripts/vancouver_data.py info parking-tickets-2017-2019

# Fetch data
python3 scripts/vancouver_data.py fetch parking-tickets-2017-2019 --limit 5

# Fetch with filters
python3 scripts/vancouver_data.py fetch parking-tickets-2017-2019 --where "year='2019'" --limit 10

# Export as CSV
python3 scripts/vancouver_data.py fetch parking-tickets-2017-2019 --limit 100 --csv > tickets.csv
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword |
| `list` | List all datasets |
| `info <dataset-id>` | Show dataset metadata and fields |
| `fetch <dataset-id>` | Fetch data rows (opts: `--limit`, `--where`, `--select`, `--order`, `--csv`) |

## Query Parameters

- `--limit N` — Max rows to return (default: 10)
- `--where "condition"` — SQL-like filter
- `--select "col1,col2"` — Choose specific columns
- `--order "col DESC"` — Sort results
- `--csv` — Output as CSV instead of JSON

## Dataset IDs

Dataset IDs are URL-safe slugs (e.g., `parking-tickets-2017-2019`). Find them via `search` or `list`, or from the dataset URL: `opendata.vancouver.ca/explore/dataset/{id}`.

## Data Sources

All data is sourced from the City of Vancouver's Open Data Portal (opendata.vancouver.ca). See [references/datasets.md](references/datasets.md) for a curated list of popular datasets.
