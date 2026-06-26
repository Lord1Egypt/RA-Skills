# stremio-unwatched

An [OpenClaw](https://openclaw.ai) skill that connects to [Stremio](https://www.stremio.com) to find unwatched TV episodes, view upcoming release calendars, and download new episodes.

## Features

- **Unwatched detection** — scans your Stremio library for series with new episodes you haven't watched yet (only episodes after your last watched, not old backlog)
- **Upcoming calendar** — shows episode air dates for the next N days using Cinemeta
- **Google Calendar sync** — pushes upcoming episodes to a dedicated "Stremio TV" Google Calendar (requires [gog](https://gogcli.sh))
- **Download** — resolves streams via your installed Stremio addons (Torrentio, TPB+, etc.) and downloads via Stremio server, transmission, aria2, deluge, or qbittorrent
- **Quality preference** — choose 1080p, 720p, 4K, or best-available
- **Dry-run by default** — always preview before downloading

## Requirements

- `curl`, `jq`
- `node` or `bun` (for watched bitfield decoding)
- A [Stremio](https://www.stremio.com) account with series in your library
- Optional: a torrent client (`transmission-remote`, `aria2c`, `deluge-console`, or `qbittorrent-nox`)
- Optional: [gog](https://gogcli.sh) for Google Calendar sync

## Install

Clone into your OpenClaw workspace skills directory:

```bash
cd /path/to/workspace/skills
git clone https://github.com/Pat-Industries/stremio-unwatched.git
```

On Debian/Ubuntu (or Docker), ensure dependencies are present:

```bash
apt-get update && apt-get install -y curl jq
```

## Usage

### Authentication

On first use, you'll be prompted for your Stremio email and password. The auth token is cached locally — your password is never stored.

```bash
scripts/stremio_auth.sh            # login (interactive)
scripts/stremio_auth.sh --check    # validate cached token
scripts/stremio_auth.sh --logout   # clear credentials
```

For non-interactive use (cron, Docker), set `STREMIO_EMAIL` and `STREMIO_PASSWORD` environment variables.

### Find unwatched episodes

```bash
scripts/stremio_unwatched.sh                      # table of all unwatched
scripts/stremio_unwatched.sh --filter "Fargo"     # specific show
scripts/stremio_unwatched.sh --season 2           # specific season
scripts/stremio_unwatched.sh --summary            # counts per show
scripts/stremio_unwatched.sh --json               # JSON output
```

Only episodes that have aired and come after your last watched episode are reported. The 70% watch threshold from Stremio is respected for in-progress episodes.

### Upcoming calendar

```bash
scripts/stremio_calendar.sh                       # next 30 days
scripts/stremio_calendar.sh --days 7              # next 7 days
scripts/stremio_calendar.sh --gcal-sync           # sync to Google Calendar
scripts/stremio_calendar.sh --gcal-clear          # clear synced events
```

Google Calendar sync creates a dedicated **"Stremio TV"** calendar — it never touches your default calendar. Requires [gog](https://gogcli.sh) to be installed and authenticated.

### Download episodes

```bash
scripts/stremio_download.sh                       # download all unwatched
scripts/stremio_download.sh --dry-run             # preview only
scripts/stremio_download.sh --filter "Silo"       # specific show
scripts/stremio_download.sh --limit 5             # cap at 5 episodes
scripts/stremio_download.sh --quality 1080p       # prefer 1080p
scripts/stremio_download.sh --magnets             # output magnet links only
```

Download priority: Stremio local server (if running) → auto-detected torrent client → magnet link output.

### Check download status

```bash
scripts/stremio_status.sh                         # server info
scripts/stremio_status.sh --hash <infoHash>       # specific torrent
scripts/stremio_status.sh --watch                 # live refresh
```

## How it works

1. Authenticates against the Stremio central API (`api.strem.io`)
2. Fetches your library via the datastore API
3. For each series, pulls full episode metadata from [Cinemeta](https://v3-cinemeta.strem.io)
4. Decodes Stremio's watched bitfield (zlib-compressed, base64-encoded bit array) to determine which episodes you've seen
5. Resolves streams by querying your installed Stremio addons
6. Downloads via the local streaming server or a standalone torrent client

## License

MIT
