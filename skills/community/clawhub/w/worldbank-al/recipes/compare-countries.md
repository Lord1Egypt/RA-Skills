# Recipe · Compare countries

**The API is open — no API key.**

## Goal

Compare one indicator across multiple countries over a time window.

## When to use

The user asks for a cross-country comparison (e.g. "Compare GDP of the USA,
China, and India 2020–2023").

## Inputs

| Input | Example | Notes |
|-------|---------|-------|
| Countries | `USA;CHN;IND` | Join ISO3 codes with `;`. |
| Indicator | `NY.GDP.MKTP.CD` | Search if unknown. |
| Window | `date: "2020:2023"` | Range for comparison. |

## Steps

1. Discover the indicator if needed:
   ```json
   { "tool": "worldbank_search_indicators", "arguments": { "q": "GDP current US dollars", "limit": 3 } }
   ```
2. Fetch all countries in **one** call:
   ```json
   { "tool": "worldbank_indicator_data",
     "arguments": { "country": "USA;CHN;IND", "indicator": "NY.GDP.MKTP.CD", "date": "2020:2023" } }
   ```
3. Group records by country; handle `null` per cell.
4. Build a comparison table; pair with the unit.
5. Cite all countries and the year(s).

## Output

A comparison table + a single citation listing the countries.

## Example

| Country | GDP 2023 (current US$) |
|---------|------------------------|
| United States | ~27.36 trillion |
| China | ~17.79 trillion |
| India | ~3.55 trillion |

> **World Bank, GDP (current US$) (NY.GDP.MKTP.CD), United States / China /
> India, 2023.** https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

> Values illustrative. Use live results.
> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## Edge cases

- **Mixed availability:** one country may have `null` for a year — mark that cell
  "data not available".
- **Aggregates:** if a "country" is actually `WLD`/`EUU`/income group, label it
  as an aggregate.
- **Large result:** if `pages > 1` via `worldbank_request`, paginate.

## Production notes

- One multi-country call beats N single-country calls (fewer requests, less 429
  risk).
- Cache the combined result.
- No key: `"env": {}`.
