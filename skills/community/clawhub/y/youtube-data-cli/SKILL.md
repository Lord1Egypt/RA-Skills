---
name: youtube-data-cli
description: >
  Full YouTube Data API v3 CLI covering all 20 resources: search, channels, videos (upload/update/delete/rate),
  playlists, playlist items, comments, subscriptions, captions (upload/download), thumbnails, activities,
  channel sections, channel banners, members, memberships levels, watermarks, and more.
  Triggers: "YouTube", "YouTube search", "YouTube playlists", "YouTube comments", "YouTube subscriptions",
  "search videos", "playlist management", "video comments", "upload video", "video captions", "subtitles",
  "YouTube thumbnail", "channel members", "video categories", "channel banner", "YouTube watermark",
  "rate video", "like video", "channel sections", "YouTube activities".
---

# YouTube Data CLI Skill

You have access to `youtube-data-cli`, a CLI for the YouTube Data API v3 covering all 20 resources with 52 commands. Use it to search YouTube, manage channels/videos/playlists/comments/subscriptions, upload videos and captions, set thumbnails, and more.

## Quick start

```bash
# Check if the CLI is available
youtube-data-cli --help

# Search for videos
youtube-data-cli search --q "node.js tutorial" --type video --max-results 5

# Get a channel's public data
youtube-data-cli channels UCxxxxxxxxxxxxxx
```

If the CLI is not installed, install it:

```bash
npm install -g youtube-data-cli
```

## Authentication

| Method | Use case | Commands |
|--------|----------|----------|
| **API key** | Public data | `search`, `channels`, `videos`, `playlists`, `playlist-items`, `comment-threads`, `comments`, `channel-sections`, `i18n-*`, `video-categories`, `video-abuse-report-reasons` |
| **OAuth 2.0** | Private data + write operations | All `*-insert`/`*-update`/`*-delete` commands, `--mine` queries, `captions`, `members`, `memberships-levels`, `playlist-images`, `thumbnails-set`, `watermarks-*`, `channel-banners-insert` |

Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. `YOUTUBE_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` env vars
3. `~/.config/youtube-data-cli/credentials.json` (auto-detected)

Recommended OAuth scope: `https://www.googleapis.com/auth/youtube` (full access). Add `https://www.googleapis.com/auth/youtube.upload` if using narrower scopes but need video uploads.

**Important:** Service accounts do NOT work with YouTube APIs. You must use OAuth 2.0 with a refresh token.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON.

Global options:
- `--format <format>` -- `json` (default, pretty-printed) or `compact` (single-line)
- `--credentials <path>` -- path to credentials JSON file

Errors are written to stderr as JSON with an `error` field and a non-zero exit code.

## Commands reference

### search

Search YouTube for videos, channels, and playlists.

```bash
youtube-data-cli search --q "query" [--type video] [--max-results 10] [--order viewCount]
```

Key options: `--q` (required), `--type`, `--max-results`, `--order`, `--channel-id`, `--page-token`, `--published-after`, `--published-before`, `--region-code`, `--relevance-language`, `--safe-search`, `--video-duration`, `--event-type`

### channels / channels-update

Get or update channel details.

```bash
youtube-data-cli channels UCxxxxxxxxxxxxxx
youtube-data-cli channels                    # your own channel (OAuth)
youtube-data-cli channels-update --id UCxxxxxxxxxxxxxx --description "New desc" --country US
```

### videos / videos-insert / videos-update / videos-delete

Get, upload, update, or delete videos.

```bash
youtube-data-cli videos dQw4w9WgXcQ
youtube-data-cli videos-insert --file video.mp4 --title "My Video" --privacy private
youtube-data-cli videos-update --id VID --title "Updated Title" --category-id 22 --tags "a,b"
youtube-data-cli videos-delete --id VID
```

### videos-rate / videos-get-rating / videos-report-abuse

Rate videos and report abuse.

```bash
youtube-data-cli videos-rate --id VID --rating like
youtube-data-cli videos-rate --id VID --rating none       # remove rating
youtube-data-cli videos-get-rating --id VID1,VID2
youtube-data-cli videos-report-abuse --video-id VID --reason-id REASON_ID
```

### playlists / playlists-insert / playlists-update / playlists-delete

Manage playlists.

```bash
youtube-data-cli playlists --channel-id UCxxxxxxxxxxxxxx
youtube-data-cli playlists --mine
youtube-data-cli playlists-insert --title "My Playlist" --privacy public
youtube-data-cli playlists-update --id PLxxxxxxxxxxxxxx --title "New Title"
youtube-data-cli playlists-delete --id PLxxxxxxxxxxxxxx
```

### playlist-items / playlist-items-insert / playlist-items-update / playlist-items-delete

Manage videos in playlists.

```bash
youtube-data-cli playlist-items --playlist-id PLxxxxxxxxxxxxxx
youtube-data-cli playlist-items-insert --playlist-id PLxxxxxxxxxxxxxx --video-id dQw4w9WgXcQ
youtube-data-cli playlist-items-update --id ITEM_ID --playlist-id PLxxxxxxxxxxxxxx --video-id dQw4w9WgXcQ --position 0
youtube-data-cli playlist-items-delete --id ITEM_ID
```

### comment-threads / comment-threads-insert

List and post top-level comments.

```bash
youtube-data-cli comment-threads --video-id dQw4w9WgXcQ
youtube-data-cli comment-threads-insert --video-id dQw4w9WgXcQ --text "Great video!"
```

Key options for listing: `--video-id`, `--channel-id`, `--id`, `--order`, `--search-terms`, `--max-results`, `--page-token`

### comments / comments-insert / comments-update / comments-delete / comments-set-moderation-status

Manage comment replies and moderation.

```bash
youtube-data-cli comments --parent-id COMMENT_ID
youtube-data-cli comments-insert --parent-id COMMENT_ID --text "Thanks!"
youtube-data-cli comments-update --id COMMENT_ID --text "Updated text"
youtube-data-cli comments-delete --id COMMENT_ID
youtube-data-cli comments-set-moderation-status --id COMMENT_ID --moderation-status published
```

### subscriptions / subscriptions-insert / subscriptions-delete

Manage subscriptions.

```bash
youtube-data-cli subscriptions --mine
youtube-data-cli subscriptions-insert --channel-id UCxxxxxxxxxxxxxx
youtube-data-cli subscriptions-delete --id SUBSCRIPTION_ID
```

### activities

List channel activities.

```bash
youtube-data-cli activities --channel-id UCxxxxxxxxxxxxxx
youtube-data-cli activities --mine
```

### captions / captions-insert / captions-update / captions-download / captions-delete

Manage video captions (subtitles).

```bash
youtube-data-cli captions --video-id VID
youtube-data-cli captions-insert --video-id VID --file subs.srt --language en --name "English"
youtube-data-cli captions-update --id CAP_ID --file new-subs.srt
youtube-data-cli captions-download --id CAP_ID --tfmt srt --output subs.srt
youtube-data-cli captions-delete --id CAP_ID
```

### channel-banners-insert

Upload a channel banner image. Returns a URL to use with channels-update.

```bash
youtube-data-cli channel-banners-insert --file banner.jpg
```

### channel-sections / channel-sections-insert / channel-sections-update / channel-sections-delete

Manage channel page sections.

```bash
youtube-data-cli channel-sections --channel-id UCxxxxxxxxxxxxxx
youtube-data-cli channel-sections-insert --type singlePlaylist --title "Featured" --playlist-ids PLxxxxxxxxxxxxxx
youtube-data-cli channel-sections-update --id SECTION_ID --type singlePlaylist --title "Updated"
youtube-data-cli channel-sections-delete --id SECTION_ID
```

### i18n-languages / i18n-regions

List supported languages and regions.

```bash
youtube-data-cli i18n-languages
youtube-data-cli i18n-regions
```

### members / memberships-levels

List channel members and membership levels (OAuth required).

```bash
youtube-data-cli members
youtube-data-cli memberships-levels
```

### playlist-images / playlist-images-insert / playlist-images-update / playlist-images-delete

Manage playlist cover images.

```bash
youtube-data-cli playlist-images --parent PLxxxxxxxxxxxxxx
youtube-data-cli playlist-images-insert --playlist-id PLxxxxxxxxxxxxxx --file cover.jpg
youtube-data-cli playlist-images-delete --id IMAGE_ID
```

### thumbnails-set

Upload a custom thumbnail for a video (OAuth required).

```bash
youtube-data-cli thumbnails-set --video-id VID --file thumb.jpg
```

### video-categories / video-abuse-report-reasons

List video categories and abuse report reasons.

```bash
youtube-data-cli video-categories --region-code US
youtube-data-cli video-abuse-report-reasons
```

### watermarks-set / watermarks-unset

Manage channel watermarks (OAuth required).

```bash
youtube-data-cli watermarks-set --channel-id UCxxxxxxxxxxxxxx --file watermark.png
youtube-data-cli watermarks-unset --channel-id UCxxxxxxxxxxxxxx
```

## Workflow guidance

### Discover content

1. Search for videos: `youtube-data-cli search --q "topic" --type video --max-results 10`
2. Get video details: `youtube-data-cli videos VIDEO_ID`
3. Read comments: `youtube-data-cli comment-threads --video-id VIDEO_ID`

### Upload and manage videos

1. Upload: `youtube-data-cli videos-insert --file video.mp4 --title "Title" --privacy private`
2. Set thumbnail: `youtube-data-cli thumbnails-set --video-id VID --file thumb.jpg`
3. Add captions: `youtube-data-cli captions-insert --video-id VID --file subs.srt --language en --name "English"`
4. Make public: `youtube-data-cli videos-update --id VID --title "Title" --privacy public`

### Manage playlists

1. List your playlists: `youtube-data-cli playlists --mine`
2. Create a new one: `youtube-data-cli playlists-insert --title "Favorites" --privacy private`
3. Add videos: `youtube-data-cli playlist-items-insert --playlist-id PL_ID --video-id VID`
4. Reorder: `youtube-data-cli playlist-items-update --id ITEM_ID --playlist-id PL_ID --video-id VID --position 0`

### Comment management

1. List comments on a video: `youtube-data-cli comment-threads --video-id VID --order time`
2. Post a comment: `youtube-data-cli comment-threads-insert --video-id VID --text "..."`
3. Reply to a comment: `youtube-data-cli comments-insert --parent-id COMMENT_ID --text "..."`
4. Moderate: `youtube-data-cli comments-set-moderation-status --id COMMENT_ID --moderation-status published`

### Channel management

1. Get channel info: `youtube-data-cli channels`
2. Update branding: `youtube-data-cli channels-update --id CH_ID --description "..." --country US`
3. Upload banner: `youtube-data-cli channel-banners-insert --file banner.jpg`
4. Set watermark: `youtube-data-cli watermarks-set --channel-id CH_ID --file watermark.png`
5. Manage sections: `youtube-data-cli channel-sections --mine`

## Error handling

- **OAuth credentials required** -- write operations need `client_id`, `client_secret`, `refresh_token`
- **Token refresh failed** -- refresh token may be expired, user needs to re-authorize
- **No credentials found** -- provide credentials via `--credentials`, env vars, or default file
- **HTTP 403 Forbidden** -- insufficient scopes or API not enabled

## API documentation

- [youtube-data-cli documentation](https://github.com/Bin-Huang/youtube-data-cli)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
