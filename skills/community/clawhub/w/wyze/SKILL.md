---
name: "wyze"
description: "Control Wyze smart-home devices — lights (on/off/dim/color/temp), plugs, and wall switches — from your assistant. Unofficial Wyze API via wyze-node."
homepage: "https://github.com/noelportugal/wyze-node"
metadata:
  openclaw:
    emoji: "💡"
    requires: { bins: ["node"] }
---

# Wyze devices

Control Wyze **lights** (bulbs, color/mesh bulbs, light strips), **plugs**, and
**wall switches** through the bundled `wyze` CLI, which wraps
[`wyze-node`](https://www.npmjs.com/package/wyze-node). Credentials stay local;
after a one-time `login` it runs on a cached token (no password).

> Unofficial: `wyze-node` uses Wyze's developer API Key auth and
> reverse-engineered endpoints. Not affiliated with or endorsed by Wyze; Wyze
> may change their API at any time.

## When to use
Any request to control or check Wyze home devices: turn lights/plugs/switches
on or off, dim or recolor lights, or see what's on.

## Setup (once)
1. Install the dependency:
   `npm install --prefix "{baseDir}/scripts" wyze-node`
   (or have `wyze-node` installed globally, or set `WYZE_NODE_DIR` to a clone)
2. Get a free developer API Key + Key ID at
   https://developer-api-console.wyze.com/#/apikey/view
3. Put `WYZE_EMAIL`, `WYZE_KEY_ID`, `WYZE_API_KEY` in `WYZE_ENV`
   (default `~/.openclaw/secrets/wyze.env`) or the environment.
4. Cache a login token **in a terminal**:
   `node "{baseDir}/scripts/wyze" login`
   (prompts for your password; never written to disk — only a refresh token is
   cached). After this, all commands run without a password.

## Run
```
node "{baseDir}/scripts/wyze" <command> [args]
```

## Commands
- `list [lights|plugs|switches]` — controllable devices with on/off state
- `on  <name|all> [lights|plugs|switches]` — turn on
- `off <name|all> [lights|plugs|switches]` — turn off
- `brightness <name> <0-100>` — lights only
- `color <name> <RRGGBB>` — color/mesh bulbs & strips only (e.g. `FF8800`)
- `temp <name> <kelvin>` — lights only (`2700` warm, `5000` cool)
- `status <name>`
- `login` — interactive one-time setup (run in a terminal)

`<name>` is a case-insensitive substring of the device's nickname; a name that
matches several devices applies to all of them. `all` targets every controllable
device (optionally narrow with a kind: `off all lights`).

## Examples
- "turn off the lights" → `off all lights`
- "turn off everything" → `off all`
- "turn off the porch light" → `off "porch"`
- "turn on the christmas tree" → `on "christmas"`
- "dim the living room to 20%" → `brightness "living room" 20`
- "what's on?" → `list`

## Safety
- Confirm before turning **off all** devices, or any device whose name implies a
  **door/garage/opener/gate** (a plug or switch may actuate it). A single named
  turn-on/off is fine to do directly.
- Plugs and switches control whatever is wired to them — act on the user's named
  target, not assumptions.

## Configuration (env vars)
- `WYZE_NODE_DIR` — path to a `wyze-node` clone (fallback). Default
  `~/code/wyze-node`.
- `WYZE_ENV` — secrets file (default `~/.openclaw/secrets/wyze.env`).
- `WYZE_TOKEN_DIR` — where the cached login (`./scratch`) is stored (default:
  `WYZE_NODE_DIR` if present, else `~/.openclaw/wyze`).

## Notes
- Device kinds: lights = product_type Light/MeshLight/LightStrip; plugs =
  Plug/OutdoorPlug; wall switches = model LD_SS1. Other Wyze devices (cameras,
  sensors, lock, vacuum, scale) are supported by `wyze-node` but not exposed here.
- If calls fail with auth errors, the cached token expired — ensure the keys are
  set and re-run `login`.
- License: MIT. Backed by the open-source `wyze-node` client.
