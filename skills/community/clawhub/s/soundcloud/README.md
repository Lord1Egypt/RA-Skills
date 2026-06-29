# SoundCloud API Skill

[![ClawHub](https://img.shields.io/badge/%F0%9F%A6%9E_ClawHub-Published-22c55e?style=flat)](https://clawhub.ai/leosaucedo/soundcloud)

Search, analyze, and manage SoundCloud tracks, playlists, and users — all from the command line.

## Onboarding

### 1. Create a SoundCloud App

1. Go to <https://soundcloud.com/you/apps> and click **Register a new application**
2. Give it a name (e.g. "ClawHub SoundCloud Skill")
3. Set the **Redirect URI** to `http://localhost:8080/callback`
4. Copy your **Client ID** and **Client Secret**

### 2. Set Environment Variables

```bash
export SOUNDCLOUD_CLIENT_ID="your_client_id"
export SOUNDCLOUD_CLIENT_SECRET="your_client_secret"
```

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`) to persist across sessions.

### 3. Verify Setup

```bash
./scripts/search_tracks.sh "test" --limit 1
```

If this returns results, your app token is working. No manual token management needed — the skill auto-acquires and caches tokens.

### 4. (Optional) Enable Write Operations

For playlists, likes, and follows, run the OAuth helper:

```bash
./scripts/auth_soundcloud.sh
```

This opens a browser for you to authorize the app, then saves a user token for write operations.

### Why Token Caching?

SoundCloud deprecated the old `?client_id=` query parameter — all API calls now require `Authorization: Bearer <token>` headers. The skill automatically:

- Acquires an **app token** (OAuth2 `client_credentials` grant) on first use
- Caches it at `~/.cache/soundcloud/` with `chmod 600` permissions
- Refreshes it when it expires (tokens last ~1 hour)

This avoids hitting the token endpoint on every call and keeps your API usage efficient. The cache is local-only, encrypted at rest on disk, and never sent anywhere.

## Features

- **Track Search** — Filter by genre, BPM, duration, sort by hotness/plays/likes
- **Track Analysis** — Full metadata including BPM, key, license, engagement stats
- **User Profiles** — Stats, bio, following/followers, tracks, playlists
- **Playlist Management** — Create, update, delete playlists
- **Track Interactions** — Like/unlike tracks, follow/unfollow users
- **Batch Operations** — Bulk like, metadata download, availability checks
- **CSV/JSON Output** — Machine-readable output for pipelines and data analysis

## Prerequisites

- **Bash 4+** with `jq` and `curl`
- A [SoundCloud API application](https://soundcloud.com/you/apps) with Client ID and Client Secret

## Installation

```bash
# Clone or copy the skill into your workspace
export SOUNDCLOUD_CLIENT_ID="your_client_id"
export SOUNDCLOUD_CLIENT_SECRET="your_client_secret"
```

The skill auto-acquires and caches an app token on first use — no manual token setup needed for read operations.

## Configuration

### Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `SOUNDCLOUD_CLIENT_ID` | Yes | API application identifier |
| `SOUNDCLOUD_CLIENT_SECRET` | Yes | API application secret |
| `SOUNDCLOUD_USER_TOKEN` | No | OAuth token for write operations |

### Token System

The skill manages two token types automatically:

| Token | Grant Type | Used For | Auto-Managed |
|---|---|---|---|
| App Token | `client_credentials` | Read operations (search, profiles, track info) | Yes |
| User Token | `authorization_code` | Write operations (playlists, likes, follows) | Via OAuth helper |

Token cache is stored at `~/.cache/soundcloud/` with `chmod 600` permissions.

## Usage

### Search & Discovery

```bash
# Basic search
./scripts/search_tracks.sh "lofi hip hop"

# Filtered search
./scripts/search_tracks.sh "jazz" --genre "jazz" --bpm-min 60 --bpm-max 120 --limit 20

# Machine-readable output
./scripts/search_tracks.sh "ambient" --csv > results.csv
./scripts/search_tracks.sh "electronic" --json | jq '.'
```

### Track Analysis

```bash
# By track ID
./scripts/analyze_track.sh 637795515

# By URL (auto-resolved)
./scripts/analyze_track.sh "https://soundcloud.com/artist/track-name"
```

### User Operations

```bash
# Profile with stats
./scripts/get_user_info.sh "username"

# With tracks and playlists
./scripts/get_user_info.sh "username" --with-tracks 5 --with-playlists 3

# List playlists
./scripts/get_user_playlists.sh "username" --limit 20 --with-tracks
```

### Write Operations (require user token)

```bash
# Liking tracks
./scripts/like_track.sh 637795515

# Following users
./scripts/follow_user.sh "username"

# Playlist management
./scripts/create_playlist.sh "My Mix" --description "Curated gems" --tracks "123,456,789"
./scripts/update_playlist.sh PLAYLIST_ID --title "Renamed Mix" --sharing private
./scripts/delete_playlist.sh PLAYLIST_ID
```

### Batch Operations

```bash
# Like a list of tracks from file
./scripts/batch_operations.sh like-tracks track_ids.txt

# Download full metadata for analysis
./scripts/batch_operations.sh download-metadata track_ids.txt --delay 1

# Check which tracks are still available
./scripts/batch_operations.sh check-availability track_ids.txt --verbose
```

## Script Reference

| Script | Purpose | Auth Required |
|---|---|---|
| `search_tracks.sh` | Search tracks with filters | App token |
| `analyze_track.sh` | Full track metadata | App token |
| `get_user_info.sh` | User profile + stats | App token |
| `get_user_playlists.sh` | List user playlists | App token |
| `follow_user.sh` | Follow/unfollow users | User token |
| `like_track.sh` | Like/unlike tracks | User token |
| `create_playlist.sh` | Create playlists | User token |
| `update_playlist.sh` | Update playlist metadata | User token |
| `delete_playlist.sh` | Delete playlists | User token |
| `batch_operations.sh` | Bulk track operations | User token (most actions) |
| `auth_token.sh` | Token status, refresh, test | — |
| `auth_soundcloud.sh` | Interactive OAuth flow | — |

## API Reference

Full endpoint documentation is available in `references/api_endpoints.md`. Key endpoints:

- `GET /tracks` — Search and list tracks
- `GET /tracks/{id}` — Track metadata
- `GET /users/{id}` — User profile
- `POST /playlists` — Create playlist
- `PUT /me/favorites/{id}` — Like a track
- `PUT /me/followings/{id}` — Follow a user

## Error Handling

| Code | Meaning | Resolution |
|---|---|---|
| 401 | Unauthorized | Check credentials, refresh token |
| 403 | Forbidden | Need user token for this operation |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Implement backoff |

All scripts include automatic status code checking and informative error messages.
