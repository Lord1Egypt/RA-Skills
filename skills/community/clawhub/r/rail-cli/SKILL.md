---
name: rail-cli
description: UK National Rail CLI — live departures, arrivals, station search, destination filtering, batch station search from stdin, and lightweight field selection for agents. Use when checking UK rail boards, resolving station names/CRS codes, filtering departures or arrivals, or when an agent needs machine-friendly station search via `rail search --stdin` or `rail search --select`.
homepage: https://rail-cli.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "🚆",
        "requires":
          {
            "bins": ["rail"],
            "env": ["DARWIN_ACCESS_TOKEN"],
          },
        "primaryEnv": "DARWIN_ACCESS_TOKEN",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/rail-cli",
              "bins": ["rail"],
              "label": "Install rail-cli (npm)",
            },
          ],
      },
  }
---

# rail-cli

Use `rail` for UK National Rail data: live departures, arrivals, station search, destination filtering, and agent-friendly batch search.

Setup

- `npm install -g @shan8851/rail-cli`
- Get a free Darwin access token: https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration
- `export DARWIN_ACCESS_TOKEN=your_token` or add to `.env`
- Station search works without a token. Departures and arrivals require one.

Departures

- From a station: `rail departures KGX`
- By station name: `rail departures "kings cross"`
- Filter to destination: `rail departures "edinburgh" --to "york"`
- Include calling points: `rail departures KGX --expand`
- Limit results: `rail departures KGX --limit 5`

Arrivals

- At a station: `rail arrivals "leeds"`
- By CRS code: `rail arrivals LDS`
- Filter from origin: `rail arrivals "leeds" --from "london"`
- Include calling points: `rail arrivals LDS --expand`
- Limit results: `rail arrivals LDS --limit 5`

Station Search

- Search by name: `rail search "waterloo"`
- Return only CRS codes: `rail search "waterloo" --select crs`
- Return only names: `rail search "waterloo" --select name`
- Return explicit name + CRS projection: `rail search "waterloo" --select name,crs`
- Batch search from stdin: `printf "waterloo\nvictoria\n" | rail search --stdin`
- Batch search as JSON: `printf "waterloo\nvictoria\n" | rail search --stdin --json`

Output

- All commands default to text in TTY, JSON when piped
- Force JSON: `rail departures KGX --json`
- Force text: `rail departures KGX --text`
- Disable colour: `rail --no-color departures KGX`
- Success envelope: `{ ok, schemaVersion, command, requestedAt, data }`
- Error envelope: `{ ok, schemaVersion, command, requestedAt, error }`

Agent Notes

- `rail search --stdin` is pipeline-only and expects newline-delimited queries on stdin
- `rail search --select` is intentionally narrow: `name`, `crs`, or `name,crs`
- `rail search --stdin` and a positional query cannot be used together
- Search output stays stable unless projection flags are explicitly used
- Errors are structured and suitable for agent retry/self-correction

Configuration

- `DARWIN_ACCESS_TOKEN` — required for departures/arrivals (free registration)
- `RAIL_API_URL` — optional, override Huxley2 instance URL (default: public instance)

Notes

- Accepts station names ("kings cross", "leeds") and CRS codes (`KGX`, `LDS`, `EDB`)
- CRS codes are 3-letter station identifiers
- Covers every National Rail station in Great Britain
- Data powered by National Rail Darwin via Huxley2
- Exit codes: 0 success, 2 bad input or ambiguity, 3 upstream failure, 4 internal error
- When a station name is ambiguous, the error includes candidate suggestions
