---
name: "wyze-sensors"
description: "Read Wyze sensor states — contact (door/window open/closed), motion (detected/clear), and temperature/humidity. Read-only. Unofficial Wyze API via wyze-node."
homepage: "https://github.com/noelportugal/wyze-node"
metadata:
  openclaw:
    emoji: "🚪"
    requires: { bins: ["node"] }
---

# Wyze sensors

Read Wyze **sensor** states through the bundled `sensors` CLI, which wraps
[`wyze-node`](https://www.npmjs.com/package/wyze-node). Reuses the same cached
login as the `wyze` skill (no password). **Read-only** — sensors report state,
they aren't controllable.

> Unofficial: `wyze-node` uses Wyze's developer API Key auth and
> reverse-engineered endpoints. Not affiliated with or endorsed by Wyze; Wyze
> may change their API at any time.

## When to use
"Is the front door open?", "any motion in the driveway?", "what's the
temperature in the office?", "are all the doors closed?"

## Setup (once)
Shares the `wyze` skill's setup:
1. `npm install --prefix "{baseDir}/scripts" wyze-node`
2. `WYZE_EMAIL`, `WYZE_KEY_ID`, `WYZE_API_KEY` in `WYZE_ENV`
   (default `~/.openclaw/secrets/wyze.env`) — keys from
   https://developer-api-console.wyze.com/#/apikey/view
3. Cache a login token once via the `wyze` skill's `login` (shared token).

## Run
```
node "{baseDir}/scripts/sensors" [list|status] [arg]
```

## Commands
- `list [contact|motion|climate]` — all sensors with current state, optionally
  filtered to one kind.
- `status <name>` — the sensor(s) whose nickname contains `<name>`.

Reported states:
- **contact** — `closed` / `OPEN`
- **motion** — `clear` / `MOTION`
- **climate** (temperature/humidity) — e.g. `78.6°F, 75% humidity`
- a `⚠ low battery` flag is appended when the sensor reports low battery.

## Examples
- "are the doors closed?" → `list contact`
- "office temperature?" → `status office`
- "what do all the sensors say?" → `list`

## Configuration (env vars)
- `WYZE_NODE_DIR` (default `~/code/wyze-node`) or an npm-installed `wyze-node`
- `WYZE_ENV` (default `~/.openclaw/secrets/wyze.env`)
- `WYZE_TOKEN_DIR` (default: `WYZE_NODE_DIR` if present, else `~/.openclaw/wyze`)

## Notes
- Covers `product_type` ContactSensor, MotionSensor, and TemperatureHumidity.
  State is read from the device list's `device_params` (no per-sensor call).
  Values reflect the last report the sensor pushed to Wyze, not a live poll.
- License: MIT. Backed by the open-source `wyze-node` client.
