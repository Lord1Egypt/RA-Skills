# Jimeng API Image Generation

Generate high-quality AI images using Volcengine's Jimeng 4.0 API.

## Features

- Text-to-image generation with customizable prompts
- Image-to-image editing and style transfer
- Multiple resolution presets (1K, 2K, 4K)
- Custom dimensions with flexible aspect ratios
- Batch image generation
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
export JIMENG_API_URL="https://visual.volcengineapi.com"
export JIMENG_API_TIMEOUT=120
export JIMENG_POLL_INTERVAL=2
export JIMENG_MAX_POLL_ATTEMPTS=60
```

## Usage

### Text-to-Image

```bash
# Basic usage (2K resolution by default)
scripts/generate_image.py "A white Siamese cat sitting on a windowsill, sunlight streaming in"

# Specify resolution preset
scripts/generate_image.py "Mountain sunset landscape" --size 4K

# Custom dimensions
scripts/generate_image.py "Wide landscape" --width 2560 --height 1440

# Save to file
scripts/generate_image.py "Serene lake at sunset" --output lake.png
```

### Image-to-Image

```bash
# Style transfer
scripts/generate_image.py "Change to watercolor style" --images https://example.com/input.jpg

# Multiple input images
scripts/generate_image.py "Combine into collage" --images img1.jpg img2.jpg img3.jpg
```

### Command-Line Options

```
scripts/generate_image.py PROMPT [OPTIONS]

Arguments:
  PROMPT              Text prompt for image generation (required, max 800 chars)

Options:
  --size SIZE         Image size: 1K, 2K, 4K or WxH (default: 2K)
  --width WIDTH       Exact width (requires --height)
  --height HEIGHT     Exact height (requires --width)
  --images URL [...]  Input image URLs for image-to-image (max 10)
  --watermark         Add "AI Generated" watermark
  --scale FLOAT       Text influence 0-1 (default: 0.5)
  --force-single      Force single image output
  --output PATH       Download image to file
  --json              Output raw JSON response
```

## Image Sizes

### Preset Resolutions

| Preset | Resolution | Use Case |
|--------|------------|----------|
| 1K | 1024×1024 | Quick previews |
| 2K | 2048×2048 | Default, good quality |
| 4K | 4096×4096 | High-resolution output |

### Recommended Aspect Ratios

| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| 1:1 | 2048×2048 | Social media posts |
| 4:3 | 2304×1728 | Presentations |
| 16:9 | 2560×1440 | Widescreen displays |
| 9:16 | 1440×2560 | Mobile vertical |
| 3:2 | 2496×1664 | Photography |

### Constraints

- Width × Height: [1024×1024, 4096×4096]
- Aspect ratio (width/height): [1/16, 16]
- Recommended: Use 2K+ for better quality

## Limits

### Input

- Prompt: max 800 characters
- Images: max 10 files, ≤15MB each
- Format: JPEG, PNG only
- Resolution: ≤4096×4096
- Aspect ratio: [1/3, 3]

### Output

- Max images: 15 - (input image count)
- Format: PNG
- URL validity: 24 hours

## Error Handling

| Code | Message | Solution |
|------|---------|----------|
| 50411 | Pre Img Risk Not Pass | Check input image content |
| 50511 | Post Img Risk Not Pass | Modify prompt and retry |
| 50412 | Text Risk Not Pass | Remove sensitive words |
| 50429 | Rate limit exceeded | Wait and retry |
| timeout | Request timeout | Increase `JIMENG_API_TIMEOUT` |

## Reference Documentation

- [Jimeng AI 4.0 API Documentation](https://www.volcengine.com/docs/85621/1817045)
- [HTTP Request Example](https://www.volcengine.com/docs/6444/1390583)
- [Volcengine Console](https://console.volcengine.com)
- [API Key Management](https://console.volcengine.com/iam/key_manage/)
