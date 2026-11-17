---
name: ytapi-youtube-transcript
description: "Get the transcript, subtitles or captions of a YouTube video (plain text, Markdown, timestamped JSON, SRT or VTT, any language) through the YTAPI API. Use when the user shares a YouTube link or video ID and wants what was said: to read, summarize, quote, translate or search it. Also use when yt-dlp or youtube-transcript-api fails with HTTP 429, a bot check or an IP block, common on servers and cloud agents. 中文：YouTube 字幕、视频文字稿。"
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
    emoji: "📝"
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
    tags: [youtube, transcript, subtitles, captions, srt, vtt]
    category: media
---

# YouTube transcripts

Transcripts and subtitles for any YouTube video with captions, from [YTAPI](https://ytapi.dev/?utm_source=skill&utm_medium=skill-file).

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

## Get a transcript (1 credit)

```bash
curl -s "https://api.ytapi.dev/v1/transcripts?video_id=VIDEO_ID_OR_URL&format=text" \
  -H "Authorization: Bearer $YTAPI_API_KEY"
```

| Param | Default | Values |
| --- | --- | --- |
| `video_id` | required | 11-character ID or a YouTube URL |
| `format` | `segments` | `text`, `markdown`, `segments` (JSON with start/end seconds), `sentences`, `srt`, `vtt`, `word_timestamps` |
| `languages` | `*` | Comma-separated codes in order of preference; `*` is the video's own language. `en,*` = English if available, else the original |
| `word_level` | `false` | Word timings on auto-generated tracks (with `format=word_timestamps`) |

- Use `format=text` or `markdown` to read, summarize or quote; `segments`
  when you need timestamps (link a moment as `https://youtu.be/VIDEO_ID?t=SECONDS`);
  `srt` or `vtt` for subtitle files.
- Which languages exist, for free: `GET /v1/videos/VIDEO_ID/basic-info`
  (`available_languages`, each `manual` or `asr`).
- Long videos give long transcripts: save to a file and read it in parts.
- `404 language_not_found` / `captions_disabled`: no captions in those
  languages, or none at all. Try `languages=*`.

## Credits and errors

Only successful responses use credits; errors are free. New accounts get 200
free credits. Until a credit pack is bought, a key can make 1 request per
second and 100 per day (UTC); `429 daily_limit_exceeded` means that day's
limit is used up (it resets at 00:00 UTC; any pack removes it).
`402 insufficient_credits` means the balance is empty: packs from $9 at
<https://ytapi.dev/?utm_source=skill&utm_medium=skill-file#pricing>. `401` means the key is missing or wrong.

For video details, search, channels, playlists and batches in one skill,
install `ytapi`. Full reference: https://docs.ytapi.dev
