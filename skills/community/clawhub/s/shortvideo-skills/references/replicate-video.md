# Replicate Video (vidu/replicate-video)

Replicate and transform existing videos with new product images.

## Description

Creates new videos by combining an existing video with product/model images. The AI replicates the style and motion of the original video while incorporating new visual elements.

## Credit Cost

| Resolution | Credits/Second |
|------------|---------------|
| 540p | 9 |
| 720p | 12 |
| 1080p | 15 |

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REPLICATE-VIDEO WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PREPARE FILES                                                            │
│     ├─ Video: local file / OSS path / URL                                   │
│     ├─ Product images: local files / OSS paths / URLs                       │
│     └─ Model images: local files / OSS paths / URLs                         │
│                                                                              │
│  2. PROCESS FILES                                                            │
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
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video <video_path> \
  --aspect-ratio <ratio> \
  --resolution <resolution> \
  [--product-images <img1> <img2> ...] \
  [--model-images <img1> <img2> ...] \
  [--prompt "<text>"]
```

### Create Task (without polling)

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video <video_path> \
  --aspect-ratio <ratio> \
  --resolution <resolution> \
  [--product-images ...] \
  [--model-images ...] \
  --no-poll
```

### Poll for Results (separate script)

```bash
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids <video_id1> <video_id2>
```

## Parameters

| Parameter | Type | Required | Valid Values | Description |
|-----------|------|----------|--------------|-------------|
| `--video` | string | Yes | - | Source video path (5-300 seconds) |
| `--aspect-ratio` | string | Yes | `16:9`, `9:16` | Video aspect ratio |
| `--resolution` | string | Yes | `540p`, `720p`, `1080p` | Output resolution |
| `--product-images` | list | No* | 1-7 total with model | Product image paths |
| `--model-images` | list | No* | 1-7 total with product | Model image paths |
| `--prompt` | string | No | Max 2000 chars | Text prompt |
| `--remove-audio` | flag | No | - | Remove audio from result |
| `--no-poll` | flag | No | - | Disable automatic polling |

*At least one image (product or model) is required.

## File Path Types

| Type | Example | Behavior |
|------|---------|----------|
| Local file | `/Users/xxx/Downloads/video.mp4` | Upload to OSS, use returned path |
| OSS path | `d2mm4m9addr0008000a0.mp4` | Use directly |
| URL | `https://example.com/video.mp4` | Download to temp file, upload to OSS, use returned path |

**Note for URLs**: When providing HTTP/HTTPS URLs, the script will:
1. Download the file to a temporary file
2. Upload the temporary file to OSS
3. Use the OSS path for task creation
4. Clean up the temporary file after completion

## Constraints

- **Video duration**: 5-300 seconds
- **Images**: At least 1 image required, max 7 total (product + model combined)
- **Aspect ratio**: Only `16:9` or `9:16`
- **Resolution**: `540p`, `720p`, or `1080p`
- **Prompt**: Maximum 2000 characters
- **Max file size**: 100MB per file

## Examples

### With Local Video and Product Images

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video /Users/xxx/Downloads/template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images /Users/xxx/Downloads/product1.jpg /Users/xxx/Downloads/product2.jpg
```

### With URLs

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video https://example.com/template.mp4 \
  --aspect-ratio 9:16 \
  --resolution 720p \
  --product-images https://example.com/product.jpg
```

### With Model Images and Prompt

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video d2mm4m9addr0008000a0.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --model-images model1.jpg model2.jpg \
  --prompt "Fashion showcase with modern urban style"
```

### Mixed Product and Model Images

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images product1.jpg product2.jpg \
  --model-images model.jpg
```

### Without Automatic Polling

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images product.jpg \
  --no-poll
```

### With Remove Audio

```bash
source ~/.zshrc && python3 scripts/replicate-video.py \
  --video template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images product.jpg \
  --remove-audio
```

## Response

### Create Task Response

```json
{
  "status": "success",
  "task_id": "task_pqr678",
  "video_ids": ["video_stu901"],
  "asset_ids": [],
  "consumed_credit": 300,
  "credit": 700,
  "sub_credit": 0
}
```

### Fetch Video Response

```json
{
  "status": "success",
  "videos": [
    {
      "id": "video_stu901",
      "task_id": "task_pqr678",
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
      }
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

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/oss/upload` | POST | Upload local files to OSS |
| `/api/task/create` | POST | Create video generation task |
| `/api/video/fetch` | GET | Fetch video status and results |

## Notes

- Source video must be 5-300 seconds
- At least one image (product or model) is required
- Maximum 7 images total (product + model combined)
- Higher resolution = more credits consumed
- Automatic polling waits for video completion (use `--no-poll` to disable)
- Video URLs are in `specs["1080p"].video` field