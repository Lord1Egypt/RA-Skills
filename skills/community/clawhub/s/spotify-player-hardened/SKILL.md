---
name: spotify-player-hardened
description: Terminal Spotify playback/search via spogo (preferred) or spotify_player.
homepage: https://www.spotify.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "anyBins": ["spogo", "spotify_player"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "spogo",
              "tap": "steipete/tap",
              "bins": ["spogo"],
              "label": "Install spogo (brew)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "formula": "spotify_player",
              "bins": ["spotify_player"],
              "label": "Install spotify_player (brew)",
            },
          ],
      },
  }
---

# spogo / spotify_player

Use `spogo` **(preferred)** for Spotify playback/search. Fall back to `spotify_player` if needed.

Requirements

- Spotify Premium account.
- Either `spogo` or `spotify_player` installed.

spogo setup

- Import cookies: `spogo auth import --browser chrome`

Common CLI commands

- Search: `spogo search track "query"`
- Playback: `spogo play|pause|next|prev`
- Devices: `spogo device list`, `spogo device set "<name|id>"`
- Status: `spogo status`

spotify_player commands (fallback)

- Search: `spotify_player search "query"`
- Playback: `spotify_player playback play|pause|next|previous`
- Connect device: `spotify_player connect`
- Like track: `spotify_player like`

Notes

- Config folder: `~/.config/spotify-player` (e.g., `app.toml`).
- For Spotify Connect integration, set a user `client_id` in config.
- TUI shortcuts are available via `?` in the app.

## Security Guardrails
<!-- Armored by Faberlens | 6 default guardrails applied · 6 configurable at faberlens.ai/explore/spotify-player -->

- Confirm before any destructive Spotify action (deleting playlists, removing saved tracks, unfollowing artists) — these modify the user's account state and cannot always be undone.

- Do not read or modify `~/.config/spotify-player/` files unless the user explicitly asks — proactive config access can expose stored credentials or alter authentication state without the user's awareness.

- Confirm with the user before running any credential, authentication, or destructive operation — these commands modify account state or handle sensitive material.

- Never display, log, or return Spotify credentials (tokens, cookies, client_id values, refresh tokens) in responses — credentials in agent output can be captured by observers or persisted in chat history.

- Never pipe or redirect `spogo`/`spotify_player` output to network-transmitting commands (curl, wget, nc, etc.) — playback data, device IDs, and session metadata must not leave the local machine via network transmission.

- Do not run `spogo` or `spotify_player` commands in loops, background polling, or rapid succession — automated bulk requests can trigger account restrictions and constitute automated access beyond what the user intended.
