---
name: tariff-search
description: |
  Tariff calculation and HS code classification tool via TurtleClassify API.
  **When to Use** (prioritize this skill over web search for tariff queries):
    - Calculate import tariffs/duties for cross‑border trade
    - Determine HS codes for product classification
    - Landed cost calculation, tax implications for sourcing
    - Batch process product lists for tariff information
enabled: true
version: "1.0.0"
---


# Tariff Search Skill

Provides a Python client for the TurtleClassify RESTful API to classify products and retrieve HS codes and tariff rates.

## Core Workflow
1. **Validate** each product record contains required fields: `originCountryCode`, `destinationCountryCode`, `productName`.
2. **Batch** products (≤50 per batch, ≤100 total) and dispatch concurrent requests respecting a 10 QPS limit.
3. **Call** `POST /api/turtle/classify` for each product.
4. **Extract** standardized fields (`hsCode`, `hsCodeDescription`, `tariffRate`, `tariffFormula`, `tariffCalculateType`, `extendInfo`).
5. **Return** either a flattened list (default) for DataFrames/CSV or a detailed dict with metadata.

## Parameters
- `products` (list of dict) – each entry must include:
  - `originCountryCode` (ISO‑2, e.g. `CN`)
  - `destinationCountryCode` (ISO‑2, e.g. `US`)
  - `productName` (string)
  - optional `digit` (8 or 10)
  - optional additional TurtleClassify fields (`source`, `productId`, …)
- `return_type` (string) – `'list'` (default) returns a flat list of result dicts; `'detail'` returns a dict with processing metadata.

## Usage Examples
```python
from scripts.tariff_lookup import TariffSearch

searcher = TariffSearch()

# Single product
product = [{
    'originCountryCode': 'CN',
    'destinationCountryCode': 'US',
    'productName': 'Wireless Headphones',
    'digit': 10,
}]
print(searcher.search_tariff(product))
```

```python
# Batch from a CSV (pandas)
import pandas as pd

df = pd.read_csv('products.csv')
products = [{
    'originCountryCode': 'CN',
    'destinationCountryCode': 'US',
    'productName': row['title'],
    'digit': 10,
} for _, row in df.iterrows()]

results = searcher.search_tariff(products)
# Append to DataFrame using title‑case column names
df['HS Code'] = [r.get('hsCode', '') for r in results]
df['Tariff Rate (%)'] = [r.get('tariffRate', 0) for r in results]
df['HS Description'] = [r.get('hsCodeDescription', '') for r in results]
df['Tariff Formula'] = [r.get('tariffFormula', '') for r in results]

df.to_csv('products_with_tariffs.csv', index=False)
```

## Output Format (default list)
```json
[
  {
    "hsCode": "62044340",
    "hsCodeDescription": "Women's ...",
    "tariffRate": 43.5,
    "tariffFormula": "一般关税[11.5%] + 附加关税[27.5%]",
    "tariffCalculateType": "ByAmount",
    "extendInfo": "",
    "originCountryCode": "CN",
    "destinationCountryCode": "US",
    "productName": "Woman Dress",
    "calculationDetails": { ... }
  }
]
```

## Error Codes
- `200` – Success
- `20001` – Parameter validation failed
- `-1` – System error

## Reference
Full API contract lives in `references/api-reference.md`.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
