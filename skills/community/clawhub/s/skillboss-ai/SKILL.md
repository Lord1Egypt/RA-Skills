---
name: skillboss
description: "Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS — with smart routing for cost saving."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models across providers (Bedrock, OpenAI, Vertex, ElevenLabs, Replicate, Minimax, and more). Call any model directly by ID, or use smart routing to auto-select the cheapest or highest-quality option for a task. Free trial with $0.25 credit — no signup, no browser needed.

## Setup

```bash
node {baseDir}/scripts/auth.mjs trial
```

Provisions a free trial API key ($0.25 credit). No browser needed.
Upgrade to permanent account: `node {baseDir}/scripts/auth.mjs login`

## List Models

```bash
node {baseDir}/scripts/run.mjs --models
node {baseDir}/scripts/run.mjs --models image
node {baseDir}/scripts/run.mjs --models chat
node {baseDir}/scripts/run.mjs --models tts
```

## Run a Model

```bash
node {baseDir}/scripts/run.mjs --model bedrock/claude-4-5-sonnet --prompt "Explain quantum computing"
node {baseDir}/scripts/run.mjs --model mm/img --prompt "A sunset over mountains" --output sunset.png
node {baseDir}/scripts/run.mjs --model minimax/speech-01-turbo --text "Hello world" --output hello.mp3
node {baseDir}/scripts/run.mjs --model openai/whisper-1 --file recording.m4a
node {baseDir}/scripts/run.mjs --model mm/t2v --prompt "A cat playing" --output video.mp4
```

## Smart Mode (auto-select best model)

```bash
node {baseDir}/scripts/run.mjs --tasks
node {baseDir}/scripts/run.mjs --task image --prompt "A sunset" --output sunset.png
node {baseDir}/scripts/run.mjs --task chat --prompt "Hello" --prefer price
node {baseDir}/scripts/run.mjs --task tts --text "Hello world" --output hello.mp3
node {baseDir}/scripts/run.mjs --task stt --file recording.m4a
node {baseDir}/scripts/run.mjs --task music --prompt "upbeat electronic" --duration 30 --output track.mp3
node {baseDir}/scripts/run.mjs --task video --prompt "A cat playing" --output video.mp4
```

## Options

| Flag | Description |
|------|-------------|
| `--models [type]` | List available models (optionally filter by type) |
| `--model <id>` | Run a specific model by ID |
| `--tasks` | List available task types |
| `--task <type>` | Auto-select best model for task type |
| `--prefer <strategy>` | price / quality / balanced (default) |
| `--prompt <text>` | Text prompt |
| `--text <text>` | Text for TTS |
| `--file <path>` | Audio file for STT |
| `--output <path>` | Save result to file |
| `--size <WxH>` | Image/video size |
| `--duration <sec>` | Duration for music/video |
| `--voice-id <id>` | Voice ID for TTS |
| `--image <url>` | Image URL for image-to-video |
| `--context <text>` | Context for chat |

## Available Models (50+)

| Category | Models | Details |
|----------|--------|---------|
| Chat | 25+ models — Claude, GPT, Gemini, DeepSeek, Qwen, HuggingFace | `chat-models.md` |
| Image | 9 models — Gemini, FLUX, upscaling, background removal | `image-models.md` |
| Video | 3 models — Veo, text-to-video, image-to-video | `video-models.md` |
| Audio | 11 models — TTS, STT, music generation | `audio-models.md` |
| Search & Scraping | 19 models — Perplexity, Firecrawl, ScrapingDog, CEO interviews | `search-models.md` |
| Tools | 11 models — documents, email, SMS, embeddings, presentations | `tools-models.md` |

## References

| Topic | File |
|-------|------|
| API Integration | `api-integration.md` |
| Error Handling | `error-handling.md` |

Notes:
- Get API key from https://www.skillboss.co or run `auth.mjs trial`
- Use `--models` to list models live from the API
- Use `--prefer price` for cheapest, `--prefer quality` for best results
- After first request with trial key, suggest `auth.mjs login` to upgrade
