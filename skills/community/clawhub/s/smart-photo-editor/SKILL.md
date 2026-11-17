---
name: smart-photo-editor
license: MIT
description: |
  AI-powered photo editing and restoration skill - smart object removal, background removal, old photo restoration, and basic edits.

metadata:
  author: Team
  version: "1.5.1"
  category: ai/image-editing
  compatibility: Requires Node.js 18+ and network access to VolcEngine Ark API (with Seedream model enabled) for AI features.
---

# Smart Photo Editor Skill

AI-powered photo editing and restoration skill for OpenClaw. Unifies Seedream (AI edits), ImageMagick (basic edits), and OpenCV (programmatic fixes) into one intuitive workflow.

## Overview

All-in-one intelligent photo editing skill - automatically selects the best tool for each image processing task.

✨ **Key Advantages:**
- ✅ **Smart Tool Selection** - Automatically chooses Seedream / ImageMagick / OpenCV based on task
- ✅ **Unified Interface** - All operations use the same calling pattern
- ✅ **Bilingual Support** - Optimized prompts for both Chinese and English contexts
- ✅ **Automatic Fallback** - Switches to backup tools if primary tool fails
- ✅ **Large Image Auto-Handling** - Avoids "image too large" API errors

## Feature Availability

This skill provides two tiers of functionality:

### ✅ Works out of the box (no extra dependencies)

These features only require ImageMagick and/or OpenCV (both widely available on Linux/macOS):

- **Resize / Crop / Smart-crop** — dimension changes, aspect-ratio-preserving scaling
- **Color adjustment** — brightness, contrast, saturation, grayscale
- **Perspective correction** — 4-point skew/warp correction
- **Smart compression** — quality targeting, binary-search for target file size
- **HDR tonemapping** — log/bilateral/shadow/highlight recovery
- **Background removal (basic)** — solid-color background removal via ImageMagick
- **Geometric inpainting** — wire/line/rect removal with known coordinates (`inpaint.py`)

### 🔒 Requires Seedream skill (AI features)

These features require the `byted-ark-seedream-skill` (VolcEngine Ark Agent Plan, managed skill):

- **Object removal (natural language)** — remove objects described in text (people, vehicles, watermarks)
- **Old photo restoration** — AI scratch/dust/fading repair
- **Scene replacement (`replace-scene`)** — put subject into a new scene via multi-reference fusion
- **Background removal (AI)** — rembg-based, or Seedream-based for complex edges

> **Note:** The `byted-ark-seedream-skill` is an OpenClaw managed skill that requires a VolcEngine Ark account with the Seedream model enabled. Install with `openclaw skills install byted-ark-seedream-skill`.

---

## Trigger Conditions

Activates automatically when users mention keywords like:
- photo editing, edit image, retouch, smart photo edit
- remove object, delete object, erase, remove person, remove watermark, remove logo, 去除, 消除
- remove background, background removal, cutout, 抠图, 换背景
- restore, fix, old photo restoration, repair, 修复老照片, 老照片修复
- portrait retouching, portrait edit, smooth skin, whiten teeth, enhance eyes, remove blemish, red eye, 美颜, 人像精修, 红眼
- replace scene, change scene, put subject in, 换场景, 多图融合
- color adjustment, color correction, color grading, brightness, 调色, 色彩调整
- crop, resize, compress, auto crop, smart crop, 裁剪, 自动裁剪, 智能裁剪
- perspective, fix skew, flatten, perspective correct, 透视矫正, 视角矫正
- hdr, tonemap, highlight recovery, shadow recovery, 高动态, 阴影增强
- sharpen, denoise, 锐化, 降噪

---

## Tool Selection Policy

The skill mixes three classes of tool. Picking the right one for each task is
what makes the unified entry-point useful, so the routing is explicit:

**Use Seedream first for semantic / generative edits.**
- Object removal in complex scenes (people, vehicles, watermarks, signs)
- Old-photo restoration (scratches, fading, color loss)
- Background replacement / scene swap
- Subjective enhancement: “make this look better / natural / cinematic”
- Edits where the model must infer missing visual content
- Natural-language requests, especially in Chinese

For these, Seedream is the value-add. OpenCV/ImageMagick can’t compete on
quality, and a deterministic tool can’t “invent” plausible content.

**Use deterministic tools first for mechanical edits.**
- Resize, crop, format conversion
- Compression / quality targeting
- Brightness, contrast, saturation, gamma adjustments
- Geometric inpainting when coordinates are known (wires, dust spots,
  exact rectangles — call `inpaint.py` directly)
- Batch operations where reproducibility matters

For these, Seedream would be slower, costlier, and less predictable.

**Encoded policy (auto mode):**
```text
semantic edit / restoration / object removal       → Seedream first; deterministic fallback
mechanical edit / resize / crop / compress / color → deterministic tools first
user explicitly asks for AI / natural restoration  → Seedream
user explicitly forces a tool with --tool ...      → honored verbatim
```

**Per-task defaults (`--tool auto`):**

| Task | Default | Notes |
|------|---------|-------|
| `remove-object` | **Seedream** | OpenCV branch only fires when Seedream is unavailable; redirects to `inpaint.py` for known-geometry cases |
| `restore` | **Seedream** | Seedream-only operation by design |
| `remove-background` | **rembg** | ImageMagick fallback for solid-color backgrounds when rembg is missing |
| `resize` / `crop` / `color-adjust` | **OpenCV/ImageMagick** | Deterministic, instant, free |
| `smart-compress` | **OpenCV** | Content-aware quality + format selection |
| `perspective-correct` | **OpenCV** | Document/whiteboard correction |
| `hdr-tonemap` | **OpenCV** | All four modes (auto / bilateral / log / shadows) are deterministic |
| `replace-scene` | **Seedream** | AI-only; no deterministic fallback (would produce poor results). If Seedream is unavailable, returns error directing user to install the Seedream skill. |

Override with `--tool seedream | opencv | imagemagick | rembg`.

---

## Installation & Dependencies

### Standard Installation Path
`~/.openclaw/skills/smart-photo-editor/`

### Python Interpreter
All Python scripts (`scripts/*.py`) use a portable `#!/usr/bin/env python3` shebang.

You can run them directly:

```bash
./scripts/edit.py --help
```

Or explicitly with your Python of choice (e.g. a virtualenv where you have
installed the dependencies below):

```bash
python3 scripts/edit.py --help
```

**Make sure the Python interpreter you use has the required dependencies**
(OpenCV, Pillow, NumPy). Optional deps (`piexif`, `exif`, `rembg`) add extra
features; the skill will gracefully skip those features if they are missing.

```bash
# Sanity check — required deps\python3 -c "import cv2, numpy, PIL; print('core deps ok')"

# Sanity check — full deps (includes optional rembg/piexif/exif)
python3 -c "import cv2, numpy, PIL, piexif, exif, rembg; print('all deps ok')"
```

### Required & Optional Dependencies
| Dependency | Required | Purpose | Installation |
|------------|----------|---------|--------------|
| **byted-ark-seedream-skill** | ✅ Required | AI object removal, old photo restoration, image-to-image editing | Requires VolcEngine Ark API access. Follow [official setup guide](https://www.volcengine.com/docs/82379/2375486) to enable Seedream model access |
| **imagemagick** | ✅ Required | Basic image editing (resize, crop, format conversion, color adjustments) | `sudo apt install imagemagick` (Debian/Ubuntu) or `brew install imagemagick` (macOS) |
| **opencv-python-headless** | ✅ Required | Wire removal, spot removal, image resizing | `pip install opencv-python-headless` |
| **rembg** | ⚠️ Optional | AI-powered background removal (better results for complex scenes) | `pip install rembg` |
| **piexif** | ⚠️ Optional | EXIF metadata preservation during edits | `pip install piexif` |
| **exif** | ⚠️ Optional | Extended EXIF tag reading | `pip install exif` |

### Install Optional Dependencies
```bash
source ~/.openclaw/venv-clawd/bin/activate
pip install rembg piexif exif
```

### Cloudflare R2 Upload (Large Reference Images)

When a reference image (subject or scene image) exceeds **1.5 MB**, the skill can upload it to Cloudflare R2 instead of embedding it as a base64 data URI. This avoids hitting Seedream API payload size limits.

**R2 is optional.** Without configuration, large images fall back to base64 data URI (which may fail for very large files due to CLI argument limits).

**To enable R2 upload, deploy your own Cloudflare Worker:**

1. Create a Cloudflare R2 bucket and a Worker that accepts PUT requests (see the [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/))
2. Set the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `SEEDREAM_UPLOAD_TOKEN` | ✅ Yes | Bearer token for your R2 upload worker. |
| `SEEDREAM_UPLOAD_WORKER_URL` | ✅ Yes | Your worker URL, e.g. `https://your-worker.your-subdomain.workers.dev`. |

```bash
# Add to your shell profile or ~/.openclaw/.env
export SEEDREAM_UPLOAD_TOKEN="your-token-here"
export SEEDREAM_UPLOAD_WORKER_URL="https://your-worker.your-subdomain.workers.dev"
```

Without both variables, large images gracefully fall back to the data URI path (works for most cases; may hit CLI arg limits for very large multi-image batches).

### VolcEngine Ark Setup
For AI editing features (object removal, photo restoration), ensure:
1. You have a VolcEngine Ark account with API access
2. The Seedream (豆包生图) model is enabled for your account
3. Your OpenClaw configuration has valid VolcEngine API credentials

See the [official VolcEngine Ark documentation](https://www.volcengine.com/docs/82379/2375486) for detailed setup instructions.

---

## Core Features & Implementation

### 1. Object Removal
**Primary Tool:** Seedream Image-to-Image  
**Fallback Tool:** OpenCV Inpainting (small scratches/lines)

**Usage:**
```bash
# AI method (recommended) - complex scenes
image_generate \
  model="byted-ark-seedream-skill" \
  mode="image-to-image" \
  image="/path/to/photo.jpg" \
  reference_strength=0.85 \
  prompt="Remove the [object description] located at [location description]. Restore the seamless texture, keep everything else exactly the same."
```

**OpenCV method** — simple lines/minor imperfections:
```bash
# Remove horizontal wire
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type wire --y 760 --thickness 10

# Remove diagonal/angled line (supports any angle)
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type line --x1 100 --y1 200 --x2 500 --y2 400 --thickness 3

# Remove rectangular region (watermarks, logos, text)
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type rect --x 50 --y 50 --w 400 --h 80 --feather 5

# Remove multiple sensor dust spots in one command
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type spots --spots "100,150,8;200,300,10;50,400,6"

# Remove multiple lines in one command
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type lines --lines "0,100,800,100,3;100,200,500,400,5"

# Batch processing from JSON config
./scripts/inpaint.py /path/to/photo.jpg /path/to/output.jpg \
  --type batch --batch tasks.json

# JSON config example (tasks.json):
# {
#   "operations": [
#     {"type": "spot", "x": 100, "y": 150, "radius": 8},
#     {"type": "spot", "x": 200, "y": 300, "radius": 10},
#     {"type": "wire", "y": 500, "thickness": 5},
#     {"type": "rect", "x": 50, "y": 50, "w": 200, "h": 50, "feather": 10}
#   ]
# }
```

**Algorithm Selection:**
- `ns` (Navier-Stokes) - Better for textures and larger regions (default for wire/line)
- `telea` (Telea) - Faster, better for small regions (default for spot)
Use `--algo ns` or `--algo telea` to override the default selection.

**Prompt Optimization Examples:**
- "Remove the black power cable at the bottom of the image" → "Remove the thin black horizontal power cable at the bottom 20% of the image. Restore the mountain texture seamlessly, keep everything else exactly the same."
- "Remove the pedestrian in the middle" → "Remove the pedestrian in the center. Fill with matching background texture naturally."

---

### 2. Background Removal
**Primary Tool:** rembg (AI)  
**Fallback Tool:** ImageMagick (inline – solid color backgrounds)

**Usage:**
```bash
# rembg AI method (complex backgrounds)
rembg i input.jpg output.png

# ImageMagick method (solid color backgrounds)
./scripts/remove_bg.sh input.png output.png 20 "#FFFFFF"
```

---

### 3. Old Photo Restoration
**Primary Tool:** Seedream Image-to-Image

**Usage:**
```bash
image_generate \
  model="byted-ark-seedream-skill" \
  mode="image-to-image" \
  image="/path/to/old_photo.jpg" \
  reference_strength=0.7 \
  prompt="Restore this old photo. Remove all scratches, dust spots, and damage. Enhance clarity and contrast. Restore natural, vivid colors while preserving the original photo's character. Do not change the composition or subjects."
```

---

### 4. Basic Editing
**Primary Tool:** ImageMagick + OpenCV

**Common Commands:**
```bash
# Resize
convert input.jpg -resize 1920x1920\> output.jpg

# Crop
convert input.jpg -crop 800x600+100+50 output.jpg

# Format conversion + compression
convert input.png -quality 85 output.webp

# Color adjustment
convert input.jpg -brightness-contrast 10x5 output.jpg  # Brighter, higher contrast
convert input.jpg -modulate 100,130,100 output.jpg      # Increase saturation
convert input.jpg -grayscale Rec709Luma output.jpg      # Convert to B&W
```

**OpenCV Operations (inpaint.py):**
```bash
# Denoise (reduce noise in low-light photos)
./scripts/inpaint.py input.jpg output.jpg --type denoise --strength 15

# Sharpen (enhance edges and focus)
./scripts/inpaint.py input.jpg output.jpg --type sharpen --strength 1.5

# Brightness/contrast/gamma adjustment
./scripts/inpaint.py input.jpg output.jpg --type adjust --brightness 15 --contrast 10 --gamma 0.9
```

### 5. Portrait Retouching
**Primary Tool:** OpenCV (face detection + image processing)  
**Dependencies:** `opencv-python-headless` (already required)

Portrait retouching provides face-aware enhancements for portrait photography:
- **Skin smoothing** — bilateral filter preserves edges while softening skin
- **Red-eye removal** — detects and corrects flash red-eye
- **Teeth whitening** — targets lower-face region, preserves surrounding
- **Eye enhancement** — brightens and sharpens eyes
- **Face brightness/contrast** — applies adjustments only to detected face
- **Blemish removal** — removes small spots using inpainting
- **Skin tone enhancement** — warm, healthy color correction

```bash
# Skin smoothing only
./scripts/portrait.py input.jpg output.jpg --smooth 3

# All enhancements (balanced)
./scripts/portrait.py input.jpg output.jpg --all

# Subtle preset (conservative)
./scripts/portrait.py input.jpg output.jpg --subtle

# Custom combination
./scripts/portrait.py input.jpg output.jpg \
  --smooth 2 --enhance-eyes --whiten-teeth 0.3 --brightness 10

# JSON output
./scripts/portrait.py input.jpg output.jpg --all --json
```

| Parameter | Description |
|-----------|-------------|
| `--smooth` | Skin smoothing strength 1-10 |
| `--denoise` | Denoise strength 1-30 |
| `--red-eye` | Remove flash red-eye |
| `--whiten-teeth` | Teeth whitening strength 0.1-0.8 |
| `--enhance-eyes` | Brighten/sharpen eyes |
| `--brightness` | Face brightness -100 to 100 |
| `--contrast` | Face contrast -100 to 100 |
| `--gamma` | Face gamma correction 0.1-3.0 |
| `--sharpen` | Sharpening strength 0.5-3.0 |
| `--blemish-removal` | Remove small blemishes |
| `--skin-tone` | Warm skin tone enhancement |
| `--all` | Apply all enhancements (balanced) |
| `--subtle` | Conservative all enhancements |
| `--no-auto-detect` | Skip face/eye detection |
| `--no-exif` | Do not preserve EXIF |
| `--json` | JSON output mode |

### 6. EXIF Preservation
**Automatic:** All write operations preserve EXIF metadata by default  
**Tool:** `scripts/exif_utils.py` — standalone EXIF utility

All editing scripts automatically preserve EXIF metadata from input to output.

```bash
# Read EXIF from an image
./scripts/exif_utils.py read photo.jpg

# Strip EXIF from an image
./scripts/exif_utils.py strip photo.jpg -o output.jpg

# Copy EXIF from one image to another
./scripts/exif_utils.py copy source.jpg dest.jpg
```

Supported tags: Make, Model, DateTime, Orientation, Exposure Time, F-Number, ISO, Focal Length, Lens Model, and more.

---

### 7. Smart Crop (Auto-Crop)
**Primary Tool:** OpenCV saliency detection + optional GrabCut refinement  
**Dependencies:** `opencv-python-headless` (already required)

Automatically detects the most "interesting" region in an image and crops to it.
Uses OpenCV's StaticSaliencyFineGrained algorithm by default, with spectral and edge-based fallbacks.

```bash
# Auto-crop to salient region with default padding
./scripts/smart_crop.py input.jpg output.jpg

# Crop to specific aspect ratio
./scripts/smart_crop.py input.jpg output.jpg --aspect 16/9

# Crop to 4:3 with 10% margin around subject
./scripts/smart_crop.py input.jpg output.jpg --aspect 4/3 --padding 0.1

# Resize to exact dimensions after smart crop
./scripts/smart_crop.py input.jpg output.jpg --width 800 --height 600

# Use GrabCut refinement for cleaner boundaries
./scripts/smart_crop.py input.jpg output.jpg --grabcut

# Generate debug saliency map overlay
./scripts/smart_crop.py input.jpg output.jpg --debug
```

| Parameter | Description |
|-----------|-------------|
| `--aspect`, `-a` | Aspect ratio (e.g. `16/9`, `4/3`, `1/1`) |
| `--width`, `-w` | Target width in pixels |
| `--height`, `-H` | Target height in pixels |
| `--padding`, `-p` | Margin around subject (0.0-0.5, default 0.05) |
| `--threshold`, `-t` | Saliency threshold 0.05-0.95 (default 0.3) |
| `--algorithm` | `auto` / `finegrained` / `spectral` / `edge` |
| `--grabcut`, `-g` | Use GrabCut to refine crop boundary |
| `--debug`, `-d` | Generate debug saliency map overlay |

### 8. Perspective Correction
**Primary Tool:** OpenCV (auto-detection + warpPerspective)

Auto-detects document/sheet borders using edge detection + contour analysis and corrects perspective distortion. Also supports manual corner specification.

```bash
# Auto-detect and correct
./scripts/edit.py --task perspective-correct --image doc.jpg --output flat.jpg

# With manual corners (top-left, top-right, bottom-right, bottom-left)
./scripts/edit.py --task perspective-correct --image doc.jpg --output flat.jpg \
  --corners "100,50,600,50,600,800,100,800"

# Batch JSON
./scripts/edit.py --json < tasks.json
```

| Parameter | Description |
|-----------|-------------|
| `--corners` | 4 points as CSV `x1,y1,x2,y2,x3,y3,x4,y4` (TL,TR,BR,BL). Omit for auto-detection |

**Algorithm:** Adaptive threshold → contour detection → largest 4-point quadrilateral → perspective transform.

---

### 9. Intelligent Compression
**Primary Tool:** OpenCV (content analysis + format-specific encoding)

Content-aware image compression using entropy, edge density, and color variance analysis to auto-select the best format and quality.

```bash
# Auto-select best format and quality
./scripts/edit.py --task smart-compress --image photo.jpg --output optimized.jpg

# Target file size (auto binary-searches quality)
./scripts/edit.py --task smart-compress --image photo.jpg --output optimized.jpg --target-kb 200

# Force WebP with specific quality
./scripts/edit.py --task smart-compress --image photo.jpg --output optimized.webp \
  --format webp --quality 85

# Batch JSON
./scripts/edit.py --json < tasks.json
```

| Parameter | Description |
|-----------|-------------|
| `--target-kb` | Target output size in KB (enables binary-search for optimal quality) |
| `--format` | Force output: `jpeg` | `png` | `webp` |

**Auto-decision logic:**
- **JPEG** — high entropy (>6.5) + dense edges → complex photographic content
- **PNG** — low color variance (<500) + low edges → flat graphics/screenshots; or alpha channel detected
- **Quality** — auto-selected based on entropy (65–92) unless `--target-kb` is specified

---

### 10. HDR / Tonemapping
**Primary Tool:** OpenCV (multi-scale bilateral decomposition + CLAHE)

HDR-style tone mapping to enhance dynamic range on single images. Uses bilateral filter decomposition to separate illumination from detail, compress the illumination layer's dynamic range, then recombine — producing natural-looking highlight/shadow recovery.

```bash
# Auto mode (default — picks best method based on image analysis)
./scripts/edit.py --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg

# Bilateral mode — detail-preserving compression (best for most photos)
./scripts/edit.py --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode bilateral --strength 1.2

# Log mode — fast global compression (good for screenshots/graphics)
./scripts/edit.py --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode log --gamma 2.2

# Shadows mode — lighten dark regions (backlit photos)
./scripts/edit.py --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode shadows --strength 1.5

# Highlight mode — compress blown highlights
./scripts/edit.py --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode highlight --strength 1.2
```

| Parameter | Description |
|-----------|-------------|
| `--mode` | auto / bilateral / log / shadows / highlight (default: auto) |
| `--strength` | Enhancement strength 0.1-2.0 (default: 1.0) |
| `--gamma` | Gamma value for log mode (default: 2.2) |

**Algorithm:** Bilateral filter decomposition — base (illumination) layer compressed with S-curve; detail layer preserved and boosted; adaptive saturation adjustment.

---

### 11. Scene Replacement
**Primary Tool:** Seedream multi-reference image fusion (AI-only, no deterministic fallback)

Place a subject (portrait / pet / product) into a new scene using Seedream's
multi-reference image fusion. Wraps 豆包 app's "多图融合" + "换场景" feature.

**Requires:** the `byted-ark-seedream-skill` (this task is AI-only; an
OpenCV/ImageMagick fallback would produce poor results and is intentionally
omitted).

**Usage:**
```bash
# 1) Subject + scene image (most common)
./scripts/edit.py --task replace-scene \
    --subject photo.jpg --scene cafe.png --output out.jpg

# 2) Subject + text-only scene description
./scripts/edit.py --task replace-scene \
    --subject pet.jpg --scene-prompt "阳光下的草地" --output out.jpg

# 3) Product photo into lifestyle scene
./scripts/edit.py --task replace-scene \
    --subject product.png --scene lifestyle.jpg --output out.jpg \
    --subject-type product

# 4) Custom prompt override (full artistic control)
./scripts/edit.py --task replace-scene \
    --subject portrait.jpg --scene beach.jpg --output out.jpg \
    --prompt "把人物放在黄昏海边沙滩，长发随风，光线偏暖，景深虚化"

# 5) Subject in center, close-up framing
./scripts/edit.py --task replace-scene \
    --subject portrait.jpg --scene studio.jpg --output out.jpg \
    --position center --scale close

# 6) Full-body shot, subject on the right
./scripts/edit.py --task replace-scene \
    --subject portrait.jpg --scene beach.jpg --output out.jpg \
    --position right --scale full

# 7) JSON batch with position/scale
./scripts/edit.py --json < tasks.json
```

**Argument table:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--subject` / `-S` | path | ✅ | — | Subject image (portrait / pet / product) |
| `--scene` | path | ⚠️ one of | — | Target scene image |
| `--scene-prompt` | string | ⚠️ one of | — | Target scene text description (used if no scene image) |
| `--subject-type` | enum | ❌ | `auto` | `auto` / `portrait` / `pet` / `product`. Selects prompt template + reference_strength. |
| `--prompt` / `-p` | string | ❌ | (from template) | Override the default prompt |
| `--reference-strength` | float | ❌ | 0.85 (portrait/pet) / 0.90 (product) | How strongly Seedream must preserve the subject. Higher = stricter. |
| `--watermark` | flag | ❌ | `false` | Add Seedream watermark. Default OFF (most uses are product / academic). |
| `--position` | enum | ❌ | `center` | Horizontal subject placement: `left` / `center` / `right`. Feeds into the scene-prompt as positional hint.
| `--scale` | enum | ❌ | `medium` | Subject framing: `close` (特写) / `medium` (中景) / `full` (全身). Feeds into the scene-prompt as framing hint.
| `--output-format` | enum | ❌ | follow subject | `jpeg` / `png` / `webp` |
| `--output` / `-o` | path | ❌ | auto | Output path |

**Validation rules:**
- `--subject` is required.
- **Exactly one** of `--scene` / `--scene-prompt` is required (both → error).
- If `--scene-prompt` is given, it must be at least 3 characters.
- Subject image is auto-resized to 2048px max side (existing API limit helper).

**Subject-type auto-detection:**
When `--subject-type auto` is passed (default), the skill uses two heuristics:
1. **Filename keyword** — `pet/cat/dog/...` → `pet`; `portrait/selfie/face/...` → `portrait`; `product/item/bottle/...` → `product`
2. **Corner solidity check** — if all 4 corners are within 15 RGB units, classified as `product` (typical product shot on flat backdrop)

If neither heuristic matches, falls back to `portrait` (most common case).
For certainty, always pass `--subject-type` explicitly.

**JSON batch format:**
```json
{
  "operations": [
    {"task": "replace-scene", "subject": "p1.jpg", "scene": "office.jpg",
     "output": "p1_office.jpg", "subject-type": "portrait"},
    {"task": "replace-scene", "subject": "p2.jpg", "scene-prompt": "雪山日落",
     "output": "p2_mountain.jpg", "subject-type": "portrait"},
    {"task": "replace-scene", "subject": "shoe.png", "scene": "running_track.jpg",
     "output": "shoe_track.jpg", "subject-type": "product", "reference-strength": 0.9}
  ]
}
```

**JSON batch key naming:** JSON keys use **underscores** (Python identifier
convention): `scene_prompt`, `subject_type`, `reference_strength`, etc. The
CLI flags use dashes (`--scene-prompt`, `--subject-type`). The skill
**automatically normalizes** dashed JSON keys to underscored ones, so both
work; use whichever is more natural for your tooling.

**Output:**
The result JSON envelope includes a `generation_time_s` field (extracted from
Seedream's own metadata) for quota tracking.

---

## Unified API Interface

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `task` | string | - | ✅ | Task type: `remove-object` / `remove-background` / `restore` / `resize` / `crop` / `color-adjust` / `perspective-correct` / `smart-compress` / `hdr-tonemap` / `replace-scene` |
| `image` | string | - | ✅ | Input image path |
| `prompt` | string | "" | ❌ | Object description/location (required for remove-object) |
| `tool` | string | "auto" | ❌ | Force specific tool: `auto` / `seedream` / `imagemagick` / `opencv` / `rembg` |
| `output_format` | string | "jpeg" | ❌ | Output format: jpeg / png / webp |
| `quality` | integer | 95 | ❌ | Output quality (0-100) |

---

## Intelligent Decision Flow

```
User request → Analyze task type
    ↓
Object removal? → Seedream (default) → Failed? → OpenCV fallback
    ↓
Background removal? → Detect background → Solid? ImageMagick : rembg
    ↓
Old photo restoration? → Seedream (reference_strength=0.7)
    ↓
Basic editing? → ImageMagick
```

---

## Examples

### Remove Power Cable
```
Task: Remove the black power cable at the bottom of the image
Parameters:
  task: remove-object
  image: mountain.jpg
  prompt: "Remove the thin black horizontal power cable at the bottom 20% of the image. Restore the mountain texture seamlessly, keep everything else exactly the same."
  tool: seedream
```

### Old Photo Restoration
```
Task: Restore this old photo
Parameters:
  task: restore
  image: old_photo.jpg
  prompt: "Remove scratches and dust spots, enhance clarity, restore natural colors"
```

### Background Removal
```
Task: Remove background from portrait photo
Parameters:
  task: remove-background
  image: portrait.jpg
  tool: auto
```

### Portrait Retouching
```bash
# Apply all portrait enhancements
./scripts/portrait.py input.jpg output.jpg --all

# Subtle skin smoothing and eye enhancement
./scripts/portrait.py input.jpg output.jpg --smooth 2 --enhance-eyes
```

---

## Error Handling & Fallbacks

1. **Seedream API failure** → surface the Seedream error verbatim; for known-geometry cases use `scripts/inpaint.py` directly (`--type spot/wire/rect`) or pass `--tool opencv` to get the inpaint.py guidance message.
2. **Seedream skill unavailable / `--tool opencv`** → `op_remove_object` returns an actionable redirect listing common `inpaint.py` invocations.
3. **Image too large** → Auto-resize to 2048px max side, process, output.
4. **rembg not installed** → Auto-fallback to ImageMagick remove-bg.
5. **Unsupported format** → Auto-convert to JPEG for processing.

---

## Large Image Handling Strategy

- Seedream API limit: ~2048px maximum side length
- Auto-detect image dimensions, if exceeded:
  1. Proportionally resize to 2048px max side
  2. Perform editing operation
  3. Output processed image
- Prevents "image too large" errors

---

## Skill File Structure

```
smart-photo-editor/
├── SKILL.md              # This file
├── README.md             # Quick start guide
├── scripts/
│   ├── edit.py           # ⭐ Unified CLI entry point (all operations)
│   ├── inpaint.py        # OpenCV wire/spot/line/rect/denoise/sharpen/adjust
│   ├── portrait.py        # Portrait retouching (skin, eyes, teeth, etc.)
│   ├── smart_crop.py     # Smart auto-crop based on saliency detection
│   ├── exif_utils.py     # EXIF read/strip/copy utility
│   └── remove_bg.sh      # Background removal wrapper
└── examples/             # Before/after comparison examples
```

---

## Unified CLI (`edit.py`)

The recommended entry point for all photo editing operations.

```bash
# Object removal (AI)
./scripts/edit.py --task remove-object --image photo.jpg \
  --prompt "Remove the person in the center" --output out.jpg

# Old photo restoration
./scripts/edit.py --task restore --image old_photo.jpg --output restored.jpg

# Background removal
./scripts/edit.py --task remove-background --image portrait.png --output no_bg.png

# Resize
./scripts/edit.py --task resize --image photo.jpg --output small.jpg --width 800

# Crop
./scripts/edit.py --task crop --image photo.jpg --output crop.jpg \
  --x 100 --y 100 --width 400 --height 300

# Color adjustment
./scripts/edit.py --task color-adjust --image photo.jpg --output bright.jpg \
  --brightness 20 --saturation 30

# Batch mode (JSON)
./scripts/edit.py --json < batch_tasks.json
```

### Unified Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--task` | string | **required** | Operation: `remove-object`, `restore`, `remove-background`, `resize`, `crop`, `color-adjust`, `perspective-correct`, `smart-compress`, `hdr-tonemap` |
| `--image` / `-i` | string | **required** | Input image path |
| `--output` / `-o` | string | auto | Output path (default: `{input}.{task}{ext}`) |
| `--prompt` / `-p` | string | - | Description for AI operations |
| `--tool` / `-t` | string | `auto` | Force tool: `auto`, `seedream`, `opencv`, `imagemagick`, `rembg` |
| `--width` / `-w` | int | - | Target width (resize/crop) |
| `--height` / `-H` | int | - | Target height (resize/crop) |
| `--max-dim` | int | - | Max dimension, maintains aspect (resize) |
| `--x`, `--y` | int | - | Offset for crop |
| `--brightness` | float | - | Brightness: -100 to 100 |
| `--contrast` | float | - | Contrast: -100 to 100 |
| `--saturation` | float | - | Saturation: -1 to 1 |
| `--grayscale` | flag | false | Convert to grayscale |
| `--corners` | string | - | Perspective corners: `x1,y1,x2,y2,x3,y3,x4,y4` (TL,TR,BR,BL) |
| `--target-kb` | int | - | Target file size in KB (smart-compress quality search) |
| `--format` | string | - | Output format: `jpeg` \| `png` \| `webp` |
| `--mode` | string | auto | HDR tonemap mode: auto / bilateral / log / shadows / highlight |
| `--strength` | float | 1.0 | Enhancement strength 0.1-2.0 (hdr-tonemap) |
| `--gamma` | float | 2.2 | Gamma value for log mode (hdr-tonemap) |
| `--quality` | int | auto | Output quality 1-100 (jpeg/webp; ignored when `--target-kb` is set) |
| `--position` | string | - | Horizontal placement for `replace-scene`: `left` / `center` / `right` |
| `--scale` | string | - | Framing for `replace-scene`: `close` / `medium` / `full` |
| `--subject` / `-S` | string | - | Subject image path (required for `replace-scene`) |
| `--scene` | string | - | Scene image path (one of `--scene` or `--scene-prompt` for `replace-scene`) |
| `--scene-prompt` | string | - | Scene text description (one of `--scene` or `--scene-prompt` for `replace-scene`) |
| `--subject-type` | string | `auto` | Subject type for `replace-scene`: `auto` / `portrait` / `pet` / `product` |
| `--reference-strength` | float | 0.85 | How strongly Seedream preserves the subject |
| `--watermark` | flag | false | Add Seedream watermark (default OFF) |
| `--json` | flag | false | Emit JSON result envelope on stdout. Combine with `--batch` (or piped stdin) for JSON batch input. |
| `--batch` / `-b` | string | - | JSON file for batch operations |

### JSON Batch Format

```json
{
  "operations": [
    {"task": "remove-object", "image": "a.jpg", "prompt": "Remove the person", "output": "a_out.jpg"},
    {"task": "restore", "image": "b.jpg", "output": "b_out.jpg"},
    {"task": "resize", "image": "c.jpg", "output": "c_small.jpg", "width": 800}
  ]
}
```

---

## Changelog

### 1.5.0 — 2026-07-19

**New `replace-scene` parameters**
- `--position {left,center,right}` — controls horizontal placement of the subject in the generated scene. Feeds into the scene-prompt as a positional hint so Seedream places the subject accordingly.
- `--scale {close,medium,full}` — controls subject framing (特写/中景/全身). Feeds into the scene-prompt as a framing hint.

**R2 large-file upload for Seedream reference images**
- When a reference image exceeds 1.5 MB, the skill can upload to Cloudflare R2 and pass the public URL to Seedream instead of embedding a base64 data URI.
- Requires self-deployed Cloudflare R2 Worker + `SEEDREAM_UPLOAD_TOKEN` and `SEEDREAM_UPLOAD_WORKER_URL` env vars.
- Without R2 configured, large images gracefully fall back to base64 data URI.

### 1.4.0 — 2026-07-14

**New feature: `replace-scene` task**
Adds a new AI-driven task that places a subject (portrait / pet / product) into
a new scene using Seedream's multi-reference image fusion. Wraps 豆包 app's
"多图融合" + "换场景" feature.
- New `--subject` (alias of `--image` for this task) + mutually-exclusive
  `--scene` (image) or `--scene-prompt` (text) input pair.
- `--subject-type {auto,portrait,pet,product}` selects a per-type prompt
  template and reference_strength. `auto` uses filename keyword + corner
  solidity heuristics.
- `--watermark` defaults to OFF (most uses are product / academic).
- New `_call_seedream(reference_images=...)` parameter — passes a JSON array
  of data URIs to Seedream (which accepts up to 14 reference images).
- Subject image is auto-resized to 2048px max side; temp files are cleaned up.
- Returns `info.generation_time_s` extracted from Seedream's metadata for
  quota tracking.

**Bug fixes (incidental, surfaced by v1.4.0 testing)**
- `process_batch` now normalizes dashed JSON keys (`scene-prompt` →
  `scene_prompt`, `target-kb` → `target_kb`, `subject-type` → `subject_type`,
  `no-maintain-aspect` → `no_maintain_aspect`) before unpacking into
  `process(**op)`. Previously these were silently dropped into the trailing
  `**kwargs` and the real parameter received its default — a very confusing
  failure mode (especially for `target-kb` where the result was a wildly
  different file size than requested).
- `process()` now translates `no_maintain_aspect=True` (from JSON batch) to
  `maintain_aspect=False` (the inverted semantics the `op_resize` function
  expects), mirroring the same translation `main()` does for the CLI.

**Docs**
- New section 11 "Scene Replacement" with 6 worked examples, full argument
  table, validation rules, auto-detection logic, and JSON batch format.
- Updated Tool Selection Policy + Per-task defaults tables to include
  `replace-scene`.
- Updated Unified API Interface task list.

### 1.3.4 — 2026-07-14

**ImageMagick argument fix**
- `op_resize` / `op_crop` / `op_color_adjust` / `op_remove_background` (ImageMagick fallback): all ImageMagick CLI arguments are now passed as separate list elements instead of single space-joined strings. Previously ImageMagick would reject commands like `-resize 800x800>` because the flag and value were concatenated into one string.

**HDR bilateral saturation fix**
- `_tonemap_bilateral` no longer performs a pseudo-HSV operation directly on BGR channels (which corrupted colors). Now uses proper `cv2.cvtColor(BGR→HSV)` → boost saturation → `cv2.cvtColor(HSV→BGR)`.

**Background removal fallback fix**
- `remove_bg.sh` ImageMagick fallback: corrected `matte` floodfill coordinates (was passing RGB values as coordinates; now uses `0,0`). Removed erroneous `-alpha extract` which turned output into a pure alpha mask.
- `edit.py` ImageMagick fallback: replaced `-trim` (which merely cropped edges) with `-transparent <detected-bg-color>` so the result is actually a transparent-background image.

**Runtime robustness**
- `op_remove_background` now probes both `$PATH` and the team venv (`venv-clawd/bin/rembg`) for `rembg`, matching Laoguo's actual deployment environment.
- `_call_seedream` guards against `shutil.copyfile(local, output_path)` when source and destination are the same file (would truncate to zero bytes).
- `_save_with_quality` now derives the actual output format from the file extension, preventing OpenCV warnings when `--format` and `--output` disagree (e.g. `--output foo.webp --format png`).

**CLI**
- Added `--no-maintain-aspect` flag for `resize` task to allow non-proportional stretching.

### 1.3.3 — 2026-06-13

**Tool selection policy**
- Codified the routing policy (see "Tool Selection Policy" near the top of this file): Seedream first for semantic / generative edits, deterministic tools first for mechanical edits.
- `op_remove_object` no longer keyword-sniffs the prompt for "wire / cable / line / spot / dust / scratch" and silently routes to a stub. `--tool auto` now picks Seedream when available; the OpenCV branch surfaces an actionable redirect to `scripts/inpaint.py` for known-geometry cases.
- The redirect message also lists the most common `inpaint.py` invocations (`--type spot`, `--type wire`, `--type rect`) so users have a clear next step instead of a guess.

### 1.3.2 — 2026-06-13

**Bug fixes**
- `op_resize` / `op_crop` / `op_color_adjust` no longer raise `TypeError: got an unexpected keyword argument 'mode'`. The CLI's `--mode` flag is now only forwarded for `hdr-tonemap`. (Was reported as "numpy 2.x compat issue"; root cause was kwargs leakage.)
- `smart-compress --target-kb` no longer crashes with `No such file or directory: foo.q55.tmp`. The binary-search probe file now uses the format's real extension (`.jpg/.png/.webp`) so OpenCV can pick a codec.
- `--quality` is now an actual CLI flag, declared in argparse and forwarded into `op_smart_compress` (was documented but unrecognized).
- `--json` on a single-operation invocation now emits a JSON envelope on stdout instead of blocking on stdin. Batch input is still accepted via `--batch FILE` or piped stdin.
- Markdown code fence around the AI-method / OpenCV-method examples is correctly paired (was rendered with broken nesting).
- `compatibility` frontmatter key moved under `metadata.compatibility` (was rejected by the OpenClaw skill validator as an unknown top-level key).
- `_tonemap_shadows` annotation corrected from `np.float32` to `np.ndarray`.

**Seedream bridge rewrite**
The previous integration referenced a non-existent `bin/generate.sh` and a non-existent Python module. `_call_seedream` now invokes `node scripts/generate.js` with `--prompt`, `--mode image-to-image`, `--reference_images <data-URI JSON array>`, `--reference_strength`, and `--optimize false`, parses the JSON envelope from stdout, locates the first `download_success` image, and stages its `local_path` to the caller's `output_path`. Local file paths are encoded as `data:image/<type>;base64,<...>` data URIs because Seedream's validator only accepts HTTP URLs or data URIs. Verified end-to-end with a real ARK API call (200×200 input → 2048×2048 generated output, ~30 s).

**Docs**
- Added "Python Interpreter" section: all scripts hard-shebang the team venv (`~/.openclaw/venv-clawd/bin/python`); running them under system Python will spuriously report `piexif/exif/rembg` as missing.
- `--quality` and `--json` table entries clarified.
