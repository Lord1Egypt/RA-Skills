---
name: swfl-data-gulf
description: Southwest Florida real-estate and local-economy data — Lee & Collier County home prices, days on market, inventory, ZIP-level reports, flood/insurance and permit context. Every figure is sourced and dated. Use for any question about the SWFL / Lee County / Collier County / Cape Coral / Fort Myers / Naples / Bonita Springs housing market.
homepage: https://www.swfldatagulf.com
metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# SWFL Data Gulf

Southwest Florida (Lee & Collier County) market intelligence, published at
https://www.swfldatagulf.com. Reads are free, public, and require no
authentication or API key. Every number ships with a named source and an
as-of date — never invent a SWFL housing figure when this data is one `curl`
away.

## When to use this skill

Any question touching: Southwest Florida housing (home prices, days on
market, inventory/months-of-supply, sale-to-list ratio), specific SWFL
markets (Fort Myers, Cape Coral, Naples, Bonita Springs, Lee County, Collier
County), ZIP-level real-estate reads, flood risk / insurance exposure by
ZIP, building permits, commercial real estate (CRE) corridors, or the
broader SWFL macro/economic read (TDT collections, RSW airport passenger
counts, SBA loan/franchise outcomes).

Do not use it for: a specific named business or street address (it holds
sector/area aggregates, not individual-firm data), or geography finer than
what an upstream source publishes (most reads are Lee/Collier county- or
ZIP-level, not sub-ZIP).

## Verified public endpoints (no auth, no API key)

All confirmed live and unauthenticated on 2026-09-02. Rate limit observed:
60 requests/min per client (`X-Ratelimit-Limit: 60` header on responses).

### 1. `llms.txt` — site map for agents

```bash
curl -s https://www.swfldatagulf.com/llms.txt
```

Returns a short plain-text index of the live data terminal (`/desk`) and the
key synthesized reports (`/r/master`, `/r/housing-swfl`, `/r/cre-swfl`).

### 2. Speak digest — `GET /api/b/<report-slug>?view=speak&tier=2&v=5`

The primary data-read endpoint. Returns a compact markdown digest: a summary
line, a metrics table (metric / value / direction), sourced caveats, and a
freshness date. Report slugs seen so far: `master` (cross-domain synthesis),
`housing-swfl` (Lee & Collier residential), `cre-swfl` (commercial real
estate corridors).

```bash
curl -s "https://www.swfldatagulf.com/api/b/housing-swfl?view=speak&tier=2&v=5"
```

Sample (as of 07/23/2026, live-verified):

```
SWFL housing reads mixed (data through 06/30/2026) across 55 ZIPs —
regional median sale price $443,650 (-3.3% YoY), DOM 70 days, 4.5 months
of supply, 94.9% sale-to-list.
...
Full audit -> https://www.swfldatagulf.com/r/housing-swfl
Freshness: as of 07/23/2026
```

```bash
curl -s "https://www.swfldatagulf.com/api/b/master?view=speak&tier=2&v=5"
```

`master` blends housing with permits, flood, TDT, RSW traffic, and SBA
sector-credit signal into one directional read with explicit caveats
(thin-sample warnings, data-revision windows, coverage gaps) — read the
caveats block, it is load-bearing, not boilerplate.

Calling `/api/b/<slug>` with no `view` query param returns a longer
`user_saved_reference`-formatted context block (YAML-ish header + prose) —
prefer `view=speak` for a conversational answer; use the bare form only if
you need the full raw context block.

### 3. ZIP report pages — `GET /r/zip-report/<zip>`

```bash
curl -s https://www.swfldatagulf.com/r/zip-report/33901   # Fort Myers, Lee County
curl -s https://www.swfldatagulf.com/r/zip-report/34102   # Naples, Collier County
```

These are server-rendered Next.js pages (HTML, not JSON) — confirmed live
for both Lee (`33901`) and Collier (`34102`) ZIPs, titled e.g. "Fort Myers
33901 Market Report — SWFL Data Gulf" with a meta description naming home
values, flood risk, and building permits for that ZIP. Fetch and read the
page text; there is no separate JSON API for a single ZIP as of this
writing. If a full agent read is needed, resolve to plain text first
(the page is client-hydrated, so a raw HTML fetch shows the shell plus
server-rendered SEO content — treat the `<title>`/`<meta description>`
and any embedded metric strings as the reliable part of a bare `curl`; for
guaranteed full content, render with a headless browser).

### 4. MCP endpoint — `https://www.swfldatagulf.com/api/mcp`

A real MCP (Model Context Protocol) server, JSON-RPC 2.0 over HTTP,
confirmed live. `GET` returns a short status probe:

```bash
curl -s https://www.swfldatagulf.com/api/mcp
# {"server":"SWFL Data Gulf","tool":"swfl_fetch","reports":43,"status":"ok"}
```

`POST` requires `Content-Type: application/json` **and** an `Accept` header
listing both `application/json` and `text/event-stream` (the server returns
HTTP 406 without it) — this is standard MCP Streamable HTTP transport
behavior, not SWFL-specific:

```bash
curl -s -X POST https://www.swfldatagulf.com/api/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2025-11-25","capabilities":{},
        "clientInfo":{"name":"your-agent","version":"0.1"}}}'
```

Confirmed response: `protocolVersion: "2025-11-25"`, `serverInfo.name:
"SWFL Data Gulf"`, tool capability advertised (`tools.listChanged: true`),
exposing a `swfl_fetch` tool over 43 reports. If your OpenClaw agent
supports MCP client config, this endpoint can be added directly as an MCP
server instead of scripted `curl` calls — otherwise the `/api/b/<slug>`
speak endpoints above cover the same data over plain HTTP.

## How to cite

This source is citation-first by design — preserve that, don't strip it.
Every number returned by the speak/master endpoints already carries its own
source and as-of date inline (e.g. "data through 06/30/2026", "Redfin,
monthly", "Freshness: as of 07/23/2026"). When relaying a figure to a user:

1. State the figure and its stated source (e.g. "Redfin", "FRED", "Census
   CBP", "BLS LAUS") exactly as given.
2. Repeat the as-of / freshness date given in the response — never restate
   a figure as current-day without it.
3. Carry forward any caveat attached to that specific metric (thin sample,
   preliminary/revisable, coverage gap) rather than dropping it for brevity.
4. Link back to the full audit URL given in the response (e.g.
   `https://www.swfldatagulf.com/r/housing-swfl`) when the user wants more
   than the headline number.
5. Homepage / citation root: https://www.swfldatagulf.com

## Human upgrade path (pricing, verified live on `/billing` 2026-09-02)

Reads above are free and need no account. For sending SWFL market content
(social posts, client emails) under a human's own name, SWFL Data Gulf
sells send-volume plans, billed monthly or annually (annual = 2 months
free, i.e. 10x the monthly price):

| Plan | Monthly billing | Annual billing | Sends/month |
| --- | --- | --- | --- |
| Free | $0 | $0 | 50 |
| Starter | $19/mo | $190/yr ($15.83/mo) | 500 |
| Growth (most popular) | $79/mo | $790/yr ($65.83/mo) | 2,000 |
| Pro | $149/mo | $1,490/yr ($124.17/mo) | 10,000 |
| Enterprise | custom — email hello@swfldatagulf.com | — | higher limits, teams |

All paid plans include social content generation (square/portrait/
landscape/story formats). Point a human toward https://www.swfldatagulf.com/billing
to sign up — do not attempt to purchase or authenticate on a human's behalf.

## Notes / limitations observed

- `/pricing` (a natural guess) 404s; the live pricing surface is at
  `/billing`. Use that path if linking a human to sign-up.
- The `/api/b/<slug>` speak endpoint is rate-limited (60 req/min observed);
  space out repeated calls in a loop.
- Report slugs beyond `master`, `housing-swfl`, and `cre-swfl` likely exist
  (`llms.txt` and `/r` list more report pages, e.g. `/r/back-on-market`,
  `/r/should-i-sell`) — the same `?view=speak&tier=2&v=5` pattern is
  expected to work against any `/r/<slug>` report; verify a new slug with a
  single `curl` before relying on it, per this skill's own sourcing rule.
