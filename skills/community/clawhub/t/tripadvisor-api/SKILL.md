---
name: tripadvisor-api
description: >-
  Query TripAdvisor location data (search, nearby, details, photos, reviews)
  straight from a shell with curl against the Terra REST API
  (terra.tripadvisor.com), instead of running the tripadvisor-mcp server —
  plus a no-API-key fallback that reads a location's public page through the
  fpx browser bridge. Use when you want TripAdvisor data without the MCP, in
  a script, or on a machine where the MCP isn't installed. Triggers on "check
  TripAdvisor", "TripAdvisor location/restaurant/hotel/attraction search,
  details, photos, reviews", or any TripAdvisor data request that should hit
  the API directly.
---

# TripAdvisor Terra API via curl (no MCP)

TripAdvisor's **Terra** API (`terra.tripadvisor.com/api`) is a plain
API-key REST API reachable directly from a server or shell — no browser
bridge needed. This skill shells out to `curl` with the key in an
`X-API-Key` header, exactly as `tripadvisor-mcp`'s `src/client.ts` does.
Terra is the current API (the legacy Content API sunsets 2026-08-31); it
has **no write endpoints** — everything here is a read.

A second, smaller tier at the bottom covers the one thing Terra can't do
without a key: reading a location's core details from the public
consumer page via the `fpx` browser bridge.

## One-time setup: get a Terra key

```sh
# Prefer the env var tripadvisor-mcp itself reads (check its .env first):
grep -h TRIPADVISOR_API_KEY ~/git/tripadvisor-mcp/.env 2>/dev/null
export TRIPADVISOR_API_KEY='...'
```

If you don't have one: create a free **Discover**-tier key at
https://www.tripadvisor.com/developers (pay-as-you-go, 10 QPS / 10,000
calls/day). A **legacy** Content API key does NOT work here (and vice
versa) — a mismatched key gets a `403`.

## Core call pattern

```sh
BASE=https://terra.tripadvisor.com/api

curl -sS "$BASE/locations/search?query=Golden%20Gate%20Bridge" \
  -H "X-API-Key: $TRIPADVISOR_API_KEY" -H 'accept: application/json' \
  | jq '.data[].location | {id, name: (.names[] | select(.primary) | .value)}'
```

Every call needs just the two headers above — no session/cookie, no
mutual TLS. Ready-to-run recipes for all 6 endpoints are in
`references/terra-endpoints.md`.

## The one rule: resolve a location id first

Details/photos/reviews are keyed by numeric `location_id` — get one from
`ta_search_locations`'s equivalent, `GET /locations/search`, before
calling the id-scoped endpoints:

```sh
curl -sS "$BASE/locations/search?query=Golden+Gate+Bridge" \
  -H "X-API-Key: $TRIPADVISOR_API_KEY" | jq -r '.data[].location.id'
# 104675
```

## Response shapes (quick reference)

- List endpoints (`search`, `nearby`, `reviews`, `photos`) wrap results:
  `{"data": [...], "pagination": {"page","size","total_pages","total_elements"}}`.
- `GET /locations` (batch) and `GET /locations/{id}` (details) do **not**
  wrap in `pagination` — batch returns `{"data": [...]}`, details returns
  the location object directly.
- A **location** object keys `names`/`descriptions`/`addresses` as
  **arrays** tagged by language — the primary entry has `"primary": true`
  (`jq '.names[] | select(.primary) | .value'`), not a flat `name` field.

Full field lists and all 6 curl+jq recipes: `references/terra-endpoints.md`.

## Output / error contract

- A 2xx body is JSON; pipe to `jq`.
- `400` — validation error; body is `{type, title, status, detail,
  field_errors: [{field, message}], trace_id}` — `detail`/`field_errors`
  name the bad param.
- `401`/`403` — key missing, invalid, or the wrong API family (legacy key
  on Terra, or vice versa).
- `404` — unknown id, or a typo'd path (`/locations/{id}` is **plural**;
  the singular form 404s).
- `429` — QPS (10) or daily quota (10,000) exceeded on the Discover tier;
  back off and retry (the response may carry `Retry-After`).

## Fallback tier: no API key (fpx browser bridge)

TripAdvisor's consumer site (`www.tripadvisor.com`) is DataDome-walled, so
it can't be curled directly — but a location's public detail page is
plain server-rendered HTML with a clean `application/ld+json` block
(name, rating, review count, address, phone, coordinates), reachable with
**no API key** by routing the fetch through your own signed-in browser
tab via `fpx` (`@fetchproxy/cli`). Use this when you don't have (or don't
want to use) a Terra key, or `ta_get_location_details` is blocked.

```sh
npm install -g @fetchproxy/cli                      # provides `fpx`
fpx profile add tripadvisor --domain tripadvisor.com # fetch capability only
fpx pair -p tripadvisor                              # prints a pair code → approve in ContextMint Bridge
```

Requires the **ContextMint Bridge** extension
([releases](https://github.com/nullnet-app/contextmint-bridge/releases) —
Chrome: load the chrome zip unpacked; Safari isn't available yet, so use Chrome for now)
with an open `www.tripadvisor.com` tab. ContextMint Bridge is the fetchproxy extension renamed, same maintainer; source at https://github.com/nullnet-app/contextmint-bridge — build it or verify the release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`. This covers attractions, hotels, and restaurants — it does **not**
return individual review text (only the aggregate rating/count). Fetch +
parse recipe: `references/web-fallback.md`.

### fpx exit codes (fetch verbs)

- `0` — success.
- `2` — bridge unavailable: extension not connected / pairing pending →
  `fpx pair -p tripadvisor`.
- `3` — bot wall: the tab hasn't cleared DataDome → open/refresh a
  `www.tripadvisor.com` tab and retry.
- `4` — upstream non-2xx from TripAdvisor.

## Notes

- Terra reads only — nothing here mutates TripAdvisor data.
- This project (`tripadvisor-mcp`) is developed and maintained by AI
  (Claude Code).
