# vlm-image-helper

[English](README.md) | [中文](README.zh-CN.md)

> Visual inspection helper for VLM and OCR workflows.

`vlm-image-helper` helps an agent assist a vision model in seeing an image more clearly before re-analysis. It is not a general-purpose image editor—it is a targeted visual aid for resolving ambiguities that block confident OCR or visual understanding.

## Problem

Vision models often encounter situations where they cannot confidently read text or distinguish similar characters:

- **Character confusion**: Cannot tell `O` from `0`, `I` from `l` or `1`, `B` from `8`
- **Orientation issues**: Text is sideways, upside-down, or tilted
- **Resolution limits**: Small text or distant details are unreadable
- **Contrast problems**: Faded scans, dark photos, washed-out screenshots
- **Partial visibility**: Only one region of the image matters, but the rest creates noise

When a model says "I cannot confidently read this" or "the image is unclear", it needs a better view—not a full image edit.

## Solution

`vlm-image-helper` provides **semantic presets** so the agent can describe regions naturally:

- Say **"top-left"** instead of guessing pixel coordinates
- Say **"center"** instead of calculating percentages
- Say **"x2"** instead of computing scale factors

The agent thinks in natural language; the skill translates to precise operations.

## What You Get

- **Semantic crop presets**: `top-left`, `center`, `bottom-right`, `left-half`, etc.
- **Semantic scale presets**: `x2`, `x3`, `x4`
- **Rotation**: any angle for misaligned text
- **Enhancement**: auto-enhance, contrast, sharpness for readability
- **Format conversion**: file path ↔ base64 for re-input
- **Minimal edits**: smallest transformation that removes ambiguity

## How It Works

```text
1. Model encounters ambiguous region in image
2. Agent chooses semantic preset (e.g., "bottom-right")
3. Script applies minimal transformation
4. Agent re-inputs processed image for re-analysis
5. Model confirms or agent iterates with tighter crop
```

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Semantic crop** | `--crop-preset top-left`, `center`, `bottom-right`, etc. |
| **Semantic zoom** | `--scale-preset x2`, `x3`, `x4` |
| **Rotation** | `--rotate 90`, `--rotate -15`, any angle |
| **Enhancement** | `--auto-enhance`, `--contrast 1.5`, `--sharpness 2.0` |
| **Pipeline** | Chain multiple operations in one command |
| **Passthrough** | Convert file to base64 without any edits |

## Installation

**Prerequisite:**
```bash
pip install Pillow
# or
uv pip install Pillow
```

**Install the skill:**
```bash
# Clone the repo
git clone https://github.com/your-org/vlm-image-helper.git

# Copy to your skills directory
# macOS / Linux
cp -r vlm-image-helper/* ~/.claude/skills/vlm-image-helper/

# Windows (PowerShell)
Copy-Item -Recurse vlm-image-helper/* $env:USERPROFILE\.claude\skills\vlm-image-helper\
```

## Quick Examples

```bash
# Rotate sideways text
python scripts/image_helper.py image.png --rotate 90 -o rotated.png

# Crop bottom-right quadrant and zoom 3x
python scripts/image_helper.py image.png --crop-preset bottom-right --scale-preset x3 -o detail.png

# Enhance low-contrast text
python scripts/image_helper.py image.png --auto-enhance -o enhanced.png

# Convert file to base64 for re-input
python scripts/image_helper.py image.png --base64

# Full pipeline: rotate, crop center, zoom 2x, output base64
python scripts/image_helper.py screenshot.png --rotate 5 --crop-preset center --scale-preset x2 --base64
```

## When to Use

- Model cannot confidently read text in an image
- Model cannot distinguish similar characters (`O/0`, `I/l/1`)
- Model says the image is unclear or low quality
- Only one region of the image is relevant
- Model would benefit from a second pass on a clearer view

## When NOT to Use

- General-purpose image editing (crop, resize, filter for aesthetic purposes)
- Batch image processing
- Image format conversion (unless for re-input to vision model)

## Repository Structure

```text
vlm-image-helper/
|-- SKILL.md                 # Core workflow and decision guide
|-- README.md
|-- scripts/
|   `-- image_helper.py      # Main CLI tool
|-- references/
|   |-- cli-reference.md     # Full CLI documentation
|   `-- presets.md           # Preset tables and heuristics
`-- agents/
    `-- openai.yaml          # OpenAI-compatible agent config
```

## License

This project is licensed under the [MIT License](LICENSE).
