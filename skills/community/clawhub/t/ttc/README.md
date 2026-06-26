# @lucasygu/ttc

CLI for Toronto Transit Commission — real-time bus & streetcar arrivals, vehicle tracking, live monitoring, and alerts from the terminal.

No API key required. All data comes from TTC's public GTFS-RT feeds.

> ### Easiest way to get started
>
> Paste this to your AI coding agent (Claude Code, Cursor, Codex, Windsurf, OpenClaw, etc.):
>
> **"Install the `@lucasygu/ttc` Toronto transit CLI via npm and run `ttc status` to verify it works. Repo: https://github.com/lucasygu/ttc-cli"**
>
> OpenClaw users can also run: **`clawhub install ttc`**
>
> The agent handles installation and verification. No API key or auth needed — all feeds are public.
>
> Once installed, try: **"What's the next streetcar at King and Spadina?"** — the agent will run `ttc next "king spadina"` and show you real-time arrivals.

## Install

```bash
npm install -g @lucasygu/ttc
# Or via ClawHub (OpenClaw ecosystem)
clawhub install ttc
```

Requires Node.js >= 22. Supports **macOS, Windows, and Linux**.

## What You Can Do

- **Next arrivals** — Check when the next bus or streetcar is coming at any stop
- **Live vehicle tracking** — See real-time positions of all vehicles on a route
- **Nearby stops** — Auto-detect your location (macOS) and find the closest stops with arrivals
- **Service alerts** — Check disruptions and delays on surface routes and subway
- **Live monitoring** — Watch any command on a loop with auto-refresh (like `watch` for transit)
- **Stop & route search** — Fuzzy search stops by name, list all routes, filter by type
- **System status** — Quick overview of active vehicles, routes, and alerts

When used through an AI agent, you can ask natural language questions like "Is the 504 running right now?" and the agent calls the right commands. Each CLI command also works standalone.

## Quick Start

```bash
# Next arrivals at a stop (fuzzy name matching)
ttc next "king spadina"
ttc next 8126                          # by stop code

# Route info with active vehicles
ttc route 504

# Live vehicle positions
ttc vehicles 504

# Service alerts
ttc alerts
ttc alerts --broad                     # include subway alerts

# Nearby stops + arrivals (auto-detects location on macOS)
ttc nearby
ttc nearby 43.6453,-79.3806           # or provide coordinates

# All surface routes
ttc routes
ttc routes --type streetcar

# Fuzzy stop search
ttc search "broadview station"

# Active stops on a route
ttc stops 504

# System status
ttc status

# Live monitoring — re-run any command on an interval
ttc loop 3m next "king spadina"        # watch arrivals every 3 min
ttc loop 5m alerts                     # monitor disruptions
ttc loop 2m vehicles 504              # track vehicles approaching
ttc loop 30s nearby                    # refresh as you walk
```

All commands support `--json` for programmatic use.

## Commands

| Command | Description |
|---------|-------------|
| `next <stop>` | Next arrivals at a stop (name, stop ID, or stop code) |
| `route <number>` | Route info: type, directions, active vehicles, alerts |
| `vehicles [route]` | Live vehicle positions with status and occupancy |
| `alerts [route]` | Service alerts and disruptions |
| `nearby [lat,lng]` | Nearest stops with upcoming arrivals |
| `routes` | List all surface routes |
| `search <query>` | Fuzzy search for stops by name |
| `stops <route>` | Active stops on a route |
| `status` | System overview: vehicles, routes, alerts, data freshness |
| `loop <interval> <cmd>` | Re-run any ttc command on an interval (e.g. `3m`, `30s`, `1h`) |

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--json` | Output as JSON (for scripts and AI agents) | `false` |

### Route Filtering

| Option | Description | Default |
|--------|-------------|---------|
| `--type <type>` | Filter routes: `bus`, `streetcar` | all |

### Alert Options

| Option | Description | Default |
|--------|-------------|---------|
| `--broad` | Include subway alerts (default: surface only) | `false` |

### Nearby Options

| Option | Description | Default |
|--------|-------------|---------|
| `--radius <meters>` | Search radius in meters | `500` |

## Location Detection (macOS)

On macOS, `ttc nearby` automatically detects your location using CoreLocation. A Swift helper app is compiled during installation (requires Xcode Command Line Tools). The first run will prompt for location permission — grant it once and it works automatically from then on.

If you don't have Xcode tools, location auto-detect is skipped and you can still pass coordinates manually.

## Data Sources

- **Real-time**: GTFS-RT protobuf feeds from `bustime.ttc.ca` (vehicles, predictions, alerts)
- **Static**: Stop names, route info, and trip headsigns bundled from [Open Toronto GTFS](https://open.toronto.ca/dataset/merged-gtfs-ttc-routes-and-schedules/)
- **Coverage**: Surface transit (buses + streetcars). Subway alerts available with `--broad`.

## AI Agent Integration

### Claude Code

Installs automatically as a Claude Code skill. Use `/ttc` in Claude Code:

```
/ttc next "union station"
/ttc nearby
/ttc alerts --json
```

You can give natural language instructions:

- *"What's the next streetcar at King and Spadina?"*
- *"Are there any service alerts on the 504?"*
- *"Show me all vehicles on the 510 route"*
- *"Watch nearby arrivals every 2 minutes"*

Claude will automatically pick the right command and parse the output.

### OpenClaw / ClawHub

Officially supports [OpenClaw](https://openclaw.ai) and [ClawHub](https://docs.openclaw.ai/tools/clawhub). Install via ClawHub:

```bash
clawhub install ttc
```

All `ttc` commands are available in OpenClaw after installation.

## Programmatic Usage

```typescript
import { TtcClient } from "@lucasygu/ttc";

const client = new TtcClient();
const vehicles = await client.getVehicles("504");       // live positions
const arrivals = await client.getNextArrivals("12345");  // predictions for a stop
const alerts = await client.getAlerts();                 // service alerts
```

## Development

```bash
git clone https://github.com/lucasygu/ttc-cli.git
cd ttc-cli
npm install --ignore-scripts
npm run update-gtfs    # download fresh GTFS data
npm run build
node dist/cli.js status
```

## License

MIT
