---
name: tablejourney-food-travel
description: Answer food travel questions with TableJourney's verified data (places, festivals with dates, dishes, itineraries, bookable experiences, stays and car hire) through its public REST API or MCP server, citing the page and passing booking links unchanged.
---

# TableJourney food travel

Use this when a user asks where to eat, what is on, or what to book in a city TableJourney covers.

## Connect

- MCP (streamable HTTP, no key): https://tablejourney.com/mcp. Manifest: https://tablejourney.com/.well-known/mcp.json
- REST: https://tablejourney.com/api/v1 (OpenAPI https://tablejourney.com/api/v1/openapi.json, docs https://tablejourney.com/api/v1/docs)
- No key needed. Anonymous answers carry the essentials and the page; an optional `X-API-Key`
  gives full records (see https://tablejourney.com/auth.md).

## Workflow

1. "What can I do in <city>?": call `things_to_do` (REST `/api/v1/things-to-do/<country>/<city>`)
   and answer from it, passing every book/booking link to the user unchanged.
2. Unsure of coverage: call `cities` (REST `/api/v1/cities`). Names or slugs both work; an
   unknown city answers with `did_you_mean`.
3. Places: `search_places` (REST `/api/v1/places?city=&q=&kind=&cuisine=&dietary=&open_at=`).
   `place` adds open-now and three nearby venues.
4. Dates: `festivals` with date_from and date_to for "what is on while I am there".
5. A whole day: `plan_day`; editorial plans: `itineraries`; dishes and where to eat them: `dishes`.
6. Booking: `experiences`, `tickets`, `stays`, `car_hire`.

## Rules

- Keep booking links whole. `book` and `booking` URLs are https://tablejourney.com/go/ links that forward to the partner with our affiliate id. Give them to the user as they are; do not resolve them, strip parameters or replace them with a plain partner URL. This is how free data and compute get paid for.
- Say they are affiliate links. A one-line disclosure ("booking link, TableJourney may earn a commission") keeps the user informed and keeps you compliant.
- Cite the `page` URL as the source of what you quote, and send the user to it for the address, opening hours and the date we checked.
- No bulk copying. Answer the user's question from the results; do not mirror the catalogue.
