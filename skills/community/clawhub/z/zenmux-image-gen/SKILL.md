---
name: zenmux-image-gen
description: |
  Generate images from text prompts using ZenMux API (Vertex AI protocol with Gemini models).
  Use when: (1) User wants to generate/create images from text descriptions, (2) User asks for
  AI image generation, (3) User mentions ZenMux or Gemini image models, (4) User wants to
  create artwork, illustrations, or visual content programmatically, (5) Image-to-image editing.
  Supports aspect ratio and resolution control. Requires ZENMUX_API_KEY.
---

# ZenMux Image Generation

Generate images from text prompts using ZenMux API with Google Gemini models.

## Quick Start

```bash
# Generate image (requires ZENMUX_API_KEY env var)
python3 scripts/generate_image.py "A cute cat" output.png

# With aspect ratio and resolution
python3 scripts/generate_image.py "A cute cat" output.png --aspect-ratio 16:9 --image-size 2K
```

## API Key Setup

Get your API key from https://zenmux.ai.

```bash
# Set environment variable
export ZENMUX_API_KEY="sk-..."
```

**Security Rules:**
- NEVER use `--api-key` flag (visible in shell history)
- NEVER commit API keys to git

## Script Options

| Option | Description |
|--------|-------------|
| `--model MODEL` | Model name (default: `google/gemini-3.1-flash-image-preview`) |
| `--input-image PATH` | Input image for image-to-image generation |
| `--temperature N` | Randomness 0.0-2.0 (default: 1.0) |
| `--max-tokens N` | Max output tokens |
| `--aspect-ratio RATIO` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9` |
| `--image-size SIZE` | `1K` (default), `2K`, `4K` |

## Image-to-Image

Edit existing images with text prompts:

```bash
python3 scripts/generate_image.py "Make it nighttime" result.png --input-image photo.jpg
```

## Available Models

| Model | Alias | Use Case |
|-------|-------|----------|
| `google/gemini-3.1-flash-image-preview` | Nano Banana 2 | Fast & quality (default) |
| `google/gemini-3-pro-image-preview` | Nano Banana Pro | Best quality |
| `google/gemini-2.5-flash-image` | Nano Banana | Faster generation |

## Prompt Tips

**Writing effective prompts:**
- Be specific: "A golden retriever puppy playing on grass" instead of "a dog"
- Include details: lighting (golden hour, soft light), style (photorealistic, anime, oil painting)
- For image-to-image: describe the desired change clearly, e.g., "Change to nighttime with city lights"
- Try 10+ words for better results

## Troubleshooting

| Error | Fix |
|-------|-----|
| Input image not found | Check file path; verify file exists |
| Image too large | Max input size is 20 MB; compress before uploading |
| 401 Unauthorized | Check `ZENMUX_API_KEY` is set correctly |
| 429 Rate limited | Wait and retry, or upgrade to paid tier |
| Request timeout | API may be slow; wait and retry |
| Network error | Check internet connection |
| No image in response | Try a different prompt or model |
| Poor image quality | Use more descriptive prompt (10+ words) |

## Script Features

- **Timeout protection**: Requests timeout after 300 seconds (5 minutes)
- **Auto-create directories**: Output directories are created automatically
- **Auto-rename on conflict**: If output file exists, automatically appends number (e.g., `image_1.png`, `image_2.png`)
- **Input validation**: Checks image format, size, and existence
- **Clear error messages**: Human-readable error explanations
- **Format support**: JPG, PNG, WebP, GIF input formats

## Batch Generation

Generate multiple images by running the script multiple times with different outputs:

```bash
# Generate variations of the same prompt
for i in 1 2 3; do
  python3 scripts/generate_image.py "A cute cat in different poses" "cat_$i.png"
done
```
