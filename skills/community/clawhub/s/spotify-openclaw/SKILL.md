---
name: spotify-openclaw
description: "Full Spotify Premium control + deep music intelligence for OpenClaw. Playback: play by name/URI/playlist, pause, next, prev, volume, shuffle, queue. Auto-launches Spotify if closed. Analysis: top tracks & artists across 3 time periods, genre profile, liked songs breakdown. Discovery: find similar music via related artists graph — works without Spotify's blocked Recommendations API. One-command playlist builder. Credentials stored in macOS Keychain. Triggers: play, pause, next, volume, shuffle, what's playing, top tracks, genre analysis, find similar music, create playlist."
homepage: https://github.com/mixx85/spotify-openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "spotipy",
              "label": "Install spotipy",
            },
          ],
      },
  }
---

# spotify-openclaw

**Full Spotify Premium control + music intelligence for OpenClaw.**

Control playback, analyze your taste, and discover new music — all from chat. 100% local, no extra cloud services.

## ✨ What makes this different

| Feature | This skill | Basic Spotify skills |
|---------|-----------|---------------------|
| Playback control | ✅ play/pause/next/prev/volume/shuffle/queue | ✅ |
| Auto-launch Spotify | ✅ opens app if closed, waits, plays | ❌ |
| Taste analysis | ✅ top tracks & artists × 3 time periods | ❌ |
| Genre profile | ✅ full genre breakdown | ❌ |
| Music discovery | ✅ works without blocked Recommendations API | ❌ |
| Liked songs search | ✅ filter by artist, count, stats | ❌ |
| One-command playlists | ✅ creates + fills in one command | ❌ |
| Multi-language | ✅ English + Russian voice triggers | ❌ |

## 📦 Requirements

- macOS with Spotify Premium
- Free Spotify Developer app — [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Python 3 + spotipy (`pip install spotipy`)

## ⚙️ Setup (one-time)

**1. Create Spotify app** at developer.spotify.com → add redirect URI: `http://127.0.0.1:8888/callback`

**2. Store credentials in macOS Keychain:**
```bash
security add-generic-password -a openclaw -s openclaw.spotify.client_id -w "YOUR_CLIENT_ID"
security add-generic-password -a openclaw -s openclaw.spotify.client_secret -w "YOUR_CLIENT_SECRET"
```

**3. Copy script to OpenClaw scripts folder:**
```bash
cp spotify.py ~/.openclaw/scripts/spotify.py
```

**4. First auth** (browser opens once, then token is cached):
```bash
python3 ~/.openclaw/scripts/spotify.py now
```

## ⚡ Quick start

```bash
# Play something
python3 ~/.openclaw/scripts/spotify.py play "Massive Attack"

# What's playing now
python3 ~/.openclaw/scripts/spotify.py now

# Discover new music based on your taste
python3 ~/.openclaw/scripts/spotify.py discover

# Build this month's playlist (creates + fills in one command)
python3 ~/.openclaw/scripts/spotify.py make-playlist "Top March 2026" short 20
```

## 🎮 All Commands

### Playback
```bash
python3 ~/.openclaw/scripts/spotify.py play                    # resume
python3 ~/.openclaw/scripts/spotify.py play "track name"       # search & play
python3 ~/.openclaw/scripts/spotify.py play spotify:track:URI  # by URI
python3 ~/.openclaw/scripts/spotify.py pause
python3 ~/.openclaw/scripts/spotify.py next
python3 ~/.openclaw/scripts/spotify.py prev
python3 ~/.openclaw/scripts/spotify.py volume 70
python3 ~/.openclaw/scripts/spotify.py volume up / down
python3 ~/.openclaw/scripts/spotify.py shuffle on / off
python3 ~/.openclaw/scripts/spotify.py queue "track name"
python3 ~/.openclaw/scripts/spotify.py now
python3 ~/.openclaw/scripts/spotify.py devices
```

### Analysis
```bash
python3 ~/.openclaw/scripts/spotify.py top-tracks [short|medium|long] [limit]
python3 ~/.openclaw/scripts/spotify.py top-artists [short|medium|long] [limit]
python3 ~/.openclaw/scripts/spotify.py genres [short|medium|long]
python3 ~/.openclaw/scripts/spotify.py recent [limit]
python3 ~/.openclaw/scripts/spotify.py liked [limit]
python3 ~/.openclaw/scripts/spotify.py liked-all
python3 ~/.openclaw/scripts/spotify.py liked-by-artist "Artist Name"
python3 ~/.openclaw/scripts/spotify.py playlists
python3 ~/.openclaw/scripts/spotify.py search "query" [track|artist|album] [limit]
python3 ~/.openclaw/scripts/spotify.py track-info URI
```

Periods: `short` = 4 weeks · `medium` = 6 months · `long` = all time

### Discovery & Playlists
```bash
# Discover by genre profile
python3 ~/.openclaw/scripts/spotify.py discover

# Expand from artist (depth=hops, n=tracks per artist)
python3 ~/.openclaw/scripts/spotify.py discover "Portishead" 3 3

# Related artists
python3 ~/.openclaw/scripts/spotify.py related-artists "The Cure" 10

# Top tracks of any artist
python3 ~/.openclaw/scripts/spotify.py artist-top-tracks "Massive Attack" 5

# Create playlist from top tracks — one command, creates + fills
python3 ~/.openclaw/scripts/spotify.py make-playlist "Top March 2026" short 20

# Manage playlists
python3 ~/.openclaw/scripts/spotify.py create-playlist "My Playlist" "Description"
python3 ~/.openclaw/scripts/spotify.py add-to-playlist PLAYLIST_ID URI1 URI2
```

> **Note:** Spotify's `recommendations` and `audio_features` APIs are blocked for new developer apps. This skill uses `related_artists` + `artist_top_tracks` for discovery instead — no workarounds needed.

## 💡 Agent tips

- Chain `related-artists` → `artist-top-tracks` → `add-to-playlist` for smart discovery playlists
- Use `liked-by-artist` to build themed playlists from your library
- `genres long` gives the most accurate taste profile
- Use `playlists` to get playlist IDs before playing one

> **ALWAYS run `python3 ~/.openclaw/scripts/spotify.py [cmd]`** — never respond with text only.
