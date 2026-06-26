---
name: qweather-city-weather
description: Query QWeather city codes and real-time weather with bundled executable scripts. Use when users need to resolve city names to QWeather location IDs/adcodes, fetch current weather, or run portable weather queries on machines that do not host the original app.
---

# qweather-city-weather

Use this skill primarily via the bundled script:

- `scripts/qweather_query.py`

This makes the skill portable across machines and independent from a local Next.js service.

## Prerequisites

- Python 3.10+ available
- Required QWeather API key:
  - set `QWEATHER_API_KEY`, or
  - pass `--api-key`
- Required QWeather API host:
  - set `QWEATHER_API_HOST`, or
  - pass `--api-host`

## Default execution flow

1. Search city candidates and get location IDs:

```bash
python3 scripts/qweather_query.py search-city --query "Hangzhou" --api-host "<QWEATHER_API_HOST>" --api-key "<QWEATHER_API_KEY>"
```

2. Pick best city by `id/name/adm1/adm2`.

3. Query current weather with location ID:

```bash
python3 scripts/qweather_query.py get-weather --location "101210101" --api-host "<QWEATHER_API_HOST>" --api-key "<QWEATHER_API_KEY>"
```

4. Or run one-shot city -> weather:

```bash
python3 scripts/qweather_query.py city-weather --query "Hangzhou" --api-host "<QWEATHER_API_HOST>" --api-key "<QWEATHER_API_KEY>"
```

## Script command reference

- `search-city`
  - required: `--query`
  - optional: `--number` (default `10`)
- `get-weather`
  - required: `--location`
- `city-weather`
  - required: `--query`
  - optional: `--preferred-name` for exact city-name match

Global options for all subcommands:

- `--api-key`
- `--api-host`
- `--timeout` (seconds, default `5.0`)

## Output and error contract

- Success: JSON with `success: true`
- Failure: JSON with `success: false` + `error`, process exits non-zero
- Never guess city when no result; return explicit no-match failure

## Direct API reference

For endpoint and payload details of the official QWeather API, read:

- `references/qweather-http-contract.md`
