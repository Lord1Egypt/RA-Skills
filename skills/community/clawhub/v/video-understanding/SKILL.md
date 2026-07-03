---
name: video-understanding
description: Use whenever the user provides any video URL, YouTube link, or video file, even if they only ask to watch, look at, react to, understand, analyze, summarize, transcribe, inspect, or extract answers from the video.
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["yt-dlp", "ffmpeg"]
      env: ["GEMINI_API_KEY"]
    primaryEnv: "GEMINI_API_KEY"
    install:
      - id: "yt-dlp-brew"
        kind: "brew"
        formula: "yt-dlp"
        bins: ["yt-dlp"]
        label: "Install yt-dlp (brew)"
      - id: "ffmpeg-brew"
        kind: "brew"
        formula: "ffmpeg"
        bins: ["ffmpeg"]
        label: "Install ffmpeg (brew)"
---

# Video Understanding (Gemini)

Analyze videos using Google Gemini's multimodal video understanding. Supports 1000+ video sources via yt-dlp.

## Requirements

- Python 3.10+ with `uv`
- `yt-dlp` — `brew install yt-dlp` / `pip install yt-dlp`
- `ffmpeg` — `brew install ffmpeg` (for merging video+audio streams)
- `GEMINI_API_KEY` environment variable

## Trigger Rule

Use this skill first whenever the user provides a video URL, YouTube link, or video file. The trigger is the video input itself, not whether the user explicitly says "Gemini," "analyze," or "transcribe."

Casual asks like "watch this," "look at this," "what is this?," "you laugh," or "what happens here?" still require this skill.

## Gotchas

- If the skill cannot run because `GEMINI_API_KEY` or another dependency is missing, report that blocker before falling back to local extraction.
- Requires `yt-dlp` and `ffmpeg` installed (sanity-check with `which yt-dlp` / `which ffmpeg`).
- Gemini File API uploads are reusable for follow-up questions while `ACTIVE`, but expire after about 48 hours.
- Gemini explicit CachedContent can speed repeated questions, but has model-specific minimum token counts and storage billing.
- The analyze script downloads non-YouTube videos locally first unless a valid cached Gemini file handle is reused.
- YouTube age-restricted or private videos require authentication cookies.

## Default Output

Returns structured JSON:
- **transcript** — Verbatim transcript with `[MM:SS]` timestamps
- **description** — Visual description (people, setting, UI, text on screen, flow)
- **summary** — 2-3 sentence summary
- **duration_seconds** — Estimated duration
- **speakers** — Identified speakers

## Usage

### Analyze a video (structured JSON output)

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4"
```

Local video files work too:

```bash
uv run {baseDir}/scripts/analyze_video.py "/path/to/video.mp4"
```

### Ask a question (adds "answer" field)

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" -q "What product is shown?"
```

### Continue questions against the same video

Use a stable `--session-key` for the conversation or Slack thread. `--reuse-file-cache` keeps and reuses an `ACTIVE` Gemini File API handle instead of re-uploading; stale handles automatically fall back to a fresh upload/download.

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" --session-key "slack-thread-123" --reuse-file-cache -q "Summarize this"
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" --session-key "slack-thread-123" --reuse-file-cache --continue-chat -q "What happens after the pricing screen?"
```

For long videos with repeated follow-ups, add `--use-context-cache` to try Gemini explicit CachedContent. If Gemini rejects caching, the script falls back to File API reuse.

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" --session-key "slack-thread-123" --reuse-file-cache --use-context-cache --cache-ttl-seconds 3600 -q "Find all UI errors"
```

### Override prompt entirely

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" -p "Custom prompt" --raw
```

### Download only (no analysis)

```bash
uv run {baseDir}/scripts/analyze_video.py "https://example.com/video.mp4" --download-only -o video.mp4
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-q` / `--question` | Question to answer (added to default fields) | none |
| `-p` / `--prompt` | Override entire prompt (ignores -q) | structured JSON |
| `-m` / `--model` | Gemini model | gemini-2.5-flash |
| `--fallback-model` | Optional fallback model for transient Gemini errors | none |
| `-o` / `--output` | Save output to file | stdout |
| `--keep` | Keep downloaded video file | false |
| `--download-only` | Download only, skip analysis | false |
| `--max-size` | Max file size in MB | 500 |
| `--raw` | Raw text output instead of JSON | false |
| `--reuse-file-cache` | Keep/reuse Gemini File API upload handles for follow-ups | false |
| `--use-context-cache` | Try Gemini explicit CachedContent for repeated questions | false |
| `--cache-ttl-seconds` | TTL for explicit CachedContent | 3600 |
| `--cache-dir` | Local directory for cache records | `~/.openclaw/cache/video-understanding` |
| `--session-key` | Conversation/thread key for follow-up reuse | none |
| `--continue-chat` | Include prior cached outputs as follow-up context | false |
| `--purge-cache` | Delete cached Gemini handles for this asset/session | false |

## How It Works

1. **Local video files** → Uploaded directly to Gemini File API
2. **YouTube URLs** → Passed directly to Gemini (no download needed)
3. **All other URLs** → Downloaded via yt-dlp → uploaded to Gemini File API → poll until processed
4. With `--reuse-file-cache`, valid Gemini file handles are reused for follow-up questions; expired/deleted handles trigger a fresh upload/download
5. With `--use-context-cache`, the script tries Gemini CachedContent and falls back to File API reuse if caching is unavailable
6. Gemini analyzes video with structured prompt → returns JSON
7. Temp local files are cleaned up automatically; remote Gemini uploads are deleted unless reuse/cache mode is enabled

## Supported Sources

Any URL supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md): Loom, YouTube, TikTok, Vimeo, Twitter/X, Instagram, Dailymotion, Twitch, and 1000+ more.

## Tips

- Use `-q` for targeted questions on top of the full analysis
- Use `--session-key` plus `--reuse-file-cache` for Slack-thread follow-ups so Loom/local videos are not re-uploaded every turn
- Use `--continue-chat` when the follow-up relies on prior wording like "that screen" or "the second speaker"
- Use `--purge-cache` when done with a sensitive video to delete the remote Gemini handles
- YouTube is fastest (no download step)
- YouTube follow-ups resend the public URL and optional prior context; there is no documented durable YouTube asset handle
- Transient Gemini 503/high-demand errors are retried; set `--fallback-model` only when that model has quota on the account
- Large videos (10min+) work fine — Gemini File API supports up to 2GB (free) / 20GB (paid)
- The script auto-installs Python dependencies via `uv`
