# seaart-video

Generate AI videos using the [SeaArt](https://www.seaart.ai) platform directly from Claude Code.

Supports **Text-to-Video** and **Image-to-Video** generation with multiple models including SeaArt Sono Cast, Vidu Q3 Turbo, Kling 3.0, and Wan 2.6.

## Requirements

- Python 3
- `requests` library (`pip install requests`)
- A SeaArt account and authentication token (`SEAART_TOKEN`)

## Setup

Get your token from the `T` cookie on seaart.ai, then run:

```
/update-config set SEAART_TOKEN="your_token_here"
```

## Usage

Just ask Claude to generate a video:

- "Generate a video of a sunset over the ocean"
- "Turn this image into a video of her walking"
- "Make a 16:9 video of a rainy city street using Kling 3.0"

## Security

This skill sends your prompt and any provided image URLs to seaart.ai. See `SKILL.md` for the full security and privacy disclosure.
