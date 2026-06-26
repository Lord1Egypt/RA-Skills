---
name: social-video-downloader
description: Download videos from Instagram Reels, TikTok, YouTube Shorts, Twitter/X clips,
  and other social media platforms. Use when the user clearly wants to download/save/grab a
  video from a social media link. Triggers on URLs containing instagram.com/reel,
  instagram.com/p/, tiktok.com, youtube.com/shorts, x.com/*/status, twitter.com/*/status.
  Do NOT trigger if the user is just sharing a link for context or asking about the content —
  only activate when download intent is clear (e.g. "download this", "save this",
  "grab this video", "send me this").
---

# Social Video Downloader

Download social media videos via yt-dlp and send them to the user.

## Requirements

- `yt-dlp` must be installed
- `ffmpeg` recommended for best format support

## Setup

See [SETUP.md](SETUP.md) for installation and configuration.

## Workflow

1. Verify download intent is clear from the user's message
2. Run the download script:
   ```bash
   python3 scripts/download.py "<url>" /tmp
   ```
3. On `SUCCESS:<path>`, send file to user via the message tool
4. On `ERROR:...`, report failure to user
5. After sending, delete the temp file with `rm <path>`

## Sending the File

Use the `message` tool with `action=send`, `media=<path>`, and `buttons=[]`.

If file exceeds Telegram's 50MB limit, inform the user and provide the file path instead.

## Supported Platforms

Instagram (Reels, Posts), TikTok, YouTube Shorts, Twitter/X, Reddit, Facebook, Vimeo, Dailymotion, Twitch, Bilibili, and more.

## Security

The script includes these protections:

- **URL allowlist** — only pre-approved domains can be downloaded from
- **SSRF protection** — blocks URLs resolving to private/internal IP ranges
- **Command injection protection** — URLs are validated against shell metacharacters, and `--` separator prevents option injection
- **Subprocess isolation** — URLs passed as separate arguments, never interpolated into shell strings

## Safety Guards

- **No playlists** — `--no-playlist` prevents accidentally downloading hundreds of files
- **Metadata check** — verifies video info before downloading
- **Retry limit** — `--retries 2` stops after failures to avoid bans
- **Timeout** — `--socket-timeout 30` bails on stalled connections
- **Timestamp filenames** — `social_dl_<timestamp>.mp4` prevents filename collisions
