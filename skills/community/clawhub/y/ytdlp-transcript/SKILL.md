---
name: youtube-transcript
description: Fetch and summarize transcripts from any YouTube video. Paste a URL and your agent reads the video for you — summarize, translate, extract insights.
---

# youtube-transcript

Fetch and summarize transcripts from any YouTube video using yt-dlp.

## Usage

Ask your agent:
- "Get the transcript of [YouTube URL]"
- "Summarize this video: [YouTube URL]"
- "What is the main message of [YouTube URL]?"
- "Translate and explain this video: [YouTube URL]"

## How It Works

Uses `yt-dlp` to download auto-generated or manual captions from YouTube.
Supports all languages — defaults to Portuguese (pt), falls back to English (en).

## Requirements

- `yt-dlp` installed: `brew install yt-dlp`
- Node.js 18+

## Script

```bash
node skills/youtube-transcript/transcript.js <youtube-url-or-id> [lang]
```

## Example

```bash
node skills/youtube-transcript/transcript.js https://www.youtube.com/watch?v=LAdJsmTe8LM pt
```
