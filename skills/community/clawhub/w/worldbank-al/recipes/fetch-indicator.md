# Recipe · Fetch a single indicator

**The API is open — no API key.**

## Goal

Retrieve one indicator's time series for one country and present it with a
citation.

## When to use

The user asks for a specific metric for a specific country (e.g. "What is
France's inflation rate recently?").

## Inputs

| Input | Example | Notes |
|-------|---------|-------|
| Country | `FRA` | ISO3 (or ISO2 `FR`). |
| Indicator | `FP.CPI.TOTL.ZG` | Search if unknown. |
| Window | `mrv: 5` or `date: "2015:2023"` | Latest vs. trend. |

## Steps

1. If the indicator code is unknown, discover it:
   ```json
   { "tool": "worldbank_search_indicators", "arguments": { "q": "inflation consumer prices", "limit": 5 } }
   ```
2. (Optional) Confirm the unit:
   ```json
   { "tool": "worldbank_indicator_metadata", "arguments": { "indicator": "FP.CPI.TOTL.ZG" } }
   ```
3. Fetch the data:
   ```json
   { "tool": "worldbank_indicator_data",
     "arguments": { "country": "FRA", "indicator": "FP.CPI.TOTL.ZG", "mrv": 5 } }
   ```
4. Handle `null`/empty honestly; pair values with the unit.
5. Cite.

## Output

A short table of year → value with a citation.

## Example

| Year | Inflation (annual %) |
|------|----------------------|
| 2023 | 4.9 |
| 2022 | 5.2 |
| 2021 | 1.6 |
| 2020 | 0.5 |
| 2019 | 1.1 |

> **World Bank, Inflation, consumer prices (annual %) (FP.CPI.TOTL.ZG), France,
> 2019–2023.** https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG

> Values illustrative. Use live results.
> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## Edge cases

- **Empty array:** widen the date or use a larger `mrv`; verify the codes.
- **Recent year null:** report "not yet available" for that year.
- **Wrong code → `[{message}]`:** re-search the indicator and retry once.

## Production notes

- Cache by `country + indicator + mrv/date`.
- No key: `"env": {}`.
