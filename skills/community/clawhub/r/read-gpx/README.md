# Read GPX Skill

Read GPX files for trail running, cycling, hiking, and race planning.

This skill helps an agent parse `.gpx` route files, extract checkpoints, summarize elevation, describe route difficulty, and build practical pacing or roadbook recommendations.

## What It Does

- Parses GPX 1.0/1.1 track points and elevations.
- Extracts waypoints as CP/checkpoint candidates.
- Snaps waypoints to the nearest track point and reports the track kilometer.
- Calculates distance, thresholded climb/descent, elevation range, and segment stats.
- Guides agents to create pacing plans, clock-time roadbooks, and race execution advice.

## Use Cases

- "Read this GPX and tell me the total distance and climbing."
- "Find every CP and calculate each segment's distance, climb, and descent."
- "Build a 10h/11h/12h pacing table from this trail race GPX."
- "I start at 22:15. Give me CP arrival times."
- "Based on my recent race result, how should I pace this route?"

## CLI Helper

```bash
python3 scripts/read_gpx.py route.gpx
```

JSON output:

```bash
python3 scripts/read_gpx.py route.gpx --format json
```

Adjust elevation smoothing:

```bash
python3 scripts/read_gpx.py route.gpx --gain-threshold 5
```

## Install

Clone or install the skill into your agent skills directory:

```bash
git clone https://github.com/forrestIsRunning/read-gpx-skill.git ~/.codex/skills/read-gpx
```

For ClawHub, install with the published slug once available:

```bash
clawhub install read-gpx
```

## Files

- `SKILL.md` - Agent workflow and recommendation guidance.
- `scripts/read_gpx.py` - Deterministic GPX parser using only Python standard library.
- `agents/openai.yaml` - UI metadata for compatible agent runtimes.
