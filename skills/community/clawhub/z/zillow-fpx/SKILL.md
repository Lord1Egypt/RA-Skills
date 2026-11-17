---
name: zillow-fpx
description: >-
  Query zillow.com (US real-estate portal) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the zillow-mcp server — search
  listings, pull a full property record by zpid, price/tax/Zestimate
  history, photos, market reports, and your signed-in saved
  searches/homes, all via one-shot HTTP calls through a signed-in browser
  tab. Use when you want Zillow data without the MCP, in a script, or on
  a machine where the MCP isn't installed.
---

# Zillow via fpx (no MCP)

Zillow fronts `www.zillow.com` with a PerimeterX bot-wall that blocks
plain `curl`/Node requests, and several tools (saved searches/homes)
need an actual signed-in session. `fpx` routes every request through the
user's own signed-in browser tab (the ContextMint Bridge extension), so the
same page loads that a real visit would.

This is the same data the `zillow_*` MCP tools return — every property
tool is a scrape of Zillow's server-rendered Next.js pages
(`__NEXT_DATA__`), not a documented JSON API. No credentials are stored
anywhere; auth (for the saved-data endpoints) is just "have a signed-in
zillow.com tab open."

## One-time setup

```sh
npm install -g @fetchproxy/cli             # provides `fpx`
fpx profile add zillow --domain zillow.com # only the fetch capability is needed
fpx pair -p zillow                         # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
([releases](https://github.com/nullnet-app/contextmint-bridge/releases)), with an
open `www.zillow.com` tab, and its Chrome **Site access** allowing
`zillow.com`. (ContextMint Bridge is the renamed fetchproxy extension from the
same maintainer; build it from source or verify the release zip with
`shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.) For the saved-searches/saved-homes calls, that tab must
also be **signed in**. Pairing persists — after the first approval every
later `fpx` call reuses it.

## Core call

Every endpoint here is a GET of a server-rendered HTML page (Zillow is a
Next.js app; the whole page state is embedded as JSON in a
`<script id="__NEXT_DATA__">` tag) — there is no JSON API to hit
directly. Fetch, then pull the JSON out of the HTML:

```sh
fpx get 'https://www.zillow.com/homedetails/12345_zpid/' -p zillow > /tmp/page.html
python3 -c '
import re, sys, json
html = open("/tmp/page.html").read()
m = re.search(r"<script[^>]*id=[\"\x27]__NEXT_DATA__[\"\x27][^>]*>(.*?)</script>", html, re.S | re.I)
print(json.dumps(json.loads(m.group(1))["props"]["pageProps"]))
' | jq '.'
```

`references/pages.md` has the extractor as a reusable one-liner plus the
per-page `pageProps` field paths (search results, property detail,
photos, price/tax/Zestimate history, saved searches/homes, market
report) and the address-autocomplete GraphQL call, all transcribed from
the MCP's `src/tools/*.ts` (which parse the exact same pages).

## The one rule: resolve the location first (search only)

`zillow_search_properties`'s two-step dance is exactly what
`/homes/<slug>_rb/` needs: fetch the bare slug path first to get Zillow's
resolved `regionSelection` + `mapBounds`, THEN re-fetch with those pinned
into a `searchQueryState` query param alongside your filters — a filtered
fetch without the pinned region silently falls back to the user's last
search region instead of honoring the slug. A full-address query can
resolve straight to a `homedetails` page (no region at all) — see
`references/pages.md` §1 for both shapes. Property lookups by `zpid`
need no resolve step — `/homedetails/<zpid>_zpid/` is direct.

## Auth

No login is stored or passed by `fpx` — the saved-searches
(`/myzillow/SavedSearches`) and saved-homes (`/myzillow/favorites`) pages
simply render your saved data (or redirect to `/user/login`) depending on
whether the tab riding the bridge is signed in. Everything else is
anonymous.

## Exit codes (fetch verbs)

- `0` — success. A signed-out redirect (`/user/login`, `?login=true`) or
  a captcha interstitial (body contains `captcha-delivery`, small body)
  can still ride in a `0` response — check the fetched HTML, `fpx`
  doesn't know Zillow's sign-in/bot-wall markers.
- `2` — bridge unavailable: extension not connected or pairing pending →
  run `fpx pair -p zillow`, confirm a zillow.com tab is open.
- `3` — bot wall: the tab hasn't cleared PerimeterX → open/refresh a
  `www.zillow.com` tab and retry.
- `4` — upstream non-2xx from Zillow.

## Notes

- `fpx health -p zillow` shows bridge connection state when a call fails.
- Zillow publishes no consumer API — these are the same private
  server-rendered pages the zillow.com web app itself loads, reached
  through your own signed-in tab.
- This project is developed and maintained by AI (Claude).
