---
name: tfl-cli
description: London transport CLI — tube status, journey planning, live arrivals, disruptions, bike docks, and agent-friendly projection via `--output <path>` for route, arrivals, and bikes. Use when checking TfL line status, planning London journeys, getting live arrivals, finding bike docks, searching stops, or when an agent needs one value or subtree instead of the full response.
homepage: https://tfl-cli.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "🚇",
        "requires": { "bins": ["tfl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/tfl-cli",
              "bins": ["tfl"],
              "label": "Install tfl-cli (npm)",
            },
          ],
      },
  }
---

# tfl-cli

Use `tfl` for London transport: tube status, journey planning, disruptions, live arrivals, bike availability, and stop search.

Setup

- `npm install -g @shan8851/tfl-cli`
- Optional: set `TFL_APP_KEY` for higher rate limits (basic usage works without any key)

Status

- All lines: `tfl status`
- Specific line: `tfl status jubilee`
- Filter by mode: `tfl status --mode tube,dlr`

Disruptions

- Current disruptions: `tfl disruptions`
- Specific line: `tfl disruptions piccadilly`

Journey Planning

- Station to station: `tfl route "waterloo" "kings cross"`
- Postcode to postcode: `tfl route "SE1 9SG" "EC2R 8AH"`
- Arrive by time: `tfl route "waterloo" "bank" --arrive-by --time 09:00`
- With preferences: `tfl route "waterloo" "paddington" --preference least-interchange`
- Via a waypoint: `tfl route "waterloo" "paddington" --via "bank"`
- Project one route field: `tfl route "SE1 9SG" "EC2R 8AH" --output journeys.0.durationMinutes`
- Project route legs: `tfl route "waterloo" "canary wharf" --output journeys.0.legs`

Arrivals

- Next arrivals: `tfl arrivals "waterloo"`
- Specific line: `tfl arrivals "king's cross" --line northern --limit 5`
- Filter direction: `tfl arrivals "waterloo" --direction inbound`
- Project one value: `tfl arrivals "waterloo" --output arrivals.0.timeToStationSeconds`
- Project in JSON: `tfl arrivals "waterloo" --json --output arrivals.0.lineName`

Bikes

- Near postcode: `tfl bikes "SE1 9SG"`
- Custom radius: `tfl bikes "waterloo" --radius 750 --limit 5`
- Project one value: `tfl bikes "SE1 9SG" --output bikePoints.0.bikes`
- Project one subtree: `tfl bikes "SE1 9SG" --output bikePoints.0`

Search

- Find stops/stations: `tfl search stops "paddington"`
- Limit results: `tfl search stops "paddington" --limit 10`

Output

- All commands default to text in TTY and JSON when piped
- Force JSON: `tfl status --json`
- Force text: `tfl status --text`
- Disable colour: `tfl --no-color status`
- Success envelope: `{ ok, schemaVersion, command, requestedAt, data }`
- Error envelope: `{ ok, schemaVersion, command, requestedAt, error }`

Agent Notes

- `--output <path>` is available on `route`, `arrivals`, and `bikes`
- Paths use dot notation with zero-based array indexes, for example `journeys.0.durationMinutes` or `arrivals.0.lineName`
- In text mode, scalar projections print just the value
- In text mode, object or array projections print plain pretty JSON
- Projection errors are structured: malformed paths return `INVALID_INPUT`, missing paths return `NOT_FOUND`

Notes

- No API key required for basic usage
- Accepts station names, postcodes (`SE1 9SG`), coordinates (`51.50,-0.12`), and TfL stop IDs
- Status and disruptions cover tube, overground, DLR, and Elizabeth line
- Exit codes: 0 success, 2 bad input or ambiguity, 3 upstream failure, 4 internal error
- When a station name is ambiguous, the error includes candidate suggestions
