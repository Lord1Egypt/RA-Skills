# Wakapi API (this skill)

Companion to **[SKILL.md](../SKILL.md)** — URLs, authentication, **`stats`** vs **`summaries`**, interval presets, **curl**, and timeouts.

## What this skill calls

[Wakapi](https://github.com/muety/wakapi) exposes a **native** REST API and a **compat** layer under **`/api/compat/wakatime/v1`** (route shape familiar to editor plugins). This CLI uses **read-only GET** plus native **`GET /api/health`**.

## Official resources

- Project: <https://github.com/muety/wakapi>
- Example public instance: <https://wakapi.dev>
- Native health (source): [`routes/api/health.go`](https://github.com/muety/wakapi/blob/master/routes/api/health.go)

## Environment

| Variable | Required | Notes |
|----------|----------|--------|
| **`WAKAPI_URL`** | Yes | Origin only, **no** trailing `/` (e.g. `https://wakapi.dev`). |
| **`WAKAPI_API_KEY`** | Yes* | HTTP Basic, key only. *Not used for **`health`**. |

## Authentication

For **projects**, **stats**, **summaries**, **all-time-since**, **status-bar**:

```http
Authorization: Basic <base64(api_key)>
Accept: application/json
```

**`GET /api/health`** is **unauthenticated** in default Wakapi routing (liveness + DB ping). This CLI sends **`Content-Type: application/json`** so the response body is JSON (`{"app":1,"db":1}`).

## CLI output (matches `wakapi_query.py`)

| Case | Stream | Notes |
|------|--------|--------|
| Success | stdout | JSON; authenticated subcommands use **indented** JSON. **`health`** prints **`{"healthy": …}`** and may add **`detail`** when unhealthy. |
| HTTP/API error | stderr | JSON with **`http_status`** / **`error`**; exits **1**. |
| Network / URL error | stderr | Text message; exits **2**. |

## Path prefixes

Let **`ORIGIN`** = **`WAKAPI_URL`** (no trailing `/`).

| Use case | Base path |
|----------|-----------|
| **Health** | **`{ORIGIN}/api/health`** |
| Most read-only stats (compat) | **`{ORIGIN}/api/compat/wakatime/v1/users/current/...`** |
| **Status bar today** only | **`{ORIGIN}/api/v1/users/current/statusbar/today`** |

## Endpoints used by this CLI (GET)

| Subcommand | URL |
|------------|-----|
| `health` | **`{ORIGIN}/api/health`** |
| `projects` | `{ORIGIN}/api/compat/wakatime/v1/users/current/projects` |
| `all-time-since` | `…/compat/wakatime/v1/users/current/all_time_since_today` |
| `stats <range>` | `…/compat/wakatime/v1/users/current/stats/{range}` |
| `summaries` | `…/compat/wakatime/v1/users/current/summaries` |
| `status-bar` | `{ORIGIN}/api/v1/users/current/statusbar/today` |

`{range}` in **`stats`** must be a **named interval** Wakapi understands (passed to `ParseInterval` / [`models/interval.go`](https://github.com/muety/wakapi/blob/master/models/interval.go)), e.g. `last_7_days`, `today`, `year`. **Not** a calendar **`YYYY`** or **`YYYY-MM`** path segment (unlike hosted WakaTime’s stats API) — use **`summaries --start` / `--end`** for a fixed calendar window.

### `stats` vs `summaries` (“range” is not the same)

| Command | Where `range` lives | Typical values (Wakapi) |
|---------|---------------------|-------------------------|
| **`stats <range>`** | **Path** after `/stats/` | `today`, `yesterday`, `week`, `month`, `year`, `last_7_days`, `last_30_days`, `last_6_months`, `last_year`, `all_time`, … — see [compat stats handler](https://github.com/muety/wakapi/blob/master/routes/compat/wakatime/v1/stats.go) / `interval.go` |
| **`summaries`** | **Query** `range=…` **or** `start`+`end` | Same **interval aliases** as presets, **or** explicit **`YYYY-MM-DD`** dates |

Do not assume a **`summaries`** preset string works as a **`stats`** path segment without checking (and vice versa).

**`stats` CLI flags:**

| Flag | Query param | Meaning |
|------|-------------|--------|
| `--timeout N` | `timeout` | Keystroke timeout (**API**), not HTTP socket (HTTP **60** s) |
| `--writes-only true\|false` | `writes_only` | |

**`summaries` CLI flags:**

| Flag | Query param | Notes |
|------|-------------|--------|
| `--range VALUE` | `range` | Mutually exclusive with `--start`/`--end` |
| `--start` / `--end` | `start`, `end` | `YYYY-MM-DD`, both required together |
| `--timezone` | `timezone` | IANA TZ |
| `--project` | `project` | |
| `--branches` | `branches` | Comma-separated |
| `--timeout N` | `timeout` | API keystroke timeout |
| `--writes-only` | `writes_only` | |

## Summaries: `--range` presets (Wakapi)

Wakapi resolves `range` with its interval model ([`models/interval.go`](https://github.com/muety/wakapi/blob/master/models/interval.go), [`helpers/interval.go`](https://github.com/muety/wakapi/blob/master/helpers/interval.go)). Many **aliases** map to the same interval (e.g. `7_days`, `last_7_days`, `Last 7 Days`).

### Fixed dates

Use **`--start` and `--end`** (`YYYY-MM-DD`). One calendar day → **same date twice**.

### Common `--range` values (CLI passes through as `range=`)

| `--range` (examples) | Meaning |
|----------------------|--------|
| `today` | Start of today → now |
| `yesterday`, `day` | Previous calendar day |
| `week` | This week (per user **week start**) → now |
| `month` | This calendar month → now |
| `year` | This calendar year → now |
| `last_7_days`, `7_days` | Rolling 7 days ending now |
| `last_14_days`, `14_days` | Rolling 14 days |
| `last_30_days`, `30_days` | Rolling 30 days |
| `last_week` | Previous full week (depends on `start_of_week`) |
| `last_month` | Previous calendar month |
| `last_year`, `12_months`, `last_12_months` | **Rolling 12 months** ending now — *not* “calendar year 2024” |
| `all_time`, `any`, `All Time` | Epoch → now; can be **large/slow** |

More aliases: `Last 7 Days from Yesterday`, `This Week`, `6_months` / `last_6_months`, etc. See **`models/interval.go`** and [`routes/compat/wakatime/v1/summaries.go`](https://github.com/muety/wakapi/blob/master/routes/compat/wakatime/v1/summaries.go).

## CLI examples (aligned with SKILL.md)

```bash
export WAKAPI_URL="https://your-wakapi.example"
export WAKAPI_API_KEY="…"

python3 scripts/wakapi_query.py --help
python3 scripts/wakapi_query.py summaries --help

# health → GET {ORIGIN}/api/health (no key); --timeout = HTTP socket (default 15s)
python3 scripts/wakapi_query.py health
python3 scripts/wakapi_query.py health --timeout 30

# projects / all-time-since → compat; status-bar → /api/v1/... only
python3 scripts/wakapi_query.py projects
python3 scripts/wakapi_query.py projects --timeout 120
python3 scripts/wakapi_query.py status-bar
python3 scripts/wakapi_query.py all-time-since

# stats → …/compat/.../stats/{range} (named intervals only; no stats/2026)
python3 scripts/wakapi_query.py stats today
python3 scripts/wakapi_query.py stats yesterday
python3 scripts/wakapi_query.py stats week
python3 scripts/wakapi_query.py stats month
python3 scripts/wakapi_query.py stats year
python3 scripts/wakapi_query.py stats last_7_days
python3 scripts/wakapi_query.py stats last_30_days
python3 scripts/wakapi_query.py stats last_6_months
python3 scripts/wakapi_query.py stats last_year
python3 scripts/wakapi_query.py stats all_time
python3 scripts/wakapi_query.py stats last_7_days --timeout 300

# summaries --range → ?range= (Wakapi intervals; see table above)
python3 scripts/wakapi_query.py summaries --range today
python3 scripts/wakapi_query.py summaries --range yesterday
python3 scripts/wakapi_query.py summaries --range week
python3 scripts/wakapi_query.py summaries --range month
python3 scripts/wakapi_query.py summaries --range year
python3 scripts/wakapi_query.py summaries --range last_7_days
python3 scripts/wakapi_query.py summaries --range "Last 7 Days"
python3 scripts/wakapi_query.py summaries --range "Last 7 Days from Yesterday"
python3 scripts/wakapi_query.py summaries --range last_14_days
python3 scripts/wakapi_query.py summaries --range last_30_days
python3 scripts/wakapi_query.py summaries --range last_week
python3 scripts/wakapi_query.py summaries --range last_month
python3 scripts/wakapi_query.py summaries --range last_year
python3 scripts/wakapi_query.py summaries --range all_time

# summaries: optional filters (either --range or --start/--end)
python3 scripts/wakapi_query.py summaries --range last_7_days --timezone Asia/Shanghai
python3 scripts/wakapi_query.py summaries --range week --project myapp --branches main,develop
python3 scripts/wakapi_query.py summaries --range today --writes-only true --timeout 300

# summaries: fixed window ?start=&end=
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07 --timezone America/New_York
python3 scripts/wakapi_query.py summaries --start 2026-03-01 --end 2026-03-07 --branches main,develop
python3 scripts/wakapi_query.py summaries --start 2026-03-18 --end 2026-03-18 \
  --project myapp --branches main,develop --timezone Asia/Shanghai --writes-only false

python3 scripts/wakapi_query.py -d projects
```

## CLI vs HTTP timeouts

| Subcommand | HTTP socket |
|------------|-------------|
| `health` / `projects` / `status-bar` / `all-time-since` | Subcommand **`--timeout`**; defaults **15** s (`health`) and **60** s |
| `stats` / `summaries` | Fixed **60** s; **`--timeout`** = **API** keystroke parameter |

## curl examples

Replace **`ORIGIN`** with **`WAKAPI_URL`**. **`API_KEY`** = Wakapi API key.

```bash
# Basic auth: password = API key only (no username) → base64(key)
API_KEY='your-api-key'
B64=$(printf '%s' "$API_KEY" | base64 | tr -d '\n')
ORIGIN='https://wakapi.dev'
COMPAT="$ORIGIN/api/compat/wakatime/v1/users/current"

# Health: no Authorization header; JSON response if Content-Type: application/json on request
curl -sS -H 'Content-Type: application/json' -H 'Accept: application/json' \
  "$ORIGIN/api/health"

# Plain-text health (optional)
curl -sS "$ORIGIN/api/health"

# Compat v1 user endpoints
curl -sS -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  "$COMPAT/projects"

curl -sS -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  "$COMPAT/all_time_since_today"

curl -sS -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  "$COMPAT/stats/last_7_days"

# stats + API query params (not HTTP socket timeout)
curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "timeout=120" \
  --data-urlencode "writes_only=true" \
  "$COMPAT/stats/last_7_days"

# summaries preset
curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "range=today" \
  "$COMPAT/summaries"

curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "range=last_7_days" \
  --data-urlencode "timezone=Asia/Shanghai" \
  "$COMPAT/summaries"

# summaries preset + project/branches/writes_only/timeout (API params)
curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "range=week" \
  --data-urlencode "project=myapp" \
  --data-urlencode "branches=main,develop" \
  --data-urlencode "timeout=300" \
  --data-urlencode "writes_only=true" \
  "$COMPAT/summaries"

# summaries fixed window
curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "start=2026-03-01" \
  --data-urlencode "end=2026-03-07" \
  "$COMPAT/summaries"

# Single day + filters
curl -sS -G -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  --data-urlencode "start=2026-03-18" \
  --data-urlencode "end=2026-03-18" \
  --data-urlencode "project=myapp" \
  --data-urlencode "branches=main,develop" \
  --data-urlencode "timezone=Asia/Shanghai" \
  "$COMPAT/summaries"

# Status bar: not under compat prefix
curl -sS -H "Authorization: Basic $B64" -H 'Accept: application/json' \
  "$ORIGIN/api/v1/users/current/statusbar/today"
```

## Not covered by this skill

- Heartbeats, user admin, and other **native** `/api/...` routes — see Wakapi source under `routes/api`.
- Deployments with a **subpath** (`base_path`): URLs must include that prefix; this script assumes **root** deployment.
