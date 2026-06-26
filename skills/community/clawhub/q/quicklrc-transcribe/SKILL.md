---
name: quicklrc-transcribe
description: Generate synced lyrics or subtitle files (LRC, SRT, WebVTT, ASS, TTML) from any audio/video URL or YouTube link using the QuickLRC AI API.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - QUICKLRC_API_KEY
      bins:
        - curl
    primaryEnv: QUICKLRC_API_KEY
    envVars:
      - name: QUICKLRC_API_KEY
        required: true
        description: QuickLRC API key. Obtain from https://quicklrc.com/dashboard.
    emoji: "🎵"
    homepage: https://quicklrc.com/docs/api
---

# quicklrc-transcribe

Generate a time-synced lyrics or subtitle file from an audio or video URL using the QuickLRC API.

## What it does

- **Auto-transcribe** — sends an audio/video URL and gets back a synced subtitle file
- **Force-align** — provide plain-text lyrics and the API snaps each line to the audio
- **Word-level timestamps** — karaoke-style output with per-word timing
- **Smart sections** — auto-detect [Verse 1], [Chorus], etc.
- Supports YouTube URLs directly

## Auth

Set `QUICKLRC_API_KEY` to your API key from https://quicklrc.com/dashboard.

```bash
export QUICKLRC_API_KEY=qlrc_...
```

## Usage

### Auto-transcribe → LRC (default)

```bash
curl -X POST https://quicklrc.com/api/v1/transcribe \
  -H "Authorization: Bearer $QUICKLRC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fileUrl": "https://example.com/song.mp3"}'
```

### Force-align lyrics → LRC

```bash
curl -X POST https://quicklrc.com/api/v1/transcribe \
  -H "Authorization: Bearer $QUICKLRC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/song.mp3",
    "lyrics": "Hello world\nThis is line two"
  }'
```

### Word-level karaoke + smart sections → SRT

```bash
curl -X POST https://quicklrc.com/api/v1/transcribe \
  -H "Authorization: Bearer $QUICKLRC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/song.mp3",
    "format": "srt",
    "isWordLevel": true,
    "smartSections": true
  }'
```

### YouTube URL

```bash
curl -X POST https://quicklrc.com/api/v1/transcribe \
  -H "Authorization: Bearer $QUICKLRC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fileUrl": "https://youtube.com/watch?v=dQw4w9WgXcQ", "format": "lrc"}'
```

## Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `fileUrl` | string | yes | — | Public audio/video URL or YouTube URL |
| `lyrics` | string | no | — | Plain-text lyrics for forced alignment |
| `format` | string | no | `lrc` | `lrc`, `srt`, `webvtt`, `ass`, `ttml`, `txt` |
| `isWordLevel` | boolean | no | `false` | Per-word timestamps (karaoke) |
| `smartSections` | boolean | no | `false` | Auto-insert [Verse 1], [Chorus] labels |

## Response

HTTP 200 — plain text subtitle file in the requested format.

## Credits

Cost = audio duration rounded up to the nearest minute. Failed requests are not charged. Check remaining credits at https://quicklrc.com/dashboard.

## Errors

| Status | Meaning |
|---|---|
| 401 | Invalid or missing API key |
| 400 | Missing `fileUrl` or invalid `format` |
| 402 | File duration exceeds remaining credits |
| 403 | Usage limit exceeded |
| 500 | Processing error — not charged |
