---
name: soundcloud
description: Interact with SoundCloud API for searching tracks, managing playlists, user operations, and audio discovery. Use when the user asks to search for music on SoundCloud, create/edit playlists, get track information, find user profiles, manage favorites, or work with SoundCloud audio content. Requires SOUNDCLOUD_CLIENT_ID and SOUNDCLOUD_CLIENT_SECRET for all operations; SOUNDCLOUD_USER_TOKEN for write operations (playlists, likes, follows).
metadata:
  author: github.com/LeoSaucedo
---

# SoundCloud API Skill

## Overview

This skill enables interaction with SoundCloud's API for music discovery, playlist management, user operations, and audio content analysis.

## Quick Start

### Authentication Setup

All API calls now require the `Authorization: Bearer <token>` header. The old `?client_id=` query parameter is deprecated.

```bash
# Required for ALL operations
export SOUNDCLOUD_CLIENT_ID="your_client_id"
export SOUNDCLOUD_CLIENT_SECRET="your_client_secret"

# Optional: For write operations (playlists, likes, follows)
# Run the OAuth helper to get one:
./scripts/auth_soundcloud.sh
# Or set manually:
export SOUNDCLOUD_USER_TOKEN="your_oauth_token"
```

### Token System

Two token types are managed automatically:

| Token Type | Grant | Used For | Managed |
|---|---|---|---|
| **App Token** | `client_credentials` | Search, track info, user profiles, playlists (read) | Auto-acquired & cached |
| **User Token** | `authorization_code` | Create playlists, like tracks, follow users | Via `auth_soundcloud.sh` |

Token cache: `~/.cache/soundcloud/`

### Basic Usage

```bash
# Search for tracks
./scripts/search_tracks.sh "lofi hip hop" --limit 10

# Get user info
./scripts/get_user_info.sh "nocopyrightsounds" --with-tracks 5

# Analyze a track
./scripts/analyze_track.sh "https://soundcloud.com/artist/track"

# Check token status
./scripts/auth_token.sh status
```

## Scripts Reference

### Search & Discovery

#### `scripts/search_tracks.sh`
Search tracks with filters and formatted output.

```bash
./scripts/search_tracks.sh "search query" [options]
```

**Options:** `--limit N`, `--genre "genre"`, `--bpm-min N`, `--bpm-max N`, `--duration-min N`, `--duration-max N`, `--sort "field"`, `--json`, `--csv`

#### `scripts/analyze_track.sh`
Get detailed track information from ID or URL.

```bash
./scripts/analyze_track.sh "track_id_or_url"
```

**Output:** Metadata, audio properties (BPM, key), engagement stats, license, stream/download URLs.

### User Operations

#### `scripts/get_user_info.sh`
Get user profile with stats, bio, and optional tracks/playlists.

```bash
./scripts/get_user_info.sh "username_or_id" [--with-tracks N] [--with-playlists N] [--json]
```

#### `scripts/get_user_playlists.sh`
List playlists for a user.

```bash
./scripts/get_user_playlists.sh "username_or_id" [--limit N] [--with-tracks] [--json]
```

#### `scripts/follow_user.sh`
Follow or unfollow a user (requires user token).

```bash
./scripts/follow_user.sh "username_or_id" [--unfollow]
```

### Track Interactions

#### `scripts/like_track.sh`
Like or unlike a track (requires user token).

```bash
./scripts/like_track.sh "track_id_or_url" [--unlike]
```

### Playlist Management

#### `scripts/create_playlist.sh`
Create a new playlist (requires user token).

```bash
./scripts/create_playlist.sh "Playlist Name" [--description "text"] [--tracks "id1,id2"] [--sharing public|private] [--genre "genre"] [--tags "tag1,tag2"] [--no-confirm]
```

#### `scripts/update_playlist.sh`
Update playlist title, description, sharing, tracks (requires user token).

```bash
./scripts/update_playlist.sh PLAYLIST_ID [--title "New Title"] [--description "text"] [--sharing public|private] [--add-tracks "id1,id2"] [--remove-tracks "id1,id2"] [--set-tracks "id1,id2"]
```

#### `scripts/delete_playlist.sh`
Delete a playlist (requires user token).

```bash
./scripts/delete_playlist.sh PLAYLIST_ID [--force]
```

### Batch Operations

#### `scripts/batch_operations.sh`
Perform operations on multiple tracks from a file.

```bash
./scripts/batch_operations.sh [action] [file] [options]
```

**Actions:**
- `like-tracks` — Like all tracks in file (requires user token)
- `unlike-tracks` — Unlike all tracks in file (requires user token)
- `add-to-playlist` — Add tracks to a playlist (requires user token + `--playlist-id`)
- `download-metadata` — Download full metadata JSON for all tracks
- `check-availability` — Check which tracks are still available

**File format:** One track ID per line, or CSV with IDs in first column.

### Authentication

#### `scripts/auth_token.sh`
Token manager — source'd by other scripts. Standalone usage:

```bash
./scripts/auth_token.sh status    # Show token status
./scripts/auth_token.sh refresh   # Force app token refresh
./scripts/auth_token.sh test      # Test API connectivity
./scripts/auth_token.sh app       # Print app token
./scripts/auth_token.sh user      # Print user token (if available)
```

#### `scripts/auth_soundcloud.sh`
Interactive OAuth flow to get a user token for write operations.

```bash
./scripts/auth_soundcloud.sh
```

Walks through: browser authorization → code exchange → token save.

## Authentication Reference

### Client Credentials (App Token)
Used automatically for all read operations. Requires `SOUNDCLOUD_CLIENT_ID` + `SOUNDCLOUD_CLIENT_SECRET`.

```bash
curl -X POST https://api.soundcloud.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "grant_type=client_credentials"
```

### Authorization Code (User Token)
Required for write operations. Run `./scripts/auth_soundcloud.sh` for interactive setup, or:

1. Register app at https://soundcloud.com/you/apps
2. Redirect URI: `http://localhost:8080/callback`
3. Authorize via browser
4. Exchange code for token

## Common Use Cases

### Music Discovery Pipeline
```bash
# 1. Search for tracks
./scripts/search_tracks.sh "study beats" --genre "lofi" --bpm-min 60 --bpm-max 80 --limit 50 --csv > candidates.csv

# 2. Analyze specific tracks
./scripts/analyze_track.sh "track_id"

# 3. Create playlist (requires user token)
./scripts/create_playlist.sh "Study Focus" --description "Concentration music" --tracks "id1,id2,id3"
```

### User Profile Analysis
```bash
./scripts/get_user_info.sh "artistname" --with-tracks 10 --with-playlists 5
```

### Batch Processing
```bash
# Download metadata for a list of tracks
echo -e "123\n456\n789" > track_ids.txt
./scripts/batch_operations.sh download-metadata track_ids.txt --delay 1

# Check which tracks are still available
./scripts/batch_operations.sh check-availability track_ids.txt
```

## Error Handling

### Common HTTP Status Codes
- **401 Unauthorized:** Missing/invalid credentials or expired token
- **403 Forbidden:** Insufficient permissions (trying to write without user token)
- **404 Not Found:** Resource doesn't exist
- **429 Too Many Requests:** Rate limit exceeded

### Script Error Handling
All scripts include:
- Automatic token acquisition and refresh
- HTTP status code checking
- JSON response parsing with error detection
- Graceful failure with informative messages

### Token Issues
```bash
# Check token status
./scripts/auth_token.sh status

# Force refresh app token
./scripts/auth_token.sh refresh

# Re-run OAuth for user token
./scripts/auth_soundcloud.sh
```

## References

- [SoundCloud API Reference](https://developers.soundcloud.com/docs/api/reference)
- [Security Updates](https://developers.soundcloud.com/blog/security-updates-api/)
- See `references/` for: `api_endpoints.md`, `oauth_flow.md`, `best_practices.md`
