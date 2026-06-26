---
name: social-downloader
description: Download TikTok, Instagram Reel, X/Twitter video, YouTube Short, or other social video links with yt-dlp. Use when the user asks to download/save/send a social video in best quality, or asks to download/transcribe a reel/TikTok and turn it into a reusable skill.
---

# Social Downloader

Use this for social video links.

## Modes

### 1. Download best quality and send back

```bash
bash skills/social-downloader/scripts/download_best.sh "<url>" /tmp/social-download
```

Then inspect the output and send the downloaded video back to the user.

### 2. Download + transcribe for skill creation

```bash
python3 skills/social-downloader/scripts/download_transcribe.py "<url>" --out /tmp/social-skill-source
```

Then:
1. Read the transcript.
2. Extract the reusable workflow.
3. Create or update a concise OpenClaw skill.

## Rules

- Prefer best available quality with `yt-dlp`.
- Do not re-encode unless needed for compatibility or file size.
- Keep downloaded files in a clear local output folder.
- Never hardcode cookies, API keys, auth tokens, or private credentials into the skill.
- If a site requires login/cookies, ask before using a logged-in browser/session.
