---
name: ytapi-youtube-channels
description: "Look up a YouTube channel by @handle or ID and list its latest uploads, all videos (newest, most popular or oldest first) or playlists, or read a playlist's videos, through the YTAPI API. Use for creator research, monitoring a channel for new videos, or collecting a channel's or playlist's videos to summarize. 中文：YouTube 频道、播放列表、最新视频。"
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
    emoji: "📺"
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
    tags: [youtube, channel, playlist, uploads, creators]
    category: media
---

# YouTube channels and playlists

Channels and playlists from [YTAPI](https://ytapi.dev/?utm_source=skill&utm_medium=skill-file): profiles, uploads and playlist contents.

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

## Channels (1 credit each)

`CHANNEL` is an `@handle` or a `UC...` ID.

```bash
# Profile: title, handle, description, subscriber and video counts
curl -s "https://api.ytapi.dev/v1/channels/CHANNEL" -H "Authorization: Bearer $YTAPI_API_KEY"

# Latest uploads
curl -s "https://api.ytapi.dev/v1/channels/CHANNEL/latest" -H "Authorization: Bearer $YTAPI_API_KEY"

# All uploads, paged; sort_by: newest (default), popular, oldest
curl -s "https://api.ytapi.dev/v1/channels/CHANNEL/videos?sort_by=popular" -H "Authorization: Bearer $YTAPI_API_KEY"

# The channel's playlists
curl -s "https://api.ytapi.dev/v1/channels/CHANNEL/playlists" -H "Authorization: Bearer $YTAPI_API_KEY"
```

## Playlists (1 credit per page)

```bash
curl -s "https://api.ytapi.dev/v1/playlists/PLAYLIST_ID" -H "Authorization: Bearer $YTAPI_API_KEY"
```

## Paging

Paged responses carry `has_more` and `next_cursor`. Pass
`cursor=NEXT_CURSOR` to get the next page. Stop when you have enough: every
page costs a credit.

## Transcripts of the videos (1 credit each)

```bash
curl -s "https://api.ytapi.dev/v1/transcripts?video_id=VIDEO_ID&format=text" \
  -H "Authorization: Bearer $YTAPI_API_KEY"
```

For more than a handful of videos, use one batch (up to 100 tasks, 1 credit
per successful task): `POST /v1/batch`, then poll `GET /v1/batch/{id}`.
See <https://docs.ytapi.dev/batch/run>.

## Credits and errors

Only successful responses use credits; errors are free. New accounts get 200
free credits. Until a credit pack is bought, a key can make 1 request per
second and 100 per day (UTC); `429 daily_limit_exceeded` means that day's
limit is used up (it resets at 00:00 UTC; any pack removes it).
`402 insufficient_credits` means the balance is empty: packs from $9 at
<https://ytapi.dev/?utm_source=skill&utm_medium=skill-file#pricing>. `401` means the key is missing or wrong.

For video details, search, channels, playlists and batches in one skill,
install `ytapi`. Full reference: https://docs.ytapi.dev
