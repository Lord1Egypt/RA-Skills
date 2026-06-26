---
name: reel-to-skill
description: Download a TikTok, Instagram Reel, X video, or short-form video URL locally, extract/transcribe the audio, analyse the teaching or workflow inside it, and turn it into a concise OpenClaw skill. Use when the user sends a social video link and asks to learn from it, make a skill from it, extract the process, or build a reusable workflow without manually downloading the video.
---

# Reel to Skill

Use this when the user provides a TikTok/Instagram Reel/X video/short-form video link and wants a skill from it.

## Workflow

1. Download the video locally with `scripts/download_transcribe.py`.
2. Transcribe the audio.
3. Extract the repeatable procedure, decision rules, examples, and caveats.
4. Create a skill folder under `skills/<skill-name>/`.
5. Keep `SKILL.md` concise and procedural.
6. Do not hardcode API keys, cookies, tokens, or user secrets into the skill.

## Script

Run:

```bash
python3 skills/reel-to-skill/scripts/download_transcribe.py "<url>" --out /tmp/reel-skill
```

The script uses:
- `yt-dlp` for downloading
- `ffmpeg` for audio extraction
- OpenAI transcription if `OPENAI_API_KEY` is available

If transcription is unavailable, extract frames and ask the user for a transcript or use available audio tooling.
