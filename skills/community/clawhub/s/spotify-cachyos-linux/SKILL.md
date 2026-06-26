---
name: spotify-linux
description: Control Spotify on Linux via MPRIS DBus. Use when: (1) launching Spotify from command line, (2) playing/pausing/skipping tracks, (3) searching songs and switching playback to a specific track, (4) any Spotify playback control task on Linux.
---

# Spotify Linux Control

Control Spotify desktop client on Linux through MPRIS DBus — no browser automation, no simulated clicks.

## Prerequisites

- Spotify desktop client installed (`/opt/spotify/spotify`, wrapped by `/usr/bin/spotify`)
- An active X11/Wayland session with `$XAUTHORITY` available
- `dbus-send` (bundled with DBus, always present)

## Quick Start

```bash
# Pause/Play toggle
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause

# Next/Previous
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous
```

## 1. Launch Spotify (Detached)

Spotify must be launched with proper X11 auth and fully detached from the agent process tree, so OpenClaw restarts don't kill it.

### Step-by-step

```bash
# 1. Discover Xauthority path
XAUTHORITY=$(ps aux | grep -E 'Xwayland|Xorg' | grep -oP '\-auth \S+' | head -1 | cut -d' ' -f2)

# 2. Launch with setsid (fully detached, survives agent restarts)
DISPLAY=:0 XAUTHORITY="$XAUTHORITY" setsid -f spotify >/dev/null 2>&1

# 3. Wait for DBus registration (Spotify needs ~5-8 seconds)
for i in $(seq 1 10); do
  sleep 1
  if dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
    /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep -q spotify; then
    break
  fi
done
```

Key: `setsid -f` puts Spotify in its own session, independent of the launching process tree. Without it, `nohup &` still binds the process to the same session and it dies when the parent session terminates.

## 2. Search and Play a Track

MPRIS has no search method. The workflow: web-search → extract Spotify track ID → `OpenUri`.

```bash
# Step 1: Search the web for the track to get its Spotify URL
# Example search: "李白 李荣浩 spotify"
# Extract the track ID from URL like: https://open.spotify.com/track/0aLtafjN146xAdZeqYN8Ho

# Step 2: Call OpenUri with the spotify:track:<ID> URI
TRACK_ID="0aLtafjN146xAdZeqYN8Ho"
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:track:$TRACK_ID"
```

Urgent: the Spotify client loads the track and starts playing immediately — no additional Play call needed after OpenUri.

URL types supported:
- `spotify:track:<id>` — single track
- `spotify:album:<id>` — full album
- `spotify:playlist:<id>` — playlist
- `spotify:artist:<id>` — artist page

## 3. Read Playback State

```bash
# Current play/pause status
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:PlaybackStatus

# Current track metadata (title, artist, album, URL, art, etc.)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:Metadata
```

Key metadata fields in returned dict:
- `xesam:title` — track title
- `xesam:artist` — artist (array)
- `xesam:album` — album name
- `xesam:url` — Spotify web URL
- `mpris:trackid` — internal track ID path
- `mpris:artUrl` — album art URL

## 4. Volume Control

```bash
# Set volume (0.0 to 1.0)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Set \
  string:org.mpris.MediaPlayer2.Player string:Volume \
  variant:double:0.5

# Read current volume
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:Volume
```

## 5. Check If Spotify Is Running

```bash
# Quick: process check
pgrep -a spotify

# Reliable: DBus check (confirms fully initialized)
dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep spotify
```

DBus check is preferred because it confirms the client is fully initialized and ready for commands; process check alone can give false positives when Spotify is still starting up.

## 6. Play Daily Recommendation Playlists

"今日推荐" / "每日推荐" maps to Spotify's Daily Mix series — personalized playlists updated daily. Other recommendation playlists include Discover Weekly and Release Radar.

```bash
# Daily Mix 1-6 (personalized, content varies per user/region)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZF1E37SmkLuYDrmF"  # Daily Mix 1 (Chinese music)

# Discover Weekly (每周新发现)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZEVXcJZyENOWUFo7"

# Release Radar (新歌雷达)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZEVXbhM8yqJpzH4B"
```

Note: Daily Mix URIs with `37i9dQZF1E37` prefix are personalized — the same URI shows different content for each user. Content displayed in search results may differ from what the user hears.

## Common DBus Destinations

| Action       | Method                                                  |
| ------------ | ------------------------------------------------------- |
| Play         | `org.mpris.MediaPlayer2.Player.Play`                   |
| Pause        | `org.mpris.MediaPlayer2.Player.Pause`                  |
| PlayPause    | `org.mpris.MediaPlayer2.Player.PlayPause`              |
| Next         | `org.mpris.MediaPlayer2.Player.Next`                   |
| Previous     | `org.mpris.MediaPlayer2.Player.Previous`               |
| Stop         | `org.mpris.MediaPlayer2.Player.Stop`                   |
| Seek         | `org.mpris.MediaPlayer2.Player.Seek` (int64:offset-us) |
| OpenUri      | `org.mpris.MediaPlayer2.Player.OpenUri` (string:uri)   |
| SetPosition  | `org.mpris.MediaPlayer2.Player.SetPosition` (trackId,position) |
