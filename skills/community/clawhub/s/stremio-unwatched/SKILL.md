---
name: stremio-unwatched
description: >
  Check Stremio library for unwatched TV episodes, view upcoming release calendar,
  and download new episodes. Use when you need to: (1) find unwatched episodes in
  Stremio library, (2) see upcoming episode air dates, (3) download pending episodes
  via Stremio server or torrent clients, (4) sync Stremio episode calendar to Google
  Calendar. Connects to the Stremio central API and Cinemeta addon. Supports
  transmission, aria2, deluge, and qbittorrent for standalone downloads.
metadata:
  {
    "openclaw":
      {
        "emoji": "📺",
        "os": ["linux", "darwin"],
        "requires":
          { "bins": ["curl", "jq"], "anyBins": ["node", "bun"] },
      },
  }
---

# Stremio Unwatched

Manage unwatched TV episodes from your Stremio library.

## Install

Clone into the OpenClaw workspace skills directory:

```bash
cd /path/to/openclaw-workspace/skills
git clone https://github.com/pat-industries/stremio-unwatched.git
```

Dependencies: `curl`, `jq`, and `node` (or `bun`). Install any missing ones:

```bash
# Debian/Ubuntu (Docker)
apt-get update && apt-get install -y curl jq

# node should already be present; verify:
node --version
```

## Authentication

First-time use prompts for Stremio email/password. The auth key is cached in `~/.openclaw/credentials/stremio.json`.

```bash
scripts/stremio_auth.sh            # Login (interactive)
scripts/stremio_auth.sh --check    # Validate cached key
scripts/stremio_auth.sh --logout   # Clear credentials
```

## List library

```bash
scripts/stremio_library.sh                  # All series
scripts/stremio_library.sh --filter "name"  # Filter by name
scripts/stremio_library.sh --id tt1234567   # Specific show
```

## Find unwatched episodes

The core feature. Fetches metadata from Cinemeta, decodes the watched bitfield, and identifies episodes that have aired but haven't been watched.

```bash
scripts/stremio_unwatched.sh                      # Table of all unwatched
scripts/stremio_unwatched.sh --filter "show"      # Specific show
scripts/stremio_unwatched.sh --season 2            # Specific season
scripts/stremio_unwatched.sh --json                # JSON output
scripts/stremio_unwatched.sh --summary             # Counts per show
```

An episode is "unwatched" if it has aired, is not flagged in the watched bitfield, and playback progress is under 70%.

## Upcoming calendar

Shows upcoming episode air dates using Cinemeta's `calendar-videos` endpoint.

```bash
scripts/stremio_calendar.sh                    # Next 30 days
scripts/stremio_calendar.sh --days 7           # Next 7 days
scripts/stremio_calendar.sh --filter "show"    # Specific show
scripts/stremio_calendar.sh --json             # JSON output
```

### Google Calendar sync

Syncs upcoming episodes to a **dedicated "Stremio TV" Google Calendar** (never the default calendar). Requires the `gog` skill (gogcli).

```bash
scripts/stremio_calendar.sh --gcal-sync         # Sync upcoming to Google Calendar
scripts/stremio_calendar.sh --gcal-clear        # Remove all Stremio TV events
scripts/stremio_calendar.sh --gcal-sync --days 14  # Sync next 2 weeks only
```

Events are created with purple color, deduplicated by summary, and include the Stremio video ID in the description.

## Download episodes

Resolves streams via installed Stremio addons, then downloads. Priority: Stremio server (if running) > auto-detected torrent client > magnet link output.

```bash
scripts/stremio_download.sh                         # All unwatched (interactive)
scripts/stremio_download.sh --filter "show"         # Specific show
scripts/stremio_download.sh --limit 5                # Max 5 episodes
scripts/stremio_download.sh --quality 1080p          # Prefer 1080p
scripts/stremio_download.sh --client transmission    # Force client
scripts/stremio_download.sh --dry-run                # Preview only
scripts/stremio_download.sh --magnets                # Output magnet links
```

Supported torrent clients (auto-detected): `transmission-remote`, `aria2c`, `deluge-console`, `qbittorrent-nox`.

## Check download status

```bash
scripts/stremio_status.sh                       # Server info
scripts/stremio_status.sh --hash <infoHash>     # Specific torrent progress
scripts/stremio_status.sh --watch               # Live refresh (5s)
```

## API details

For endpoint documentation, data structures, and the watched bitfield format, see `references/stremio_api.md`.
