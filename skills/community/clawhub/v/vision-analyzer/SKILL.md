---
name: vision-analyzer
description: |
  Analyze images using Ollama Cloud's Kimi K2.5 vision capabilities.
  Use when user wants to describe, understand, or get information about an image.
  Works with local image files, screenshots, or downloaded images.
  Supports JPG, PNG, GIF, WebP formats.
metadata:
  author: clawdia
  version: "1.0.1"
---

# Vision Analyzer

Analyze images using Kimi K2.5 multimodal vision capabilities through Ollama Cloud API.

## When to Use

- User wants to know what's in an image
- Describing screenshots or photos
- Understanding UI elements, text in images
- Analyzing memes, charts, diagrams

## Quick Start

```bash
python3 ~/.openclaw/workspace/skills/vision-analyzer/scripts/vision_analyze.py <image_path> [prompt]
```

## Examples

Describe an image:
```bash
python3 ~/.openclaw/workspace/skills/vision-analyzer/scripts/vision_analyze.py photo.jpg
```

Ask specific question:
```bash
python3 ~/.openclaw/workspace/skills/vision-analyzer/scripts/vision_analyze.py screenshot.png "What UI elements do you see?"
```

## Common Image Locations

- Downloads: `/mnt/chromeos/MyFiles/Downloads/`
- Screenshots: `/mnt/chromeos/MyFiles/Downloads/`
- Home directory: `~/`

## Configuration

Set your Ollama API key as environment variable:

```bash
export OLLAMA_API_KEY="your-api-key-here"
```

Get your API key from [ollama.com/settings](https://ollama.com/settings)

## API Configuration

The skill uses Ollama Cloud API with Kimi K2.5 model.
API key is read from `OLLAMA_API_KEY` environment variable.

## Supported Formats

- JPG/JPEG
- PNG
- GIF
- WebP

## Output

Returns a natural language description of the image content.
