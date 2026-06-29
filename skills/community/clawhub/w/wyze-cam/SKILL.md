---
name: "wyze-cam"
description: "View and control Wyze cameras — snapshot/thumbnail image, siren, floodlight/spotlight, motion & notification toggles, power. Unofficial Wyze API via wyze-node."
homepage: "https://github.com/noelportugal/wyze-node"
metadata:
  openclaw:
    emoji: "📷"
    requires: { bins: ["node"] }
---

# Wyze cameras

View and control Wyze **cameras** through the bundled `cam` CLI, which wraps
[`wyze-node`](https://www.npmjs.com/package/wyze-node). Reuses the same cached
login as the `wyze` skill (no password).

> Unofficial: `wyze-node` uses Wyze's developer API Key auth and
> reverse-engineered endpoints. Not affiliated with or endorsed by Wyze; Wyze
> may change their API at any time.

## When to use
Any request to see a camera ("show me the driveway", "snapshot the front door")
or control one: siren, floodlight/spotlight, toggle motion detection or
notifications, turn a camera on/off.

## Setup (once)
Shares the `wyze` skill's setup. If you haven't already:
1. Install the dependency: `npm install --prefix "{baseDir}/scripts" wyze-node`
2. Put `WYZE_EMAIL`, `WYZE_KEY_ID`, `WYZE_API_KEY` in `WYZE_ENV`
   (default `~/.openclaw/secrets/wyze.env`) — keys from
   https://developer-api-console.wyze.com/#/apikey/view
3. Cache a login token once via the `wyze` skill's `login` (shared token).
4. **Live snapshot only** — for `snapshot` (a fresh WebRTC frame), also install
   the optional deps: `npm install --prefix "{baseDir}/scripts" werift ws ffmpeg-static`
   (and have `ffmpeg` available). Not needed for any other command.

## Run
```
node "{baseDir}/scripts/cam" <command> [args]
```

## Commands
- `list` — cameras with online/offline state
- `thumbnail <name>` — latest cached thumbnail URL (fast, dependency-free; may
  lag by minutes and isn't available on every model)
- `snapshot <name> [outpath]` — capture a **live** frame to a JPG and print the
  path (needs the optional WebRTC deps; works on newer wired models — older V1
  cams and some battery models can't negotiate a stream)
- `on <name>` / `off <name>` — power the camera on/off
- `siren <name> on|off`
- `floodlight <name> on|off` (alias `spotlight`, `light`)
- `motion <name> on|off` — motion detection
- `notifications <name> on|off` — push notifications
- `recording <name> on|off` — motion-triggered recording

`<name>` is a case-insensitive substring of the camera's nickname and must match
exactly one camera (it lists the conflicts if not).

## Getting an image
Prefer `thumbnail` first — it's instant and needs no extra deps. Use `snapshot`
when you need a *current* frame and the camera supports WebRTC. Attach the
resulting image to the user.

## Safety
- The **siren** is loud — only fire it on an explicit, specific request, and
  confirm before turning it on.
- Some Wyze cameras drive a **garage-door** controller. Treat any camera whose
  name implies a door/garage/opener with the same caution as a door: confirm
  first.
- Act on the user's named camera, not all cameras at once.

## Configuration (env vars)
- `WYZE_NODE_DIR` (default `~/code/wyze-node`) or an npm-installed `wyze-node`
- `WYZE_ENV` (default `~/.openclaw/secrets/wyze.env`)
- `WYZE_TOKEN_DIR` (default: `WYZE_NODE_DIR` if present, else `~/.openclaw/wyze`)

## Notes
- Cameras are `product_type` Camera. Thumbnails are signed, time-limited URLs.
- License: MIT. Backed by the open-source `wyze-node` client.
