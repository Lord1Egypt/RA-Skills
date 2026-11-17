---
name: yt-dlp-download-skill
description: yt-dlp-powered downloader for YouTube, Bilibili, X (Twitter), TikTok/Douyin, and more. Given a video URL, download video (720p/1080p/best), extract MP3/audio-only, fetch subtitles (specify languages), and optionally download playlists; auto-merges audio/video.
metadata:
  openclaw:
    emoji: "⬇️"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["yt-dlp"]
      anyBins: ["ffmpeg"]
    install:
      - id: uv-yt-dlp
        kind: uv
        package: "yt-dlp"
        bins: ["yt-dlp"]
        label: "Install yt-dlp (uv/pipx)"
      - id: brew-ffmpeg
        kind: brew
        formula: "ffmpeg"
        bins: ["ffmpeg"]
        os: ["darwin"]
        label: "Install ffmpeg (brew)"
---

# yt-dlp Video Downloader (OpenClaw)

Use yt-dlp to download videos from thousands of sites.

## When to use
- User shares a video URL and asks to download
- User requests audio-only (MP3) extraction
- User needs subtitles or specific quality

## Safety and authorization
- Download only the URL and media requested by the user. Default to a single video; enable playlists only when requested.
- Announce the network download and destination before execution. A download request authorizes these ordinary effects, not access to browser sessions or unrelated files.
- Use the helper script below. It passes arguments as a Bash array, accepts HTTP(S) URLs, and ignores local yt-dlp configuration. Never build commands with `eval` or interpolate untrusted text into shell source.
- Default to anonymous access. Do not read browser profiles, cookies, credentials, or environment secrets automatically, including after a 403 error.
- If authentication is needed, explain that browser cookies contain sensitive session data and that using them sends matching cookies to the requested service. Obtain explicit authorization for the browser/profile and target before a separate authenticated invocation. Never print, export, or upload cookie stores. The helper intentionally has no authentication option.
- Use the existing sandbox with access to the output directory and required network endpoints. Do not request blanket permissions, elevated execution, or change permissions to bypass a failure.
- Do not install dependencies, change startup files, create scheduled jobs, or modify this skill during a download. If dependencies are missing, explain the required installation and its local changes; install only when authorized.

## Prerequisites
`yt-dlp` must be installed. MP3 extraction requires `ffmpeg`; merging separate video/audio streams also requires it. Installer metadata describes available installation methods, not permission to run them automatically.

## Common commands
Run the bundled helper from this skill's directory, passing each argument separately through the execution tool (or properly shell-quoting literal values).

```bash
# Best available quality, single video
bash scripts/download.sh -- "https://example.com/video"
# MP3 audio
bash scripts/download.sh --audio -- "https://example.com/video"
# Subtitles
bash scripts/download.sh --subs -- "https://example.com/video"
# Maximum height; use 1080 for 1080p
bash scripts/download.sh --quality 720 -- "https://example.com/video"
# Explicit output directory
bash scripts/download.sh --path "$HOME/Downloads/yt-dlp" -- "https://example.com/video"
# List formats without writing downloads
bash scripts/download.sh --list -- "https://example.com/video"
# Playlist, only when requested
bash scripts/download.sh --playlist -- "https://example.com/playlist"
```

## Workflow
1. Resolve the requested video/audio, subtitles, quality and destination; ask only if needed.
2. Check dependencies and announce the destination and network access.
3. Invoke the helper with the requested options and exactly one HTTP(S) URL. Pass the configured `download_path` through `--path` when set.
4. Report the saved location or error. Do not claim success if the command fails.

## Troubleshooting
- 403 or login required: report the access failure. Do not automatically retry with browser cookies; follow the authentication authorization rule above.
- Missing dependency: explain what is needed and seek installation authorization if not already provided.
- Interrupted download: one retry with the same anonymous options is reasonable; stop if it fails again.
- Format unavailable: list formats, then choose one consistent with the requested quality.
