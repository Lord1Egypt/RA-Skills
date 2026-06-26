# 📽️ xai-studio

xAI Studio — an [OpenClaw](https://openclaw.ai) skill for generating and editing images and videos via the xAI API. Supports text-to-image, batch generation, image editing, style transfers, multi-turn chaining, text-to-video, image-to-video, video editing, and concurrent processing — all from a single expandable CLI.

## Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.10+ |
| **API Key** | `XAI_API_KEY` environment variable with image-generation access |

## Quick Start

### Via ClawHub

Install directly with the [ClawHub CLI](https://clawhub.ai/H0llyW00dzZ/xai-studio):

```bash
clawhub install xai-studio
```

### Manual Setup

```bash
# 1. Clone the skill
git clone https://github.com/H0llyW00dzZ/xai-studio-skills.git
cd xai-studio-skills

# 2. Create a virtual environment and install the SDK
python3 -m venv venv
venv/bin/pip3 install xai-sdk

# 3. Set your API key
export XAI_API_KEY="xai-..."

# 4. Generate an image
venv/bin/python3 scripts/run.py generate --prompt "A futuristic cityscape at dawn"
```

## Commands

### `generate` — Text-to-image

```bash
# Single image
venv/bin/python3 scripts/run.py generate --prompt "Mountain landscape at sunrise" --aspect-ratio 16:9

# Batch (up to 10 images)
venv/bin/python3 scripts/run.py generate --prompt "Abstract art" --count 4

# High resolution
venv/bin/python3 scripts/run.py generate --prompt "An astronaut in LEO" --resolution 2k
```

### `edit` — Edit existing images

```bash
# Edit a local file
venv/bin/python3 scripts/run.py edit --prompt "Render as a pencil sketch" --image photo.png

# Edit using a URL
venv/bin/python3 scripts/run.py edit --prompt "Add warm lighting" --image https://example.com/photo.jpg

# Combine multiple images (up to 3)
venv/bin/python3 scripts/run.py edit --prompt "Add the cat to the landscape" --image cat.png --image landscape.png
```

### `concurrent` — Parallel style transfers

```bash
# Apply multiple styles to the same image in parallel
venv/bin/python3 scripts/run.py concurrent --image photo.png --prompt "oil painting" --prompt "pencil sketch" --prompt "pop art"
```

### `multi-turn` — Iterative edit chaining

> **Note:** Unlike `edit` (which accepts up to 3 images in a single call), `multi-turn` takes exactly **1 source image** but has **no hard limit on the number of `--prompt` steps**. Each step's output is automatically re-encoded and fed into the next step as input, so you can chain as many sequential edits as you need on a single image.

```bash
# Each output feeds into the next edit
venv/bin/python3 scripts/run.py multi-turn --image photo.png --prompt "Add dramatic clouds" --prompt "Make it a sunset" --prompt "Add lens flare"
```

## Image CLI Flags

| Flag | Default | Subcommands | Description |
|---|---|---|---|
| `--prompt` | *(required)* | all image | Generation / edit prompt (repeatable in concurrent & multi-turn) |
| `--count` | `1` | generate | Number of images (max 10) |
| `--image` | *(required)* | edit, concurrent, multi-turn | Source image path or URL (edit supports up to 3x) |
| `--model` | `grok-imagine-image` | all image | xAI model name |
| `--aspect-ratio` | `1:1` | all image | Aspect ratio (e.g. `16:9`, `4:3`, `auto`) |
| `--resolution` | API default | all image | `1k` or `2k` |
| `--format` | `base64` | all image | `base64` or `url` |
| `--out-dir` | `media/xai-output` | all image | Output directory |

## Output

Images are saved to `<out-dir>/<YYYY-MM-DD>/<prefix>_<NNN>_<HHMMSS>.<ext>`, organized by UTC date. The prefix reflects the subcommand: `generate`, `edit`, `style` (concurrent), or `step` (multi-turn). The file extension is detected automatically from image magic bytes (PNG, JPEG, WebP, GIF).

---

### `video-generate` — Text-to-video or image-to-video

```bash
# Text-to-video
venv/bin/python3 scripts/run.py video-generate --prompt "A rocket launching from Mars" --duration 10 --resolution 720p

# Image-to-video (animate a still image)
venv/bin/python3 scripts/run.py video-generate --prompt "Animate this scene" --image photo.png --duration 5
```

### `video-edit` — Edit existing video

```bash
venv/bin/python3 scripts/run.py video-edit --prompt "Add a silver necklace" --video https://example.com/clip.mp4
```

### `video-concurrent` — Parallel video edits

```bash
venv/bin/python3 scripts/run.py video-concurrent --video https://example.com/clip.mp4 \
  --prompt "Add a wide-brimmed hat" --prompt "Change outfit to red" --prompt "Add a necklace"
```

## Video CLI Flags

| Flag | Default | Subcommands | Description |
|---|---|---|---|
| `--prompt` | *(required)* | all video | Generation or edit prompt |
| `--duration` | `5` | video-generate | Duration in seconds (1–15) |
| `--image` | *(optional)* | video-generate | Source image for image-to-video |
| `--video` | *(required)* | video-edit, video-concurrent | Source video URL |
| `--model` | `grok-imagine-video` | all video | xAI video model name |
| `--aspect-ratio` | API default | all video | Aspect ratio (e.g. `16:9`, source for editing) |
| `--resolution` | API default | all video | `480p` or `720p` |
| `--out-dir` | `media/xai-output` | all video | Output directory |
| `--timeout` | API default | all video | Max polling wait (seconds) |
| `--poll-interval` | SDK default | all video | Seconds between status checks |

Videos are saved as `.mp4` to `<out-dir>/<YYYY-MM-DD>/<prefix>_<NNN>_<HHMMSS>.mp4`. The prefix reflects the subcommand: `video` (generate), `video_edit`, or `video_style` (concurrent).

## ClawHub

This skill is published on [ClawHub](https://clawhub.ai/H0llyW00dzZ/xai-studio). Install it directly in your OpenClaw environment:

```
clawhub install xai-studio
```

## License

[MIT-0](LICENSE)
