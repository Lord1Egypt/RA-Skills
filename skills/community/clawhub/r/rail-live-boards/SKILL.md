---
name: rail-live-boards
description: "Query UK National Rail live boards, delays, cancellations, platforms, and service details."
---

# Rail Live Boards

Use this skill for live UK rail departure and arrival boards, disruption notices, platform checks, and service details.

## Setup

Requires a valid Rail Data API key:
1. Set `RAILDATA_API_KEY` in the environment.
2. `NATIONAL_RAIL_TOKEN` is accepted as a fallback.
3. The helper calls `https://api1.raildata.org.uk/1010-live-arrival-and-departure-boards-arr-and-dep1_1/LDBWS/api/20220120/GetArrDepBoardWithDetails/{crs}`.

## Commands

```bash
./scripts/rail-live-boards.py board PAD
./scripts/rail-live-boards.py departures PAD --rows 5
./scripts/rail-live-boards.py arrivals MAN --rows 5
./scripts/rail-live-boards.py search paddington
```

## Reading Results

The helper prints live JSON.

Useful fields:
- `locationName`, `crs`, `generatedAt`
- `nrccMessages[]`
- `trainServices[]`
- Per service:
  - `std` / `etd`
  - `sta` / `eta`
  - `platform`
  - `operator`
  - `origin[]`
  - `destination[]`
  - `isCancelled`, `cancelReason`, `delayReason`
  - `formation.coaches` when present

## Notes

- Use 3-letter CRS codes like `PAD`, `EUS`, `MAN`, `RDG`.
- Keep the API key private.
- If you need a compact summary for chat, read the first few services and the disruption messages first.
