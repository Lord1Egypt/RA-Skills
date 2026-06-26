---
name: spotify-safe-play
description: Safer Spotify playback for OpenClaw on setups where direct spogo play is unreliable.
homepage: https://github.com/surdragon-design/spotify-safe-player
metadata:
  {
    "openclaw":
      {
        "requires": { "anyBins": ["spogo"] }
      },
  }
---

# Spotify Safe Play

Use this skill when the user wants to play Spotify tracks, albums, or playlists and the machine is known to have unreliable direct `spogo play` behavior.

Files included with this skill

- Wrapper script: `./bin/spotify-safe-play`

Preferred commands

- Search track: `spogo search track "query"`
- Search album: `spogo search album "query"`
- Search playlist: `spogo search playlist "query"`
- Safe playback: `./skills/spotify-safe-play/bin/spotify-safe-play <spotify-uri-or-url-or-id> [--device "..."]`
- Pause / resume / next / previous: `spogo pause`, `spogo play`, `spogo next`, `spogo prev`
- Devices: `spogo device list`, `spogo device set "<name|id>"`
- Status: `spogo status`

Playback rules

- For tracks, the wrapper safely queues the requested track and skips to it.
- For albums and playlists, the wrapper expands the public Spotify page into track URIs, queues them in normal order, skips once into the first track, then exits immediately.
- After the first target track starts, do not send extra `next`, `play`, or verification loops.
- Avoid direct `spogo play <track>` on affected machines because it may resume the current context instead of switching to the requested content.
- If the user has separately installed `spotify-safe-play` into PATH, `spotify-safe-play <item> ...` is also acceptable.

Requirements

- Spotify Premium
- `spogo` installed and authenticated
- Bash, `curl`, `grep`, and `awk`
- An active Spotify Connect target such as Spotify Web Player or the desktop app
