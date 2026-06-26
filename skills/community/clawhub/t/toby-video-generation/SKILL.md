---
name: seedance-video
description: "Generate AI videos using SkillBoss API Hub. Use when the user wants to: (1) generate videos from text prompts, (2) generate videos from images (first frame, first+last frame, reference images), or (3) query/manage video generation tasks. Supports Seedance 1.5 Pro (with audio), 1.0 Pro, 1.0 Pro Fast, and 1.0 Lite models."
version: 1.0.0
category: file-generation
argument-hint: "[text prompt or task ID]"
requires.env: [SKILLBOSS_API_KEY]
---

# Seedance Video Generation

Generate AI videos via SkillBoss API Hub's unified video generation capability.

## Prerequisites

The user must set the `SKILLBOSS_API_KEY` environment variable. You can set it by running:

```bash
export SKILLBOSS_API_KEY="your-api-key-here"
```

**Base URL**: `https://api.skillbossai.com/v1/pilot`

## Supported Models

SkillBoss API Hub automatically routes to the optimal video generation model. Model hints are passed via the `inputs` field and honored when available.

| Model | Model Hint | Capabilities |
|-------|-----------|-------------|
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` | Text-to-video, Image-to-video (first frame, first+last frame), Audio support, Draft mode |
| Seedance 1.0 Pro | `doubao-seedance-1-0-pro-250428` | Text-to-video, Image-to-video (first frame, first+last frame) |
| Seedance 1.0 Pro Fast | `doubao-seedance-1-0-pro-fast-250528` | Text-to-video, Image-to-video (first frame only) |
| Seedance 1.0 Lite T2V | `doubao-seedance-1-0-lite-t2v-250219` | Text-to-video only |
| Seedance 1.0 Lite I2V | `doubao-seedance-1-0-lite-i2v-250219` | Image-to-video (first frame, first+last frame, reference images 1-4) |

**Default model**: `doubao-seedance-1-5-pro-251215` (latest, supports audio)

## Execution (Recommended: Python CLI Tool)

A Python CLI tool is provided at `~/.claude/skills/seedance-video/seedance.py` for robust execution with proper error handling and local image base64 conversion. **Prefer using this tool over raw curl commands.**

### Quick Examples with Python CLI

```bash
# Text-to-video (create + download)
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "小猫对着镜头打哈欠" --download ~/Desktop

# Image-to-video from local file
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "人物缓缓转头微笑" --image /path/to/photo.jpg --download ~/Desktop

# Image-to-video from URL
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "风景画面缓缓推进" --image "https://example.com/image.jpg" --download ~/Desktop

# First + last frame
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "花朵从含苞到盛开" --image first.jpg --last-frame last.jpg --download ~/Desktop

# Reference images (Lite I2V)
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "[图1]的人物在跳舞" --ref-images ref1.jpg ref2.jpg --model doubao-seedance-1-0-lite-i2v-250219 --download ~/Desktop

# Custom parameters
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "城市夜景延时摄影" --ratio 21:9 --duration 8 --resolution 1080p --generate-audio false --download ~/Desktop

# Draft mode (cheaper preview)
python3 ~/.claude/skills/seedance-video/seedance.py create --prompt "海浪拍打沙滩" --draft true --download ~/Desktop

# Generate final video from draft
python3 ~/.claude/skills/seedance-video/seedance.py create --draft-task-id <DRAFT_TASK_ID> --resolution 720p --download ~/Desktop
```

## Alternative: Raw curl Commands

### Text-to-Video

```bash
[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1

RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{
    "type": "video",
    "inputs": {
      "prompt": "YOUR_PROMPT_HERE",
      "ratio": "16:9",
      "duration": 5,
      "resolution": "720p",
      "generate_audio": true
    },
    "prefer": "balanced"
  }')

VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['video_url'])")
echo "Video URL: $VIDEO_URL"
```

### Image-to-Video (First Frame, URL)

```bash
[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1

RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{
    "type": "video",
    "inputs": {
      "prompt": "YOUR_PROMPT_HERE",
      "image": "IMAGE_URL_HERE",
      "ratio": "adaptive",
      "duration": 5,
      "resolution": "720p",
      "generate_audio": true
    },
    "prefer": "balanced"
  }')

VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['video_url'])")
echo "Video URL: $VIDEO_URL"
```

### Image-to-Video (First Frame, Local File)

```bash
[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1

IMG_PATH="/path/to/image.png"
IMG_EXT="${IMG_PATH##*.}"
IMG_EXT_LOWER=$(echo "$IMG_EXT" | tr '[:upper:]' '[:lower:]')
IMG_BASE64=$(base64 < "$IMG_PATH" | tr -d '\n')
IMG_DATA_URL="data:image/${IMG_EXT_LOWER};base64,${IMG_BASE64}"

RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d "{
    \"type\": \"video\",
    \"inputs\": {
      \"prompt\": \"YOUR_PROMPT_HERE\",
      \"image\": \"${IMG_DATA_URL}\",
      \"ratio\": \"adaptive\",
      \"duration\": 5,
      \"resolution\": \"720p\",
      \"generate_audio\": true
    },
    \"prefer\": \"balanced\"
  }")

VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['video_url'])")
echo "Video URL: $VIDEO_URL"
```

### Image-to-Video (First + Last Frame)

```bash
[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1

RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{
    "type": "video",
    "inputs": {
      "prompt": "YOUR_PROMPT_HERE",
      "image": "FIRST_FRAME_IMAGE_URL",
      "last_frame": "LAST_FRAME_IMAGE_URL",
      "ratio": "adaptive",
      "duration": 5,
      "resolution": "720p",
      "generate_audio": true
    },
    "prefer": "balanced"
  }')

VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['video_url'])")
echo "Video URL: $VIDEO_URL"
```

### Reference Image-to-Video

```bash
[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1

RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{
    "type": "video",
    "inputs": {
      "prompt": "[图1]的人物在跳舞",
      "ref_images": ["REF_IMAGE_URL_1"],
      "ratio": "16:9",
      "duration": 5,
      "resolution": "720p"
    },
    "prefer": "balanced"
  }')

VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['video_url'])")
echo "Video URL: $VIDEO_URL"
```

### Download and Open Video

```bash
OUTPUT_PATH="$HOME/Desktop/seedance_video_$(date +%Y%m%d_%H%M%S).mp4"
curl -s -o "$OUTPUT_PATH" "$VIDEO_URL"
echo "Video saved to: $OUTPUT_PATH"
open "$OUTPUT_PATH"
```

## Optional Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `doubao-seedance-1-5-pro-251215` | Model hint to pass to SkillBoss API Hub |
| `ratio` | string | `16:9` (text2vid) / `adaptive` (img2vid) | Aspect ratio: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive` |
| `duration` | integer | `5` | Video duration in seconds (4-12 for 1.5 Pro, 2-12 for others). Set `-1` for auto (1.5 Pro only) |
| `resolution` | string | `720p` | Resolution: `480p`, `720p`, `1080p` |
| `seed` | integer | `-1` | Random seed for reproducibility. -1 = random |
| `camera_fixed` | boolean | `false` | Fix camera position |
| `watermark` | boolean | `false` | Add watermark to video |
| `generate_audio` | boolean | `true` | Generate synchronized audio (Seedance 1.5 Pro only) |
| `draft` | boolean | `false` | Generate draft/preview video at lower cost (Seedance 1.5 Pro only, forces 480p) |
| `return_last_frame` | boolean | `false` | Return last frame image URL (for chaining consecutive videos) |
| `service_tier` | string | `default` | `default` (online) or `flex` (offline, 50% cheaper, slower) |

## Image Requirements

- Formats: jpeg, png, webp, bmp, tiff, gif (1.5 Pro also supports heic, heif)
- Aspect ratio (width/height): between 0.4 and 2.5
- Dimensions: 300-6000 px per side
- Max file size: 30 MB

## 通过飞书发送视频文件（OpenClaw）

详见 [how_to_send_video_via_feishu_app.md](how_to_send_video_via_feishu_app.md)

## Rules

1. **Always check** that `SKILLBOSS_API_KEY` is set before making API calls: `[ -z "$SKILLBOSS_API_KEY" ] && echo "Error: SKILLBOSS_API_KEY not set" && exit 1`
2. **Default to Seedance 1.5 Pro** hint (`doubao-seedance-1-5-pro-251215`) unless user requests a specific model.
3. **Default to 720p, 16:9, 5 seconds, with audio** for text-to-video.
4. **Default to adaptive ratio** for image-to-video (auto-adapts to the input image).
5. **Video URLs expire in 24 hours** - always download immediately after generation.
6. For local image files, convert to base64 data URL format before sending.
7. Always show the user the video URL so they can access the result.
8. When generation fails, display the error message clearly and suggest possible fixes.
