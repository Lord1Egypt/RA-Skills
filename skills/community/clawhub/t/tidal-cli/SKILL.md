---
name: tidal-cli
description: "Control Tidal music streaming from the terminal. Use when the user wants to search Tidal's catalog (artists, albums, tracks, videos, playlists), manage playlists (create, rename, delete, add/remove tracks), manage library/favorites, play music, explore artist/track info, find similar artists or tracks, get personalized recommendations, or view user profile. Triggers on: music-related requests mentioning Tidal, playlist management, music search, 'play this song', 'add to my playlist', 'find this artist on Tidal', 'what playlists do I have', 'recommend me something', 'similar artists to'."
metadata:
  openclaw:
    requires:
      bins: ["tidal-cli"]
    install:
      - id: node
        kind: node
        package: "@lucaperret/tidal-cli"
        bins: ["tidal-cli"]
        label: "Install tidal-cli (npm)"
---

# tidal-cli

CLI for Tidal music streaming. Search catalog, manage playlists, control library, play tracks, explore artists, discover new music.

## First-Time Setup

If `tidal-cli` is not authenticated, run auth first. This opens the user's browser for Tidal login (one-time):

```bash
tidal-cli auth
```

Credentials persist at `~/.tidal-cli/session.json` and auto-refresh.

## Search

```bash
tidal-cli --json search artist "Radiohead"
tidal-cli --json search album "OK Computer"
tidal-cli --json search track "Karma Police"
tidal-cli --json search video "Paranoid Android"
tidal-cli --json search playlist "90s Rock"
```

JSON output returns `[{id, type, name, extra: {popularity, duration, ...}}]`.

## Artist

```bash
tidal-cli --json artist info <id>        # name, bio, genres, popularity
tidal-cli --json artist tracks <id>      # top tracks
tidal-cli --json artist albums <id>      # discography
tidal-cli --json artist similar <id>     # similar artists
```

## Track

```bash
tidal-cli --json track info <id>         # title, artists, album, duration, ISRC, BPM, key
tidal-cli --json track similar <id>      # similar tracks
```

## Playlists

```bash
tidal-cli --json playlist list
tidal-cli --json playlist create --name "My Playlist" --desc "Description"
tidal-cli --json playlist rename --playlist-id <id> --name "New Name"
tidal-cli --json playlist delete --playlist-id <id>
tidal-cli --json playlist add-track --playlist-id <id> --track-id <track-id>
tidal-cli --json playlist remove-track --playlist-id <id> --track-id <track-id>
tidal-cli --json playlist add-album --playlist-id <id> --album-id <album-id>
```

## Library / Favorites

```bash
tidal-cli --json library add --artist-id <id>
tidal-cli --json library add --album-id <id>
tidal-cli --json library add --track-id <id>
tidal-cli --json library remove --artist-id <id>
```

## Recommendations & User

```bash
tidal-cli --json recommend              # My Mixes, Discovery, New Arrivals
tidal-cli --json user profile           # account info
```

## Playback

```bash
tidal-cli playback play <track-id>
tidal-cli playback play <track-id> --quality LOSSLESS
tidal-cli --json playback info <track-id>
tidal-cli --json playback url <track-id>
```

Quality options: `LOW`, `HIGH`, `LOSSLESS`, `HI_RES`.

## Agent Patterns

**Always use `--json`** for programmatic access. Place it before the subcommand.

**Search then act:**
```bash
TRACK_ID=$(tidal-cli --json search track "Bohemian Rhapsody" | jq -r '.[0].id')
tidal-cli --json playlist add-track --playlist-id <id> --track-id "$TRACK_ID"
```

**Create themed playlist:**
```bash
PL_ID=$(tidal-cli --json playlist create --name "Road Trip" | jq -r '.id')
# search and add tracks using $PL_ID
```

**Discovery workflow (search artist -> similar -> top tracks -> add to playlist):**
```bash
ARTIST_ID=$(tidal-cli --json search artist "Portishead" | jq -r '.[0].id')
SIMILAR=$(tidal-cli --json artist similar "$ARTIST_ID" | jq -r '.[0].id')
TRACK_ID=$(tidal-cli --json artist tracks "$SIMILAR" | jq -r '.[0].id')
tidal-cli --json playlist add-track --playlist-id <id> --track-id "$TRACK_ID"
```

**Cover art:** `track info` and `album info` return a `coverUrl` field (640x640 JPEG). Always show it to the user when displaying track or album details — render it as an image.

**Exit codes:** 0 = success, 1 = error, 2 = missing argument. Errors go to stderr with `Error:` prefix.
