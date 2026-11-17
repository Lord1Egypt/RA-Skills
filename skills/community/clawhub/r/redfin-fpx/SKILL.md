---
name: redfin-fpx
description: >-
  Query redfin.com (US real-estate portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the redfin-mcp server — resolve
  locations/addresses, search for-sale listings, read property detail
  (price, beds/baths, price history, tax history), market trends,
  comparable rentals, climate risk, photos, and (signed-in) saved homes
  and saved searches, via one-shot calls through a signed-in browser tab.
  Use when you want Redfin data without the MCP, in a script, or on a
  machine where the MCP isn't installed.
---

# Redfin via fpx (no MCP)

Redfin fronts `www.redfin.com` — including every `/stingray/...` JSON
endpoint — with an AWS WAF challenge that blocks plain `curl`/Node
requests regardless of headers. `fpx` routes the request through the
user's own signed-in browser tab (the ContextMint Bridge extension), which has
already cleared the challenge, so the same request succeeds. Most reads
are anonymous (no Redfin login needed — just an open tab); the saved-homes
and saved-searches endpoints additionally require the tab to be signed in
to redfin.com.

This is the same data the `redfin_*` MCP tools return, reached with one
CLI call instead of a running server. Every call rides through the bridge
(no bootstrap-then-direct-fetch shortcut) — Redfin validates each request
at the session level.

## One-time setup

```sh
npm install -g @fetchproxy/cli              # provides `fpx`
fpx profile add redfin --domain redfin.com  # only the fetch capability is needed
fpx pair -p redfin                          # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
(from https://github.com/nullnet-app/contextmint-bridge/releases), with an
open `www.redfin.com` tab, and its Chrome **Site access** allowing
`redfin.com`. Pairing persists — after the first approval every later
`fpx` call reuses it.

ContextMint Bridge is the fetchproxy extension renamed, same maintainer (see https://github.com/chrischall/fetchproxy#extension); source at https://github.com/nullnet-app/contextmint-bridge — build it yourself or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`. Safari isn't available yet — use Chrome.

## Core call

Almost every endpoint is a GET to a `/stingray/...` path. Redfin prefixes
every stingray JSON body with a literal anti-CSRF `{}&&`, so strip that
before piping to `jq`:

```sh
fpx get 'https://www.redfin.com/stingray/api/gis?...' -p redfin \
  | sed -E 's/^\{\}&&//' \
  | jq '.payload.homes'
```

Every stripped body is an envelope `{ version, errorMessage, resultCode,
payload }` — check `resultCode == 0` before trusting `payload` (a nonzero
code means Redfin rejected the request; `errorMessage` explains why).

Ready-to-run request paths (autocomplete, search, property detail, price
history, market trends, comparable rentals, climate risk, saved homes)
are in `references/stingray-endpoints.md`. Exhaustive field lists live in
the repo at `src/tools/*.ts` — the endpoints here are compact,
live-verified subsets.

## The one rule: resolve the location/address first

Redfin search takes numeric **region_id + region_type**, never place
names, and property detail wants a **propertyId + listingId** pair.
Always autocomplete first:

```sh
fpx get 'https://www.redfin.com/stingray/do/location-autocomplete?location=Seattle&start=0&count=1&v=2&iss=false&ooa=true&mrs=false' \
  -p redfin | sed -E 's/^\{\}&&//' \
  | jq -r '.payload.sections[] | select(.name=="Places") | .rows[0] | "\(.id)\t\(.name)"'
# 2_16163  Seattle
```

`id` is formatted `"<region_type>_<region_id>"`. An `Addresses` section
(instead of/alongside `Places`) means autocomplete resolved a specific
home rather than a region — its `url` embeds the home's canonical
`/home/<id>` path (use that with the property-detail calls instead of a
region search).

## Two-step property detail

A homedetails URL only gets you `propertyId`/`listingId` via one extra
round trip:

1. `GET /stingray/api/home/details/initialInfo?path=<url-path>` → `{propertyId, listingId, ...}`
2. `GET /stingray/api/home/details/aboveTheFold?propertyId=…&listingId=…&accessLevel=1` → the actual detail

If you already have `property_id` + `listing_id` (e.g. from a search
result), skip step 1 and go straight to `aboveTheFold` (and
`belowTheFold` for price/tax history).

## Exit codes (fetch verbs)

- `0` — success (still check the stripped envelope's `resultCode`).
- `2` — bridge unavailable: extension not connected or pairing pending → run `fpx pair -p redfin`, confirm a redfin.com tab is open.
- `3` — bot wall: the tab hasn't cleared the AWS WAF challenge → open/refresh a `www.redfin.com` tab and retry.
- `4` — upstream non-2xx from Redfin.

## Notes

- Anonymous reads only work for search/property/market/history/rentals;
  `redfin_get_saved_homes` / `redfin_get_saved_searches` need the bridged
  tab signed in to redfin.com.
- Climate-risk data is **not** a JSON endpoint — it's regex-extracted
  from the server-rendered homedetails HTML (`fpx get` the page, then
  grep/extract; see `references/stingray-endpoints.md` §7 for the field
  names to look for). There's no clean stingray path for it.
- `fpx health -p redfin` shows bridge connection state when a call fails.
- This project is developed and maintained by AI (Claude).
