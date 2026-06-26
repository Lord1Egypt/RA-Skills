---
name: yt-dlp
description: AI skill to analyze song requests, verify local workspace files, and download missing tracks directly from YouTube bypassing API limits.
homepage: https://github.com/yt-dlp/yt-dlp
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["yt-dlp","ffmpeg"]},"install":[{"id":"apt-ffmpeg","kind":"apt","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (apt)"},{"id":"pip-yt-dlp","kind":"pip","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# yt-dlp (OpenClaw Music Fetcher)

Workflow: Analyze prompt -> Identify specific track -> Check `~/.openclaw/workspace/music/` folder -> Download if missing -> Pass to cmus.

## Find the active workspace music folder

The agent must always operate within the specific OpenClaw workspace directory to ensure portability.
- Path: `~/.openclaw/workspace/music/` (Resolved as an absolute path from the user's home directory).
- Never download files to the root, current working directory, or system folders.

## Track Identification & Verification Logic

When the user requests a song (via lyrics, artist, composer, or title):
1. **Analyze:** Determine the exact track name and artist.
2. **Check Local:** Search the workspace music folder: `find ~/.openclaw/workspace/music/ -type f -iname "*<keyword>*"`
3. **Branching:**
   - If the file EXISTS: Skip download. Pass the absolute file path to the `cmus` skill.
   - If the file is MISSING: Proceed to the download step using `yt-dlp`.

## yt-dlp quick start

Ensure the directory exists, navigate to it, and download the missing track. The `ytsearch1:` prefix is used to grab the best match from YouTube Music/YouTube automatically:
- `mkdir -p ~/.openclaw/workspace/music/ && cd ~/.openclaw/workspace/music/ && yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "ytsearch1:<Exact Track Name> <Artist>"`

## Notes
- **Post-Download Action:** Always wait for the download to finish, then run `find` again to capture the final filename (as `yt-dlp` sanitizes titles) before passing it to `cmus`.
- **Generalization:** Use `~` or `$HOME` instead of hardcoded paths like `/home/huy/` to ensure the skill works for all users.
- **Dependency:** `yt-dlp` requires `ffmpeg` to extract and convert audio streams into `.mp3` format.
- Prefer highly specific search queries (Track + Artist) to ensure the agent picks the correct version of a song.
