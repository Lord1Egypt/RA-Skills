---
name: youtube-full-channel-transcripts
description: >
  Extract transcripts from all videos in a YouTube channel for free (no paid APIs).
  Uses yt-dlp to discover videos and fetch available subtitles. Saves combined transcripts
  as structured JSON or CSV.
version: 1.0.0
author: JARVIS (OpenClaw)
keywords: [youtube, transcript, channel, free, yt-dlp]
metadata:
  openclaw:
    emoji: "🎥"
    requires:
      bins:
        - yt-dlp
        - jq
---

# YouTube Full Channel Transcripts

**Free, local alternative to Apify actor** — no third-party paid APIs.

Fetches all videos from a YouTube channel (or playlist), extracts available transcripts (auto-generated or manual), and exports to JSON/CSV.

## When to Use

- "Get all transcripts from channel X"
- "Export channel Y's video subtitles"
- "Build dataset of all videos from creator Z"

## Prerequisites

- `yt-dlp` installed (https://github.com/yt-dlp/yt-dlp)
- `jq` installed (for JSON processing)
- Internet connection

## Usage

```bash
# Basic: fetch all transcripts from a channel
youtube_full_channel_transcripts channel_url="https://www.youtube.com/@SomeChannel" output_format="json"

# With filters
youtube_full_channel_transcripts channel_url="https://www.youtube.com/c/ChannelName" max_videos=50 languages="en" include_auto_generated=true
```

## Options

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel_url` | string | yes | YouTube channel URL, handle, or playlist URL |
| `output_format` | string | no | Output format: `json` (default) or `csv` |
| `max_videos` | integer | no | Limit number of videos to process (default: all) |
| `languages` | string | no | Comma-separated language codes (e.g., `en,es`). Default: `en` |
| `include_auto_generated` | boolean | no | Include auto-generated transcripts? (default: `true`) |
| `output_dir` | string | no | Directory to save results (default: `workspace/exports/youtube-transcripts`) |

## Output

- `transcripts.json` or `transcripts.csv` — structured data with:
  ```json
  {
    "video_id": "abc123",
    "title": "Video Title",
    "url": "https://youtube.com/watch?v=abc123",
    "upload_date": "20240322",
    "duration": 360,
    "language": "en",
    "transcript": "Full text...",
    "is_auto_generated": false
  }
  ```
- Summary printed to console: number of videos processed, success/failure counts.

## Implementation Details

1. **Discovery:** `yt-dlp --flat-playlist -J` to list all videos
2. **Transcript fetch:** `yt-dlp --write-subs --sub-format srt --skip-download` per video
3. **Parsing:** Extract SRT subtitles and convert to plain text
4. **Combine:** Aggregate results into JSON/CSV

## Errors & Retries

- If a video has no available transcript, it's skipped (logged)
- Network errors: retry up to 3 times with backoff
- Rate limiting: yt-dlp handles automatically; can add `--sleep-interval` if needed

## Notes

- Respect YouTube's rate limits. The tool includes small delays by default.
- Large channels (100+ videos) may take a while; use `max_videos` to limit.
- Auto-generated transcripts are more available but less accurate.
