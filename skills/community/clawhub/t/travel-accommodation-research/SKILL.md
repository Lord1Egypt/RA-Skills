---
name: travel-accommodation-research
description: Compares public accommodation, short-term rental, hotel, flight, and activity listings across Airbnb, Agoda, Hotels.com, and Trip.com using the Crawlora API. Use for travel discovery, property comparisons, host checks, availability research, and itinerary evidence without booking or payment actions.
---

# Travel accommodation research

Research public travel listings and compare accommodation options across Airbnb,
Agoda, Hotels.com, and Trip.com. Return source-aware JSON and keep dates,
currency, location, occupancy, and platform identity attached to every result.

## When to use this skill

- Compare hotels or short-term rentals for a destination and date range.
- Inspect a property's public details, reviews, calendar, or host portfolio.
- Find flights, activities, or hotel options through Agoda.
- Cross-check the same destination across multiple travel platforms.

## Setup

- Set `CRAWLORA_API_KEY` to a key from [crawlora.net](https://crawlora.net).
- Run `scripts/crawlora.sh`; it sends the key to the fixed Crawlora API host.
- Review the generated endpoint reference before using a less common route.

## Research workflow

1. Normalize destination, check-in/check-out dates, guests, currency, and
   locale before comparing platforms. Resolve each platform's own property IDs.
2. Search Airbnb, Agoda, Hotels.com, or Trip.com, then fetch detail for a
   matched shortlist. A listing ID on one platform cannot be reused on another.
3. Keep nightly rate, total displayed price, fees, taxes, cancellation terms,
   availability, and currency as separate fields. Never invent a final checkout
   total from a partial response.
4. Use Airbnb room/host reviews and hotel review routes for evidence about
   recent experience. Samples and platform filters can differ, so report the
   collection scope and date.
5. Agoda's flight and activity routes are separate surfaces. Do not mix flight
   itineraries, activities, and hotel properties in one price comparison.

## Examples

```sh
scripts/crawlora.sh /airbnb/search location="Lisbon" checkin=2026-10-10 checkout=2026-10-14 | jq '.'
scripts/crawlora.sh /agoda/hotels/search city="Lisbon" | jq '.'
scripts/crawlora.sh /hotels/autocomplete query="Lisbon" | jq '.'
scripts/crawlora.sh /tripcom/hotels/search keyword="Lisbon" | jq '.'
```

## Notes and limits

- This skill performs research only. It does not reserve rooms, purchase
  flights, submit payment, or change a host or traveler account.
- Availability and prices are time-sensitive snapshots. Record retrieval time,
  dates, occupancy, currency, and platform for every comparison.
- Some Hotels.com and Agoda surfaces accept POST bodies. Follow the generated
  endpoint reference and pass the documented body shape exactly.
- Treat ratings, reviews, and cancellation text as platform-reported evidence;
  verify material booking decisions on the originating platform.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.

## Vrbo discovery, quotes, and reviews

Use `vrbo_locations_search` to obtain the destination label, region ID, and
coordinates for POST `vrbo_search`. Send the MCP `request` value as a flat REST
JSON body, with explicit dates and party composition. Copy sort/filter/range IDs
from returned facets rather than inventing them; `limit` trims local output and
does not prove complete source search coverage. Follow returned property IDs to
property, review, and rate-calendar routes. Calendar availability and nightly
rates differ from the total quote for dates, occupants, taxes, fees, and currency.
A challenge or failed query is unavailable evidence, not an empty destination.
Travel pages are editorial/location discovery, not a booking quote.

```sh
scripts/crawlora.sh /vrbo/locations/search search_term="Paris"
```

Bound pagination, retain provider-specific IDs and timestamps, and use the exact
review cursor/options in the reference. A research request does not authorise a
booking, host message, or reservation.
