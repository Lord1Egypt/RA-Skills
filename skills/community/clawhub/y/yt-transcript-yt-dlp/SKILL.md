---
name: yt_transcript
description: Extract YouTube video transcripts from existing captions (manual or auto-generated) using yt-dlp, with optional timestamps and local SQLite caching. Use when the user asks for a YouTube transcript, captions, subtitles, or wants to turn a YouTube link into text for summarization/search.
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins:
        - python3
        - yt-dlp
    os:
      - linux
      - darwin
      - win32
user-invocable: true
---

# YouTube Transcript (Captions-Only)

Extracts transcripts from **existing** YouTube captions using yt-dlp. Prefers manual subtitles; falls back to auto-generated captions.

## Prerequisites

- Python 3.7+
- `yt-dlp` installed and on PATH (`pip install yt-dlp` or system package)

## How to Run

Script path: `{baseDir}/scripts/yt_transcript.py`

```bash
# Basic usage
python {baseDir}/scripts/yt_transcript.py <youtube_url_or_id>

# Specify language
python {baseDir}/scripts/yt_transcript.py <url> --lang en

# Plain text output
python {baseDir}/scripts/yt_transcript.py <url> --text

# Text without timestamps
python {baseDir}/scripts/yt_transcript.py <url> --text --no-ts

# Custom cache path
python {baseDir}/scripts/yt_transcript.py <url> --cache /path/to/cache.sqlite
```

## Output Formats

### JSON mode (default)

Returns a JSON object:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "lang": "en",
  "source": "manual",
  "segments": [
    { "start": 0.0, "duration": 4.2, "text": "We're no strangers to love" }
  ]
}
```

### Text mode (`--text`)

Newline-separated transcript lines. Use `--no-ts` to omit timestamps.

## Caching

Results are cached in a local SQLite database: `{baseDir}/cache/transcripts.sqlite`

Subsequent calls for the same video/lang/format are served from cache instantly.

To use a custom cache location: `--cache /path/to/transcripts.sqlite`

## Cookies (optional)

For age-restricted or members-only videos, provide a Netscape-format cookies.txt:

```bash
export YT_TRANSCRIPT_COOKIES=/path/to/cookies.txt
python {baseDir}/scripts/yt_transcript.py <url>
# or
python {baseDir}/scripts/yt_transcript.py <url> --cookies /path/to/cookies.txt
```

Cookies must be stored under `~/.config/yt-transcript/` for security.

## Troubleshooting

- **No captions available**: Video has no manual or auto-generated captions
- **yt-dlp not found**: Install with `pip install yt-dlp` or `brew install yt-dlp`
- **Age-restricted video**: Provide cookies from a logged-in YouTube session
- **Rate limited**: Wait and retry; reduce request frequency
