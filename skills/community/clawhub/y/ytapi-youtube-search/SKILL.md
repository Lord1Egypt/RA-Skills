---
name: ytapi-youtube-search
description: "Search YouTube for videos, channels, playlists or Shorts, filtered by upload date, duration or sort order, through the YTAPI API, then read the transcripts of the results. Use when the user wants to find YouTube videos on a topic, recent talks or tutorials, reviews, or what creators say about something. 中文：搜索 YouTube 视频。"
version: 1.2.0
homepage: https://ytapi.dev
license: MIT-0
required_environment_variables:
  - name: YTAPI_API_KEY
    prompt: "YTAPI API key (starts with sk_)"
    help: "Leave empty and the agent can create a free account for you (200 credits, no card), or get a key at https://ytapi.dev/app/api-keys?utm_source=skill&utm_medium=skill-file"
    required_for: "All YTAPI requests"
metadata:
  openclaw:
    emoji: "🔎"
    homepage: https://ytapi.dev
    requires:
      bins:
        - curl
    primaryEnv: YTAPI_API_KEY
    envVars:
      - name: YTAPI_API_KEY
        required: false
        description: "YTAPI API key (sk_...). If it is not set, the skill can create a free account and key with the user's email."
  hermes:
    tags: [youtube, search, videos, research]
    category: media
---

# YouTube search

Search YouTube from the agent with [YTAPI](https://ytapi.dev/?utm_source=skill&utm_medium=skill-file), then pull transcripts of what you find.

## YTAPI tools

If this session already has the YTAPI tools (`get_transcript`,
`get_video_info`, `get_video_details`, `get_video_heatmap`, `get_comments`,
`search_youtube`, `get_channel`, `get_channel_videos`,
`get_playlist_videos`), from the YTAPI connector or plugin, use them: they
need no API key and no `curl`. The REST API below is for when those tools
are missing, or for what they don't cover, such as batches.

## Setup

If `YTAPI_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md)
and follow it: the user either pastes a key or you create a free account
with their email (200 credits, no card). Send the key as
`Authorization: Bearer $YTAPI_API_KEY` and never print it.

## Search (1 credit per page)

```bash
curl -s -G "https://api.ytapi.dev/v1/search" \
  --data-urlencode "q=QUERY" -d type=video -d limit=20 \
  -H "Authorization: Bearer $YTAPI_API_KEY"
```

| Param | Values |
| --- | --- |
| `q` | Search text |
| `type` | `all`, `video`, `channel`, `playlist`, `shorts`, `movie` |
| `upload_date` | `hour`, `today`, `week`, `month`, `year` |
| `duration` | `short` (under 4 min), `medium`, `long` (over 20 min) |
| `sort_by` | `relevance`, `upload_date`, `view_count`, `rating` |
| `limit` | Results per page, 1 to 50 (default 20) |
| `cursor` | `next_cursor` from the previous page, when `has_more` is true |

Results are in `items`: `id`, `type`, `title`, `author`, `channel_id`,
`length_seconds`, `view_count_text`, `published_text`.

Free autocomplete: `GET /v1/search/suggestions?q=TEXT`.

## Then read the videos (1 credit each)

```bash
curl -s "https://api.ytapi.dev/v1/transcripts?video_id=VIDEO_ID&format=text" \
  -H "Authorization: Bearer $YTAPI_API_KEY"
```

Pick the few most relevant results by title, channel and length before
fetching transcripts; each transcript costs a credit.

## Credits and errors

Only successful responses use credits; errors are free. New accounts get 200
free credits. Until a credit pack is bought, a key can make 1 request per
second and 100 per day (UTC); `429 daily_limit_exceeded` means that day's
limit is used up (it resets at 00:00 UTC; any pack removes it).
`402 insufficient_credits` means the balance is empty: packs from $9 at
<https://ytapi.dev/?utm_source=skill&utm_medium=skill-file#pricing>. `401` means the key is missing or wrong.

For video details, search, channels, playlists and batches in one skill,
install `ytapi`. Full reference: https://docs.ytapi.dev
