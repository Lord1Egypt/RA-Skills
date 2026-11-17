# World Bank API — Full Endpoint Reference

Base URL: `https://api.worldbank.org/v2`. All endpoints are `GET`, keyless,
and return XML unless `format=json` is passed. Every list endpoint paginates
with `page` / `per_page` and returns `[metadata, rows]`; `rows` is `null` when
nothing matched. API errors arrive as **HTTP 200** with
`[{"message": [{"id": ..., "key": ..., "value": ...}]}]`.

## Contents

- [Data queries](#data-queries)
- [Countries](#countries)
- [Indicators](#indicators)
- [Topics](#topics)
- [Sources](#sources)
- [Regions, income levels, lending types](#regions-income-levels-lending-types)
- [Monthly and quarterly data](#monthly-and-quarterly-data)
- [Languages](#languages)
- [Pagination recipe](#pagination-recipe)

## Data queries

```
GET /v2/country/{codes}/indicator/{indicator}?format=json
```

`{codes}`: ISO-2 or ISO-3, semicolon-separated (`US;JP;CN`), aggregate codes,
or `all`. `{indicator}`: one code, or several semicolon-separated codes **if**
`source` is also given (indicators must all live in that source):

```
GET /v2/country/BR/indicator/NY.GDP.MKTP.CD;SP.POP.TOTL?source=2&format=json&mrv=1
```

| Parameter | Values | Notes |
|---|---|---|
| `date` | `2024`, `2000:2024`, `2025M01:2025M06`, `2024Q1:2025Q4` | Year, range, month range, quarter range |
| `mrv` | integer | Most recent N periods (may include nulls) |
| `mrnev` | integer | Most recent N non-empty values; drops countries with no data at all |
| `gapfill` | `Y`/`N` | Only meaningful with `mrv`; forward-fills gaps with last known value |
| `frequency` | `Y`, `Q`, `M` | With `mrv` on monthly/quarterly-capable sources |
| `source` | source id | Selects the database; default resolves to the indicator's home source |
| `footnote` | `y` | Adds a `footnote` string to each data point |
| `per_page` / `page` | int | Defaults 50 / 1 |

Data row fields: `indicator{id,value}`, `country{id,value}`, `countryiso3code`,
`date`, `value` (number or null), `unit`, `obs_status`, `decimal`, and
`footnote` when requested. Metadata fields: `page`, `pages`, `per_page`,
`total` (counts country×period slots including nulls), `sourceid`,
`lastupdated`.

A whole-source dump also exists (`/v2/country/all/indicator/all?source={id}`)
but is huge — prefer per-indicator queries.

## Countries

```
GET /v2/country?format=json&per_page=400          # all 295 entries (economies + aggregates)
GET /v2/country/JPN?format=json                   # one economy (ISO-2 or ISO-3)
GET /v2/country/WLD;EUU?format=json               # aggregates are addressed the same way
```

Filters (combinable): `incomeLevel=LIC`, `lendingType=IDX`, `region=EAS`.

Country object:

```json
{"id": "JPN", "iso2Code": "JP", "name": "Japan",
 "region": {"id": "EAS", "iso2code": "Z4", "value": "East Asia & Pacific"},
 "adminregion": {"id": "", "iso2code": "", "value": ""},
 "incomeLevel": {"id": "HIC", "iso2code": "XD", "value": "High income"},
 "lendingType": {"id": "LNX", "iso2code": "XX", "value": "Not classified"},
 "capitalCity": "Tokyo", "longitude": "139.77", "latitude": "35.67"}
```

Aggregates are the entries with `region.value == "Aggregates"` (78 of the 295).
Note: some economies are absent entirely (e.g. Taiwan) — their codes return
error id 120 as if invalid.

## Indicators

```
GET /v2/indicator?format=json&per_page=500&page=1   # full catalog, ~29,500 codes
GET /v2/indicator/NY.GDP.MKTP.CD?format=json        # one indicator's metadata
```

Indicator object: `id`, `name`, `unit`, `source{id,value}`, `sourceNote`
(long definition), `sourceOrganization`, `topics[]`.

**There is no text-search parameter.** To find an indicator by keyword either:

1. Page through `/v2/indicator` (~59 pages at `per_page=500`) and match names
   client-side — this is what the bundled `wb_data.py --search` does; or
2. Narrow by topic first: `/v2/topic/{id}/indicator?format=json` (see below); or
3. Narrow by source: `/v2/source/{id}/indicators?format=json`.

An indicator whose metadata exists may still have **no data** (archived series
return error id 175 on data queries — e.g. old `EN.ATM.CO2E.*` CO2 codes,
everything from the retired Doing Business source). Treat 175 as "look for a
successor code".

## Topics

21 broad topics; useful for scoped discovery.

```
GET /v2/topic?format=json                     # list all topics
GET /v2/topic/8/indicator?format=json         # all indicators under a topic (paginated)
```

| id | Topic | id | Topic |
|---|---|---|---|
| 1 | Agriculture & Rural Development | 12 | Private Sector |
| 2 | Aid Effectiveness | 13 | Public Sector |
| 3 | Economy & Growth | 14 | Science & Technology |
| 4 | Education | 15 | Social Development |
| 5 | Energy & Mining | 16 | Urban Development |
| 6 | Environment | 17 | Gender |
| 7 | Financial Sector | 18 | Millennium Development Goals |
| 8 | Health | 19 | Climate Change |
| 9 | Infrastructure | 20 | External Debt |
| 10 | Social Protection & Labor | 21 | Trade |
| 11 | Poverty | | |

## Sources

~70 databases. Most everyday series live in source **2** (World Development
Indicators). You only need `source=` for multi-indicator calls, for series
outside WDI (e.g. Worldwide Governance Indicators need `source=3` — see
`indicators.md` for their renamed codes and quirks), or for monthly/quarterly
frequencies.

```
GET /v2/source?format=json&per_page=100       # list all sources
GET /v2/source/2?format=json                  # one source
GET /v2/source/3/indicators?format=json       # indicators within a source
```

Notable sources: 2 World Development Indicators · 3 Worldwide Governance
Indicators · 6 International Debt Statistics · 12 Education Statistics ·
14 Gender Statistics · 15 Global Economic Monitor (monthly/quarterly) ·
16 Health Nutrition and Population · 20/22/23 Quarterly Public/External Debt ·
28 Global Findex · 40 Population estimates and projections ·
46 Sustainable Development Goals · 57 WDI Archives.

## Regions, income levels, lending types

```
GET /v2/region?format=json&per_page=60        # 43 regions/aggregate groupings
GET /v2/incomeLevel?format=json               # 7 income classifications
GET /v2/lendingType?format=json               # 4 lending categories
```

Income levels: `HIC` High · `UMC` Upper-middle · `MIC` Middle · `LMC`
Lower-middle · `LMY` Low & middle · `LIC` Low · `INX` Not classified.
Lending types: `IBD` IBRD · `IDX` IDA · `IDB` Blend · `LNX` Not classified.

Frequently used aggregate codes for data queries: `WLD` World · `EUU`
European Union · `EMU` Euro area · `OED` OECD members · `EAS` East Asia &
Pacific · `ECS` Europe & Central Asia · `LCN` Latin America & Caribbean ·
`MEA` Middle East & North Africa · `NAC` North America · `SAS` South Asia ·
`SSF` Sub-Saharan Africa · `AFE`/`AFW` Africa Eastern/Western · `ARB` Arab
World · plus every income-level id above.

## Monthly and quarterly data

Almost everything is **annual**. Sub-annual series exist only in a few
sources and require the `source` parameter:

```
# Monthly exchange rate from Global Economic Monitor (source 15)
GET /v2/country/CN/indicator/DPANUSSPB?format=json&date=2025M01:2025M06&source=15

# Quarterly public sector debt (source 20)
GET /v2/country/GB/indicator/DP.DOD.DECD.CR.GG.CD?format=json&mrv=4&source=20
```

Dates come back as `2025M03` / `2025Q4` strings. With `mrv`, add
`frequency=M` or `frequency=Q` to pick the granularity.

## Languages

Insert a 2-letter language code between `/v2` and the rest of the path to get
translated labels (codes and numeric values are unchanged; untranslated
strings fall back to English):

```
GET /v2/zh/country/CN/indicator/NY.GDP.MKTP.CD?format=json&mrv=1
```

Fully supported: `en`, `es`, `fr`, `ar`, `zh`.

## Pagination recipe

```python
def wb_all_pages(url, **params):
    rows, page = [], 1
    while True:
        body = requests.get(url, params={"format": "json", "per_page": 1000,
                                         "page": page, **params}, timeout=30).json()
        if isinstance(body[0], dict) and "message" in body[0]:
            raise ValueError(body[0]["message"][0]["value"])
        rows += body[1] or []
        if page >= int(body[0]["pages"]):
            return rows
        page += 1
```

In practice a single request with `per_page=20000` (large values are accepted)
covers almost every data query without paging; paging matters mainly for the
full `/v2/indicator` catalog.
