---
name: wakapi
description: >-
  Wakapi coding stats (summaries, projects, today status, totals) via a small Python
  CLI. Requires WAKAPI_URL. WAKAPI_API_KEY is HTTP Basic (Authorization Basic base64(key))
  for all calls except health, which uses native GET /api/health (no key). Use for
  Wakapi / self-hosted coding time and project/language breakdowns.
homepage: https://github.com/chensoul/wakapi-skill
repository: https://github.com/chensoul/wakapi-skill
metadata: {"openclaw": {"requires": {"env": ["WAKAPI_URL", "WAKAPI_API_KEY"]}, "primaryEnv": "WAKAPI_API_KEY"}}
---

# Wakapi API query

## When to use

The user wants **read-only** stats from a **Wakapi** instance: time ranges, projects/languages, today’s status line, all-time total, or project list.

## Documentation map

| Document | Use it for |
|----------|------------|
| **This file** | Env vars, subcommand overview, copy-paste CLI examples |
| **[references/wakapi-api.md](references/wakapi-api.md)** | Full URLs (`/api/health` vs compat prefix), **`stats` path** vs **`summaries` query `range`**, preset table, optional **summaries** filters, **curl**, timeouts |

## Requirements

| Category | Detail |
|----------|--------|
| **Runtime** | **Python 3**, **stdlib only**. Entry: [`scripts/wakapi_query.py`](scripts/wakapi_query.py). Run from the **skill root** (directory that contains `SKILL.md`). |
| **Environment** | **`WAKAPI_URL`** — instance **origin**, no trailing `/` (required). **`WAKAPI_API_KEY`** — required for every subcommand **except** **`health`**. |
| **Network** | Outbound **HTTPS** (or `http://` if your instance uses it) to **`WAKAPI_URL`**. |
| **Authentication** | **HTTP Basic**: `Authorization: Basic` + base64(**API key only**). |
| **Registry** | **`metadata.openclaw`**: **`requires.env`** = `["WAKAPI_URL", "WAKAPI_API_KEY"]`, **`primaryEnv`** = **`WAKAPI_API_KEY`**. |

No other environment variables are read by the CLI.

## Subcommands at a glance

| Subcommand | API key? | What it calls |
|------------|----------|----------------|
| **`health`** | No | Native **`GET {WAKAPI_URL}/api/health`** (JSON if `Content-Type: application/json`) |
| **`projects`** | Yes | Compat **`…/compat/wakatime/v1/users/current/projects`** |
| **`status-bar`** | Yes | **`{WAKAPI_URL}/api/v1/users/current/statusbar/today`** |
| **`all-time-since`** | Yes | Compat **`…/all_time_since_today`** |
| **`stats <range>`** | Yes | Compat **`…/stats/{range}`** — `{range}` is a **URL path** segment |
| **`summaries`** | Yes | Compat **`…/summaries`** — **`--range`** *or* **`--start` + `--end`**; optional **`--project`**, **`--branches`**, **`--timezone`**, **`--timeout`** (API), **`--writes-only`** |

**`stats`** vs **`summaries`:** different meanings of “range”; see **[references/wakapi-api.md](references/wakapi-api.md)**.

## Prerequisites

1. Set **`WAKAPI_URL`**. Set **`WAKAPI_API_KEY`** for all commands except **`health`**.
2. Do **not** paste secrets into chat. If the key is missing, ask the user to configure the environment.

## Usage

Run from the skill root. **`--help`** / **`summaries --help`** list all flags.

```bash
# WAKAPI_URL required always; WAKAPI_API_KEY required for all subcommands except health.
export WAKAPI_URL="https://your-wakapi.example"
export WAKAPI_API_KEY="…"

# --- Help ---
python3 scripts/wakapi_query.py --help
python3 scripts/wakapi_query.py summaries --help

# --- health: native GET /api/health (no API key); JSON body if Content-Type: application/json ---
python3 scripts/wakapi_query.py health
python3 scripts/wakapi_query.py health --timeout 30   # HTTP socket timeout (default 15s)

# --- projects / all-time-since: compat …/compat/wakatime/v1/... | status-bar: /api/v1/... ---
python3 scripts/wakapi_query.py projects
python3 scripts/wakapi_query.py projects --timeout 120
python3 scripts/wakapi_query.py status-bar
python3 scripts/wakapi_query.py all-time-since

# --- stats: compat path …/stats/{range} — Wakapi named intervals only (see models/interval.go), NOT YYYY / YYYY-MM ---
python3 scripts/wakapi_query.py stats today
python3 scripts/wakapi_query.py stats yesterday
python3 scripts/wakapi_query.py stats week
python3 scripts/wakapi_query.py stats month
python3 scripts/wakapi_query.py stats year              # this calendar year (not "stats 2026")
python3 scripts/wakapi_query.py stats last_7_days
python3 scripts/wakapi_query.py stats last_30_days
python3 scripts/wakapi_query.py stats last_6_months
python3 scripts/wakapi_query.py stats last_year         # rolling ~12 months in Wakapi
python3 scripts/wakapi_query.py stats all_time
python3 scripts/wakapi_query.py stats last_7_days --timeout 300   # API keystroke query param, not HTTP socket
# Fixed calendar month/year → use summaries --start/--end, e.g. March 2026:
# python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-31

# --- summaries --range: compat ?range= (Wakapi interval aliases; snake_case and Title Case) ---
# Calendar day / week / month / year (lowercase tokens)
python3 scripts/wakapi_query.py summaries --range today
python3 scripts/wakapi_query.py summaries --range yesterday
python3 scripts/wakapi_query.py summaries --range week
python3 scripts/wakapi_query.py summaries --range month
python3 scripts/wakapi_query.py summaries --range year
# Rolling windows
python3 scripts/wakapi_query.py summaries --range last_7_days
python3 scripts/wakapi_query.py summaries --range "Last 7 Days"          # same interval as last_7_days
python3 scripts/wakapi_query.py summaries --range "Last 7 Days from Yesterday"
python3 scripts/wakapi_query.py summaries --range last_14_days
python3 scripts/wakapi_query.py summaries --range last_30_days
# Previous week / month; rolling 12 months (not calendar year)
python3 scripts/wakapi_query.py summaries --range last_week
python3 scripts/wakapi_query.py summaries --range last_month
python3 scripts/wakapi_query.py summaries --range last_year
python3 scripts/wakapi_query.py summaries --range all_time              # epoch → now; can be large/slow

# --- summaries: optional filters (with --range or with --start/--end) ---
python3 scripts/wakapi_query.py summaries --range last_7_days --timezone Asia/Shanghai
python3 scripts/wakapi_query.py summaries --range week --project myapp --branches main,develop
python3 scripts/wakapi_query.py summaries --range today --writes-only true --timeout 300

# --- summaries: --start + --end (cannot use with --range) ---
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07 --timezone America/New_York
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07 --branches main,develop
python3 scripts/wakapi_query.py summaries --start 2026-03-18 --end 2026-03-18 \
  --project myapp --branches main,develop --timezone Asia/Shanghai --writes-only false

# --- Debug ---
python3 scripts/wakapi_query.py -d projects
```

More **`--range`** values and interval semantics: **[references/wakapi-api.md](references/wakapi-api.md)**.

## Interpreting output

Responses are JSON on stdout. Summarize totals and human-readable fields for the user.

On HTTP errors the CLI prints JSON to **stderr** and exits non-zero. **`health`** uses **`GET /api/health`**: stdout is **`{"healthy": true|false}`** and may include **`detail`** when unhealthy (Wakapi app/db flags).

## If something fails

- **`WAKAPI_URL`** reachable? **`WAKAPI_API_KEY`** set (except **`health`**)?
- **Summaries:** use **`--range`** *or* both **`--start`** and **`--end`** (same calendar day → same date twice). Optional **`--project`**, **`--branches`**, **`--timezone`**, **`--timeout`** (API), **`--writes-only`**. Run **`summaries --help`**.
- Debug: **`-d`** / **`--debug`**. **`--timeout`** on `health` / `projects` / `status-bar` / `all-time-since` = **HTTP socket** time. On **`stats`** / **`summaries`**, **`--timeout`** = **API** keystroke parameter; HTTP stays **60** s.
