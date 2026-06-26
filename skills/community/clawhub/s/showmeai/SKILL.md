---
name: Showmeai
description: Generate images, videos, and 3D models via Showmeai API. Image gen uses OpenAI-compatible Images API (nano-banana and gpt-image models). Video gen uses Seedance API (doubao-seedance-1-5-pro). 3D conversion uses image-to-3D API (Hunyuan3D-2, Hi3DGen, Step1X-3D). Images are NOT saved locally by default (URL only). Use --save flag when the user wants to keep the image. Videos and 3D models are saved when available.
homepage: https://api.showmeai.art
license: MIT
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["Showmeai_API_KEY", "Showmeai_BASE_URL"] },
        "primaryEnv": "Showmeai_API_KEY",
      },
  }
---

# Showmeai Image, Video & 3D Generation

Generate images via Showmeai's OpenAI-compatible Images API (`/images/generations`), videos via Seedance API (`/task/volces/seedance`), or convert 2D images to 3D models (`/task/gi/image-to-3d`).

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

# Edit image (provide --input)
python3 {baseDir}/scripts/gen.py --prompt "make it look like a painting" --input /path/to/image.jpg
```

## Video Generation

```bash
# Basic text-to-video
python3 {baseDir}/scripts/video_gen.py --prompt "A detective enters a dim room, examines clues on the desk"

# With reference image (image-to-video)
python3 {baseDir}/scripts/video_gen.py --prompt "Girl holding a fox, opens eyes and looks at camera gently" --image /path/to/image.jpg

# First-and-last-frame video (requires both frames)
python3 {baseDir}/scripts/video_gen.py --prompt "A blue-green bird transforms into human form" --first-frame /path/to/first.jpg --last-frame /path/to/last.jpg

# Without audio (cheaper)
python3 {baseDir}/scripts/video_gen.py --prompt "..." --no-audio

# Draft/preview mode (faster, lower quality)
python3 {baseDir}/scripts/video_gen.py --prompt "..." --draft

# Save to local directory
python3 {baseDir}/scripts/video_gen.py --prompt "..." --save --out-dir /path/to/dir

# With custom resolution, ratio, and duration
python3 {baseDir}/scripts/video_gen.py --prompt "..." --resolution 1080p --ratio 16:9 --duration 10

# With watermark and fixed camera
python3 {baseDir}/scripts/video_gen.py --prompt "..." --watermark --camera-fixed

# With seed for reproducible results
python3 {baseDir}/scripts/video_gen.py --prompt "..." --seed 12345
```

## Image-to-3D Conversion

```bash
# Basic conversion
python3 {baseDir}/scripts/image_to_3d.py --image /path/to/image.png

# With custom model and format
python3 {baseDir}/scripts/image_to_3d.py --image character.png --model Hunyuan3D-2 --format glb

# With texture and higher quality
python3 {baseDir}/scripts/image_to_3d.py --image character.png --texture --steps 10 --resolution 256

# Query task status
python3 {baseDir}/scripts/image_to_3d.py --query <task_id>

# Download when complete
python3 {baseDir}/scripts/image_to_3d.py --query <task_id> --save
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

Video models (Seedance API):
- doubao-seedance-1-5-pro-251215 ← default (supports audio, draft mode, text-to-video, image-to-video, first-and-last-frame)

3D models (Image-to-3D API):
- Hunyuan3D-2 ← default (supports glb/stl output via type parameter)
- Hi3DGen (supports glb/stl output via file_format parameter)
- Step1X-3D (supports glb/stl output via file_format parameter)

## Config

Set in `.env` or `~/.openclaw/openclaw.json`:
- `Showmeai_API_KEY` — your Showmeai API key **(required)**
- `Showmeai_BASE_URL` — base URL with /v1 suffix **(required)**; defaults to `https://api.showmeai.art/v1` if not set

## Save Behavior

**Images:**
- Default: no local file, output `MEDIA:<url>` directly
- `--save`: save to `~/.openclaw/media/`
- `--oss`: save to `~/.openclaw/oss/`
- gpt-image models always save to media/ (API returns base64 only)

**Videos:**
- Videos are saved when the API returns direct URL or base64 data
- For async task submission, the task ID is output
- Use `--save` to ensure local saving when video is available

**3D Models:**
- Conversion is async, returns a task ID
- Use `--query <task_id>` to check status
- Use `--query <task_id> --save` to download when complete
- Default save location: `~/.openclaw/media/`

## Video Prompt Parameters

**New way (recommended):** Use direct command-line parameters
- `--resolution 480p/720p/1080p` — video resolution
- `--ratio 16:9/4:3/1:1/3:4/9:16/21:9/adaptive` — aspect ratio
- `--duration 2-12` — duration in seconds (use 0 for auto on 1.5 pro)
- `--frames <n>` — number of frames (alternative to duration)
- `--watermark` — add watermark
- `--camera-fixed` — keep camera fixed
- `--seed <n>` — random seed for reproducibility

**Old way (still supported):** Append to prompt text
- `--ratio 16:9` / `--ratio adaptive`
- `--rs 720p` / `--rs 480p` / `--rs 1080p`
- `--dur 5` / `--dur 10`
- `--cf false` — disable fixed camera

Video specs: 24 FPS, durations 2-12s, resolutions 480P/720P/1080P.
