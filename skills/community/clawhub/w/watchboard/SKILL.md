---
name: watchboard
description: "Query Watchboard intelligence dashboards (watchboard.dev) for structured event data, casualties, KPIs, contested claims, and daily digests across 51+ trackers covering conflicts, politics, culture, and science. Use when: (1) user asks about current events covered by a Watchboard tracker (Iran conflict, Gaza, Ukraine, Sinaloa, etc.), (2) user wants structured intelligence data instead of web search, (3) user asks for casualty figures, KPIs, or contested claims about tracked events, (4) user wants a briefing or summary of a tracked topic. NOT for: topics not covered by any tracker, breaking news less than ~24h old (data updates nightly at 6 AM UTC)."
---

# Watchboard Intelligence Dashboards

Query structured intelligence data from [watchboard.dev](https://watchboard.dev) — 51+ trackers covering conflicts, politics, culture, science, and space with AI-curated daily updates and source tiers.

**Zero dependencies** — stdlib only (urllib, json). Works on any machine with Python 3.8+.

## API

Public JSON API at `https://watchboard.dev/api/v1/`. No API key needed. CORS enabled. Data cached 1h server-side.

| Endpoint | Returns |
|----------|---------|
| `/api/v1/trackers.json` | Directory of all trackers with metadata |
| `/api/v1/trackers/{slug}.json` | Full tracker: config, meta, KPIs, digest, recent events |
| `/api/v1/breaking.json` | Trackers with active breaking news |
| `/api/v1/kpis/{slug}.json` | Just KPIs for a tracker |
| `/api/v1/events/{slug}.json` | Last 30 events for a tracker |
| `/api/v1/search-index.json` | All event titles for client-side search |

## CLI

Run `python3 scripts/watchboard.py <command>`:

| Command | Use | Token cost |
|---------|-----|-----------|
| `list [--domain X] [--status X]` | Show all trackers (dynamic from API) | Low |
| `summary <slug>` | Meta + latest digest + top KPIs | Low (~2-3KB) |
| `breaking` | All trackers with breaking news | Low-Medium |
| `events <slug> [--limit N]` | Recent events (last 30) | Medium |
| `kpis <slug>` | All KPIs with contested notes | Medium |
| `search <query> [--tracker slug]` | Search events across all/one tracker | Medium |
| `detail <slug>` | Full tracker data (all sections) | Medium-High |
| `rss <slug>` | RSS feed (fallback) | Low |

Add `--json` to any command for raw JSON output (useful for programmatic processing).

### Examples

```bash
# Quick briefing on Iran conflict
python3 scripts/watchboard.py summary iran-conflict

# What's breaking right now?
python3 scripts/watchboard.py breaking

# Casualty figures and key metrics
python3 scripts/watchboard.py kpis ukraine-war

# Find events mentioning "ceasefire"
python3 scripts/watchboard.py search ceasefire

# Events in Gaza, last 10
python3 scripts/watchboard.py events gaza-war --limit 10

# All conflict trackers
python3 scripts/watchboard.py list --domain conflict

# Full detail with raw JSON
python3 scripts/watchboard.py --json detail iran-conflict
```

## Strategy

1. **Quick briefing** → `summary <slug>` — meta + digest + top KPIs in one call
2. **What's happening now?** → `breaking` — all trackers with active developments
3. **Specific data** (casualties, oil prices, KPIs) → `kpis <slug>` with contested notes
4. **Recent events** → `events <slug>` — last 30 events with sources and types
5. **Find specific events** → `search "keyword"` across all trackers, or `--tracker slug` to narrow
6. **Deep dive** → `detail <slug>` — everything in one call (config, meta, KPIs, digest, events)
7. **RSS fallback** → `rss <slug>` — if JSON API is unavailable

## Data quality

Every data point has a source tier:
- **Tier 1**: Official/primary sources (Pentagon, CENTCOM, government statements)
- **Tier 2**: Major news outlets (Reuters, AP, Al Jazeera, NPR)
- **Tier 3**: Academic/analytical sources
- **Tier 4**: Unverified/social media

KPIs include contested flags with detailed notes showing conflicting claims from different sources.

## Caching

Results cached 1h locally in `/tmp/watchboard-cache/`. Server data updates 1-4 times daily (nightly digest at ~6 AM UTC, breaking events throughout the day).

## Tracker discovery

The tracker list is **dynamic** — fetched from the API at runtime, not hardcoded. Currently 51+ trackers across domains:

- **conflict**: iran-conflict, gaza-war, ukraine-war, sudan-conflict, etc.
- **governance**: sheinbaum-presidency, amlo-presidency, trump-presidencies, etc.
- **culture**: bad-bunny, bts, world-cup-2026
- **space**: artemis-2, spacex-history
- **human-rights**: ayotzinapa, ice-history
- **science**: quantum-theory, covid-pandemic
- **historical**: world-war-2, september-11, tlatelolco-1968

Use `list` to see the current full directory. Use `list --domain conflict` to filter.
