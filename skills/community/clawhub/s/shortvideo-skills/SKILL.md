---
name: shortvideo
description: "Create videos using ShortVideo API. Supports product-to-video, image-to-ad-video, and replicate-video. Use this skill when users want to: generate product videos, create ad videos from images, or replicate existing videos. Also trigger on: 生成视频, 产品视频, 视频生成, 制作视频, video generation, create video, product video, ad video."
allowed-tools: Bash(python3 *)
metadata: {"openclaw": {"emoji": "🎬"}}
---

# ShortVideo Creator

Create videos using ShortVideo backend API with multiple task types.

## Authentication Setup (Required for First Use)

ShortVideo requires API credentials. Configure via environment variables:

### Method 1: Claude Code Config

Add to `~/.claude/settings.json`:

```json
{
  "env": {
    "SHORTVIDEO_BASE_URL": "https://api.shortvideo.ai",
    "SHORTVIDEO_API_KEY": "your-api-key-here"
  }
}
```

### Method 2: OpenClaw Config

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "shortvideo": {
        "env": {
          "SHORTVIDEO_BASE_URL": "https://api.shortvideo.ai",
          "SHORTVIDEO_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

### Method 3: Shell Environment Variable

Add to `~/.zshrc` (or `~/.bashrc`):

```bash
export SHORTVIDEO_BASE_URL="https://api.shortvideo.ai"
export SHORTVIDEO_API_KEY="your-api-key-here"
```

Then reload: `source ~/.zshrc`

> **Note**: When executing scripts, if environment variables are not found, try running with `source ~/.zshrc && python3 scripts/...`

---

## Subcommands

### product-to-video - Generate product video from image

Generate a marketing video from a single product image using Sora2 AI.

**Trigger**: product-to-video, 产品视频, product video

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "<product_name>" \
  --image <image_path> \
  --aspect-ratio <16:9|9:16> \
  --duration 12 \
  [--product-info "<description>"] \
  [--no-poll]
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--product-name` | Yes | - | Product name |
| `--image` | Yes | local/OSS/URL | Product image path |
| `--aspect-ratio` | Yes | `16:9`, `9:16` | Video ratio |
| `--duration` | Yes | `12` | Duration (only 12s supported) |
| `--product-info` | No | - | Product description |
| `--no-poll` | No | - | Disable auto polling |

**Credit Cost**: 100 (fixed)

**Example:**
```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Premium Headphones" \
  --image https://example.com/product.jpg \
  --aspect-ratio 16:9 \
  --duration 12
```

---

### image-to-ad-video - Create ad video from images

Create advertisement videos from 1-7 product images.

**Trigger**: image-to-ad-video, 广告视频, ad video, image to video

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images <image1> <image2> ... \
  --duration <8|15|30|60> \
  --aspect-ratio <16:9|9:16|1:1> \
  [--prompt "<text>"] \
  [--no-poll]
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--images` | Yes | 1-7 paths | Image paths (local/OSS/URL) |
| `--duration` | Yes | `8`, `15`, `30`, `60` | Duration in seconds |
| `--aspect-ratio` | Yes | `16:9`, `9:16`, `1:1` | Video ratio |
| `--prompt` | No | max 2000 chars | Style prompt |
| `--no-poll` | No | - | Disable auto polling |

**Credit Cost**: 30 per second

**Example:**
```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images d2mm4m9addr0008000a0.png \
  --duration 15 \
  --aspect-ratio 16:9
```

---

### replicate-video - Replicate video with new images

Replicate an existing video style with new product/model images.

**Trigger**: replicate-video, 视频复刻, video replication

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video <video_path> \
  --aspect-ratio <16:9|9:16> \
  --resolution <540p|720p|1080p> \
  [--product-images <img1> <img2> ...] \
  [--model-images <img1> <img2> ...] \
  [--prompt "<text>"] \
  [--remove-audio] \
  [--no-poll]
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--video` | Yes | local/OSS/URL | Source video (5-300s) |
| `--aspect-ratio` | Yes | `16:9`, `9:16` | Video ratio |
| `--resolution` | Yes | `540p`, `720p`, `1080p` | Output resolution |
| `--product-images` | No* | 1-7 paths | Product images |
| `--model-images` | No* | 1-7 paths | Model images |
| `--prompt` | No | max 2000 chars | Style prompt |
| `--remove-audio` | No | - | Remove audio |
| `--no-poll` | No | - | Disable auto polling |

*At least one image (product or model) is required.

**Credit Cost**: 9-15 per second (by resolution)

**Example:**
```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images product.jpg
```

---

### poll-videos - Poll for video results

Poll for video generation results status.

**Trigger**: poll-videos, 查询视频, check video status

```bash
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids <id1> <id2> [options]
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `--video-ids` | Yes | Video IDs to check |
| `--once` | No | Single check without polling |
| `--max-attempts` | No | Max polling attempts (default: 60) |
| `--interval` | No | Polling interval in seconds (default: 10) |

**Video Status Codes:**
| Status | Description |
|--------|-------------|
| 0 | Pending |
| 1 | Processing |
| 2 | Completed |
| 3 | Failed |

**Example:**
```bash
# Continuous polling
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids video_abc123

# Single check
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids video_abc123 --once
```

---

## File Path Types

All file parameters support:

| Type | Example | Behavior |
|------|---------|----------|
| Local file | `/Users/xxx/file.jpg` | Upload to OSS |
| OSS path | `d2mm4m9addr0008000a0.png` | Use directly |
| URL | `https://example.com/file.jpg` | Download → Upload |

## Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp` | 100MB |
| Videos | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` | 100MB |

## API Response Format

```json
// Success
{"code": 0, "data": {...}}

// Failure
{"code": 1, "info": "error message"}
```

## Reference Documentation

- [Product to Video](references/product-to-video.md)
- [Image to Ad Video](references/image-to-ad-video-v2.md)
- [Replicate Video](references/replicate-video.md)