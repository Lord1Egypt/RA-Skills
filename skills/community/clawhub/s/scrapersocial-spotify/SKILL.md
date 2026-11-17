---
name: spotify-api
version: 1.0.4
description: Spotify data toolkit via ScraperSocial — tracks, albums, artists, top tracks, playlists and catalogue search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - spotify
  - music
  - playlists
  - artists
  - social-media
  - api
  - mcp
allowed-tools: Bash(node:*)
metadata:
  openclaw:
    primaryEnv: SCRAPERSOCIAL_KEY
    homepage: https://scrapersocial.com
    requires:
      env:
        - SCRAPERSOCIAL_KEY
    network:
      allow:
        - api.scrapersocial.com
    shell:
      only: scripts/*.js
---

# Spotify API skill

Read public Spotify catalogue data as clean JSON. This Spotify API skill returns a track, album, artist, an artist's top tracks, a playlist, or search results across the catalogue — 2 credits per call, no OAuth dance, no token refresh loop.

This skill wraps **6 live Spotify endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a Spotify link and wants the track, album or artist details.
- You are building a music research or recommendation workflow that needs catalogue metadata.
- You want an artist's top tracks or the contents of a public playlist.

### Do not use this skill when

- **You are building a real music app.** Spotify's own Web API is free, richer, covers playback and user libraries, and is the licensed route. Use this when you want one client across many platforms and no OAuth setup.
- **You need audio, streams or private library data.** Catalogue metadata only.
- **You need listener counts or royalties.** Not published, not available.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 6 documented `/v1/spotify/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_album.js` | Get Spotify album. | handle | 2 credits |
| `get_artist.js` | Get Spotify artist. | handle | 2 credits |
| `get_artist_top_tracks.js` | List Spotify artist top tracks. | handle | 2 credits per track |
| `get_playlist.js` | Get Spotify playlist. | handle | 2 credits |
| `search.js` | List Spotify search. | query | 2 credits per result |
| `get_track.js` | Get Spotify track. | handle | 2 credits |
| `call_endpoint.js` | Call any `/v1/spotify/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/spotify-api/scripts/search.js "Radiohead"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/spotify/album` | handle | album | 2 credits | no |
| `/v1/spotify/artist` | handle | artist | 2 credits | no |
| `/v1/spotify/artist-top-tracks` | handle | track | 2 credits per track | yes |
| `/v1/spotify/playlist` | handle | playlist | 2 credits | no |
| `/v1/spotify/search` | query | result | 2 credits per result | yes |
| `/v1/spotify/track` | handle | track | 2 credits | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get a Spotify track as JSON?

`get_track.js` with the track handle, 2 credits. Albums, artists and playlists have their own scripts at the same price.

### How do I get an artist's top tracks?

`get_artist_top_tracks.js` with the artist handle, 2 credits per track returned.

### Why not just use Spotify's official API?

If Spotify is your only source, do — it is free and more complete. This exists so one key and one envelope cover Spotify alongside the other 32 platforms here.

### Is this an official Spotify API?

No. ScraperSocial is independent and not affiliated with Spotify. It returns publicly available catalogue data only.

## Links

- [Spotify data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
