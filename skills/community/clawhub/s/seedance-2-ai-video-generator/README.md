# Seedance 2.0 Video Generator

End-to-end AI video generation using the Loova Seedance 2.0 API. Create videos from text prompts or local media (images/video/audio) via the Seedance 2.0 video API. Requests use **multipart/form-data** with File uploads, so OpenClaw users can attach files directly. Automatic job submission and result polling.

**ClawHub / OpenClaw** – Use this Skill when the user asks for Loova video, Seedance 2.0, or image-to-video generation.

**Note:** Video generation can take **up to 3 hours** depending on server load. The script polls until the task completes and will notify the user at start.

## Overview

- **Submit** – `POST https://api.loova.ai/api/v1/video/seedance-2` to create a video generation task
- **Poll** – `GET https://api.loova.ai/v1/tasks?task_id=...` until the task completes
- **Auth** – `Authorization: Bearer <API_KEY>`; get your API key after logging in at [loova.ai](https://loova.ai/)

## Upload to ClawHub

Upload this repository (or the skill folder) to ClawHub for OpenClaw. Expected structure:

```
├── SKILL.md           # Main instructions (triggers and usage)
├── QUICK_START.md     # Short setup and run guide
├── README.md          # This file
├── reference.md       # API reference
├── requirements.txt  # Python deps (requests, python-dotenv)
├── .env.example       # Example env (LOOVA_API_KEY)
└── scripts/
    └── run_seedance.py   # Submit + poll script
```

## Setup

### 1. Get API key

Open [https://loova.ai/api](https://loova.ai/api) in a browser, sign in to your account, and get your API key from the Loova API page.

### 2. Configure credentials

**Option A – .env (recommended)**  
The script loads `.env` automatically (via `python-dotenv`), same as [ai-video-gen](https://clawhub.ai/rhanbourinajd/ai-video-gen).

```bash
cp .env.example .env
# Edit .env and set:
LOOVA_API_KEY=your_api_key_here
```

**Option B – Environment variable**

```bash
export LOOVA_API_KEY="your_api_key_here"
```

Do not hardcode the key in code.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Requires: `requests`, `python-dotenv`.

## Usage

### Via OpenClaw / Agent

The agent uses this Skill when the user mentions Loova video, Seedance 2.0, text-to-video, or image-to-video. It can run the script with the appropriate `--prompt` and optional `--files`, `--duration`, `--ratio`, etc.

### Run the script locally

```bash
# Prompt only
python scripts/run_seedance.py --prompt "Camera slowly pushes in"

# With options
python scripts/run_seedance.py --prompt "Person smiles" --model seedance_2_0_fast --duration 8 --ratio "16:9"

# With local image file(s)
python scripts/run_seedance.py --prompt "Person turns head" --files "a.jpg"
```

Output: the script prints the final result JSON (including the video URL when the task succeeds).

## Parameters

| Parameter    | Required | Description                                                                 |
|-------------|----------|-----------------------------------------------------------------------------|
| `--prompt`  | Yes      | Text prompt for the video                                                   |
| `--model`   | No       | `seedance_2_0` (default) or `seedance_2_0_fast`   |
| `--duration`| No       | Duration in seconds, 4–15 (default 5)                                       |
| `--ratio`   | No       | Aspect ratio (default `16:9`)                                               |
| `--function-mode` | No | `first_last_frames` or `omni_reference`                              |
| `--files`   | No       | Comma-separated local file paths (sent as multipart FormData File uploads; images/video/audio) |

See [reference.md](reference.md) for full API details and [QUICK_START.md](QUICK_START.md) for a minimal setup guide.
