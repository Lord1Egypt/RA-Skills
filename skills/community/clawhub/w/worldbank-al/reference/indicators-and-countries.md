# Reference · Indicators & Country Codes

How to address **what** (indicators) and **who** (countries/aggregates), plus
date and `mrv` usage. **The API is open — no API key.**

---

## Popular indicator codes by topic

### Economy & Growth

| Code | Indicator | Unit |
|------|-----------|------|
| `NY.GDP.MKTP.CD` | GDP | current US$ |
| `NY.GDP.PCAP.CD` | GDP per capita | current US$ |
| `NY.GDP.MKTP.KD.ZG` | GDP growth | annual % |
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices | annual % |

### Labor

| Code | Indicator | Unit |
|------|-----------|------|
| `SL.UEM.TOTL.ZS` | Unemployment | % of labor force |

### Health & Population

| Code | Indicator | Unit |
|------|-----------|------|
| `SP.POP.TOTL` | Population, total | persons |
| `SP.DYN.LE00.IN` | Life expectancy at birth | years |

### Environment

| Code | Indicator | Unit |
|------|-----------|------|
| `EN.ATM.CO2E.PC` | CO2 emissions | metric tons per capita |

### Poverty

| Code | Indicator | Unit |
|------|-----------|------|
| `SI.POV.DDAY` | Poverty headcount ratio | % of population |

> If a code is unknown, **search** with `worldbank_search_indicators`; don't guess.

---

## Country codes

`country` accepts several forms:

| Form | Example | Meaning |
|------|---------|---------|
| ISO3 | `USA`, `CHN`, `BRA` | Single country (preferred). |
| ISO2 | `US`, `CN`, `BR` | Single country (alternate). |
| `all` | `all` | Every country/aggregate. |
| Multiple | `USA;CHN;IND` | Several entities in one call (join with `;`). |

Resolve unknown codes with `worldbank_country` (omit `country` to list all).

---

## Aggregates (not single countries)

The dataset includes **aggregate** entities. Treat these as groups, never as
individual countries:

| Code | Aggregate |
|------|-----------|
| `WLD` | World |
| `EUU` | European Union |
| `HIC` | High income (income-level aggregate) |
| `UMC` | Upper middle income |
| `LMC` | Lower middle income |
| `LIC` | Low income |

Income-level and region aggregates come from the `incomelevel` / `region`
endpoints (via `worldbank_request`). When reporting, label aggregates clearly.

---

## Date and `mrv` usage

| Param | Form | Use |
|-------|------|-----|
| `date` | `YYYY` | A single year, e.g. `2022`. |
| `date` | `YYYY:YYYY` | A range, e.g. `2010:2023` (trends/charts). |
| `mrv` | integer `N` | The **N most recent values** (latest figures). |

Guidance:

- Use `mrv` for "the latest" — it adapts even when the newest year is missing.
- Use a `date` range for trends and time-series charts.
- The newest year(s) may still be `null` (annual data lag).

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
