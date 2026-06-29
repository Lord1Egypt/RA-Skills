---
name: "wyze-vacuum"
description: "Check and control a Wyze robot vacuum — status (battery, docked/cleaning), start, pause, and send to dock. Unofficial Wyze API via wyze-node."
homepage: "https://github.com/noelportugal/wyze-node"
metadata:
  openclaw:
    emoji: "🤖"
    requires: { bins: ["node"] }
---

# Wyze vacuum

Check and control a Wyze **robot vacuum** through the bundled `vacuum` CLI,
which wraps [`wyze-node`](https://www.npmjs.com/package/wyze-node). Reuses the
same cached login as the `wyze` skill (no password).

> Unofficial: `wyze-node` uses Wyze's developer API Key auth and
> reverse-engineered endpoints. Not affiliated with or endorsed by Wyze; Wyze
> may change their API at any time.

## When to use
"Is the vacuum charged?", "start the vacuum", "pause the vacuum", "send the
vacuum back to its dock".

## Setup (once)
Shares the `wyze` skill's setup:
1. `npm install --prefix "{baseDir}/scripts" wyze-node`
2. `WYZE_EMAIL`, `WYZE_KEY_ID`, `WYZE_API_KEY` in `WYZE_ENV`
   (default `~/.openclaw/secrets/wyze.env`) — keys from
   https://developer-api-console.wyze.com/#/apikey/view
3. Cache a login token once via the `wyze` skill's `login` (shared token).

## Run
```
node "{baseDir}/scripts/vacuum" <command> [name]
```

## Commands
- `status [name]` — battery %, docked/charging vs cleaning vs idle, last clean
  duration, connection state. With no name, uses the only vacuum.
- `start [name]` — begin a cleaning sweep.
- `pause [name]` — pause the current sweep.
- `dock [name]` — return to the charging dock.

`<name>` is a case-insensitive substring of the vacuum's nickname; needed only
if you have more than one.

## Safety
- `start` sends a robot moving through the home. It's low-stakes, but on a clear
  request only — don't start a sweep on a vague aside.
- Act on the user's named vacuum, not assumptions.

## Configuration (env vars)
- `WYZE_NODE_DIR` (default `~/code/wyze-node`) or an npm-installed `wyze-node`
- `WYZE_ENV` (default `~/.openclaw/secrets/wyze.env`)
- `WYZE_TOKEN_DIR` (default: `WYZE_NODE_DIR` if present, else `~/.openclaw/wyze`)

## Notes
- Vacuums use Wyze's "venus" service (`product_type` JA_RO2). Status fields come
  from the device heartBeat (battery, charge_state, mode, clean_time).
- License: MIT. Backed by the open-source `wyze-node` client.
