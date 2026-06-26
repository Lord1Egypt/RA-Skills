---
name: youtube-transcript-fetcher
description: Fetch full YouTube transcripts with robust InnerTube fallback. Use when extracting captions/transcripts from a YouTube URL, channel, or batch config, especially when normal transcript tools fail, uploader subtitles are missing, or YouTube auto-generated captions may still be recoverable.
metadata:
  openclaw:
    requires:
      bins: ["python3", "yt-dlp"]
    install:
      - id: apt-yt-dlp
        kind: apt
        package: yt-dlp
        bins: ["yt-dlp"]
        label: Install yt-dlp (apt)
      - id: brew-yt-dlp
        kind: brew
        formula: yt-dlp
        bins: ["yt-dlp"]
        label: Install yt-dlp (brew)
---

Fetch transcripts from YouTube videos. Prefer this skill when the goal is to obtain source transcript text, not to summarize.

Run `./youtube-transcript-fetcher --url <youtube-url>` for a single video.
Run `./youtube-transcript-fetcher --channel <channel-id-or-handle> --hours <n>` for recent channel videos.
Run `./youtube-transcript-fetcher --config config/channels.example.json --daily` for batch mode.

The main script is `scripts/youtube_transcript_fetcher.py`.
It uses watch-page scraping plus InnerTube player API fallback with multiple client profiles (`ANDROID`, `WEB`, `TVHTML5_SIMPLY_EMBEDDED_PLAYER`, `IOS`) to recover caption tracks that simpler methods miss, including cases where only YouTube auto-generated captions are available.

Install Python dependencies with `pip install -r requirements.txt` before first use.

Return the transcript text from the generated JSON output. Do not rely on summary fields because this skill is intentionally transcript-first.
