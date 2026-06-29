---
name: smart-photo-editor
license: MIT
description: |
  AI-powered photo editing and restoration skill - smart object removal, background removal, old photo restoration, and basic edits.

metadata:
  author: Team
  version: "1.3.3"
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

## Trigger Conditions

Activates automatically when users mention keywords like:
- photo editing, edit image, retouch, smart photo edit
- remove object, delete object, erase
- remove background, background removal, cutout
- restore, fix, old photo restoration, repair
- color adjustment, color correction, color grading
- crop, resize, compress

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

Override with `--tool seedream | opencv | imagemagick | rembg`.

---

## Installation & Dependencies

### Standard Installation Path
`~/.openclaw/skills/smart-photo-editor/`

### Python Interpreter
All Python scripts (`scripts/*.py`) carry a hard shebang pointing at the team
virtual environment:

```
#!/home/guoxh/.openclaw/venv-clawd/bin/python
```

**Always invoke them via the venv** (or run them directly with `./scripts/edit.py`).
Running under system Python (`/usr/bin/python3 scripts/edit.py ...`) will report
missing optional deps (`piexif`, `exif`, `rembg`) even when they are installed
in the venv.

```bash
# Sanity check (the venv ships everything required + optional)
/home/guoxh/.openclaw/venv-clawd/bin/python -c \
  "import cv2, numpy, PIL, piexif, exif, rembg; print('ok')"
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

## Unified API Interface

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `task` | string | - | ✅ | Task type: `remove-object` / `remove-background` / `restore` / `resize` / `crop` / `color-adjust` / `perspective-correct` / `smart-compress` / `hdr-tonemap` |
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

### 1.3.3 — 2026-06-13

**Tool selection policy**
- Codified the routing policy (see "Tool Selection Policy" near the top of this file): Seedream first for semantic / generative edits, deterministic tools first for mechanical edits.
- `op_remove_object` no longer keyword-sniffs the prompt for "wire / cable / line / spot / dust / scratch" and silently routes to a stub. `--tool auto` now picks Seedream when available; the OpenCV branch surfaces an actionable redirect to `scripts/inpaint.py` for known-geometry cases.
- The redirect message also lists the most common `inpaint.py` invocations (`--type spot`, `--type wire`, `--type rect`) so users have a clear next step instead of a guess.
