---
name: ytapi-youtube-summarize
description: "Summarize a YouTube video, or the latest videos of a channel, into notes with key points, quotes and timestamped links, using transcripts from the YTAPI API. Use when the user shares a YouTube link and asks what it says, wants a TL;DR, notes, chapters, key takeaways or a digest of a creator's new uploads. Works on servers and cloud agents where direct YouTube fetching is blocked. 中文：总结 YouTube 视频、生成笔记。"
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
    emoji: "🧾"
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
    tags: [youtube, summary, summarize, notes, video]
    category: media
---

# Summarize YouTube videos

Turn a YouTube video, or a channel's new uploads, into notes, using transcripts from [YTAPI](https://ytapi.dev/?utm_source=skill&utm_medium=skill-file).

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

## One video

1. Details (free): title, channel, length, caption languages.

   ```bash
   curl -s "https://api.ytapi.dev/v1/videos/VIDEO_ID/basic-info" -H "Authorization: Bearer $YTAPI_API_KEY"
   ```

2. Transcript with timestamps (1 credit). Save it to a file; long videos
   give long transcripts.

   ```bash
   curl -s "https://api.ytapi.dev/v1/transcripts?video_id=VIDEO_ID&format=segments&languages=en,*" \
     -H "Authorization: Bearer $YTAPI_API_KEY" -o /tmp/ytapi-transcript.json
   ```

   `segments` holds `text` with `start` seconds. For a shorter file without
   timestamps, use `format=text`.

3. Write the summary in the user's language:
   - one or two sentences on what the video is about;
   - the key points, each with a link to its moment:
     `https://youtu.be/VIDEO_ID?t=START_SECONDS`;
   - notable quotes, quoted exactly;
   - say if the captions were auto-generated (`track_kind` is `asr`), since
     names and numbers may be misheard.

   For a video over an hour, summarize it section by section, then combine.

## A channel's new videos

1. Latest uploads (1 credit): `GET /v1/channels/@HANDLE/latest`.
2. Pick the videos the user cares about (for example, published since the
   last digest), fetch each transcript with `format=text`, and summarize each
   in a few lines with its link.

Each transcript costs a credit; ask before summarizing more than about ten
videos.

## Credits and errors

Only successful responses use credits; errors are free. New accounts get 200
free credits. Until a credit pack is bought, a key can make 1 request per
second and 100 per day (UTC); `429 daily_limit_exceeded` means that day's
limit is used up (it resets at 00:00 UTC; any pack removes it).
`402 insufficient_credits` means the balance is empty: packs from $9 at
<https://ytapi.dev/?utm_source=skill&utm_medium=skill-file#pricing>. `401` means the key is missing or wrong.

For video details, search, channels, playlists and batches in one skill,
install `ytapi`. Full reference: https://docs.ytapi.dev
