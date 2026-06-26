---
name: smtools-image-generation
description: >
  Generate images from text prompts using AI models via OpenRouter, Kie.ai, or YandexART.
  Use when the user asks to generate, create, draw, or illustrate an image.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - OPENROUTER_API_KEY
    primaryEnv: OPENROUTER_API_KEY
    optionalEnv:
      - KIE_API_KEY
---

# Image Generation Skill

Generate images from text prompts. Default provider is **OpenRouter** (synchronous). Alternative: **Kie.ai** (async, task-based).

## When to Activate

Activate when the user asks to:
- Generate, create, draw, paint, illustrate, or render an image
- Make a picture, artwork, photo, or illustration
- Visualize something as an image
- Edit, modify, or transform an existing image

## How to Use

Run the generation script with an absolute path to avoid directory change prompts:

```bash
bash SKILL_DIR/scripts/run.sh --prompt "PROMPT" [OPTIONS]
```

Replace `SKILL_DIR` with the absolute path to this skill's root directory.

### Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Text prompt (required) |
| `--provider` | `openrouter` (default), `kie`, or `yandexart` |
| `-m, --model` | Model name (provider-specific) |
| `-i, --input` | Input image for editing (path or URL) |
| `-o, --output` | Output file path |
| `-c, --config` | Path to config.json |
| `--list-models` | List available models |
| `-v, --verbose` | Debug output to stderr |

### Output

The script outputs JSON to stdout:

```json
{"status": "ok", "image_path": "/absolute/path/to/image.png", "model": "google/gemini-3.1-flash-image-preview", "provider": "openrouter"}
```

After successful generation, show the user the image path and confirm the image was created.

## Image Editing

When the user wants to **edit, modify, or transform an existing image**, use the `-i` flag to pass the input image:

```bash
bash SKILL_DIR/scripts/run.sh -p "EDITING INSTRUCTION" -i /path/to/source/image.png
```

**How to decide:**
- User says "draw/generate/create X" → generate from scratch (no `-i`)
- User says "edit/change/modify this image" or references an existing image file → use `-i` with the path to that image
- User provides an image path and an editing instruction → use `-i`

The editing prompt should describe **what to change**, e.g. "Add sunglasses", "Make the background blue", "Remove the text".

## Provider Selection

- **OpenRouter** (default): Fast, synchronous. Models: `google/gemini-3.1-flash-image-preview`, `openai/gpt-image-1`, `google/imagen-4`, `stabilityai/stable-diffusion-3`. Requires `OPENROUTER_API_KEY`.
- **Kie.ai**: Async task-based. Models: `nano-banana-2`, `flux-ai`, `midjourney`, `google-4o-image`, `ghibli-ai`. Requires `KIE_API_KEY`. Use when the user explicitly requests Kie.ai or a Kie-specific model.
- **YandexART**: Async task-based. Models: `yandex-art/latest`. Requires `YANDEX_IAM_TOKEN` and `YANDEX_FOLDER_ID`. Use when the user explicitly requests YandexART or Yandex.

## Examples

Basic generation:
```bash
bash SKILL_DIR/scripts/run.sh -p "A serene mountain lake at sunset"
```

Specific model:
```bash
bash SKILL_DIR/scripts/run.sh -p "Cyberpunk cityscape" -m "google/imagen-4"
```

Kie.ai provider:
```bash
bash SKILL_DIR/scripts/run.sh -p "Studio Ghibli forest" --provider kie -m ghibli-ai
```

Edit an existing image:
```bash
bash SKILL_DIR/scripts/run.sh -p "Add a rainbow to the sky" -i /path/to/photo.png
```

Custom output path:
```bash
bash SKILL_DIR/scripts/run.sh -p "A red fox" -o /tmp/fox.png
```

## Error Handling

| Error | Action |
|-------|--------|
| Missing API key | Tell the user to set the environment variable (`OPENROUTER_API_KEY` or `KIE_API_KEY`) |
| Network/timeout error | Retry once. If still failing, inform the user |
| No image in response | Show the raw error from the JSON output |
| Kie.ai task timeout | Inform user that generation took too long, suggest retrying |

## Setup

If the skill has not been set up yet, run:
```bash
bash SKILL_DIR/setup.sh
```

## Security

- Never display or log API keys
- Never modify config.json without user permission
