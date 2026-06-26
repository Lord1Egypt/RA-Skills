---
name: video-fetch
description: Fetch, transcribe, and summarize any YouTube or Bilibili video. 4-level fallback: subtitle API → ElevenLabs STT (cloud, high-accuracy) → local Whisper → description. Supports proxy for geo-blocked regions, Bilibili cookie auth, and auto-translation to user's language. Use when the user shares a video link or asks to summarize/analyze a video.
---

# Video Content Fetcher (YouTube & Bilibili)

## Before You Start

This skill needs **1-3 things configured** depending on your use case:

| What | Why | How |
|------|-----|-----|
| **Residential IP proxy** | YouTube blocks datacenter IPs. You MUST use a residential broadband proxy (e.g., HK home broadband). VPS/cloud IPs will fail. | `--proxy socks5h://127.0.0.1:1080` (also install `pysocks`: `pip install pysocks`) |
| **ElevenLabs API key** | Default STT engine for audio transcription when no subtitles exist. Far more accurate than local Whisper, especially for Chinese. | `export ELEVENLABS_API_KEY="sk_..."` or `--stt-api-key @~/.elevenlabs_key`. Get key: https://elevenlabs.io/app/settings/api-keys |
| **Bilibili cookie** | Bilibili AI subtitles require login. Without cookie, falls back to STT. | Export `SESSDATA` + `bili_jct` from browser, save to `~/.bilibili_cookie`, use `--cookie @~/.bilibili_cookie`. See details below. |

**Minimum setup for YouTube:** proxy + ElevenLabs API key (or local Whisper)
**Minimum setup for Bilibili:** ElevenLabs API key (or local Whisper). Cookie optional but recommended.

## Quick Start

```bash
# YouTube
python3 scripts/youtube_fetch.py "https://www.youtube.com/watch?v=VIDEO_ID" --proxy socks5h://127.0.0.1:1080

# Bilibili
python3 scripts/youtube_fetch.py "https://www.bilibili.com/video/BVxxxxxxxxxx"
```

## Fallback Chain

```
1. Subtitle/Transcript API  (highest fidelity — full spoken content)
       |  if unavailable
       v
2. ElevenLabs STT  (default, cloud-based, high accuracy with punctuation)
       |  if no API key or fails
       v
3. Local Whisper  (auto-fallback, requires local install)
       |  if unavailable
       v
4. Video description  (lowest fidelity — creator's written summary only)
```

Always tell the user which source was used. If description-only, explicitly note that it's not a full transcript.

## Platform Support

| Platform | Subtitle source | STT fallback | Description fallback |
|----------|----------------|--------------|---------------------|
| YouTube | youtube-transcript-api | ElevenLabs / Whisper | HTML meta extraction |
| Bilibili | Player API (**cookie required** for AI subs) | ElevenLabs / Whisper | View API |

Platform is auto-detected from URL. Force with `--platform youtube` or `--platform bilibili`.

## Usage

```bash
# YouTube with proxy
python3 scripts/youtube_fetch.py VIDEO_URL --proxy socks5h://127.0.0.1:1080

# Bilibili (cookie required for subtitles — without it, falls back to STT/description)
# IMPORTANT: always use @filepath to avoid exposing credentials in shell history / process list
python3 scripts/youtube_fetch.py "https://www.bilibili.com/video/BVxxxxxxxxxx" --cookie @~/.bilibili_cookie

# Bilibili short link
python3 scripts/youtube_fetch.py "https://b23.tv/xxxxxx"

# Specify transcript languages (default: zh-Hans,zh-Hant,zh,en)
python3 scripts/youtube_fetch.py VIDEO_URL --langs "en,ja" --proxy PROXY

# Force local Whisper instead of ElevenLabs
python3 scripts/youtube_fetch.py VIDEO_URL --stt whisper --whisper-model medium

# Disable audio transcription entirely
python3 scripts/youtube_fetch.py VIDEO_URL --stt none

# JSON output
python3 scripts/youtube_fetch.py VIDEO_URL --json --proxy PROXY

# Save to file
python3 scripts/youtube_fetch.py VIDEO_URL --output /tmp/transcript.txt --proxy PROXY
```

## Dependencies

**Required:**
- `youtube-transcript-api` (pip) — YouTube transcript fetching
- `requests` (pip) — HTTP requests for APIs

**Required for STT (audio transcription):**
- `yt-dlp` (pip or brew) — audio download from YouTube/Bilibili

**Optional (for local Whisper, used as auto-fallback when ElevenLabs is unavailable):**
- `openai-whisper` (pip) — local audio transcription
- `ffmpeg` (system) — required by whisper

**Optional (for SOCKS5 proxy):**
- `pysocks` (pip) — required if using `socks5h://` proxies

```bash
# Required
pip install youtube-transcript-api requests

# Required for STT
pip install yt-dlp

# If using SOCKS5 proxy
pip install pysocks

# Optional: local Whisper fallback
pip install openai-whisper
brew install ffmpeg  # or apt install ffmpeg
```

## ElevenLabs STT (Default)

ElevenLabs Scribe v2 is the default speech-to-text engine. It provides significantly better accuracy than local Whisper, especially for Chinese — correct characters, automatic punctuation, and proper formatting (e.g., book title marks).

**Setup:**

```bash
# Option 1: Environment variable (recommended)
export ELEVENLABS_API_KEY="sk_your_key_here"

# Option 2: Key file
echo "sk_your_key_here" > ~/.elevenlabs_key && chmod 600 ~/.elevenlabs_key
# Then use: --stt-api-key @~/.elevenlabs_key
```

If no API key is available, the skill automatically falls back to local Whisper.

**Security:** Same rules as Bilibili cookie — use env var or `@filepath`, never pass the key directly on the command line.

Get your API key at: https://elevenlabs.io/app/settings/api-keys

## Proxy Setup

YouTube requires a proxy from geo-blocked regions. Bilibili typically works directly from China.

- SOCKS5: `socks5h://127.0.0.1:1080`
- HTTP: `http://127.0.0.1:1081`

**Important: Use residential IP proxies for YouTube.** YouTube blocks datacenter/cloud server IPs. Residential broadband IPs (e.g., Hong Kong home broadband) work reliably, while VPS/cloud IPs will likely be blocked. Recommend routing only YouTube domains through the proxy.

## Bilibili Cookie (Required for Subtitles)

Bilibili subtitles are almost entirely AI-generated and **require login to access**. Without cookies, the subtitle API returns empty results for virtually all videos, and the skill will fall back to STT or description.

**How to get your cookie:**
1. Log in to bilibili.com in your browser
2. Open DevTools (F12) > Application > Cookies
3. Copy the values of `SESSDATA` and `bili_jct`
4. Save to a file: `echo "SESSDATA=xxx;bili_jct=xxx" > ~/.bilibili_cookie && chmod 600 ~/.bilibili_cookie`
5. Use: `--cookie @~/.bilibili_cookie`

**Security warning:**
- Your Bilibili cookie is a login credential. If leaked, others can act as you (post comments, send messages, etc.)
- **Always use `--cookie @filepath`** instead of passing the cookie string directly on the command line, because:
  - Command-line arguments are visible in `ps aux` to other users on the same machine
  - They get saved to shell history (`~/.zsh_history`, `~/.bash_history`)
  - They may appear in Claude Code tool call logs
- Set file permissions: `chmod 600 ~/.bilibili_cookie`
- Add to `.gitignore` if the file is anywhere near a git repo
- Cookies expire periodically — refresh from browser when needed

## Translation & Language

**Respond in the user's conversation language.** Do not default to any hardcoded language.

- If the user speaks English, summarize in English
- If the user speaks Chinese, summarize in Chinese
- If the user speaks Japanese, summarize in Japanese
- If the transcript language differs from the user's language, translate while summarizing

This requires no extra configuration — Claude naturally adapts to the conversation language.

## When Summarizing

- **Transcript/subtitle source**: Summarize freely — this is the complete spoken content
- **ElevenLabs STT source**: High accuracy with punctuation — treat as near-transcript quality
- **Whisper STT source**: Reliable but may have character-level errors in Chinese — note this to the user
- **Description source**: Warn the user that this is the creator's written summary, not the full video content
- For long transcripts (>50K chars), break into sections and summarize incrementally
