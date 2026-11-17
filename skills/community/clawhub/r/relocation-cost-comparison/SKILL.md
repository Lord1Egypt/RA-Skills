---
name: relocation-cost-comparison
description: Compare city relocation budgets with Crawlora itemized Numbeo costs and optional US housing-market context. Use for household expense scenarios, rent comparisons, or choosing between cities with explicit currency, household, and price-basis assumptions.
---

# Relocation cost comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Build comparable household expense scenarios for the user's candidate cities.
Start with household size, housing size/location, rent versus buy, transport,
spending pattern, and budget currency. Ask only for assumptions that materially
change the result; mark provisional assumptions so the comparison can be revised.

## Resolve geography and comparable prices

1. Discover Numbeo cities from current rankings or the relevant country response's
   `cities[].city_slug`. There is no city-search/autocomplete route. Preserve the
   disambiguated city, country, and slug; similar city names are not a match.
2. Fetch itemized costs for the chosen slugs. Preserve item names and units,
   price ranges, `last_update`, contributor count, and source URL. Match the same
   basket and rent basis (bedrooms, city centre/outside centre) across cities.
3. A raw currency glyph such as `$` does not establish USD. Verify the currency
   before conversion and retain the dated, sourced or user-supplied exchange rate.
   Without a verified rate, show separate local-currency budgets and mark the
   converted comparison unavailable. Never combine amounts in different currencies.
4. For US purchase-market context, discover housing dataset region/property-type
   values and resolve the correct city/metro/county/ZIP record. Keep period and
   geography fixed. Median sale/list prices and modelled affordability metrics
   are contextual aggregates, not monthly rent quotes or the user's mortgage.
   Use Numbeo-only evidence for locations outside that dataset's coverage.

```sh
scripts/crawlora.sh /numbeo/cost-of-living/rankings scope=current
scripts/crawlora.sh /numbeo/cost-of-living/country country="United States"
# Select actual returned city slugs before requesting itemized prices:
# scripts/crawlora.sh "/numbeo/cost-of-living/city/$CITY_SLUG"
scripts/crawlora.sh /datasets/housing-markets/facets facet=region_type latest=true
```

## Calculate and present scenarios

Create a basket ledger: item/unit, monthly quantity, source price/range,
currency, observation date, monthly subtotal, and assumption. Calculate
`monthly basket = sum(unit price × monthly quantity)` using comparable units.
Keep rent, groceries, utilities, transport, and discretionary spending separate;
do not count Numbeo's composite indices as extra dollar expenses. Separate
one-time moving/setup costs from recurring spending. Missing childcare, taxes,
insurance, deposits, or fees remain excluded/unknown instead of zero. Gross
salary is not take-home income; do not imply savings without a supplied net basis.

Return the basket, city-by-city scenarios, major cost differences, excluded
items, freshness/coverage limits, and assumptions that could change the choice.
Crowdsourced ranges are observed price ranges, not confidence intervals or
individual quotes. Weight lifestyle preferences only when the user provides
weights; prices alone do not establish a universally best city. A comparison
does not authorise contacting agents, booking movers, or applying for housing.
