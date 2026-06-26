---
name: TicketMaster
slug: ticketmaster
version: 1.0.0
homepage: https://clawic.com/skills/ticketmaster
description: Search Ticketmaster events, venues, and attractions with Discovery API filters, market-aware queries, and copy-ready curl and shell helpers.
changelog: Added Discovery API workflows, venue filters, and a local shell helper for faster event lookups.
metadata: {"clawdbot":{"emoji":"🎟️","requires":{"env":["TM_API_KEY"],"bins":["curl"],"config":["~/ticketmaster/"]},"primaryEnv":"TM_API_KEY","os":["linux","darwin","win32"]}}
---

# TicketMaster

Use the open Ticketmaster Discovery API for search and lookup work. Reach for the bundled `ticketmaster.sh` helper when terminal speed matters, and fall back to raw `curl` when exact response shapes matter.

## When to Use

User needs live Ticketmaster listings, venue discovery, attraction lookup, onsale windows, or API-ready search filters. This skill stays inside the open Discovery API surface and keeps reusable defaults local.

## Architecture

Memory lives in `~/ticketmaster/`. If `~/ticketmaster/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/ticketmaster/
├── memory.md   # Preferred locale, market, city, and query defaults
├── queries.md  # Saved queries that worked well
└── logs/       # Optional helper output captures
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and API key bootstrap | `setup.md` |
| Memory template | `memory-template.md` |
| Open endpoints and response map | `endpoints.md` |
| Search recipes and curl examples | `query-patterns.md` |
| Filters, paging, and sort rules | `filters-and-pagination.md` |
| Error handling and quota limits | `errors.md` |
| Local helper CLI wrapper | `ticketmaster.sh` |

Open only the smallest file needed for the task. Most daily work is `query-patterns.md` plus `errors.md`.

## Quick Start

```bash
export TM_API_KEY="..."

./ticketmaster.sh events "coldplay" --city Madrid --country ES --size 5
./ticketmaster.sh venues "wizink" --city Madrid

curl --get "https://app.ticketmaster.com/discovery/v2/events.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "keyword=adele" \
  --data-urlencode "countryCode=GB" \
  --data-urlencode "size=3"
```

## Open Surface

- Open here: Discovery API search and lookup for events, venues, attractions, and classifications.
- Not open here: partner-only offers, cart, checkout, hold, publish, or inventory mutation flows.
- If the user asks for purchase automation, explain the boundary first instead of implying the open API can do it.

## Core Rules

### 1. Start with Discovery API, not purchase assumptions
- Use search and lookup endpoints for events, venues, attractions, and classifications first.
- Do not claim cart, order, hold, or refund actions are available through the open flow.

### 2. Always pass `apikey` as a query parameter
- Official open endpoints expect `apikey`.
- Keep the key in `TM_API_KEY` and out of files, screenshots, and pasted examples.

### 3. Constrain the search before paging
- Prefer `keyword` plus location or identity filters such as `city`, `countryCode`, `dmaId`, `marketId`, `venueId`, or `attractionId`.
- Ticketmaster documents deep paging only while `size * page < 1000`, so tighten filters early.

### 4. Use UTC timestamps and read sales windows carefully
- `startDateTime`, `endDateTime`, and onsale filters should be ISO-8601 UTC strings like `2026-05-01T00:00:00Z`.
- Read `sales.public.startDateTime`, `sales.presales`, and `dates.start` before describing availability.

### 5. Inspect embedded objects, not just the event headline
- Read `_embedded.venues`, `_embedded.attractions`, classifications, locale, and price ranges when present.
- Venue or city mismatches usually mean the query is too broad or the market is cross-listed.

### 6. Respect documented quota and rate limits
- Default quota is 5000 calls per day with 5 requests per second.
- Cache event IDs and venue IDs locally when iterating on the same search space.

### 7. Keep local defaults local
- Store locale, country, city, market, and preferred sort order in `~/ticketmaster/memory.md`.
- Never persist API keys or any purchase data in skill memory.

## Requirements

- `TM_API_KEY` from the Ticketmaster Developer Portal
- `curl` for raw requests and the bundled `ticketmaster.sh` helper
- Optional `jq` if you want prettier local output from `ticketmaster.sh`

## Common Traps

- Using `countryCode` alone for large markets -> noisy result sets and wasted quota.
- Treating Discovery results as purchase confirmation -> the open API exposes listings, not checkout guarantees.
- Paging deep without filters -> results stop being supported once `size * page` reaches 1000.
- Using local time strings -> events shift or disappear; convert to UTC ISO timestamps.
- Ignoring locale -> multilingual markets can return names or links that look inconsistent.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://app.ticketmaster.com/discovery/v2/*.json` | Search keywords, locale, timestamps, IDs, filters, and `apikey` | Search and fetch events, venues, attractions, and classifications |

Use GET discovery calls only. Keep everything else local.

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Search terms, filters, locale, timestamps, and IDs sent to Ticketmaster Discovery API
- Your API key sent as the documented `apikey` query parameter

**Data that stays local:**
- Preferences and defaults in `~/ticketmaster/`
- Saved command patterns and notes you choose to keep

**This skill does NOT:**
- Place orders, hold inventory, or bypass partner-only purchase flows
- Store `TM_API_KEY` in skill memory
- Access files outside `~/ticketmaster/`

## Scope

This skill ONLY:
- Uses the open Ticketmaster Discovery API surface
- Provides copy-ready curl queries and the bundled `ticketmaster.sh` helper
- Stores local search defaults in `~/ticketmaster/`

This skill NEVER:
- Uses hidden or undocumented endpoints
- Claims checkout, refunds, or seat locking through open Discovery API
- Writes secrets into local memory

## Trust

By using this skill, data is sent to Ticketmaster (ticketmaster.com).
Only install if you trust Ticketmaster with your search terms and event lookup data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` — General REST API patterns for request shaping and response inspection
- `booking` — Reservation workflows and confirmation hygiene when discovery turns into action
- `events` — Event-planning workflows around schedules, listings, and logistics

## Feedback
- If useful: `clawhub star ticketmaster`
- Stay updated: `clawhub sync`
