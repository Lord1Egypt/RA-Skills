# youtube-digest

An [OpenClaw](https://github.com/openclaw/openclaw) AgentSkill that lets AI agents understand YouTube videos via transcript extraction and LLM-powered summarization.

## What it does

Give any OpenClaw agent a YouTube URL, and it will:

1. **Extract metadata** — title, channel, duration, description
2. **Download subtitles** — prefers manual subs, falls back to auto-captions
3. **Generate a clean transcript** — strips VTT/SRT formatting into plain text
4. **Summarize in Chinese** (or any language) — via the agent's LLM

## How it works

```
User sends YouTube URL
        │
        ▼
Agent matches youtube-digest skill
        │
        ▼
fetch_youtube.py (yt-dlp)
        │
        ├── metadata (JSON)
        ├── subtitles (.vtt)
        └── transcript (.txt)
        │
        ▼
Agent reads transcript → LLM summary
```

**Transcript-first approach**: No GPU needed. Works with yt-dlp's subtitle extraction, which covers 90%+ of YouTube videos. For videos without any subtitles, a Whisper/ASR fallback can be added.

## Requirements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (latest recommended)
- [deno](https://deno.land/) (JS runtime, required by yt-dlp 2026+)
- Python 3.8+
- ffmpeg (optional, for video frame extraction)

## Installation

### Quick install (binary)

```bash
# yt-dlp
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod +x /usr/local/bin/yt-dlp

# deno
curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh
```

### As an OpenClaw skill

Copy this directory into your OpenClaw skills path:

```bash
# Option 1: workspace skills
cp -r youtube-digest ~/.openclaw/workspace/skills/

# Option 2: shared skills (multi-agent)
cp -r youtube-digest /path/to/shared/skills/

# Option 3: config extraDirs
# Add to openclaw.json:
# "skills": { "load": { "extraDirs": ["/path/to/skills"] } }
```

Restart the gateway to load the new skill.

## Usage

### Command line

```bash
# Basic usage
python3 scripts/fetch_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" --out /tmp/output

# With proxy (if needed)
python3 scripts/fetch_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --proxy http://your-proxy:7890 --out /tmp/output

# Prefer specific subtitle languages
python3 scripts/fetch_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --langs "zh.*,en.*,en" --out /tmp/output
```

### Output files

| File | Description |
|------|-------------|
| `summary.json` | Metadata + extraction status |
| `transcript.txt` | Clean plain-text transcript |
| `video.*.vtt` | Raw VTT subtitle file |

### As an OpenClaw agent

When an agent receives a YouTube URL, it will:

1. Read `SKILL.md` for instructions
2. Run `fetch_youtube.py` to extract subtitles
3. Read `summary.json` and `transcript.txt`
4. Use LLM to generate a summary in the user's language

## Subtitle strategy

The script uses a two-step approach to avoid YouTube's aggressive rate limiting:

1. **Step 1**: Request manual (human-uploaded) subtitles — these are reliable and never rate-limited
2. **Step 2**: If no manual subs exist, request auto-captions in the **original language only** (e.g., `en`)

> ⚠️ **Do NOT request translated auto-captions** (e.g., `zh-Hans` for an English video). YouTube's translation API triggers HTTP 429 aggressively. Let the LLM handle translation instead.

## Known issues

- **Cloud IPs may be blocked**: YouTube treats AWS/GCP/Azure IPs as bots. Use a residential proxy.
- **yt-dlp needs deno**: Since 2026, YouTube requires a JS runtime for signature solving. deno is the default.
- **No ASR fallback yet**: Videos without any subtitles will only return metadata + description.

## License

MIT

## Credits

Built by [DeckFun](https://github.com/BenHeee) team with [OpenClaw](https://github.com/openclaw/openclaw).
