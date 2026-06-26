---
name: youtube-digest
description: "Understand, summarize, translate, and extract key points from YouTube videos. Use when a user provides a YouTube URL and wants: (1) a Chinese summary, (2) a transcript or subtitle extraction, (3) translation of spoken content, (4) timestamps / chapter notes, (5) visual understanding via key frames, or (6) question answering about a video. Prefer this skill for transcript-first workflows."
---

# YouTube Digest

Use a transcript-first workflow.

## Quick workflow

1. Run `scripts/fetch_youtube.py <url> --out <dir>` to collect metadata and subtitles.
   If behind a proxy, add `--proxy <proxy-url>`.
2. If subtitles exist, read `summary.json` and the generated transcript file first.
3. If the user only wants a quick answer, summarize directly from the transcript.
4. If the user needs stronger visual grounding, extract key frames with ffmpeg after downloading the video or by using an existing local video file.
5. If no subtitles are available, report that transcript extraction needs `yt-dlp` + a speech-to-text path (for example Whisper) before promising a result.

## Default behavior

- Prefer manual subtitles over auto subtitles.
- Prefer Chinese subtitles when available; otherwise use English auto/manual subtitles.
- Keep downloads minimal: subtitles + metadata first, full video only when visual analysis is necessary.
- For long videos, produce:
  - 3-line executive summary
  - bullet timeline with timestamps
  - key insights / actionable points
  - open questions or uncertainties

## Outputs

For normal requests, return:

- Video topic
- Summary (in user's language)
- Key timestamps
- Notable quotes / insights
- If confidence is limited, say whether the result came from manual subtitles, auto subtitles, or partial metadata only.

## Files produced by the script

The fetch script writes an output directory containing:

- `summary.json` — chosen subtitle file, title, uploader, duration, and extraction status
- `transcript.txt` — plain text transcript when subtitles are available
- raw subtitle files from `yt-dlp` (VTT/SRT)

Read `summary.json` first to decide what to do next.

## Required runtime tools

- `yt-dlp` for metadata + subtitle extraction
- `deno` as JS runtime (required by yt-dlp 2026+)
- `ffmpeg` for media conversion / optional frame extraction (optional)

## Key commands

Basic extraction:

```bash
python3 scripts/fetch_youtube.py "<youtube-url>" --out /tmp/youtube-digest
```

With proxy:

```bash
python3 scripts/fetch_youtube.py "<youtube-url>" --proxy http://your-proxy:port --out /tmp/youtube-digest
```

Prefer specific subtitle languages:

```bash
python3 scripts/fetch_youtube.py "<youtube-url>" --langs zh.*,en.* --out /tmp/youtube-digest
```

## Failure handling

- If `yt-dlp` is missing, stop and install it instead of improvising.
- If YouTube blocks the request (429 or bot detection), try using a proxy or report the limitation.
- If only metadata is available, do not pretend you understood the full video.
- If subtitles are auto-generated, mention that wording may be noisy.

## References

- Read `references/install-and-deploy.md` for deployment instructions.
- Read `references/usage-patterns.md` for output templates for summaries, translations, or Q&A.
