---
name: stremio-cli
description: Stremio automation via browser + Torrentio on Mac Mini. Searches for shows/movies, selects highest-seeded streams, and plays them. Use when user wants to watch something on Stremio (especially Stargate SG-1 S4E15+ or similar). Always confirm specific season/episode if not provided. Credentials for Stremio account are in Keychain.
---

# Stremio CLI

Automates Stremio web with Torrentio addon using browser control on the Mac Mini. 

**Workflow**: Open Stremio web → search title → find episode/season → select highest-seeded Torrentio stream → play.

Perfect for quick streaming sessions. Stremio account credentials are saved in macOS Keychain (bhal.punia@icloud.com).

## When to use

Use this skill for any request like:
- "watch stargate"
- "play stremio"
- "stremio sg1"
- "put on stargate on stremio"

Always ask for specific season + episode if not given (default pattern is S4E15+ for Stargate SG-1).

## Prerequisites

- Browser tool (Playwright) available in OpenClaw
- Stremio account logged in via Keychain on Mac Mini

## How to use

Trigger with natural requests like "stremio stargate" or "watch latest episode".

The skill uses the `browser` tool to:
1. Navigate to Stremio web (with Torrentio addon active)
2. Search for the show
3. Select the correct season/episode
4. Pick the highest-seeded Torrentio stream
5. Play it

Current default: Stargate SG-1 (ask for exact S##E## if needed).

The script in `scripts/stremio_cast.py` is Portuguese/legacy and not used — we rely on the built-in browser tool instead.
