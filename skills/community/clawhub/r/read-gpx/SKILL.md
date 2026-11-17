---
name: read-gpx
description: Parse and analyze GPX route files for trail running, cycling, hiking, and race planning. Use when the user provides or references a .gpx file and asks for route distance, elevation gain/loss, waypoint/CP extraction, segment stats, terrain difficulty, pacing tables, roadbooks, cutoff planning, or checkpoint arrival estimates.
---

# Read GPX

## Quick Start

Use the bundled parser first when a local `.gpx` file is available:

```bash
python3 ~/.codex/skills/read-gpx/scripts/read_gpx.py path/to/route.gpx
```

For machine-readable output:

```bash
python3 ~/.codex/skills/read-gpx/scripts/read_gpx.py path/to/route.gpx --format json
```

The script uses only the Python standard library. It handles GPX 1.0/1.1 namespaces, track points, elevation, and waypoints.

## Workflow

1. Locate the GPX file with `rg --files -g '*.gpx' -g '*.GPX'` when the user references a local route by name.
2. Run `scripts/read_gpx.py` to extract route facts before making pacing or strategy claims.
3. Treat `<wpt>` entries as CP/checkpoint candidates. The script snaps waypoints to the nearest track point and reports the snapped track distance.
4. If no waypoints exist, say that the GPX lacks official CP points and either:
   - ask the user for a CP table, or
   - create provisional terrain-based segments and label them clearly as inferred.
5. Base pacing and roadbooks on segment distance, climb, descent, CP stop time, user ability, terrain, weather, and time of day. Do not spread target time evenly by distance unless the user explicitly asks for a simple average plan.
6. When producing race tables, include both segment time and cumulative/clock arrival time if the user gives a start time.

## Route Description

When the user asks what a route is like, describe it in practical outdoor terms:

- Total distance, gain/loss, high/low elevation, and number of CP/waypoint segments.
- Where the main climb happens, where the main descent happens, and which late-race segment deserves the most respect.
- Whether the route is front-loaded, back-loaded, rolling, descent-heavy, or likely quad-damaging.
- Any waypoint snap distances above roughly 50 m, because those may indicate CP labels are not exactly on the track.

Keep descriptions grounded in parsed GPX facts. Clearly label any terrain or surface inference that is not directly present in the GPX.

## Elevation Handling

Use the script's thresholded gain/loss instead of raw point-to-point elevation totals. Dense GPX tracks often include GPS noise that inflates climbing. The default threshold is `3 m`; adjust with:

```bash
python3 ~/.codex/skills/read-gpx/scripts/read_gpx.py route.gpx --gain-threshold 5
```

If the GPX name or race materials contain official elevation totals, compare them with the script output and explain any small difference as smoothing/threshold methodology.

## Pacing Guidance

For trail race pacing:

- Weight climbs, descents, technical terrain, night running, altitude, and late-race fatigue.
- Identify late hard segments explicitly; downhill-heavy late segments can be more damaging than their distance suggests.
- If the user provides a recent benchmark race, use it to choose a conservative target and explain the risk.
- For users reporting quad cramps or downhill damage, bias the plan toward slower descents, more CP buffer, and a stronger late-race reserve.

When generating a roadbook, prefer a compact table with:

- Segment name
- Distance
- Climb/descent
- Segment target time
- Cumulative time
- Clock arrival time
- One or two execution notes per CP/segment

## Recommendation Style

When giving advice, be explicit about confidence and assumptions:

- Separate route facts from personal recommendations.
- If the user provides recent race data, explain how it changes the pacing target.
- If the user reports cramps, stomach issues, altitude sensitivity, heat sensitivity, or night-running concerns, adjust the target conservatively.
- Give one main target, one optimistic target, and one fallback target when enough user data exists.
- Mention the most important failure mode in plain language, such as "protect the quads before CP5" or "do not chase time on the first long descent."
