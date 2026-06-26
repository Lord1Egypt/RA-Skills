# Product to Video (sora2/product-to-video)

Generate marketing videos from product images using Sora2 AI.

## Description

Creates a professional product video from a single product image. The AI analyzes the product and generates an engaging video with smooth camera movements and visual effects.

## Credit Cost

**100 credits** (fixed per video)

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PRODUCT-TO-VIDEO WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PREPARE IMAGE                                                            │
│     ├─ Local file: /Users/xxx/Downloads/product.jpg                         │
│     ├─ OSS path: d2mm4m9addr0008000a0.png                                   │
│     └─ URL: https://example.com/product.jpg                                 │
│         └─ Download to temp file → Upload to OSS                            │
│                                                                              │
│  2. PROCESS IMAGE                                                            │
│     ├─ Local file: Upload to OSS → Get OSS path                             │
│     ├─ URL: Download → Upload to OSS → Get OSS path                         │
│     └─ OSS path: Use directly                                               │
│                                                                              │
│  3. CREATE TASK                                                              │
│     POST /api/task/create                                                   │
│     ├─ Build task args with product info and image                          │
│     └─ Returns: task_id, video_ids                                          │
│                                                                              │
│  4. AI PROCESSING PIPELINE                                                   │
│     ├─ Product analysis (GPT)                                               │
│     ├─ Script generation (Gemini)                                           │
│     ├─ Image creation (Gemini Edit)                                         │
│     └─ Video generation (Sora2)                                             │
│                                                                              │
│  5. POLL FOR RESULTS (automatic)                                            │
│     GET /api/video/fetch?ids=video_id1                                      │
│     ├─ Status 0: Pending                                                    │
│     ├─ Status 1: Processing                                                 │
│     ├─ Status 2: Completed ✓                                                │
│     └─ Status 3: Failed ✗                                                   │
│                                                                              │
│  6. GET FINAL VIDEO URL                                                      │
│     video.specs["1080p"].video → OSS path                                   │
│     video.specs["1080p"].cover → Cover image                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Command

### Create Task (with automatic polling)

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "<product_name>" \
  --image <image_path> \
  --aspect-ratio <ratio> \
  --duration 12 \
  [--product-info "<description>"]
```

### Create Task (without polling)

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "<product_name>" \
  --image <image_path> \
  --aspect-ratio <ratio> \
  --duration 12 \
  [--product-info "<description>"] \
  --no-poll
```

### Poll for Results (separate script)

```bash
source ~/.zshrc && python3 scripts/poll-videos.py --video-ids <video_id>
```

## Parameters

| Parameter | Type | Required | Valid Values | Description |
|-----------|------|----------|--------------|-------------|
| `--product-name` | string | Yes | - | Name of the product |
| `--product-info` | string | No | - | Product description/details |
| `--image` | string | Yes | - | Product image path |
| `--aspect-ratio` | string | Yes | `16:9`, `9:16` | Video aspect ratio |
| `--duration` | int | Yes | `12` | Video duration in seconds |
| `--no-poll` | flag | No | - | Disable automatic polling |

**Note**: Only 12-second videos are supported.

## Image Path Types

| Type | Example | Behavior |
|------|---------|----------|
| Local file | `/Users/xxx/Downloads/product.jpg` | Upload to OSS, use returned path |
| OSS path | `d2mm4m9addr0008000a0.png` | Use directly |
| URL | `https://example.com/product.jpg` | Download to temp file, upload to OSS, use returned path |

**Note for URLs**: When providing HTTP/HTTPS URLs, the script will:
1. Download the image to a temporary file
2. Upload the temporary file to OSS
3. Use the OSS path for task creation
4. Clean up the temporary file after completion

## Constraints

- **Duration**: Only 12 seconds supported
- **Aspect ratio**: Only `16:9` or `9:16`
- **Image**: Single product image required
- **Max file size**: 100MB

## Examples

### With Local Image

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Premium Headphones" \
  --image /Users/xxx/Downloads/headphones.jpg \
  --aspect-ratio 16:9 \
  --duration 12
```

### With URL Image

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Smart Watch" \
  --image https://example.com/smartwatch.jpg \
  --aspect-ratio 9:16 \
  --duration 12
```

### With Product Info

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Premium Headphones" \
  --product-info "Wireless noise-canceling headphones with 30-hour battery life, premium sound quality" \
  --image headphones.jpg \
  --aspect-ratio 16:9 \
  --duration 12
```

### With OSS Path

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Product Name" \
  --image d2mm4m9addr0008000a0.png \
  --aspect-ratio 16:9 \
  --duration 12
```

### Without Automatic Polling

```bash
source ~/.zshrc && python3 scripts/product-to-video.py \
  --product-name "Product" \
  --image product.jpg \
  --aspect-ratio 16:9 \
  --duration 12 \
  --no-poll
```

## Response

### Create Task Response

```json
{
  "status": "success",
  "task_id": "task_abc123",
  "video_ids": ["video_xyz789"],
  "asset_ids": [],
  "consumed_credit": 100,
  "credit": 900,
  "sub_credit": 0
}
```

### Fetch Video Response

```json
{
  "status": "success",
  "videos": [
    {
      "id": "video_xyz789",
      "task_id": "task_abc123",
      "status": 2,
      "width": 1920,
      "height": 1080,
      "duration": 12,
      "specs": {
        "1080p": {
          "video": "videos/xxx/video.mp4",
          "cover": "videos/xxx/cover.jpg",
          "size": 3145728
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

- Only supports 12-second videos
- Fixed cost of 100 credits per video
- The product image should be clear and well-lit
- Works best with product photos on clean backgrounds
- AI pipeline: Product analysis → Script → Image edit → Video generation
- Automatic polling waits for video completion (use `--no-poll` to disable)
- Video URLs are in `specs["1080p"].video` field