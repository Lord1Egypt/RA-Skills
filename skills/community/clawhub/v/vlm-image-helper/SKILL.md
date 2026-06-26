---
name: vlm-image-helper
description: "Visual inspection helper for VLM and OCR workflows. Use when agent needs to help a vision model see an image more clearly before re-analysis: rotate misaligned or sideways text, crop to a relevant region, zoom small details, enhance readability, or convert an image for re-input. Trigger especially when the model cannot confidently read text, cannot tell similar characters apart such as O/0 or I/l/1, says the image is unclear, needs to inspect only one area of the image, or would benefit from a second pass on a clearer view. Do not use as a general-purpose image editor."
---

# VLM Image Helper

Treat this skill as a visual aid for the model, not as a general image editor.

Use `scripts/image_helper.py` to create a clearer intermediate image, then re-run analysis on that result.

## Core Workflow

1. Start from the original image path, a raw base64 string, or a data URI.
2. Apply the smallest transformation that is likely to remove the ambiguity.
3. Prefer semantic crop presets over manual coordinates unless the exact box is already known.
4. Return the processed image as a file or base64, then re-read that result.
5. If the image is still unclear, iterate once with a tighter crop or stronger zoom instead of stacking many edits at once.

## Quick Commands

```bash
# Rotate sideways text
python scripts/image_helper.py image.png --rotate 90 -o rotated.png

# Crop a likely area and zoom it
python scripts/image_helper.py image.png --crop-preset bottom-right --scale-preset x3 -o detail.png

# Improve low-contrast text
python scripts/image_helper.py image.png --auto-enhance -o enhanced.png

# Convert an existing file path directly to base64
python scripts/image_helper.py image.png --base64
```

## Choose the Next Action

- Text is sideways or upside down: use `--rotate`.
- Only one region matters: use `--crop-preset` first, then add `--scale-preset`.
- Small text or icons are hard to read: use `--scale-preset x2` or `x3`.
- Contrast is weak or edges are fuzzy: use `--auto-enhance`, or manually tune `--contrast` and `--sharpness`.
- Another tool needs inline image data instead of a file path: add `--base64`.
- The source image arrives as raw base64 or a data URI: use `--input-mode auto` or force `--input-mode base64` / `data-uri`.

## Input and Output Rules

- Accept a file path, raw base64 string, or data URI as input.
- Return a file with `-o` or return inline base64 with `--base64`.
- Allow passthrough output with no edits when the only goal is format conversion or path-to-base64 conversion.

## References

- Full CLI reference: `references/cli-reference.md`
- Crop and scale preset table: `references/presets.md`

## Prerequisite

Install Pillow if it is missing:

```bash
pip install Pillow
# or
uv pip install Pillow
```
