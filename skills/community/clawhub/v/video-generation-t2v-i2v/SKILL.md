---
name: video-generation
description: AI Video generation toolkit — generate videos from text prompts or input images using multiple AI models (Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, Grok Imagine Video, etc.). Support both text-to-video and image-to-video generation. Use when users ask for video creation, AI video, text to video, image to video, animate image, video generation.
---

# Video Generation Toolkit

Generate AI videos from text prompts or images using 40+ models including Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, Grok Imagine Video, etc.

## Prerequisites

**IMPORTANT**: This skill requires the [inference.sh CLI](https://inference.sh) to be installed and available in your PATH. The CLI provides access to 40+ AI video generation models.

To install inference.sh:
```bash
npm install -g @inference.sh/cli
```

Or visit https://inference.sh for installation instructions.

## Constraints

- Always output absolute paths for generated files so the web UI can render them.
- Web UI auto-renders local paths: output `.mp4/.mov` paths as plain text (NOT in code blocks or markdown links), so the UI can render a video player inline. Same for `.jpg/.png` → inline image.
- Uploaded files arrive as `[附件: /absolute/path/to/file]` in the message.
- For image-to-video, images must be accessible via public URL. Provide your own API key for ImgBB/SM.MS, or ensure images are already publicly accessible.

## Tool 1 — text_to_video.py (Text to Video)

Generate video from text prompt.

```
python nanobot/skills/VideoGeneration/scripts/text_to_video.py [options]
```

| Flag | Description |
|------|-------------|
| `--prompt TEXT` | (required) Video description in English |
| `--model NAME` | Model name, default `veo-3.1` |
| `--duration N` | Video duration in seconds, default 5 |
| `--width N` | Video width, default 1280 |
| `--height N` | Video height, default 720 |
| `--fps N` | Frames per second, default 24 |
| `--save-dir DIR` | Output dir, default `./outputs/videos` |
| `--timeout N` | Request timeout in seconds, default 600 |
| `--dry-run` | Print request and exit |

Available models:
- `veo-3.1` - Google Veo 3.1 (recommended)
- `veo-3` - Google Veo 3
- `seedance-1.5-pro` - Seedance 1.5 Pro
- `wan-2.5` - Wan 2.5
- `grok-imagine-video` - Grok Imagine Video
- `omnihuman` - OmniHuman

Output JSON example:

```json
{
  "ok": true,
  "downloaded_files": ["D:/project/.../outputs/videos/video_20260315_1.mp4"]
}
```

## Tool 2 — image_to_video.py (Image to Video)

Generate video from input image.

```
python nanobot/skills/VideoGeneration/scripts/image_to_video.py [options]
```

| Flag | Description |
|------|-------------|
| `--image PATH` | (required) Input image path |
| `--prompt TEXT` | (required) Video description in English |
| `--model NAME` | Model name, default `veo-3.1` |
| `--duration N` | Video duration in seconds, default 5 |
| `--save-dir DIR` | Output dir, default `./outputs/videos` |
| `--upload-service` | Image upload service (smms/imgbb), default imgbb |
| `--api-token` | API token for image upload (REQUIRED for ImgBB, optional for SM.MS) |
| `--timeout N` | Request timeout in seconds, default 1000 |
| `--dry-run` | Print request and exit |

Process:
1. Upload local image to cloud storage (SM.MS or ImgBB) **OR use a publicly accessible image URL**
2. Generate video using the image URL
3. Download and save locally

**IMPORTANT**: For ImgBB, you must provide an API token via `--api-token` or set `IMGBB_API_KEY` environment variable. Get your free API key at https://api.imgbb.com/

Output JSON example:

```json
{
  "ok": true,
  "downloaded_files": ["D:/project/.../outputs/videos/video_20260315_1.mp4"]
}
```
