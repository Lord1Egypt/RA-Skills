---
name: rental-housing-research
description: Research public rental communities and NYC housing listings or market series through Crawlora StreetEasy and Greystar. Use to build a rental shortlist, inspect buildings or units, compare advertised housing offers, or put NYC asking prices in dated market context.
---

# Rental housing and listing research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Build a housing shortlist with location, unit, advertised-price, and source
context. StreetEasy supplies NYC-area listings and market series; Greystar
supplies its own communities in discovered markets. Keep their scopes distinct.

## Discover geography and listing identity

- Establish location, budget/currency, dates where relevant, bedrooms, and explicit
  amenity/size needs. StreetEasy area IDs come from `streeteasy_areas`; Greystar
  market/country/state/city/neighborhood values come from `greystar_markets`.
  Their location IDs are unrelated. Do not infer resident demographics or
  neighbourhood suitability from directory content.
- Use StreetEasy rental search for monthly asks, and sales search only for a
  requested purchase comparison or market context. Repeat array query parameters
  for multiple area/amenity values. Follow returned unit/building identity into
  detail, rather than guessing a building from a similar street address.
- Greystar search returns communities; resolve its numeric property ID before
  property detail. A community's starting rent is not the price of a particular
  available unit. Price filters exclude communities without published prices,
  so an omitted community is not evidence of an absent local offer.
- For advertised apartments rather than community summaries, discover the
  accepted listing locations with `greystar_unit_locations`, then use
  `greystar_units` for available unit-level prices, floor plans, and lease terms.
  Its location slugs are separate from `greystar_markets` values, and results
  are grouped by community.
- StreetEasy market-data catalog discovers dataset and area/group choices. Match
  dataset, region, unit, frequency, period, and property type before comparing
  series. Asking-price/rent series differ from recorded sales and modelled
  indices; never merge those into one unlabeled trend. School/building metadata
  describes the source record, not guaranteed school admission or quality.
- Bound pages and retain listing IDs, addresses, unit numbers, source URLs,
  publication/update times when present, and collection time. Deduplicate
  cross-posts cautiously; two units in one building remain separate offers.

```sh
scripts/crawlora.sh /streeteasy/areas
scripts/crawlora.sh /streeteasy/market-data/catalog
scripts/crawlora.sh /greystar/markets
scripts/crawlora.sh /greystar/search query="New York" page=1 per_page=10
scripts/crawlora.sh /greystar/unit-locations query="austin"
scripts/crawlora.sh /greystar/units location="austin-tx" bedrooms=1 max_price=2500 page=1
# Use discovered area IDs and a user's budget, for example:
# scripts/crawlora.sh /streeteasy/rentals/search area_id="$AREA_ID" max_price="$BUDGET" page=1
```

## Normalize and deliver

Keep gross monthly rent, net-effective rent, concessions, starting prices,
unit-specific asks, deposits, mandatory fees, lease duration, and sale prices
separate. Compute comparable totals only from returned/sourced terms and show
unknown costs explicitly. Missing availability or price is unknown; a listing
snapshot does not guarantee vacancy, eligibility, or an accepted application.
Return a shortlist with price basis, verified location/unit identity, amenities,
source/time, and questions that could change the ranking. For market change
claims show comparable dated observations and coverage rather than turning a
single listing sample into a citywide trend. Do not submit an application,
contact landlords, book tours, or make payments from a research request.
