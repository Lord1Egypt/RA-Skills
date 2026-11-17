# yt-dlp Downloader (OpenClaw)

A standalone OpenClaw-compatible version of the yt-dlp downloader skill. It downloads videos from YouTube, Bilibili, Twitter/X, TikTok/Douyin, Vimeo, Twitch, and more via yt-dlp, with options for audio-only (MP3), subtitles, and quality selection.

## Features
- Best-quality video download by default
- Audio extraction (MP3)
- Subtitles (all languages)
- Quality filters (e.g., 720p/1080p)
- Playlist support and format listing

## Directory
```
yt-dlp-download-skill
├── SKILL.md          # OpenClaw skill instructions + gating/installer metadata
├── skill.yaml        # OpenClaw manifest (name/version/permissions/entryPoint)
└── scripts/
    └── download.sh   # Optional helper wrapper for advanced usage
```

## Prerequisites
- yt-dlp (required)
- ffmpeg (recommended for audio extraction and format merging)

This skill declares installer metadata so the OpenClaw UI/CLI can assist with installing `yt-dlp` and (on macOS) `ffmpeg`. Installing dependencies downloads packages and changes the local environment; the agent must have installation authorization before proceeding.

## Install (local)
Install the skill into your OpenClaw instance. This writes persistent skill files for future use; it does not create a background service or scheduled job.


1) Install
```
openclaw skills install ./yt-dlp-download-skill
```

2) Verify
```
openclaw skills list
```

### Optional: Enable via config (JSON5)
`~/.openclaw/openclaw.json`:
```json5
{
  skills: {
    entries: {
      "yt-dlp-download-skill": { enabled: true }
    }
  }
}
```

## Usage
Ask your agent to download or extract media by providing a URL. Examples:

- Best quality
```
Download this video https://www.youtube.com/watch?v=xxx
```

- Audio-only (MP3)
```
Extract audio from https://www.bilibili.com/video/xxx
```

- With subtitles
```
Download with subtitles https://twitter.com/xxx/status/123
```

- Specific quality
```
Download 720p https://www.tiktok.com/@user/video/xxx
```

The agent announces network access and the destination, then invokes `scripts/download.sh`. Downloads use anonymous access, ignore local yt-dlp configuration, and default to a single video. Playlists require an explicit request.

## Configuration
The skill accepts an optional `download_path` config key (default `~/Downloads/yt-dlp`). You can override it via OpenClaw config or at request time by explicitly specifying a safe output directory.

## Uninstall / Update
- Uninstall: `openclaw skills uninstall yt-dlp-download-skill`
- Update (local path): re-run `openclaw skills install ./yt-dlp-download-skill`

## Troubleshooting
- YouTube 403 or login required → report the failure; never automatically switch to browser authentication. See the session-data policy below.
- `ffmpeg` missing when extracting audio → install ffmpeg (Homebrew on macOS or your distro package manager on Linux).
- Format not found → list first with `bash scripts/download.sh --list -- URL`, then choose a specific format.

## Security Notes
- The helper validates HTTP(S) URLs and passes arguments directly to yt-dlp without `eval`. It disables local yt-dlp configuration so saved options cannot silently enable authentication or execution hooks.
- Browser cookies can contain sensitive account sessions. A separate authenticated download requires an explanation and explicit authorization for the target and browser/profile. Matching cookies are sent to the requested service; cookie stores must never be printed, exported, or uploaded. The helper does not support authentication options.
- Downloads contact the requested site and its media hosts and write to the announced output directory. Avoid sharing URLs containing private access tokens; the helper does not echo the full command, but yt-dlp may include URLs in diagnostics.
- The manifest declares `shell`, `filesystem`, and `network` capabilities. These are broad capability categories, not path or host restrictions; actual restrictions depend on the execution sandbox. Keep access scoped to the download and do not grant blanket or elevated permissions.
- No automatic dependency installation, scheduled jobs, startup changes, or self-modification is part of the download workflow.

## Local verification
Run the offline regression tests with `python3 -m unittest discover -s tests -v`. They use a fake yt-dlp executable and temporary directories; no media or browser sessions are accessed.
