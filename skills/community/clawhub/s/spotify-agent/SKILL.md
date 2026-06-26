---
name: spotify
description: Control Spotify playback, search music, manage playlists, generate discovery playlists, and analyze listening habits via the Spotify Web API. Use when asked to play/pause/skip music, search for songs, manage playlists, get recommendations, check what's playing, or anything Spotify-related. Triggers on "spotify", "play music", "what song", "playlist", "spotify play", "spotify pause", "spotify search".
env:
  - name: SPOTIFY_CLIENT_ID
    description: Spotify app client ID (or set in config.json)
    required: false
  - name: SPOTIFY_CLIENT_SECRET
    description: Spotify app client secret (or set in config.json)
    required: false
  - name: SPOTIFY_REDIRECT_URI
    description: OAuth redirect URI (default http://127.0.0.1:3000/callback)
    required: false
---

# Spotify Skill

Control Spotify playback, manage your library, discover music, and analyze listening habits.

## Prerequisites

1. Create a Spotify app at [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Add a redirect URI (e.g. `http://127.0.0.1:3000/callback`)
3. Copy `config.example.json` to `config.json` and fill in your credentials
4. Required scopes are auto-requested during auth

```bash
cp config.example.json config.json
# Edit config.json with your client_id and client_secret
```

## First-Time Authorization

```bash
python3 scripts/auth.py auth
```

Opens a browser for OAuth2. After authorizing, paste the `code` parameter from the redirect URL:

```bash
python3 scripts/auth.py auth <code>
```

Tokens are saved to `config.json` and auto-refreshed. For headless setups, run auth on a machine with a browser, then copy `config.json`.

## Commands

Run via `python3 scripts/spotify.py <command> [args]`

### Playback
| Command | Args | Description |
|---------|------|-------------|
| `now-playing` | — | Current track, artist, album, progress |
| `play` | `[uri]` | Resume playback, optionally with a specific track URI |
| `pause` | — | Pause playback |
| `next` | — | Skip to next track |
| `prev` | — | Previous track |
| `seek` | `position_ms` | Seek to position in ms |
| `volume` | `0-100` | Set volume percentage |
| `shuffle` | `on\|off` | Toggle shuffle |
| `repeat` | `off\|track\|context` | Set repeat mode |
| `queue-add` | `uri` | Add track to queue |
| `queue` | — | Get current queue |
| `devices` | — | List available devices |
| `transfer` | `device_id` | Transfer playback to device |

### Search & Discover
| Command | Args | Description |
|---------|------|-------------|
| `search` | `query` | Search tracks, artists, albums, playlists |
| `recommendations` | `[track_id]` | Get recommendations seeded from a track |
| `audio-features` | `track_id` | Danceability, energy, tempo, key, etc. |

### Library
| Command | Args | Description |
|---------|------|-------------|
| `saved-tracks` | `[limit]` | Get saved/liked tracks |
| `save` | `id1 id2 ...` | Save tracks to library |
| `playlists` | `[limit]` | List your playlists |
| `playlist-tracks` | `playlist_id` | Get tracks in a playlist |
| `create-playlist` | `name [description]` | Create a new playlist |
| `edit-playlist` | `playlist_id [new_name]` | Edit playlist name/description |
| `add-to-playlist` | `playlist_id uri1 ...` | Add tracks to playlist |
| `remove-from-playlist` | `playlist_id uri1 ...` | Remove tracks from playlist |
| `play-playlist` | `playlist_id` | Start playing a playlist from the beginning |
| `smart-playlist` | `name [source] [limit] [time_range]` | Auto-generate playlist (see below) |
| `claw-list` | `[name] [seeds] [per_seed]` | Discovery playlist (see below) |

### User Data
| Command | Args | Description |
|---------|------|-------------|
| `me` | — | Your Spotify profile |
| `top-tracks` | `[short\|medium\|long_term]` | Your top tracks |
| `top-artists` | `[short\|medium\|long_term]` | Your top artists |
| `recent` | `[limit]` | Recently played tracks |

## Smart Playlists

`smart-playlist` auto-generates playlists from your listening data:

```bash
# From your top tracks (last 6 months)
python3 scripts/spotify.py smart-playlist "My Favorites" top 30 medium_term

# From your liked/saved tracks
python3 scripts/spotify.py smart-playlist "Liked Mix" saved 20

# Recommendations based on your top tracks (discovers new music)
python3 scripts/spotify.py smart-playlist "Discover Weekly DIY" top-recs 30 short_term
```

Sources: `top` (most played), `saved` (liked songs), `top-recs` (recommendations from top tracks)
Time ranges: `short_term` (~4 weeks), `medium_term` (~6 months), `long_term` (years)

## Claw-List (Discovery Playlists)

`claw-list` creates a discovery playlist with diverse seeds from your top/saved tracks, plus mood-matched related tracks:

```bash
# Default: 5 seeds × 5 related tracks = 30 tracks
python3 scripts/spotify.py claw-list "My Mix"

# Custom: 8 seeds, 3 related each = 32 tracks
python3 scripts/spotify.py claw-list "Quick Mix" 8 3

# Larger: 10 seeds, 7 related each = 80 tracks
python3 scripts/spotify.py claw-list "Deep Dive" 10 7
```

How it works:
1. Picks diverse seed tracks from your top 50 + saved tracks (deduplicates by artist for variety)
2. For each seed: analyzes audio features (energy, valence, danceability, etc.) to determine mood
3. Adds 2 same-artist deep cuts + (per_seed - 2) mood-matched discovery tracks via search
4. Creates the playlist with all tracks interleaved (seed, related, seed, related...)

## Agent Usage Patterns

1. **"Play [song name]"** → `search` the song, then `play` the first result's URI
2. **"What's playing?"** → `now-playing`
3. **"Skip/pause/next"** → direct command
4. **"Make me a playlist of..."** → `search` for tracks, `create-playlist`, `add-to-playlist`
5. **"Music like X"** → `recommendations` seeded from X's track ID
6. **"My top artists this month"** → `top-artists short_term`
7. **"Make me a discovery mix"** → `claw-list` with desired size

## URIs

Spotify uses URIs like `spotify:track:4cOdK2wGLETKBW3PvgPWqT`. Extract the ID from URLs like `https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT` — the ID is the part after `/track/`.

## API Migration Notes (February 2026)

Spotify's February 2026 API migration removed several endpoints for dev-mode apps. This skill handles them:

- **Playlist tracks**: Uses `/playlists/{id}/items` (new) instead of `/tracks` (removed). Response field changed from `track` to `item`.
- **Create playlist**: Uses `/me/playlists` instead of `/users/{id}/playlists` (removed).
- **Recommendations**: `/recommendations` and `/related-artists` may return 404/403 in dev mode. Claw-list uses search-based discovery as a fallback.
- **Batch endpoints**: `/tracks`, `/artists`, `/albums`, `/browse/new-releases` are removed in dev mode.

Apps in Extended Quota Mode are unaffected. Request extended quota at the Spotify Developer Dashboard if needed.

## Config

- `config.json` stores OAuth2 tokens and credentials — **do not commit or share**
- Tokens auto-refresh via `auth.py` (called transparently by `spotify.py`)
- `config.example.json` is the template for new setups
- Env vars `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI` override config.json if set

## Requirements

- Python 3.8+
- A Spotify Premium account (for playback controls)
- No external Python packages needed — uses only stdlib
