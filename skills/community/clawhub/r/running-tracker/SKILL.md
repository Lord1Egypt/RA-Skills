---
name: running_tracker
description: Track, log, and analyze running workout times. Use when the user reports a new run (e.g. "1mi 8:20", "3k 15:33", "just finished a run"), asks about running history, pace, progress, personal bests, training advice based on their logged runs, or anything related to their running data.
---

# Running Tracker

Log runs and analyze running performance using the data file at `{baseDir}/runs.md`.

## Logging a New Run

### Input parsing

Runs arrive in casual formats. Extract three fields:

- **Distance**: `1mi`, `3k`, `5k`, `10k`, `1.5mi`, etc.
- **Date**: `DD/MM/YY` or natural language ("today", "yesterday"). If omitted, use today's date.
- **Time**: `M:SS` or `MM:SS` (duration to complete the distance).

### Storage

Append a new row to the markdown table in `{baseDir}/runs.md`. Store dates as `YYYY-MM-DD`. Keep the table sorted by date ascending (newest at the bottom).

### Response after logging

1. **Run stats** — compute and display:
   - Pace (min/km)
   - Speed (km/h)
   - Estimated calories burned (use 62 cal/km, no elevation)

2. **Progress note** — 2-3 sentences comparing this run to recent history. Examples: pace trend, personal best alert, slowest/fastest in N days, streak observations. Be honest — if they slowed down, say so encouragingly.

## Answering History Questions

Read `{baseDir}/runs.md` and compute whatever the user asks: averages, bests, trends, comparisons across distances, weekly/monthly summaries, training advice, etc.

### Unit conversions

- 1 mile = 1.60934 km
- Pace = total minutes / distance in km
- Speed = distance in km / (time in hours)

When the user's question involves a distance they haven't run (e.g. 10k projections), extrapolate cautiously and note the assumption.