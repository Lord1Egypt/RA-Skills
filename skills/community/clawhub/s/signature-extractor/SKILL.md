---
name: signature-extractor
version: 1.0.0
description: >
  Extract clean, transparent-background signature ink from photos.
  Use when: user provides a photo of a handwritten signature and asks to remove the background, make signature transparent, upscale resolution, deepen/darken ink, or remove red stamps/seals.
  NOT for: general photo background removal (use remove.bg or similar), color signature ink extraction, or document scanning/OCR tasks.
user-invocable: true
metadata: { "openclaw": { "requires": { "bins": ["python3"], "anyBins": [] }, "emoji": "🖊️" } }
---

# Signature Extractor

Extract handwritten signature ink from photographs or scanned documents, producing a clean transparent-background PNG. Removes white/light backgrounds, red stamps/seals, and colored paper textures while preserving black ink strokes.

## When to Run

- User provides an image and asks to "remove background from signature", "make signature transparent", "extract signature", "remove stamp/印章"
- User asks to "darken signature ink", "make ink bolder", "填满笔迹", "加深签名"
- User asks to "upscale signature", "make signature clearer", "提高签名清晰度"
- User says "去掉底色", "去除背景", "签名透明", "提取签名", "去除印章"

## Workflow

1. Identify the user's desired mode from their request:

   | Request keywords | Mode | What it does |
   |---|---|---|
   | "填满", "加深", "实心", "加粗", "solid", default | `solid` | 3x upscale + sharpen + pure black opaque ink |
   | "高清", "放大", "清晰", "upscale", "hd" | `hd` | 3x upscale + sharpen + smooth alpha gradient |
   | "去掉底色", "提取", "简单去掉", "quick", "extract" | `extract` | Original size extraction with alpha gradient |

2. Run the extraction script:

   ```bash
   python3 {baseDir}/scripts/extract_signature.py INPUT_IMAGE OUTPUT.png --mode MODE [--scale N]
   ```

   - Default scale is 3 (for `solid` and `hd` modes). Adjust `--scale` if user specifies a different multiple.
   - Output is always RGBA PNG format.

3. After completion, report: output dimensions, ink pixel count, and share the result with the user.

## How It Works

The script isolates black ink using a three-channel color filter:

1. **Brightness filter** — pixels darker than a threshold are ink candidates
2. **Red channel filter** — R minus G must be less than 40, which excludes red stamps/seals
3. **Saturation filter** — low saturation ensures only true black/grey ink is captured, not colored marks

For `solid` and `hd` modes: LANCZOS upscaling → UnsharpMask sharpening → ink extraction → Alpha channel smoothing.

## Prerequisites

```bash
pip install Pillow numpy
```
