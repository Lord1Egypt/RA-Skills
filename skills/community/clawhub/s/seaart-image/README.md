# seaart-image

Generate AI images using the [SeaArt](https://www.seaart.ai) platform directly from Claude Code.

Supports **Text-to-Image** generation with multiple models including SeaArt Infinity, SeaArt Film series, Seedream series, Nano Banana series, and more. Features smart HD/SD resolution, LoRA support, and 7 aspect ratios.

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

Just ask Claude to generate an image:

- "Generate a realistic photo of a cat by the window"
- "Use seaart-film-edit-3 to create a cinematic city night scene in 16:9"
- "Generate an anime girl under cherry blossoms with wai-ani-ponyxl"

## Security

This skill sends your prompt and generation parameters to seaart.ai. See `SKILL.md` for the full security and privacy disclosure.
