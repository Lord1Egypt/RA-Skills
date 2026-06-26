# Recipe · Country profile

**The API is open — no API key.**

## Goal

Build a snapshot of one country across several indicators (a mini profile).

## When to use

The user asks "Give me an overview of Brazil" or wants several headline metrics
for one country.

## Inputs

| Input | Example | Notes |
|-------|---------|-------|
| Country | `BRA` | ISO3. |
| Indicators | GDP, GDP/capita, population, life expectancy, inflation | Pick a small set. |
| Window | `mrv: 1` | Latest available per metric. |

## Steps

1. Get country metadata:
   ```json
   { "tool": "worldbank_country", "arguments": { "country": "BRA" } }
   ```
2. For each indicator, fetch the latest value:
   ```json
   { "tool": "worldbank_indicator_data",
     "arguments": { "country": "BRA", "indicator": "NY.GDP.MKTP.CD", "mrv": 1 } }
   ```
   Repeat for `NY.GDP.PCAP.CD`, `SP.POP.TOTL`, `SP.DYN.LE00.IN`,
   `FP.CPI.TOTL.ZG`.
3. Note the `date` of each latest value (it may differ per indicator).
4. Handle `null` (use the most recent non-null with `mrv` > 1 if needed).
5. Assemble the profile; cite each figure's year.

## Output

A profile table with metric, value, unit, and year, plus citations.

## Example

**Brazil — region: Latin America & Caribbean · income: Upper middle income ·
capital: Brasilia**

| Metric | Value | Year |
|--------|-------|------|
| GDP (current US$) | ~2.17 trillion | 2023 |
| GDP per capita (current US$) | ~10,295 | 2023 |
| Population, total | ~216 million | 2023 |
| Life expectancy at birth | ~75.9 years | 2022 |
| Inflation (annual %) | ~4.6 | 2023 |

> **World Bank, multiple indicators, Brazil, 2022–2023.** Indicator pages under
> https://data.worldbank.org/indicator (e.g. .../NY.GDP.MKTP.CD).

> Values illustrative. Use live results.
> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## Edge cases

- **Differing latest years:** state each metric's year explicitly.
- **Null latest year:** raise `mrv` to find the most recent real value, and label
  its year.

## Production notes

- Cache each indicator's latest value with its `lastupdated`.
- Consider listing each indicator's own URL in the citation block.
- No key: `"env": {}`.
