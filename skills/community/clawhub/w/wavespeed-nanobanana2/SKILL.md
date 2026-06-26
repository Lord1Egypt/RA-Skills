# Wavespeed NanoBanana2 Text-to-Image Skill

## Overview
This skill enables text-to-image generation using the Wavespeed AI NanoBanana2 API. It allows you to generate high-quality images from textual descriptions with various resolution options.

## Features
- Generate images from text prompts
- Support for multiple resolutions (1k, 2k, 4k)
- Multiple output formats (PNG, JPG, WebP)
- Environment variable-based authentication
- Error handling and validation

## Prerequisites
1. A valid Wavespeed AI API key
2. The API key must be set in the `WAVESPEED_API_KEY` environment variable

## Installation
1. Place this skill in your OpenClaw skills directory: `~/.openclaw/workspace/skills/`
2. Set the `WAVESPEED_API_KEY` environment variable with your Wavespeed API key
3. Register the skill through the OpenClaw management interface

## Usage
### Basic Usage
```javascript
{
  "skill": "wavespeed-nanobanana2",
  "parameters": {
    "prompt": "A beautiful landscape with mountains and a lake"
  }
}
```

### With Custom Resolution
```javascript
{
  "skill": "wavespeed-nanobanana2",
  "parameters": {
    "prompt": "A futuristic city skyline at night",
    "resolution": "2k"
  }
}
```

### With Custom Output Format
```javascript
{
  "skill": "wavespeed-nanobanana2",
  "parameters": {
    "prompt": "A cute dog wearing a sweater",
    "resolution": "1k",
    "output_format": "jpg"
  }
}
```

## Parameters
| Parameter       | Type       | Required | Default | Description                                  |
|-----------------|------------|----------|---------|----------------------------------------------|
| `prompt`        | String     | Yes      | -       | Text description of the image to generate    |
| `resolution`    | String     | No       | "1k"    | Image resolution (1k, 2k, or 4k)             |
| `output_format` | String     | No       | "png"   | Output image format (png, jpg, or webp)      |

## Environment Variables
- `WAVESPEED_API_KEY` (required): Your Wavespeed AI API key for authentication

## Error Handling
The skill includes comprehensive error handling for:
- Missing required parameters
- Missing or invalid API key
- API request failures
- HTTP error responses

## Notes
- Image generation may take several seconds depending on the resolution
- The API has rate limits - check Wavespeed AI documentation for details
- High-resolution images (2k, 4k) may consume more credits

## API Reference
For more details about the Wavespeed NanoBanana2 API, see:
[Wavespeed AI API Documentation](https://docs.wavespeed.ai/)