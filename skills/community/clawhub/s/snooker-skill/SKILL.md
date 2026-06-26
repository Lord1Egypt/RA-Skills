---
name: snooker
description: Look up snooker rankings, results, player profiles, live matches and head-to-head records via api.snooker.org.
version: 0.3.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: SNOOKER_API_KEY
---

# Snooker

Query live snooker data — rankings, results, player profiles, and more.

Requires an API key from api.snooker.org. Set the env var SNOOKER_API_KEY to your API key. Please note that the current API rate limit is 10 requests per minute.

## Script

```bash
{baseDir}/snooker.py <command> [options]
```

## Commands

```bash
# Current world rankings (top 20)
{baseDir}/snooker.py rankings

# Rankings for a specific season
{baseDir}/snooker.py rankings --season 2024

# Player profile (search by name)
{baseDir}/snooker.py player "O'Sullivan"
{baseDir}/snooker.py player "Ronnie"

# Player profile by numeric ID (faster — use when you already have the ID)
{baseDir}/snooker.py player-id 16

# Recent results (returns Player1ID, Player2ID, EventID — use player-id/event to resolve names)
{baseDir}/snooker.py results
{baseDir}/snooker.py results --days 3

# Event details by numeric ID
{baseDir}/snooker.py event 2205

# Live matches in progress
{baseDir}/snooker.py live

# Matches scheduled for tomorrow (default) or a specific date
{baseDir}/snooker.py upcoming
{baseDir}/snooker.py upcoming --date 2026-03-15

# Upcoming matches for a specific player (all future matches, not just tomorrow)
{baseDir}/snooker.py upcoming --player "Hawkins"
{baseDir}/snooker.py upcoming --player "Ronnie O'Sullivan"

# Tournaments active tomorrow (default) or a specific date
{baseDir}/snooker.py tournaments
{baseDir}/snooker.py tournaments --date 2026-03-15

# Full schedule (tournaments + matches) for tomorrow or a specific date
{baseDir}/snooker.py schedule
{baseDir}/snooker.py schedule --date 2026-03-15

# Head-to-head record (split name pairs by position)
{baseDir}/snooker.py h2h Ronnie O'Sullivan Mark Selby
```

## Notes

- All data is from the main professional tour (tour ID main)
- Rankings show top 20 by prize money for the current season
- `player` returns up to 3 matching results if the name is ambiguous
- `h2h` searches by last name or full name — be specific if names are ambiguous
