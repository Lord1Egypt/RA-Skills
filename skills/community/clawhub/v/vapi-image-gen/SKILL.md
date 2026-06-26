---
name: vapi-image-gen
description: Generate images via VAPI's OpenAI-compatible Images API. Supports nano-banana and gpt-image model series. Default model is nano-banana-pro. Images are NOT saved locally by default (URL only). Use --save flag when the user wants to keep the image.
homepage: https://api.v3.cm
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["VAPI_API_KEY", "VAPI_BASE_URL"] },
        "primaryEnv": "VAPI_API_KEY",
      },
  }
---

# VAPI Image Gen

Generate images via VAPI's OpenAI-compatible Images API (`/images/generations`).

## Basic Usage

```bash
python3 {baseDir}/scripts/gen.py --prompt "your prompt here"
```

## Options

```bash
# Specify model (default: nano-banana-pro)
python3 {baseDir}/scripts/gen.py --prompt "..." --model nano-banana-pro

# Higher resolution (append -2k or -4k to model name)
python3 {baseDir}/scripts/gen.py --prompt "..." --model nano-banana-pro-2k

# Save image locally (default: NO save, URL only)
python3 {baseDir}/scripts/gen.py --prompt "..." --save

# Save to OSS directory (~/.openclaw/oss/)
python3 {baseDir}/scripts/gen.py --prompt "..." --oss

# Save to custom directory
python3 {baseDir}/scripts/gen.py --prompt "..." --save --out-dir /path/to/dir

# Aspect ratio
python3 {baseDir}/scripts/gen.py --prompt "..." --aspect-ratio 16:9

# Image count
python3 {baseDir}/scripts/gen.py --prompt "..." --count 2
```

## Supported Models

nano-banana series (returns URL, fast):
- nano-banana
- nano-banana-pro  ← default
- nano-banana-2
- nano-banana-pro-2k / nano-banana-pro-4k (high res)

gpt-image series (returns base64, always saved):
- gpt-image-1
- gpt-image-1.5

## Config

Set in `.env` or `~/.openclaw/openclaw.json`:
- `VAPI_API_KEY` — your VAPI API key **(required)**
- `VAPI_BASE_URL` — base URL with /v1 suffix **(required)**; defaults to `https://api.v3.cm/v1` if not set

## Save Behavior

- Default: no local file, output `MEDIA:<url>` directly
- `--save`: save to `~/.openclaw/media/`
- `--oss`: save to `~/.openclaw/oss/`
- gpt-image models always save to media/ (API returns base64 only)
