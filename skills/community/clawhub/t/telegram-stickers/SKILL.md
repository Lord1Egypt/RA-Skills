---
name: telegram-stickers
description: Create Telegram stickers from images — static PNG stickers or animated WebM video stickers. Use when the user wants to make, process, or package Telegram stickers from photos or NFT art. Handles background removal, resizing to Telegram spec (512x512), animation (sway, bounce, shake), and upload. Knows exact @Stickers bot workflow for both static and video sticker packs.
---

# Telegram Stickers

## Specs (official — core.telegram.org)

| Type | Format | Resolution | Transparent | Max Duration | Max File |
|------|--------|-----------|-------------|-------------|---------|
| Static | PNG or WebP | 512×512 | Required | — | 512 KB |
| Video | WebM VP9 (yuva420p) | 512×512 | Required | 3 sec | 256 KB |
| Animated | TGS (Lottie) | 512×512 | Required | 3 sec | 64 KB |

> **TGS = vector only. Never attempt TGS from raster/PNG — impossible under 64KB compressed. Requires original layered vector artwork in After Effects. For NFT/photo art → use WebM video stickers.**

---

## Quickstart — One-Shot Script

For most requests, use `sticker.py` which handles the full pipeline in one command:

```bash
# Static PNG sticker
python3 scripts/sticker.py <image>

# Animated WebM sticker
python3 scripts/sticker.py <image> --animate sway    # gentle side-to-side
python3 scripts/sticker.py <image> --animate bounce  # energetic bounce
python3 scripts/sticker.py <image> --animate shake   # fast hype jitter

# Skip upload (local file only)
python3 scripts/sticker.py <image> --animate sway --no-upload
```

Output: `<name>_sticker.png` (static) or `<name>_<motion>.webm` + tmpfiles.org download URL (animated).

---

## Individual Scripts

Use these when you need fine-grained control or are processing in bulk.

### 1. Background removal + resize → PNG

```bash
python3 scripts/make_sticker.py <input_image> [output.png]
```

- Uses rembg u2net model (cached at `~/.u2net/u2net.onnx` after first run — ~170MB download)
- Crops to content → thumbnail to 512×512 → centers on transparent canvas → saves as PNG
- Warns if output exceeds 512KB

### 2. Generate animation frames

```bash
python3 scripts/animate_sway.py   <sticker.png> [--fps 24] [--duration 2.0] [--shift 18] [--angle 4] [--outdir frames_sway]
python3 scripts/animate_bounce.py <sticker.png> [--fps 24] [--duration 1.5] [--height 20] [--outdir frames_bounce]
python3 scripts/animate_shake.py  <sticker.png> [--fps 24] [--duration 1.0] [--intensity 10] [--outdir frames_shake]
```

Input must be a processed 512×512 transparent PNG (output of `make_sticker.py`).

### 3. Encode frames → WebM + upload

```bash
python3 scripts/make_webm.py <frames_dir> [output.webm] [--fps 24] [--duration 2.0] [--no-upload]
```

- Encodes VP9 WebM with transparent background (yuva420p)
- Validates duration ≤ 3s and size ≤ 256KB
- Auto-uploads to tmpfiles.org, prints direct download URL (expires ~1hr)
- **Do NOT add `-loop 0` — GIF flag, breaks WebM**

---

## Uploading to Telegram

After generating the file, upload via tmpfiles.org (already handled by `make_webm.py` / `sticker.py`):

```bash
curl -s -F "file=@sticker.png" https://tmpfiles.org/api/v1/upload
# Returns JSON → insert /dl/ after tmpfiles.org/ in the URL for direct download
```

See `references/stickers-bot-guide.md` for full @Stickers bot step-by-step.

**Key rule: always send sticker files to @Stickers bot as a Document, not a photo.** Telegram compresses photos to JPEG and destroys transparency.

---

## @Stickers Bot — Quick Reference

| Pack type | Bot command | File format |
|-----------|------------|-------------|
| Static | `/newpack` | PNG sent as Document |
| Video stickers | `/newvideo` | WebM sent as Document |

Static and video packs are **separate** — cannot mix types in one pack.

---

## Dependencies

```bash
pip install "rembg[cpu]" Pillow numpy
# ffmpeg with libvpx-vp9 (system-wide install)
```

`sticker.py` runs a dependency check on startup and prints install hints if anything is missing.
