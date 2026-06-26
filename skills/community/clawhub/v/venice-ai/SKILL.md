---
name: venice-ai
description: Complete Venice AI platform — text generation, vision/image analysis, web search, X/Twitter search, embeddings, TTS, speech-to-text, image generation, background removal, video creation, music generation, upscaling, and AI editing. Private, uncensored AI inference for everything.
homepage: https://venice.ai
metadata:
  {
    "clawdbot":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["python3"], "env": ["VENICE_API_KEY"] },
        "primaryEnv": "VENICE_API_KEY",
        "notes": "Full Venice AI platform — text, vision, images, video, audio, music, embeddings. One skill for everything.",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Venice AI — Complete Platform Skill

## What is Venice AI?

**Venice AI is the AI platform for people who don't want Big Tech watching over their shoulder.** Unlike OpenAI, Anthropic, and Google — where every prompt is logged, analyzed, and potentially used to train future models — Venice offers **true privacy** with zero data retention on private models. Your conversations stay yours.

Venice is also **uncensored**: no content filters, no refusals, no "I can't help with that." The AI answers what you actually ask, whether that's creative fiction, security research, controversial topics, or anything else mainstream AI platforms won't touch.

**Why agents should care:**
- **Private inference** — Models marked "Private" have zero data retention. Process sensitive data without it leaking into training sets.
- **TEE (Trusted Execution Environment)** — Hardware-secured inference; Venice's own servers cannot access the computation.
- **E2EE (End-to-End Encryption)** — Prompts encrypted client-side before they reach Venice's servers. Maximum privacy.
- **Uncensored responses** — No guardrails blocking legitimate use cases.
- **OpenAI-compatible API** — Drop-in replacement. Same API format, just change the base URL.
- **30+ models** — From tiny efficient models to Claude Opus 4.6, GPT-5.2, Grok-4, Gemini Pro, and Venice's own uncensored models.
- **Built-in web search** — LLMs can search the web (and X/Twitter via Grok) and cite sources in a single API call.
- **Vision/multimodal** — Analyze images, audio, and video in chat completions.
- **Image & video generation** — Flux, Sora, Runway, WAN models for visual content.
- **Music generation** — AI-composed music with optional lyrics support.
- **Background removal** — One-click transparent PNG output.

This skill gives you the **complete Venice platform** in one place.

> **⚠️ API changes:** If something doesn't work as expected, check [docs.venice.ai](https://docs.venice.ai) — the API specs may have been updated since this skill was written.

## Prerequisites

- **Python 3.10+**
- **Venice API key** (free tier available at [venice.ai/settings/api](https://venice.ai/settings/api))

## Setup

### Get Your API Key

1. Create account at [venice.ai](https://venice.ai)
2. Go to [venice.ai/settings/api](https://venice.ai/settings/api)
3. Click "Create API Key" → copy the key (starts with `vn_...`)

### Configure

**Option A: Environment variable**
```bash
export VENICE_API_KEY="vn_your_key_here"
```

**Option B: Clawdbot config** (recommended)
```json5
// ~/.clawdbot/clawdbot.json
{
  skills: {
    entries: {
      "venice-ai": {
        env: { VENICE_API_KEY: "vn_your_key_here" }
      }
    }
  }
}
```

### Verify
```bash
python3 {baseDir}/scripts/venice.py models --type text
```

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `venice.py` | Text generation, vision analysis, models, embeddings, TTS, transcription |
| `venice-image.py` | Image generation, background removal |
| `venice-video.py` | Video generation (Sora, WAN, Runway) |
| `venice-music.py` | Music generation (queue-based async) |
| `venice-upscale.py` | Image upscaling |
| `venice-edit.py` | AI image editing, multi-image editing |

---

# Part 1: Text, Vision & Audio

## Model Discovery & Selection

Venice has a huge model catalog spanning text, image, video, audio, and embeddings.

### Browse Models
```bash
# List all text models
python3 {baseDir}/scripts/venice.py models --type text

# List image models
python3 {baseDir}/scripts/venice.py models --type image

# List all model types
python3 {baseDir}/scripts/venice.py models --type text,image,video,audio,embedding

# Get details on a specific model
python3 {baseDir}/scripts/venice.py models --filter grok
```

### Model Selection Guide

| Need | Recommended Model | Why |
|------|------------------|-----|
| **Cheapest text** | `qwen3-4b` | Tiny, fast, efficient |
| **Best uncensored** | `venice-uncensored` | Venice's own uncensored model |
| **Best private + smart** | `deepseek-v3.2` | Great reasoning, efficient |
| **Vision/multimodal** | `qwen3-vl-235b-a22b` | Analyze images, video, audio |
| **Best coding** | `qwen3-coder-480b-a35b-instruct` | Massive coder model |
| **Frontier fast** | `grok-41-fast` | Fast, 262K context |
| **X/Twitter search** | `grok-4-20-beta` or `grok-41-fast` | Grok models + `--x-search` |
| **Frontier max quality** | `claude-opus-4-6` | Best overall quality |
| **Reasoning** | `kimi-k2-5` | Strong chain-of-thought |
| **Web search** | Any model + `--web-search` | Built-in web search |

---

## Text Generation (Chat Completions)

### Basic Generation
```bash
# Simple prompt
python3 {baseDir}/scripts/venice.py chat "What is the meaning of life?"

# Choose a model
python3 {baseDir}/scripts/venice.py chat "Explain quantum computing" --model deepseek-v3.2

# System prompt
python3 {baseDir}/scripts/venice.py chat "Review this code" --system "You are a senior engineer."

# Read from stdin
echo "Summarize this" | python3 {baseDir}/scripts/venice.py chat --model qwen3-4b

# Stream output
python3 {baseDir}/scripts/venice.py chat "Write a story" --stream
```

### Web Search Integration
```bash
# Auto web search (model decides when to search)
python3 {baseDir}/scripts/venice.py chat "What happened in tech news today?" --web-search auto

# Force web search with citations
python3 {baseDir}/scripts/venice.py chat "Current Bitcoin price" --web-search on --web-citations

# Web scraping (extracts content from URLs in prompt)
python3 {baseDir}/scripts/venice.py chat "Summarize: https://example.com/article" --web-scrape
```

### X/Twitter Search (via Grok)
Use Grok models to search X (Twitter) for real-time posts and discussions:
```bash
# Search X for latest AI news
python3 {baseDir}/scripts/venice.py chat "latest AI news from X today" \
  --model grok-41-fast --x-search

# Combine X search with web search
python3 {baseDir}/scripts/venice.py chat "What are people saying about OpenAI?" \
  --model grok-4-20-beta --x-search --web-search auto
```

**Note:** `--x-search` only works with Grok models (`grok-*`). It sets `enable_x_search: true` in `venice_parameters`, which routes search through xAI's infrastructure.

### Uncensored Mode
```bash
# Use Venice's own uncensored model
python3 {baseDir}/scripts/venice.py chat "Your question" --model venice-uncensored

# Disable Venice system prompts for raw model output
python3 {baseDir}/scripts/venice.py chat "Your prompt" --no-venice-system-prompt
```

### Reasoning Models
Venice supports extended reasoning/thinking modes with fine-grained effort control:

```bash
# Use a reasoning model with effort control
python3 {baseDir}/scripts/venice.py chat "Solve this math problem..." \
  --model kimi-k2-5 --reasoning-effort high

# Minimal reasoning (faster, cheaper)
python3 {baseDir}/scripts/venice.py chat "Simple question" \
  --model qwen3-4b --reasoning-effort minimal

# Maximum reasoning (slowest, most thorough)
python3 {baseDir}/scripts/venice.py chat "Complex analysis" \
  --model claude-opus-4-6 --reasoning-effort max

# Strip thinking from output (result only)
python3 {baseDir}/scripts/venice.py chat "Debug this code" --model qwen3-4b --strip-thinking

# Disable reasoning entirely
python3 {baseDir}/scripts/venice.py chat "Quick answer" --model qwen3-4b --disable-thinking
```

**Reasoning effort values** (not all models support all levels):
| Value | Description |
|-------|-------------|
| `none` | No reasoning (fastest) |
| `minimal` | Very brief thinking |
| `low` | Light reasoning |
| `medium` | Balanced (often default) |
| `high` | Thorough reasoning |
| `xhigh` | Extended reasoning |
| `max` | Maximum reasoning budget |

### Privacy: E2EE Mode
For maximum privacy, use End-to-End Encryption with supported models:
```bash
# Enable E2EE (prompts encrypted client-side before reaching Venice)
python3 {baseDir}/scripts/venice.py chat "sensitive analysis" \
  --model some-e2ee-model --enable-e2ee
```

**Privacy tiers on Venice:**
- **Standard** — Anonymized inference, no persistent logs
- **Private inference** — Hardware-isolated, zero retention
- **TEE (Trusted Execution Environment)** — Hardware-secured; Venice servers cannot access computation
- **E2EE (End-to-End Encryption)** — Prompts encrypted client-side; Venice has zero visibility

### Advanced Options
```bash
# Temperature and token control
python3 {baseDir}/scripts/venice.py chat "Be creative" --temperature 1.2 --max-tokens 4000

# JSON output mode
python3 {baseDir}/scripts/venice.py chat "List 5 colors as JSON" --json

# Prompt caching (for repeated context — up to 90% cost savings)
python3 {baseDir}/scripts/venice.py chat "Question" --cache-key my-session-123

# Show usage stats and balance
python3 {baseDir}/scripts/venice.py chat "Hello" --show-usage

# Use a Venice character
python3 {baseDir}/scripts/venice.py chat "Tell me about yourself" --character venice-default
```

---

## Vision / Image Analysis

Analyze images using multimodal vision models. Supports local files, URLs, and data URLs.

```bash
# Analyze a local image
python3 {baseDir}/scripts/venice.py analyze photo.jpg "What's in this image?"

# Analyze with default prompt (describe in detail)
python3 {baseDir}/scripts/venice.py analyze photo.jpg

# Analyze from URL
python3 {baseDir}/scripts/venice.py analyze "https://example.com/image.jpg" "Describe the scene"

# Choose vision model
python3 {baseDir}/scripts/venice.py analyze diagram.png "Explain this diagram" \
  --model qwen3-vl-235b-a22b

# Stream the analysis
python3 {baseDir}/scripts/venice.py analyze photo.jpg "Identify all objects" --stream

# Count tokens used
python3 {baseDir}/scripts/venice.py analyze photo.jpg "Analyze this" --show-usage
```

**Vision-capable models:** `qwen3-vl-235b-a22b`, `claude-opus-4-6`, `gpt-5.2`, and others — check `--list-models` for current availability.

Supported image formats: JPEG, PNG, WebP, GIF, BMP

---

## Embeddings

Generate vector embeddings for semantic search, RAG, and recommendations:

```bash
# Single text
python3 {baseDir}/scripts/venice.py embed "Venice is a private AI platform"

# Multiple texts (batch)
python3 {baseDir}/scripts/venice.py embed "first text" "second text" "third text"

# From file (one text per line)
python3 {baseDir}/scripts/venice.py embed --file texts.txt

# Output as JSON
python3 {baseDir}/scripts/venice.py embed "some text" --output json
```

Model: `text-embedding-bge-m3` (private, $0.15/M tokens)

---

## Text-to-Speech (TTS)

Convert text to speech with 60+ multilingual voices:

```bash
# Default voice
python3 {baseDir}/scripts/venice.py tts "Hello, welcome to Venice AI"

# Choose a voice
python3 {baseDir}/scripts/venice.py tts "Exciting news!" --voice af_nova

# List available voices
python3 {baseDir}/scripts/venice.py tts --list-voices

# Custom output path
python3 {baseDir}/scripts/venice.py tts "Some text" --output /tmp/speech.mp3

# Adjust speed
python3 {baseDir}/scripts/venice.py tts "Speaking slowly" --speed 0.8
```

**Popular voices:** `af_sky`, `af_nova`, `am_liam`, `bf_emma`, `zf_xiaobei` (Chinese), `jm_kumo` (Japanese)

Model: `tts-kokoro` (private, $3.50/M characters)

---

## Speech-to-Text (Transcription)

Transcribe audio files to text:

```bash
# Transcribe a file
python3 {baseDir}/scripts/venice.py transcribe audio.wav

# With timestamps
python3 {baseDir}/scripts/venice.py transcribe recording.mp3 --timestamps

# From URL
python3 {baseDir}/scripts/venice.py transcribe --url https://example.com/audio.wav
```

Supported formats: WAV, FLAC, MP3, M4A, AAC, MP4

Model: `nvidia/parakeet-tdt-0.6b-v3` (private, $0.0001/audio second)

---

## Check Balance

```bash
python3 {baseDir}/scripts/venice.py balance
```

---

# Part 2: Images & Video

## Pricing Overview

| Feature | Cost |
|---------|------|
| Image generation | ~$0.01-0.03 per image |
| Background removal | ~$0.02 |
| Image upscale | ~$0.02-0.04 |
| Image edit (single) | ~$0.04 |
| Image multi-edit | ~$0.04-0.08 |
| Video (WAN) | ~$0.10-0.50 |
| Video (Sora) | ~$0.50-2.00 |
| Video (Runway) | ~$0.20-1.00 |
| Music generation | varies by model/duration |

Use `--quote` with video/music commands to check pricing before generation.

---

## Image Generation

```bash
# Basic generation
python3 {baseDir}/scripts/venice-image.py --prompt "a serene canal in Venice at sunset"

# Multiple images
python3 {baseDir}/scripts/venice-image.py --prompt "cyberpunk city" --count 4

# Custom dimensions
python3 {baseDir}/scripts/venice-image.py --prompt "portrait" --width 768 --height 1024

# List available models and styles
python3 {baseDir}/scripts/venice-image.py --list-models
python3 {baseDir}/scripts/venice-image.py --list-styles

# Use specific model and style
python3 {baseDir}/scripts/venice-image.py --prompt "fantasy" --model flux-2-pro \
  --style-preset "Cinematic"

# Reproducible results with seed
python3 {baseDir}/scripts/venice-image.py --prompt "abstract" --seed 12345

# PNG format with no watermark
python3 {baseDir}/scripts/venice-image.py --prompt "product shot" \
  --format png --hide-watermark
```

**Key flags:** `--prompt`, `--model` (default: flux-2-max), `--count`, `--width`, `--height`, `--format` (webp/png/jpeg), `--resolution` (1K/2K/4K), `--aspect-ratio`, `--negative-prompt`, `--style-preset`, `--cfg-scale` (0-20), `--seed`, `--safe-mode`, `--hide-watermark`, `--embed-exif`, `--steps`

---

## Background Removal

Remove the background from any image, producing a transparent PNG:

```bash
# From local file
python3 {baseDir}/scripts/venice-image.py --background-remove photo.jpg

# Specify output path
python3 {baseDir}/scripts/venice-image.py --background-remove photo.jpg --output cutout.png

# From URL
python3 {baseDir}/scripts/venice-image.py --background-remove \
  "https://example.com/product.jpg" --output product-transparent.png
```

The output is always a PNG with a transparent background (alpha channel). Works best with clear subject/background separation.

---

## Image Upscale

```bash
# 2x upscale
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 2

# 4x with AI enhancement
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 4 --enhance

# Enhanced with custom prompt
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --enhance --enhance-prompt "sharpen details"

# From URL
python3 {baseDir}/scripts/venice-upscale.py --url "https://example.com/image.jpg" --scale 2
```

**Key flags:** `--scale` (1-4, default: 2), `--enhance` (AI enhancement), `--enhance-prompt`, `--enhance-creativity` (0.0-1.0), `--url`, `--output`

---

## Image Edit (AI-powered)

### Single Image Edit
AI-powered editing where the model interprets your prompt to modify the image:

```bash
# Add elements
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "add sunglasses"

# Modify scene
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "change the sky to sunset"

# Remove objects
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "remove the person in background"

# From URL
python3 {baseDir}/scripts/venice-edit.py --url "https://example.com/image.jpg" \
  --prompt "colorize this black and white photo"

# Specify output location
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "add snow" --output result.png
```

### Multi-Image Edit (up to 3 images)
Compose or blend multiple images together using advanced edit models:

```bash
# Combine 2 images
python3 {baseDir}/scripts/venice-edit.py --multi-edit base.jpg overlay.png \
  --prompt "merge these images seamlessly"

# Layer 3 images with model selection
python3 {baseDir}/scripts/venice-edit.py --multi-edit bg.jpg subject.png detail.png \
  --prompt "compose these layers into one image" --model flux-2-max-edit

# Mix local file and URL
python3 {baseDir}/scripts/venice-edit.py --multi-edit local.jpg "https://example.com/img.png" \
  --prompt "blend these two photos" --output blended.png
```

**Multi-edit models:** `flux-2-max-edit` (default), `qwen-edit`, `gpt-image-1-5-edit`

**Note:** The standard edit endpoint uses Qwen-Image which has some content restrictions. Multi-edit uses Flux-based models.

---

## Video Generation

```bash
# Get price quote first
python3 {baseDir}/scripts/venice-video.py --quote --model wan-2.6-image-to-video --duration 10s

# Image-to-video (WAN - default)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "camera pans slowly" \
  --duration 10s

# Image-to-video (Sora)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "cinematic" \
  --model sora-2-image-to-video --duration 8s --aspect-ratio 16:9 --skip-audio-param

# Video-to-video (Runway Gen4)
python3 {baseDir}/scripts/venice-video.py --video input.mp4 --prompt "anime style" \
  --model runway-gen4-turbo-v2v

# List models with available durations
python3 {baseDir}/scripts/venice-video.py --list-models
```

**Key flags:** `--image` or `--video`, `--prompt`, `--model` (default: wan-2.6-image-to-video), `--duration`, `--resolution` (480p/720p/1080p), `--aspect-ratio`, `--audio`/`--no-audio`, `--quote`, `--timeout`

**Models:**
- **WAN** — Image-to-video, configurable audio, 5s-21s
- **Sora** — Requires `--aspect-ratio`, use `--skip-audio-param`
- **Runway** — Video-to-video transformation

---

# Part 3: Music Generation

## Music Generation (AI Composed)

Venice supports AI music generation via a queue-based async API (similar to video generation). Music is generated server-side and polled for completion.

```bash
# Get price quote first
python3 {baseDir}/scripts/venice-music.py --quote --model elevenlabs-music --duration 60

# Generate instrumental music
python3 {baseDir}/scripts/venice-music.py --prompt "epic orchestral battle theme" --instrumental

# Generate music with lyrics
python3 {baseDir}/scripts/venice-music.py \
  --prompt "upbeat pop summer song" \
  --lyrics "Verse 1: Walking down the beach / feeling the heat..."

# Control duration
python3 {baseDir}/scripts/venice-music.py --prompt "ambient piano meditation" --duration 30

# Specify output location
python3 {baseDir}/scripts/venice-music.py --prompt "jazz café background" \
  --output ~/Music/venice-jazz.mp3

# List available audio models
python3 {baseDir}/scripts/venice-music.py --list-models

# Don't delete from server after download (useful for re-downloading)
python3 {baseDir}/scripts/venice-music.py --prompt "..." --no-delete

# Clean up server-side media after downloading with --no-delete
python3 {baseDir}/scripts/venice-music.py --complete QUEUE_ID
```

**Parameters:**
| Flag | Description |
|------|-------------|
| `--prompt` | Music description (style, mood, genre, instruments) |
| `--model` | Model ID (default: `elevenlabs-music`) |
| `--duration` | Duration in seconds |
| `--lyrics` | Optional lyrics text for vocal generation |
| `--instrumental` | Force instrumental (no vocals) |
| `--voice` | Voice selection for vocal tracks |
| `--language` | Language code (e.g., `en`, `es`, `fr`) |
| `--quote` | Get price estimate without generating |
| `--timeout` | Max wait time in seconds (default: 300) |
| `--poll-interval` | Status check interval (default: 10s) |

**Prompt tips for music:**
- Be specific: genre, tempo, instruments, mood
- e.g., `"chill lo-fi hip hop with piano and rain ambiance, 85 BPM"`
- e.g., `"cinematic orchestral swell, strings and brass, dramatic tension"`
- e.g., `"acoustic folk guitar, warm and intimate, fingerpicking style"`

---

# Tips & Ideas

### 🔍 Web Search + LLM = Research Assistant
Use `--web-search on --web-citations` to build a research workflow. Venice searches the web, synthesizes results, and cites sources — all in one API call.

### 🐦 X/Twitter Search via Grok
With Grok models and `--x-search`, you get real-time access to X posts and discussions. Great for trend monitoring, social listening, and news research.

### 🔓 Uncensored Creative Content
Venice's uncensored models work for both text AND images. No guardrails blocking legitimate creative use cases.

### 🔒 Maximum Privacy with TEE/E2EE
When processing sensitive data:
- Use models with **private inference** for zero data retention
- Use **TEE models** when you need hardware-level isolation
- Use **`--enable-e2ee`** for encrypted prompt delivery

### 🎯 Prompt Caching for Agents
If you're running an agent loop that sends the same system prompt repeatedly, use `--cache-key` to get up to 90% cost savings.

### 👁️ Vision Pipeline
```bash
# Analyze → describe → generate matching image
python3 scripts/venice.py analyze original.jpg "describe the style and composition" > desc.txt
python3 scripts/venice-image.py --prompt "$(cat desc.txt)" --model flux-2-max
```

### 🎤 Audio Pipeline
Combine TTS and transcription: generate spoken content with `tts`, process audio with `transcribe`. Both are private inference.

### 🎬 Video Workflow
1. Generate or find a base image
2. Use `--quote` to estimate video cost
3. Generate with appropriate duration/model
4. Videos take 1-5 minutes depending on settings

### 🎵 Music + Video
```bash
# Generate background music, then use it for video
python3 scripts/venice-music.py --prompt "cinematic adventure theme" --output bgm.mp3
python3 scripts/venice-video.py --image scene.jpg --prompt "epic journey" --audio-url bgm.mp3
```

### 🖼️ Image Cleanup Pipeline
```bash
# Generate → remove background → use in video
python3 scripts/venice-image.py --prompt "product on white background" --format png
python3 scripts/venice-image.py --background-remove output.png --output product-clean.png
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `VENICE_API_KEY not set` | Set env var or configure in `~/.clawdbot/clawdbot.json` |
| `Invalid API key` | Verify at [venice.ai/settings/api](https://venice.ai/settings/api) |
| `Model not found` | Run `--list-models` to see available; use `--no-validate` for new models |
| Rate limited | Check `--show-usage` output |
| Video stuck | Videos can take 1-5 min; use `--timeout 600` for long ones |
| Vision not working | Ensure you're using a vision-capable model (e.g., `qwen3-vl-235b-a22b`) |
| `--x-search` no effect | Only works with Grok models (`grok-*`) |
| Music timeout | Music can take 2-5 min; increase `--timeout` |
| Background removal quality | Works best with clear subject/background contrast |

## Resources

- **API Docs**: [docs.venice.ai](https://docs.venice.ai)
- **Status**: [veniceai-status.com](https://veniceai-status.com)
- **Discord**: [discord.gg/askvenice](https://discord.gg/askvenice)
- **API Key**: [venice.ai/settings/api](https://venice.ai/settings/api)
