---
name: skillboss
description: "Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS — with smart routing for cost saving."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models across providers (Bedrock, OpenAI, Vertex, ElevenLabs, Replicate, Minimax, and more). Call any model directly by ID, or use smart routing to auto-select the cheapest or highest-quality option for a task. Free trial with $0.25 credit — no signup, no browser needed.

## List Models

```bash
node {baseDir}/scripts/run.mjs models
node {baseDir}/scripts/run.mjs models image
node {baseDir}/scripts/run.mjs models chat
node {baseDir}/scripts/run.mjs models tts
```

## Run a Model

```bash
node {baseDir}/scripts/run.mjs run bedrock/claude-4-5-sonnet "Explain quantum computing"
node {baseDir}/scripts/run.mjs run mm/img "A sunset over mountains"
node {baseDir}/scripts/run.mjs run minimax/speech-01-turbo "Hello world"
node {baseDir}/scripts/run.mjs run mm/t2v "A cat playing"
```

## Smart Mode (auto-select best model)

```bash
node {baseDir}/scripts/run.mjs tasks
node {baseDir}/scripts/run.mjs task image "A sunset"
node {baseDir}/scripts/run.mjs task chat "Hello"
node {baseDir}/scripts/run.mjs task tts "Hello world"
node {baseDir}/scripts/run.mjs task music "upbeat electronic"
node {baseDir}/scripts/run.mjs task video "A cat playing"
```

## Save Media

Image/video/audio results print a URL. Save with curl:

```bash
URL=$(node {baseDir}/scripts/run.mjs run mm/img "A sunset")
curl -sL "$URL" -o sunset.png
```

## Available Models (50+)

| Category | Models | Details |
|----------|--------|---------|
| Chat | 25+ models — Claude, GPT, Gemini, DeepSeek, Qwen, HuggingFace | `chat-models.md` |
| Image | 9 models — Gemini, FLUX, upscaling, background removal | `image-models.md` |
| Video | 3 models — Veo, text-to-video, image-to-video | `video-models.md` |
| Audio | 11 models — TTS, STT, music generation | `audio-models.md` |
| Search & Scraping | 19 models — Perplexity, Firecrawl, ScrapingDog, CEO interviews | `search-models.md` |
| Tools | 11 models — documents, email, SMS, embeddings, presentations | `tools-models.md` |

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
- Use `models` to discover available models
- Use `task` for smart routing (auto-selects cheapest/best model)