---
name: suno-music
description: AI music generation via Suno API. Submit prompts, style tags, and lyrics to generate songs. Check generation status and download audio/cover art. Use when user asks to create music, generate songs, compose tracks, or produce audio content with AI.
---

# Suno Music

Generate full songs (vocals + instrumentals) via the Suno API.

## Quick Start

```bash
# Set your API key
export SUNO_API_KEY="your_key_here"

# Generate a song and wait for it to finish
python scripts/suno_api.py generate-and-wait \
  --prompt "A melancholic piano ballad about losing someone" \
  --tags "piano,ballad,sad,emotional" \
  --style "Indie Pop" \
  --title "Fading Light"
```

## Commands

| Command | Description |
|---------|-------------|
| `generate` | Submit a generation task (non-blocking) |
| `status --ids <ids>` | Check status of existing generation(s) |
| `generate-and-wait` | Submit + poll until completion |

## Full Options

### generate

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` | required | Lyrics or song description |
| `--tags` | (prompt) | Style tags, comma-separated |
| `--style` | (tags) | Music genre/style |
| `--title` | (prompt) | Song title |
| `--instrumental` | false | Instrumental only |
| `--wait` | false | Wait for first audio chunk |

### generate-and-wait

All of the above, plus:

| Flag | Default | Description |
|------|---------|-------------|
| `--poll-interval` | 5 | Seconds between status checks |
| `--max-polls` | 60 | Max polls before timeout (5min default) |

## API & Key

- **Base URL**: `https://api.sunoapi.org` (override via `SUNO_BASE_URL`)
- **Auth**: Bearer token via `SUNO_API_KEY`
- **Status flow**: `PENDING` → `TEXT_SUCCESS` → `FIRST_SUCCESS` → `SUCCESS`

## Output Fields

When complete, each generation includes:

- `audio_url` — Download link (expires ~15 days)
- `image_url` — Cover art
- `title` — Song title
- `lyric` — Full lyrics
- `tags` / `style` / `duration`

## Examples

### Generate multiple songs from one prompt

```bash
python scripts/suno_api.py generate --prompt "Summer vibes, beach party" --tags "pop,dance,summer"
python scripts/suno_api.py status --ids "12345,12346"
```

### Instrumental only

```bash
python scripts/suno_api.py generate-and-wait \
  --prompt "Cinematic orchestral build-up with brass" \
  --tags "orchestral,cinematic,epic" \
  --instrumental
```

### Custom API endpoint (e.g., self-hosted)

```bash
SUNO_BASE_URL=https://your-suno-instance.com \
  python scripts/suno_api.py generate --prompt "..."
```

## Resources

### scripts/
- `suno_api.py` — Python CLI client for Suno API (generate, status, generate-and-wait)
