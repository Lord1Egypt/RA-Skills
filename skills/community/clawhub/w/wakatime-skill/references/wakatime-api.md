# WakaTime API (this skill)

Official developer documentation: [WakaTime Developers](https://wakatime.com/developers).

This skill calls only the **hosted** API at `https://wakatime.com` (no self-hosted override). All paths below are under **`/api/v1`**.

## Authentication

Use **HTTP Basic** with the API key as the username and an **empty password**. The CLI sets:

`Authorization: Basic <base64(api_key)>`

Environment variable: **`WAKATIME_API_KEY`** (required).

## Endpoints used by `scripts/wakatime_query.py`

| CLI command | Method | Path | Notes |
|-------------|--------|------|--------|
| `health` | GET | `/api/v1/users/current/projects` | Connectivity check; response body is not parsed for health status. |
| `projects` | GET | `/api/v1/users/current/projects` | Lists projects (JSON). |
| `status-bar` | GET | `/api/v1/users/current/statusbar/today` | Today’s status bar payload (JSON). |
| `all-time-since` | GET | `/api/v1/users/current/all_time_since_today` | All-time total since “today” anchor (JSON). |
| `stats <range>` | GET | `/api/v1/users/current/stats/{range}` | `range` is a path segment (e.g. `last_7_days`, `2026`, `2026-03`, `all_time`). Optional query: `timeout`, `writes_only`. |
| `summaries` | GET | `/api/v1/users/current/summaries` | Query params: date window (`start` + `end`, or `range`), optional `project`, `branches`, `timezone`, `timeout`, `writes_only`. See [Summaries](https://wakatime.com/developers#summaries). |

### `stats` query parameters

| Parameter | Meaning |
|-----------|---------|
| `timeout` | Keystroke timeout (seconds), per WakaTime API — not the HTTP client socket timeout. |
| `writes_only` | `true` or `false`. |

### `summaries` query parameters

Provide **either** `start` and `end` (both `YYYY-MM-DD`) **or** `range` (preset). Optional filters: `project`, `branches`, `timezone`, `timeout`, `writes_only`. Details: [Summaries API](https://wakatime.com/developers#summaries).

## HTTP client behavior (CLI)

- Default HTTP socket timeouts are **60s** for most commands, **15s** for `health`, unless overridden with `--timeout` on the CLI (that flag sets **HTTP** timeout, except where noted for `stats` / `summaries` API query params named `timeout`).
- Successful responses are expected to be **JSON** (`Accept: application/json`).
- Debug: pass `-d` or `--debug` to log each request URL on stderr.

## Errors

HTTP error responses are printed as JSON on stderr, e.g. `{"http_status": …, "error": …}`. Exit code **1** for HTTP/API errors, **2** for URL/network errors (see script).
