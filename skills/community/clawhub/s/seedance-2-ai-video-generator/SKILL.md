---
name: seedance-2-ai-video-generator
displayName: Seedance 2.0 AI Video Generator (Text to Video, Image to Video, Reference to Video)
description: Generates video via Loova Seedance 2.0 API (Seedance 2.0 video). Requires LOOVA_API_KEY from .env or environment (get API key at loova.ai). Use when the user asks for Loova, Seedance 2.0, image-to-video, or Seedance 2.0 video.

metadata: {"openclaw":{"homepage":"https://api.loova.ai/api","requires":{"bins":[],"env":["LOOVA_API_KEY"]},"primaryEnv":"LOOVA_API_KEY"}}
---

# Seedance 2.0 Video Generator

Create AI videos from text or images using the latest multi-modal reference system with the Loova Seedance 2.0 API (Seedance 2.0 Video). Submit a job, poll for completion, and get the video result. **Generation may take up to 3 hours**; poll **once per minute** and return to the user immediately when status becomes **succeeded** or **failed** (or any terminal error state). **Stop polling immediately on failure/error** and return the error details to the user.

## Capabilities

1. **Image to Video** – Turn images into videos using the Loova Seedance 2.0 Video API, powered by Seedance 2.0 or Seedance 2.0 Fast.
1. **Text to Video** – Convert text into videos with the Loova Seedance 2.0 Video API, powered by Seedance 2.0 or Seedance 2.0 Fast.
2. **Multi-Modal Reference System** – Supports multiple input types, including text, images, videos, and audio. These inputs can be used as references for different parts of your video.
3. **Configurable Settings** – Customize duration (4–15 seconds), aspect ratio, and function mode (first frame, last frame, or omni reference).
4. **Attachment-friendly workflow** 
  - When users provide media via URL, pass it directly using --image-urls, --video-urls, or --audio-urls (no download required).
  - When users upload files in chat (images, videos, or audio), save them locally in the OpenClaw workspace (e.g., workspace/assets/) and pass the file paths via --files.
  - If both URLs and local files are provided for the same media type, URLs take precedence (local files of the same type will be ignored).

## Quick Start

```bash
# Generate video from prompt only
python scripts/run_seedance.py --prompt "Camera slowly pushes in, person smiles"

# With local file(s) (sent as FormData File uploads)
python scripts/run_seedance.py --prompt "Person turns head" --files "photo.jpg" --duration 8

# Fast model, custom ratio
python scripts/run_seedance.py --prompt "A cat in the sun" --model seedance_2_0_fast --ratio "16:9"
```

## Setup

### Required API Key

Obtain your API key from your account after logging in at [https://loova.ai/](https://loova.ai/). Do not hardcode the key; use environment variables or `.env`.

Add to your environment or `.env` file in the project root:

```bash
# Required for Loova API
LOOVA_API_KEY=your_api_key_here
```

Create `.env` from the example:

```bash
cp .env.example .env
# Edit .env and set LOOVA_API_KEY
```

The script loads variables from `.env` automatically (via `python-dotenv`). You can also export `LOOVA_API_KEY` in your shell.

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies: `requests`, `python-dotenv`. No FFmpeg or other system binaries required.

## Usage Examples

### 1. Text to Video (prompt only)

```bash
python scripts/run_seedance.py --prompt "A futuristic city at night with flying cars" --duration 5
```

### 2. Image to Video (with reference image URL)

```bash
python scripts/run_seedance.py --prompt "Person slowly smiles" --image-urls "https://your-cdn.com/portrait.jpg" --duration 8
```

### 3. Multiple Reference Images

```bash
python scripts/run_seedance.py --prompt "Smooth transition between scenes" --image-urls "https://example.com/a.jpg,https://example.com/b.jpg" --function-mode first_last_frames
```

### 4. Fast Model, Custom Aspect Ratio

```bash
python scripts/run_seedance.py --prompt "Ocean waves" --model seedance_2_0_fast --ratio "9:16" --duration 6
```

## Scripts Reference

| Script | Description |
|--------|-------------|
| `scripts/run_seedance.py` | Submit Seedance 2.0 video task and poll until done; prints result JSON (includes video URL on success) |

Arguments: `--prompt` (required), `--model`, `--duration`, `--ratio`, `--function-mode`, `--files` (comma-separated local paths; sent as multipart File uploads).
URL inputs: `--image-urls`, `--video-urls`, `--audio-urls` (comma-separated). When no files are uploaded, the request uses `Content-Type: application/json`; when uploading files it uses `multipart/form-data`.
Note: for multipart uploads, let the HTTP client set `Content-Type` with boundary automatically; do not set `Content-Type` manually.

## API Flow

1. **Submit** – `POST https://api.loova.ai/api/v1/video/seedance-2` with `Authorization: Bearer <API_KEY>`; response contains `task_id`.
2. **Poll** – `GET https://api.loova.ai/api/v1/tasks?task_id=<task_id>` **once per minute** until status is succeeded or failed.
3. **Result** – Response includes the video result (e.g. URL). Script prints full JSON.

## Parameters Summary

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `model` | Yes | `seedance_2_0` | `seedance_2_0` or `seedance_2_0_fast` |
| `prompt` | Yes | — | Prompt; supports @ reference syntax |
| `functionMode` | No | — | `first_last_frames` or `omni_reference` |
| (multipart) `files` | No | — | Optional File parts (images/video/audio); sent as multipart/form-data |
| `image_urls` | No | — | Optional image URL list (pass via `--image-urls`) |
| `video_urls` | No | — | Optional video URL list (pass via `--video-urls`) |
| `audio_urls` | No | — | Optional audio URL list (pass via `--audio-urls`) |
| `ratio` | No | `16:9` | Aspect ratio |
| `duration` | No | `5` | Duration in seconds (4–15) |

For full API details, see [reference.md](reference.md). For a short setup guide, see [QUICK_START.md](QUICK_START.md).
