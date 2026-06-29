---
name: watermark-remover
description: "Remove watermarks from images using Florence-2 detection + IOPaint (LaMa) inpainting. Supports batch processing and manual/automatic modes."
---

# Watermark Remover

Automatically detect and remove watermarks (especially MLS watermarks) from listing photos using Florence-2 for detection and IOPaint (LaMa) for inpainting.

## Prerequisites

```bash
pip install iopaint transformers torch pillow
# Optional OCR fallback:
pip install paddleocr paddlepaddle
```

Models auto-download on first run (~560MB total): LaMa (~100MB) + Florence-2 (~460MB).

## Quick Start

```bash
# Single image
python ~/.openclaw/workspace/skills/watermark-remover/scripts/remove_watermark.py \
  --input photo.jpg --output photo_clean.jpg

# Batch directory
python ~/.openclaw/workspace/skills/watermark-remover/scripts/remove_watermark.py \
  --input ./photos/ --output ./photos_clean/ --suffix _clean
```

## Script: `remove_watermark.py`

- `--input` — file or directory
- `--output` — file or directory (created if missing)
- `--suffix` — append to output filenames (e.g. `_clean`)
- `--model` — `lama` (default), `mat`, `migan`, or `ldm`
- `--device` — `cpu`, `cuda`, or `mps` (auto-detected)
- `--confidence` — detection threshold 0.0–1.0 (default: 0.5)
- `--padding` — mask expansion in pixels (default: 10)
- `--dry-run` — detect only, skip inpainting
- `--preserve-exif` — copy EXIF metadata (default: on)

Supported: `.jpg`, `.jpeg`, `.png`, `.webp`, `.tiff`

## Pipeline

1. *Detect* — Florence-2 object detection (or PaddleOCR fallback) finds watermark regions
2. *Mask* — Generate binary mask with padding around detected boxes
3. *Inpaint* — IOPaint LaMa fills masked region with contextually appropriate pixels

## Model Selection

- *LaMa* (default) — Fast, excellent for small text watermarks. Handles ~90% of MLS watermarks.
- *MAT* — Same speed/quality, different artifacts. Try if LaMa isn't clean enough.
- *MIGAN* — Lightest (~30MB). For CPU-only or low-VRAM environments.
- *LDM* — Slow but highest quality. For complex textures (patterned carpet, wallpaper).

Start with `lama`. Switch to `ldm` only if LaMa leaves visible artifacts.

## Troubleshooting

- *Ghost text remains* — increase `--padding` or try `ldm`
- *Blurry patch* — switch to `ldm` for complex backgrounds
- *Watermark not detected* — lower `--confidence` to 0.3
- *OOM* — use `--device cpu` or `migan` model
- *Color mismatch* — add `--match-histograms` (IOPaint ≥1.5)

## Notes

- Original images never modified in-place
- Fully deterministic (LaMa is non-stochastic)
- MLS watermarks (VMLS, CRMLS, etc.) are ideal LaMa use case: small, corner-positioned, semi-transparent text

See `references/model-comparison.md` for detailed model benchmarks.
