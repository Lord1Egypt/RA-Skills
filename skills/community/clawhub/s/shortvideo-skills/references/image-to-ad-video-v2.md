# Image to Ad Video v2 (vidu/image-to-ad-video-v2)

Generate engaging advertisement videos from product images.

## Description

Creates professional advertisement videos from 1-7 product images with AI-generated motion and effects. Supports multiple durations, aspect ratios, and optional text prompts for style guidance.

## Credit Cost

**30 credits per second** of video

| Duration | Credits |
|----------|---------|
| 8 sec    | 240     |
| 15 sec   | 450     |
| 30 sec   | 900     |
| 60 sec   | 1800    |

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     IMAGE-TO-AD-VIDEO WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PREPARE IMAGES                                                           │
│     ├─ Local file: /Users/xxx/Downloads/product.jpg                         │
│     ├─ OSS path: d2mm4m9addr0008000a0.png                                   │
│     └─ URL: https://example.com/image.jpg                                   │
│         └─ Download to temp file → Upload to OSS                            │
│                                                                              │
│  2. PROCESS IMAGES                                                           │
│     ├─ Local file: Upload to OSS → Get OSS path                             │
│     ├─ URL: Download → Upload to OSS → Get OSS path                         │
│     └─ OSS path: Use directly                                               │
│                                                                              │
│  3. CREATE TASK                                                              │
│     POST /api/task/create                                                   │
│     ├─ Build task args with OSS paths                                       │
│     └─ Returns: task_id, video_ids                                          │
│                                                                              │
│  4. POLL FOR RESULTS (automatic)                                            │
│     GET /api/video/fetch?ids=video_id1,video_id2                            │
│     ├─ Status 0: Pending                                                    │
│     ├─ Status 1: Processing                                                 │
│     ├─ Status 2: Completed ✓                                                │
│     └─ Status 3: Failed ✗                                                   │
│                                                                              │
│  5. GET FINAL VIDEO URL                                                      │
│     video.specs["1080p"].video → OSS path                                   │
│     video.specs["1080p"].cover → Cover image                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Command

### Create Task (with automatic polling)

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images <image1> <image2> ... \
  --duration <seconds> \
  --aspect-ratio <ratio> \
  [--prompt "<text>"]
```

### Create Task (without polling)

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images <image1> <image2> ... \
  --duration <seconds> \
  --aspect-ratio <ratio> \
  [--prompt "<text>"] \
  --no-poll
```

### Poll for Results (separate script)

```bash
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids <video_id1> <video_id2>
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids <video_id> --once  # Single check
```

### Fetch Result Manually

```bash
source ~/.zshrc && python3 scripts/impl.py fetch --video-ids <video_id1> <video_id2>
```

## Parameters

| Parameter | Type | Required | Valid Values | Description |
|-----------|------|----------|--------------|-------------|
| `--images` | list | Yes | 1-7 paths | Image paths (local file, OSS path, or URL) |
| `--duration` | int | Yes | `8`, `15`, `30`, `60` | Video duration in seconds |
| `--aspect-ratio` | string | Yes | `16:9`, `9:16`, `1:1` | Video aspect ratio |
| `--prompt` | string | No | Max 2000 chars | Text prompt for style guidance |
| `--no-poll` | flag | No | - | Disable automatic result polling |

**Note**: `language` is automatically set to `"en"`.

## Image Path Types

| Type | Example | Behavior |
|------|---------|----------|
| Local file | `/Users/xxx/Downloads/image.jpg` | Upload to OSS, use returned path |
| OSS path | `d2mm4m9addr0008000a0.png` | Use directly |
| URL | `https://example.com/image.jpg` | Download to temp file, upload to OSS, use returned path |

**Note for URLs**: When providing HTTP/HTTPS URLs, the script will:
1. Download the image to a temporary file
2. Upload the temporary file to OSS
3. Use the OSS path for task creation
4. Clean up the temporary file after completion

## Constraints

- **Images**: Must provide 1-7 images
- **Duration**: Must be one of `[8, 15, 30, 60]` seconds
- **Aspect Ratio**: Must be one of `["16:9", "9:16", "1:1"]`
- **Prompt**: Maximum 2000 characters
- **Max file size**: 100MB per image

## Examples

### With Local Files (Auto-upload)

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images /Users/xxx/Downloads/sneaker1.jpg /Users/xxx/Downloads/sneaker2.jpg \
  --duration 15 \
  --aspect-ratio 16:9
```

### With OSS Paths

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images d2mm4m9addr0008000a0.png \
  --duration 8 \
  --aspect-ratio 1:1
```

### With URLs

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images https://example.com/img1.jpg https://example.com/img2.jpg \
  --duration 30 \
  --aspect-ratio 9:16 \
  --prompt "Modern product showcase with elegant transitions"
```

### With Prompt

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images img1.jpg img2.jpg img3.jpg img4.jpg \
  --duration 30 \
  --aspect-ratio 9:16 \
  --prompt "Dynamic sports shoe advertisement with energetic transitions"
```

### Without Automatic Polling

```bash
source ~/.zshrc && python3 scripts/image-to-ad-video.py \
  --images d2mm4m9addr0008000a0.png \
  --duration 8 \
  --aspect-ratio 1:1 \
  --no-poll
```

### Poll for Results Separately

```bash
# After creating task without polling
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids video_abc123

# Single check (no continuous polling)
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids video_abc123 --once
```

## Response

### Create Task Response

```json
{
  "status": "success",
  "task_id": "task_jkl012",
  "video_ids": ["video_mno345"],
  "asset_ids": [],
  "consumed_credit": 240,
  "credit": 760,
  "sub_credit": 0,
  "uploads": [
    {
      "field": "images[0]",
      "path": "videos/20260312/xxx/image.jpg",
      "url": "https://xxx.oss-cn-beijing.aliyuncs.com/videos/20260312/xxx/image.jpg"
    }
  ],
  "poll_result": {
    "status": "success",
    "message": "All videos completed",
    "videos": [...],
    "attempts": 12
  }
}
```

### Fetch Video Response

```json
{
  "status": "success",
  "videos": [
    {
      "id": "video_mno345",
      "task_id": "task_jkl012",
      "user_id": "user_xxx",
      "kind": 18,
      "name": "Product Video",
      "status": 2,
      "width": 1920,
      "height": 1080,
      "duration": 15,
      "specs": {
        "1080p": {
          "video": "videos/xxx/video.mp4",
          "cover": "videos/xxx/cover.jpg",
          "size": 5242880
        }
      },
      "nsfw": false,
      "watermark": false,
      "task_type": "vidu/image-to-ad-video-v2",
      "created_at": "2026-03-12T10:00:00Z"
    }
  ]
}
```

### Video Status Codes

| Status | Description |
|--------|-------------|
| 0 | Pending - Task queued |
| 1 | Processing - Video being generated |
| 2 | Completed - Video ready ✓ |
| 3 | Failed - Generation error ✗ |

### Polling Behavior

- **Interval**: 10 seconds between checks
- **Max attempts**: 60 (approximately 10 minutes)
- **Auto-stop**: When all videos complete or any fails
- **Timeout**: Returns partial results if max attempts reached

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/oss/upload` | POST | Upload local files to OSS |
| `/api/task/create` | POST | Create video generation task |
| `/api/video/fetch` | GET | Fetch video status and results |

## Notes

- Language is always `"en"` (English only)
- Supports local file paths (auto-upload), OSS paths, and URLs
- Prompt is optional but improves results with style guidance
- Automatic polling waits for video completion (use `--no-poll` to disable)
- Video URLs are in `specs["1080p"].video` field