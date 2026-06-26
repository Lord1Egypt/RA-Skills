# Jimeng API Video Generation

Generate high-quality AI videos using Volcengine's Jimeng Video 3.0 Pro API.

## Features

- Text-to-video generation with customizable prompts
- Image-to-video (first frame as reference)
- Image-to-video (first and last frame)
- Camera movement control for image-to-video
- Multiple resolution presets (720P, 1080P, Pro)
- Configurable duration (4-10 seconds) and FPS (24-30)
- Local file output support

## Setup

### 1. Get API Credentials

[Get Access Key/Secret Key](https://www.volcengine.com/docs/85621/1995636?lang=zh#3C9mCW9O)

### 2. Configure Environment Variables

```bash
# ~/.zshrc or ~/.zshenv
export VOLC_ACCESSKEY="your_access_key_id"
export VOLC_SECRETKEY="your_secret_access_key"
```

### Optional Configuration

```bash
export JIMENG_VIDEO_API_URL="https://visual.volcengineapi.com"
export JIMENG_VIDEO_API_TIMEOUT=300
export JIMENG_VIDEO_POLL_INTERVAL=5
export JIMENG_VIDEO_MAX_POLL_ATTEMPTS=120
```

## Usage

### Text-to-Video

```bash
# Basic usage (720P, 5 seconds, 24 FPS)
scripts/generate_video.py "A golden retriever running through a field of sunflowers"

# 1080P HD video
scripts/generate_video.py "Ocean waves crashing on a beach at sunset" --mode t2v_1080p

# Longer video with higher FPS
scripts/generate_video.py "A butterfly landing on a flower" --duration 10 --fps 30

# Save to file
scripts/generate_video.py "City timelapse at night" --output city_timelapse.mp4
```

### Image-to-Video

```bash
# First frame as reference
scripts/generate_video.py "Make the image come to life" --image https://example.com/photo.jpg

# First and last frame (transition)
scripts/generate_video.py "Smooth transition" --image https://example.com/start.jpg --tail-image https://example.com/end.jpg

# Camera movement effect
scripts/generate_video.py "Zoom in slowly" --image https://example.com/landscape.jpg --mode i2v_recamera_720p
```

### Pro Mode

```bash
# High quality Pro mode (supports both text and image input)
scripts/generate_video.py "Cinematic drone shot of mountains" --mode ti2v_pro --duration 8
scripts/generate_video.py "Animate this scene" --mode ti2v_pro --image https://example.com/scene.jpg
```

### Command-Line Options

```
scripts/generate_video.py PROMPT [OPTIONS]

Arguments:
  PROMPT              Text prompt for video generation (required)

Options:
  --mode MODE         Generation mode (default: t2v_720p)
                      Pro: ti2v_pro
                      1080P: t2v_1080p, i2v_first_1080p, i2v_first_tail_1080p
                      720P: t2v_720p, i2v_first_720p, i2v_first_tail_720p, i2v_recamera_720p
  --duration SECS     Video duration: 4, 5, 6, 8, 10 (default: 5)
  --fps FPS           Frames per second: 24, 25, 30 (default: 24)
  --image URL         Input image URL for image-to-video (first frame)
  --tail-image URL    Tail image URL for first & last frame mode
  --seed INT          Random seed for reproducibility
  --output PATH       Download video to file
  --json              Output raw JSON response
```

## Generation Modes

### Pro Version (1080P HD)

| Mode | Description |
|------|-------------|
| `ti2v_pro` | Text-to-video + Image-to-video (first frame) Pro |

### 1080P Version

| Mode | Description |
|------|-------------|
| `t2v_1080p` | Text-to-video 1080P |
| `i2v_first_1080p` | Image-to-video (first frame) 1080P |
| `i2v_first_tail_1080p` | Image-to-video (first & last frame) 1080P |

### 720P Version

| Mode | Description |
|------|-------------|
| `t2v_720p` | Text-to-video 720P |
| `i2v_first_720p` | Image-to-video (first frame) 720P |
| `i2v_first_tail_720p` | Image-to-video (first & last frame) 720P |
| `i2v_recamera_720p` | Image-to-video (camera movement) 720P |

## Video Specifications

### Duration Options

| Duration | Use Case |
|----------|----------|
| 4s | Quick clips, social media |
| 5s | Default, general purpose |
| 6s | Short scenes |
| 8s | Medium-length content |
| 10s | Longer narratives |

### FPS Options

| FPS | Use Case |
|-----|----------|
| 24 | Cinematic look (default) |
| 25 | PAL video standard |
| 30 | Smooth motion, NTSC standard |

## Limits

### Input (for image-to-video)

- Format: JPEG, PNG only
- Max size: 15MB per image
- Max resolution: 4096×4096

### Output

- Format: MP4
- URL validity: 24 hours
- Generation time: 2-10 minutes depending on duration and mode

## Error Handling

| Code | Message | Solution |
|------|---------|----------|
| 50411 | Pre Img Risk Not Pass | Check input image content |
| 50511 | Post Video Risk Not Pass | Modify prompt and retry |
| 50412 | Text Risk Not Pass | Remove sensitive words |
| 50429 | Rate limit exceeded | Wait and retry |
| timeout | Request timeout | Increase `JIMENG_VIDEO_API_TIMEOUT` |

## Reference Documentation

- [Jimeng Video 3.0 Pro API Documentation](https://www.volcengine.com/docs/85621/1777001)
- [Jimeng Video 3.0 720P API](https://www.volcengine.com/docs/85621/1792710)
- [Jimeng Video 3.0 1080P API](https://www.volcengine.com/docs/85621/1792711)
- [HTTP Request Example](https://www.volcengine.com/docs/6444/1390583)
- [Volcengine Console](https://console.volcengine.com)
- [API Key Management](https://console.volcengine.com/iam/key_manage/)
