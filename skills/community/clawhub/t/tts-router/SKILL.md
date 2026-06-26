---
name: tts-router
description: Local TTS router for Apple Silicon — pull models, serve OpenAI-compatible API, synthesize speech, clone voices. Use when the user asks to "generate speech", "text to speech", "start TTS server", "pull a TTS model", "clone a voice", "speak in someone's voice", or any task involving local speech synthesis on macOS.
---

# tts-router — Local TTS Router for Apple Silicon

A CLI that manages and serves multiple TTS models locally on Apple Silicon (MLX).
Models are downloaded from HuggingFace Hub and served via OpenAI + DashScope compatible APIs.

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- `uv` installed — see https://docs.astral.sh/uv/getting-started/installation/
  (e.g. `brew install uv` or via the official installer)
- ffmpeg installed (`brew install ffmpeg`)

## Install

```bash
# From PyPI (requires --prerelease=allow due to mlx-audio upstream dep)
uvx --prerelease=allow tts-router list

# Or install with pip
pip install tts-router
```

## Commands

### `tts-router list` — Show available models

```bash
tts-router list
```

### `tts-router pull <model>` — Download model weights

```bash
tts-router pull qwen3-tts
tts-router pull kokoro
```

Models are cached in `~/.cache/huggingface/hub/`. No need to re-download.

### `tts-router serve` — Start the TTS API server

```bash
# Default: qwen3-tts on port 8091
tts-router serve

# Custom model and port
tts-router serve --model kokoro --port 9000
```

The server requires models to be pulled first.

### `tts-router say` — Synthesize speech from CLI

```bash
tts-router say "Hello world" -o hello.wav
tts-router say "Hello" --voice Vivian --model kokoro -o out.wav
```

## Available Models

| Short Name         | Features                                        |
| ------------------ | ----------------------------------------------- |
| `qwen3-tts`        | multi-speaker, emotion, instruct (default)      |
| `qwen3-tts-design` | free-form voice description                     |
| `qwen3-tts-clone`  | voice cloning with ref audio                    |
| `kokoro`           | fast, lightweight, multi-lang                   |
| `dia`              | multi-speaker dialogue, laughter/emotion sounds |
| `chatterbox`       | 23 languages, emotion control, voice cloning    |
| `orpheus`          | emotive TTS with emotion tags                   |

## Quick Start for Agent

```bash
# 1. Pull the default model
tts-router pull qwen3-tts

# 2. Start the server
tts-router serve

# 3. Generate speech (OpenAI format)
curl -X POST http://localhost:8091/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world", "voice": "Vivian"}' \
  --output output.wav
```

## API Endpoints (when serving)

| Endpoint                             | Method | Description               |
| ------------------------------------ | ------ | ------------------------- |
| `GET /`                              | GET    | Playground UI             |
| `POST /v1/audio/speech`              | POST   | OpenAI-compatible TTS     |
| `GET /v1/audio/voices`               | GET    | List available voices     |
| `GET /health`                        | GET    | Health check              |
| `POST /v1/audio/clone`               | POST   | Voice clone generation    |
| `POST /v1/audio/references/upload`   | POST   | Upload reference audio    |
| `POST /v1/audio/references/from-url` | POST   | Fetch ref audio by URL    |

## Advanced Use Cases

For more complex workflows, read the relevant reference file:

- **Clone a voice from any URL** (YouTube, Bilibili, podcast, direct audio link) →
  read `references/voice-cloning.md`
- **Use tts-router as a TTS provider in OpenClaw** →
  read `references/openclaw.md`
