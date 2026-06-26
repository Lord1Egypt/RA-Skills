---
name: flight-search
description: Search one-way flight lists from the Variflight ticket API by departure IATA city code, arrival IATA city code, and departure date.
metadata: {"openclaw":{"homepage":"https://ticket.variflight.com/","requires":{"bins":["python3"]}}}
---

# Flight Search

## Overview

Use the bundled script to query the Variflight ticket API and return one-way flight options for a single route and date.

## Workflow

1. Collect `dep`, `arr`, and `date`.
2. Validate `dep` and `arr` as three-letter IATA city codes and `date` as `YYYY-MM-DD`.
3. If the user gives city names instead of codes, infer only when the mapping is unambiguous; otherwise ask for the IATA codes.
4. Run `python3 scripts/query_flights.py --dep BJS --arr SHA --date 2026-04-21`.
5. Summarize the result with departure airport, arrival airport, times, duration, price, transfer info, and the flight tag text.

## Output Rules

- Treat API `code != 0` as a failure and surface the returned `msg`.
- Treat an empty `data.list` as a valid "no flights found" result.
- Use `--limit N` when the user only wants a subset of results.
- Use `--json` only when the user asks for raw payload data.
- Mention transfer flights separately from direct flights when summarizing.
- Do not ask the user to provide an API key for this skill.

## Script

- `scripts/query_flights.py` accepts:
  - `--dep`
  - `--arr`
  - `--date`
  - `--limit`
  - `--json`
- The script sends the fixed request parameter `flightNum=10`.

## Example

Run `python3 scripts/query_flights.py --dep BJS --arr SHA --date 2026-04-21 --limit 5` to fetch the first five displayed results for Beijing to Shanghai on April 21, 2026.
