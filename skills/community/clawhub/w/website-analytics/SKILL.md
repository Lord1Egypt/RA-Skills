---
name: website-analytics
description: Google Analytics (GA4) for AI agents — traffic stats, sources, campaigns, referrals, landing pages, events, and conversion funnels across all your websites from one CLI. Web analytics without the dashboard.
---

# Website Analytics (fleets)

Read-only GA4 analytics for every site you run, via the [fleets](https://fleets.run) CLI. One login, all sites, agent-friendly output (`--json` on everything).

## Setup (once)

```bash
npx -y fleets login --browser   # device flow: opens URL + 8-char code
fleets add <domain> --detect     # create site, auto-link GA4 + Search Console
fleets list                      # confirm sites + see sparklines
```

Token alternative: `fleets login --token fl_xxx` or `export FLEETS_TOKEN=fl_xxx`.

## Commands

Slug-first: `fleets <slug> <command> [--range 7d|30d|90d|24h] [--json] [--limit N]`

| Command | Returns |
|---|---|
| `fleets <slug>` | GA4 summary (visitors, pageviews, trend) |
| `fleets <slug> sources` | Traffic sources |
| `fleets <slug> campaigns` | UTM campaign performance |
| `fleets <slug> referrals` | Referral traffic |
| `fleets <slug> landers` | Top landing pages |
| `fleets <slug> events` | GA4 events |
| `fleets <slug> users` | Country + device breakdown |
| `fleets <slug> funnel <step1> <step2> ...` | Conversion funnel between steps |
| `fleets <slug> query "<question>"` | Natural-language analytics query |
| `fleets <slug> export` | Daily CSV/JSON export |
| `fleets list` | All sites at a glance |

## Examples

```bash
fleets myblog sources --range 30d --json
fleets shop funnel /pricing /checkout /thanks --range 90d
fleets myblog query "which campaign drove the most signups last week?"
```

## MCP alternative

Prefer tools over shell? Same data as a stdio MCP server:

```json
{ "mcpServers": { "fleets": { "command": "npx", "args": ["-y", "fleets-mcp"] } } }
```

Tools: `list_sites`, `stats`, `sources`, `campaigns`, `referrals`, `landers`, `events`, `users`, `devices`, `demographics`, `funnel`, `ask`. All read-only.

## Notes

- Read-only: this skill can never modify your GA4 property or site.
- For Search Console / SEO data use the `seo-search-console` skill; for speed + edge metrics use `site-speed-monitoring`.
