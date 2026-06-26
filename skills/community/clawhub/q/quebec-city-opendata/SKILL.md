---
name: Ville de Québec Open Data
description: "Access 37+ datasets from the City of Quebec open data portal. Search, fetch, and analyze city data on streets, permits, trees, infrastructure, and more via the CKAN API."
permissions: Bash
triggers:
  - quebec city open data
  - ville de quebec data
  - quebec dataset
  - donnees quebec
  - quebec infrastructure
---

# Ville de Québec Open Data

Access and analyze 37+ open datasets from the City of Quebec via the CKAN API hosted on donneesquebec.ca. Data covers streets, permits, trees, infrastructure, hydrography, and more.

**Portal:** https://www.ville.quebec.qc.ca/services/donnees-services-ouverts/
**Data Hub:** https://www.donneesquebec.ca/organisation/ville-de-quebec/
**Platform:** CKAN (donneesquebec.ca)
**Language:** Data and metadata primarily in French

## Quick Start

```bash
# Search for datasets
python3 scripts/quebec_data.py search "arbre"

# List all datasets
python3 scripts/quebec_data.py list

# View dataset info
python3 scripts/quebec_data.py info permis-delivres-ville-de-quebec

# Fetch data
python3 scripts/quebec_data.py fetch permis-delivres-ville-de-quebec --limit 5

# Export as CSV
python3 scripts/quebec_data.py fetch permis-delivres-ville-de-quebec --limit 100 --csv > permits.csv

# List queryable datasets
python3 scripts/quebec_data.py searchable
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword (French) |
| `list` | List all datasets |
| `info <dataset-id>` | Show dataset metadata and resources |
| `fetch <dataset-id>` | Fetch data from datastore (opts: `--limit`, `--where`, `--csv`) |
| `searchable` | List datasets with queryable resources |

## Query Parameters

- `--limit N` — Max rows to return (default: 10)
- `--where "condition"` — SQL-like filter
- `--csv` — Output as CSV instead of JSON

## Language Note

Quebec City publishes data primarily in French. Dataset names, field names, and values are in French. Search queries should use French terms (e.g., "arbre" for tree, "permis" for permits, "rue" for street).

## Data Sources

All data is sourced from the Ville de Québec via donneesquebec.ca under the Quebec Open Government Licence.
