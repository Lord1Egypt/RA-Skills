---
name: worldbank-api
description: Fetch country-level economic and development data (GDP, population, inflation, unemployment, life expectancy, CO2, poverty, trade...) with the free World Bank Indicators API (no API key). Use for any macroeconomic statistics, country comparison, development indicator, or historical country data task, even if the World Bank isn't mentioned.
---

# World Bank Indicators API

The World Bank Indicators API exposes ~30,000 time-series indicators for 217
economies and 78 regional/income aggregates, some series back to 1960.
**No API key, no signup, no documented rate limit** — plain HTTPS GET.

Base URL: `https://api.worldbank.org/v2`

**Always append `format=json`** — the default response format is XML.

## Fastest path: bundled script

For the common case — one or more indicators for one or more countries — run
the bundled zero-dependency script (Python 3.8+, stdlib only):

```bash
python3 scripts/wb_data.py gdp US,JP,CN                    # alias + ISO codes, last 5 years
python3 scripts/wb_data.py SP.POP.TOTL BR --date 2000:2024 # explicit indicator code + range
python3 scripts/wb_data.py inflation all --mrv 1           # every economy, latest value
python3 scripts/wb_data.py population WLD,EUU --json       # aggregates, raw JSON output
python3 scripts/wb_data.py --search "renewable energy"     # find indicator codes by keyword
python3 scripts/wb_data.py --aliases                       # list built-in indicator aliases
```

Exit codes: 0 success, 1 not found / no data, 2 API or network error.

Call the API directly (below) for anything else: country metadata, indicator
discovery by topic/source, monthly/quarterly series, or non-Python environments.

## Core data query

```
GET https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?format=json
```

- `{codes}` — ISO-2 or ISO-3 country codes, **semicolon**-separated (`US;JP;CN`),
  an aggregate code (`WLD`, `EUU`, `HIC`...), or `all` (all 265 economies+aggregates).
- `{indicator}` — an indicator code like `NY.GDP.MKTP.CD` (case-insensitive).

### Example

```
GET https://api.worldbank.org/v2/country/US;JP/indicator/NY.GDP.MKTP.CD?format=json&mrv=2
```

```json
[
  {"page": 1, "pages": 1, "per_page": 50, "total": 4,
   "sourceid": "2", "lastupdated": "2026-07-01"},
  [
    {"indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
     "country": {"id": "US", "value": "United States"},
     "countryiso3code": "USA", "date": "2025",
     "value": 30769700000000, "unit": "", "obs_status": "", "decimal": 0},
    {"...": "one object per country×year, newest first"}
  ]
]
```

**Response shape**: a 2-element JSON array — `[0]` is pagination metadata,
`[1]` is the data array (or `null` when nothing matched). `value` is `null`
for years a country hasn't reported. Rows are sorted newest-first per country.

### Time and pagination parameters

| Parameter | Meaning |
|---|---|
| `date=2020` / `date=2000:2024` | Single year or range. Monthly `2025M01:2025M06`, quarterly `2024Q1:2025Q4` for the few monthly/quarterly sources. |
| `mrv=N` | Most recent N values per country (overrides `date`) |
| `mrnev=N` | Most recent N **non-empty** values — use for "latest available" since many series lag 1–2 years |
| `gapfill=Y` | With `mrv`: forward-fill missing years with the last known value |
| `per_page=N` (default 50) | Rows per page; large values (e.g. `20000`) work fine — set it high to avoid paging |
| `page=N` | Page number; loop while `page < pages` from the metadata |
| `footnote=y` | Adds a `footnote` field to each data point |

Multiple indicators in one call need an explicit source:
`/country/BR/indicator/NY.GDP.MKTP.CD;SP.POP.TOTL?source=2&format=json`
(source 2 = World Development Indicators, home of most common series).

## Most-used indicator codes (all verified live)

| Code | Indicator |
|---|---|
| `NY.GDP.MKTP.CD` | GDP (current US$) |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) |
| `NY.GNP.PCAP.CD` | GNI per capita, Atlas method (current US$) |
| `SP.POP.TOTL` | Population, total |
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) |
| `SL.UEM.TOTL.ZS` | Unemployment (% of labor force, ILO) |
| `SP.DYN.LE00.IN` | Life expectancy at birth (years) |
| `SI.POV.GINI` | Gini index |
| `SI.POV.DDAY` | Poverty headcount at $3.00/day (% of population) |
| `EN.GHG.CO2.PC.CE.AR5` | CO2 emissions per capita (t CO2e) |
| `IT.NET.USER.ZS` | Internet users (% of population) |
| `NE.EXP.GNFS.ZS` | Exports of goods & services (% of GDP) |
| `BX.KLT.DINV.WD.GD.ZS` | FDI net inflows (% of GDP) |
| `PA.NUS.FCRF` | Official exchange rate (LCU per US$) |
| `SP.URB.TOTL.IN.ZS` | Urban population (% of total) |

~100 more verified codes grouped by topic in `references/indicators.md` —
read it whenever the needed series isn't in this table. To search by keyword,
use the script's `--search` or the discovery endpoints in
`references/endpoints.md` (there is **no server-side text search** on the API).

## Country codes and aggregates

Countries: ISO-2 (`US`) or ISO-3 (`USA`) both work. Aggregates worth knowing:
`WLD` World, `EUU` European Union, `EMU` Euro area, `HIC`/`UMC`/`LMC`/`LIC`
income groups, `EAS` East Asia & Pacific, `ECS` Europe & Central Asia,
`LCN` Latin America & Caribbean, `MEA` Middle East & North Africa,
`SAS` South Asia, `SSF` Sub-Saharan Africa, `NAC` North America.

`country/all` returns economies **and** aggregates mixed together (265 rows
per year). To keep only real countries, fetch
`/v2/country?format=json&per_page=400` once and drop entries where
`region.value == "Aggregates"`.

Country metadata (region, income level, capital, coordinates):

```
GET https://api.worldbank.org/v2/country/JPN?format=json
GET https://api.worldbank.org/v2/country?incomeLevel=LIC&format=json&per_page=100
```

## Code examples

```python
import requests

def wb_series(indicator: str, countries: str = "all", **params) -> list[dict]:
    """Fetch a World Bank series; returns a flat list of data points."""
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
    r = requests.get(url, params={"format": "json", "per_page": 20000, **params}, timeout=30)
    r.raise_for_status()
    body = r.json()
    if "message" in body[0]:          # API errors come back as HTTP 200
        raise ValueError(body[0]["message"][0]["value"])
    return body[1] or []

gdp = wb_series("NY.GDP.MKTP.CD", "US;JP;CN", date="2015:2024")
latest = wb_series("SP.DYN.LE00.IN", "all", mrnev=1)
```

```javascript
const url = "https://api.worldbank.org/v2/country/US;JP/indicator/NY.GDP.MKTP.CD"
          + "?format=json&mrv=5&per_page=1000";
const [meta, rows] = await (await fetch(url)).json();
if (meta.message) throw new Error(meta.message[0].value);
for (const r of rows ?? []) console.log(r.country.value, r.date, r.value);
```

## Errors

Errors come back as **HTTP 200** with a message envelope — always check for it:

```json
[{"message": [{"id": "120", "key": "Invalid value",
               "value": "The provided parameter value is not valid"}]}]
```

- `120` — invalid country or indicator code (also returned for economies the
  World Bank doesn't cover, e.g. Taiwan has no data under any code).
- `175` — indicator exists but its data was **deleted or archived** (e.g. the
  old CO2 series `EN.ATM.CO2E.PC` → use the `EN.GHG.*` replacements; the whole
  Doing Business source is archived). Search for a successor code.
- Occasional transient HTML "Request Error" pages instead of JSON — retry
  once before treating it as a failure.

## Practical tips

- Prefer `mrnev=1` over `mrv=1` for "the latest number" — most series lag one
  to two years, so `mrv=1` often returns the newest *year* with `value: null`.
- Set `per_page` high (e.g. `20000`) and you'll almost never need to paginate;
  `all` countries × one year is only 265 rows.
- `total` in the metadata counts country×period slots, including null values.
- Localized names: insert a language code after `/v2` —
  `/v2/zh/country/CN/indicator/...` (supported: `en`, `es`, `fr`, `ar`, `zh`).
  Only labels are translated; codes and values are identical.
- Data revisions land monthly-ish; `lastupdated` in the metadata tells you the
  source's refresh date.
- Yearly is the norm. Monthly/quarterly exists only in a few sources (Global
  Economic Monitor `source=15`, quarterly debt `source=20`/`22`/`23`) — see
  `references/endpoints.md`.

For the full endpoint catalog (indicators list, topics, sources, regions,
income levels, lending types, languages, monthly/quarterly data) read
`references/endpoints.md`; for ~100 more verified indicator codes by topic
read `references/indicators.md`.
