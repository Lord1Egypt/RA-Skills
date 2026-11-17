---
name: youtube-playlist-manager
description: "Search YouTube, get full video details, and manage the user's own YouTube playlists via the YouTube Data API v3. Search and video details work with just an API key, without signing in. Managing playlists needs a one-time Google OAuth sign-in in the browser: list playlists and the videos in them, create, edit (title, description, privacy) and delete playlists, add and remove videos. The sign-in is stored locally (by default in ~/.openclaw/youtube/), refreshed automatically, and revoked by logout. Every command can also print JSON (--json) for scripts. Use when the user explicitly asks to search YouTube, get details of a video, or to view or change their YouTube playlists."
summary: "YouTube search, video details (API key) and playlist management (Google OAuth sign-in) via the Data API v3."
version: 1.3.1
homepage: https://github.com/odrobnik/youtube-skill
compatibility: "Python 3.8+ (standard library only) and network access to Google APIs. Works in OpenClaw, Claude Code, Codex and other agents that read SKILL.md."
permissions:
  - "network: Google only (www.googleapis.com, accounts.google.com, oauth2.googleapis.com), plus the local sign-in callback on 127.0.0.1 (port 8923 by default, or the one passed to auth --port)"
  - "file_read: config.json, tokens.json and pending-auth.json in the skill's config folder (~/.openclaw/youtube/ by default, or YOUTUBE_SKILL_CONFIG_DIR, or ${OPENCLAW_STATE_DIR}/youtube)"
  - "file_write: tokens.json and pending-auth.json in that config folder (owner-only)"
  - "env: YOUTUBE_API_KEY, YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_SKILL_CONFIG_DIR, OPENCLAW_STATE_DIR"
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://github.com/odrobnik/youtube-skill
    requires:
      bins: ["python3"]
    primaryEnv: YOUTUBE_API_KEY
    envVars:
      - name: YOUTUBE_API_KEY
        required: false
        description: "YouTube Data API v3 key for search and video details (or api_key in config.json)."
      - name: YOUTUBE_CLIENT_ID
        required: false
        description: "OAuth client ID (Desktop app) for playlist commands (or client_id in config.json)."
      - name: YOUTUBE_CLIENT_SECRET
        required: false
        description: "OAuth client secret for playlist commands (or client_secret in config.json)."
      - name: YOUTUBE_SKILL_CONFIG_DIR
        required: false
        description: "Folder for config.json and the stored sign-in (default ~/.openclaw/youtube/)."
      - name: OPENCLAW_STATE_DIR
        required: false
        description: "OpenClaw's state folder; when set, the default config folder is ${OPENCLAW_STATE_DIR}/youtube."
---

# YouTube Playlist Manager

Search YouTube, read a video's full details, and manage your own playlists through the YouTube Data API v3.

**Entry point:** `{baseDir}/scripts/youtube.py` (Python 3 standard library only)

`{baseDir}` stands for this skill's folder, the one that contains this SKILL.md. Replace it with that folder's full path in every command, because commands run in the agent's workspace. In Claude Code the folder is `${CLAUDE_SKILL_DIR}`, which Claude Code fills in here; OpenClaw's agent resolves `{baseDir}` itself; other agents use the folder where they found this file.

## When to use

- The user explicitly asks to search YouTube, shares a YouTube video and wants its details (the full description with its links and chapters, duration, views), or wants to see or change their own YouTube playlists.
- Not for other video sites, downloading videos, or transcripts.
- `search`, `video`, `list` and `videos` only read. `create`, `edit`, `add`, `remove` and `delete` change the user's YouTube account: run them only for a change the user asked for.

## Setup

See [SETUP.md](SETUP.md). Search and video details work with just an API key, without signing in. Everything that touches the user's playlists (`list`, `videos`, `create`, `edit`, `delete`, `add`, `remove`) needs a one-time Google OAuth sign-in with `auth`.

Credentials are read from config.json in the config folder: `~/.openclaw/youtube/` by default, `${OPENCLAW_STATE_DIR}/youtube` when OpenClaw's state folder is moved (an existing `~/.openclaw/youtube/` stays in use until its files move), or any folder named by `YOUTUBE_SKILL_CONFIG_DIR`. The env vars `YOUTUBE_API_KEY`, `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` override it. The sign-in is stored in tokens.json in the same folder, readable by the owner only. Never print or share these files.

## Commands

```bash
# Search (uses the API key, or the sign-in if no key is set)
python3 {baseDir}/scripts/youtube.py search "query" [--max 1-50] [--order relevance|date|viewCount|rating|title|videoCount]
python3 {baseDir}/scripts/youtube.py search "query" [--duration short|medium|long] [--hd] [--after YYYY-MM-DD] [--channel CHANNEL_ID]

# Get full video details (uses the API key, or the sign-in if no key is set)
python3 {baseDir}/scripts/youtube.py video VIDEO_URL_OR_ID [more ...]   # full description, duration, counts, chapters

# Sign in (one-time) and out
python3 {baseDir}/scripts/youtube.py auth                      # opens a browser, waits for the localhost callback
python3 {baseDir}/scripts/youtube.py auth --manual             # prints the consent URL and exits
python3 {baseDir}/scripts/youtube.py auth --code "<redirect address or code>"
python3 {baseDir}/scripts/youtube.py logout                    # revokes the sign-in at Google, deletes tokens.json

# Playlists
python3 {baseDir}/scripts/youtube.py list
python3 {baseDir}/scripts/youtube.py create "Name" [--privacy private|unlisted|public] [--description "..."]
python3 {baseDir}/scripts/youtube.py edit PLAYLIST_ID [--title "..."] [--description "..."] [--privacy private|unlisted|public]
python3 {baseDir}/scripts/youtube.py delete PLAYLIST_ID [--yes]

# Videos in a playlist
python3 {baseDir}/scripts/youtube.py videos PLAYLIST_ID      # shows each entry's Item ID
python3 {baseDir}/scripts/youtube.py add PLAYLIST_ID VIDEO_URL_OR_ID [more ...]
python3 {baseDir}/scripts/youtube.py remove ITEM_ID [more ...] [--yes]
```

## JSON output (`--json`)

Add `--json` before or after the subcommand (`youtube.py --json list` = `youtube.py list --json`) to get machine-readable output:

- **stdout carries exactly one JSON document**, also for errors. Human-readable text, emoji and warnings go to stderr (discard with `2>/dev/null`).
- Pretty-printed (indent 2) when stdout is a terminal, compact one-line JSON when piped. UTF-8, not ASCII-escaped. YouTube's search returns video titles HTML-escaped (`&#39;`, `&amp;`); the script decodes titles, in text and JSON mode. Descriptions, video details and playlist data are passed through unchanged.
- **Errors:** `{"error": {"message": "...", "code": "..."}}` on stdout, non-zero exit (1 = failure, 2 = usage, including bad option values). `code` is Google's reason (e.g. `playlistNotFound`, `quotaExceeded`, `invalid_grant`, `access_denied`), or `not_signed_in`, `missing_credentials`, `invalid_video`, `missing_oauth_client`, `network_error`, `filesystem_error`, `usage`; `error` for anything else.
- If `add` or `remove` stops part-way on a playlist-level error, the JSON still lists what was already done, with `"ok": false` and an `error` object.

| Command | JSON shape |
|---|---|
| `search` | `[{id, video_id, title, description, channel, channel_id, published_at, url}]` |
| `video` | `[{video_id, title, description, channel, channel_id, published_at, duration, duration_seconds, view_count, like_count, comment_count, url, chapters: [{timestamp, start_seconds, title}]}]` in the order asked; a video that can't be found is `{video_id, found: false, error}` (exit 1) |
| `list` | `[{id, title, description, privacy, item_count, channel, channel_id, published_at, url}]` |
| `videos` | `[{item_id, video_id, position, title, description, channel, channel_id, published_at, playlist_id, url}]` |
| `create`, `edit` | `{ok, playlist: {...same as list...}}` |
| `add` | `{ok, playlist_id, results: [{input, ok, video_id, item_id?, title?, url?, error?}]}` (exit 1 if any failed) |
| `remove` | `{ok, items: [{item_id, found, video_id, title, playlist_id, playlist_title, removed?}]}` |
| `delete` | `{ok, deleted, playlist: {...}}` |
| `remove`/`delete` without `--yes` | the preview plus `"ok": false, "needs_confirmation": true, "dry_run": true`, exit 3 |
| `auth --manual` | `{ok, auth_url, redirect_uri, next}`; `auth --code` / `auth`: `{ok, token_file, has_refresh_token, refresh_token_expires_in}` |
| `logout` | `{ok, revoked, tokens_deleted, was_signed_in}` |

```bash
python3 {baseDir}/scripts/youtube.py --json search "lego technic" --max 3 | jq -r '.[] | "\(.title)\t\(.url)"'
python3 {baseDir}/scripts/youtube.py list --json | jq -r '.[] | select(.privacy == "private") | .id'
python3 {baseDir}/scripts/youtube.py videos PLAYLIST_ID --json | jq -r '.[].item_id'
```

## How to use it

- **`delete` and `remove` are permanent and need `--yes`.** Run them without `--yes` first: they list exactly what would go, change nothing, and exit with status 3. Show that list to the user, and only after a clear yes run the same command with `--yes`.
- **`video` gives the whole description.** `search` returns only a short excerpt; `video` returns the full text with its links, show notes and chapters, plus duration and counts, for one or many videos. Counts the owner hides are null, and live or upcoming streams have no duration yet.
- New playlists are **private** unless the user asks for something else.
- `remove` takes the **Item ID** shown by `videos`, not the video ID.
- `add` and `video` accept watch, short youtu.be, Shorts, embed and live URLs as well as bare 11-character video IDs.
- Search returns the most relevant matches. Use `--order date` only when the user wants the newest uploads.
- YouTube shows changes after a few seconds. `list` right after a change can still show the old state, and two quick `edit`s of the same playlist can undo each other, so leave about 10 seconds between them.
- **Signing in needs the user.** In cloud, container or other headless sessions always use `auth --manual`: send the user the URL and ask for the address their browser shows afterwards. It starts with `http://127.0.0.1:8923/` (or the port passed with `--port`), and that page not loading is expected. Then run `auth --code "<that address>"`. On the user's own computer, plain `auth` opens the browser and finishes by itself.
- If a command reports that the sign-in expired or was revoked, sign in again. If that happens every 7 days, point the user to the "Publish app" step in SETUP.md.

## Security and permissions

- **Network:** only Google. `https://www.googleapis.com` for the YouTube Data API; `https://accounts.google.com` and `https://oauth2.googleapis.com` for signing in and out.
- **Files:** reads config.json from the config folder (default `~/.openclaw/youtube/`); reads and writes tokens.json and, during sign-in, pending-auth.json there, all owner-only. Nothing else on disk.
- **Local:** `auth` opens the browser and listens on `http://127.0.0.1` for up to 5 minutes, on port 8923 unless `--port` picks another. Apart from that, the script starts no other programs and downloads no code.
- **Sign-in lifetime:** the stored sign-in keeps working until it is revoked. `logout` revokes it at Google and deletes tokens.json.
- **Declared scope:** the `permissions` list in the frontmatter states this same scope for reviewers and scanners. Hosts don't enforce it; it describes what the script does.

## Quota

Each Google Cloud project gets 10,000 units a day by default, reset at midnight Pacific time.

| Command | Cost |
|---|---|
| `search` | 100 units (about 100 searches a day) |
| `create`, `edit`, `delete` | 50 units per playlist |
| `add`, `remove` | 50 units per video |
| `video`, `list`, `videos`, previews | 1 unit per 50 entries |

## Limits

- **Watch Later** and watch history aren't available through the API (a Google restriction since 2016).
- The sign-in uses Google's `youtube` scope, which allows managing the whole YouTube account. The script itself only reads search results and video details, and reads and changes playlists.
- To play a playlist inside a web page or an app, see [references/iframe-player.md](references/iframe-player.md).
