# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Cross-platform Telegram Mini App pet game, delivered as an **agentskills.io** skill that runs in both **OpenClaw** (`~/.openclaw/workspace/skills/pet/`) and **Hermes Agent** (`~/.hermes/skills/games/pet/`). `install.sh` symlinks the source dir into both runtimes when present.

The repo contains **three parallel implementations** of the same game that share the `users/` JSON storage layout but are otherwise independent:

1. **Terminal CLI** (`pet-cli.js`) — standalone Node.js readline app, persists to `~/.openclaw-pet.json` (note: different file from the web/Telegram flow). Five evolution stages (Egg → 10x Legend) gated by `level`.
2. **Telegram Mini App** (`mini-app.html` + `server.js`) — Node HTTP server on port 3456 that serves the Mini App and exposes `POST /api/pet`. State per user in `users/{userId}.json`.
3. **Python web server** (`server.py` + `index.html`) — alternate backend on port 8080 with the same `POST /api/pet` contract; same per-user JSON files in `users/`. Used together with `cloudflared` to expose a public HTTPS URL for the Telegram menu button.

The Telegram entry point is registered through `SKILL.md` (frontmatter trigger `/pet`). `bot.js`, `webhook.js`, `inline-button.js`, `chat-game.js`, `chat-pet.js`, and `pet.js` are smaller helper scripts for various bot integration paths — verify which one is actually wired before editing.

## Commands

```bash
npm install                  # install deps (chalk only)
npm start                    # run the CLI pet (pet-cli.js)
node server.js               # Node Mini App backend on :3456 (BOT_TOKEN, PET_PORT envs)
python3 server.py            # Python backend on :8080 (serves index.html)
cloudflared tunnel --url http://localhost:8080   # public HTTPS for Telegram Mini App
./deploy.sh                  # npm install + npm start
```

There are no tests, lint config, or build step.

## API contract

**`server.py` (canonical, deployed)** — Python stdlib + Pillow:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | `index.html` |
| GET | `/card/<userId>.png` | 1080×1350 share card PNG (Pillow → SVG fallback) |
| POST | `/api/pet` | Action dispatcher |

POST actions: `create`, `feed`, `play`, `sleep`, `visit`, `befriend`, `playdate`, `friends`, `memorial`, `revive`. Pet schema: `{ userId, type, name, hunger, happy, energy, level, status, streak, friends[], bond{}, lastPlaydate{}, dialogues[] }`. `apply_decay()` runs on every `load_pet()` and updates `status` to `alive`/`sad`/`dead` based on `lastFed` age (3 / 7 days).

**`server.js`** — older Node implementation, only supports `create`/`feed`/`play`/`sleep`. **Does not implement** the social layer, mortality, streak, or card endpoint. Treat as legacy unless explicitly updated.

Real Telegram HMAC validation of `initData` is still a TODO in both backends.

## Cross-platform skill metadata

`SKILL.md` frontmatter follows agentskills.io with both `metadata.openclaw.requires` and `metadata.hermes.{tags,category,requires_toolsets}` blocks so the same file is loaded by either runtime. Hermes also requires `version`. Don't drop fields when editing.

## Editing notes

- The two web backends (`server.js`, `server.py`) duplicate the action math (`feed +25 hunger`, `play +20 happy / -10 energy`, `sleep +30 energy`). Keep them in sync if you change one.
- `index.html` is served by `server.py`; `mini-app.html` is served by `server.js`. They are not interchangeable.
- The Mini App URL in `README.md` and `SKILL.md` is a Cloudflared trycloudflare hostname that changes on every tunnel restart — update both files when redeploying.
- The repo has many stale/zip artifacts (`pet-deploy.zip`, `pet-web.zip`, `server.log`, `tunnel.log`, `command-response.txt`) and several design docs (`GAMEDESIGN.md`, `GAME_DESIGN_MASTERPLAN.md`, `PET_*.md`, `SCENARIO.md`) — read these for product/character intent, not implementation truth.
