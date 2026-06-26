# Image Processing Parameters & Examples — `mps_imageprocess.py`

**Features**: Image super-resolution, beautification, denoising, color enhancement, filters, resizing, blind watermarking, auto erasure, and more.

## Parameter Reference

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Image URL address |
| `--cos-input-bucket` | Input COS Bucket name (use with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/image.jpg`, **recommended**) |
| `--format` | Output format: `JPEG` / `PNG` / `BMP` / `WebP` |
| `--quality` | Image quality [1-100] |
| `--super-resolution` | Enable super-resolution (2x) |
| `--sr-type` | Super-resolution type: `lq` (low quality with noise, default) / `hq` (high quality) |
| `--advanced-sr` | Enable advanced super-resolution |
| `--adv-sr-type` | Advanced super-resolution type: `standard` (general purpose, default) / `super` / `ultra` |
| `--sr-mode` | Advanced super-resolution output mode: `percent` (scale factor) / `aspect` (aspect ratio, default) / `fixed` (fixed size) |
| `--sr-percent` | Advanced super-resolution scale factor (e.g., `3.0`) |
| `--sr-width` / `--sr-height` | Advanced super-resolution target width/height (max 4096) |
| `--sr-long-side` | Advanced super-resolution target long side (max 4096) |
| `--sr-short-side` | Advanced super-resolution target short side (max 4096) |
| `--denoise` | Denoising strength: `weak` (light) / `strong` (heavy) |
| `--quality-enhance` | Comprehensive enhancement strength: `weak` / `normal` / `strong` |
| `--color-enhance` | Color enhancement: `weak` / `normal` / `strong` |
| `--sharp-enhance` | Detail enhancement (0.0-1.0) |
| `--face-enhance` | Face enhancement strength (0.0-1.0) |
| `--lowlight-enhance` | Enable low-light enhancement |
| `--beauty` | Beauty effect, format `Type:Strength` (strength 0-100), can be specified multiple times. Types: `Whiten` (skin whitening), `Smooth` (skin smoothing), `BeautyThinFace` (face slimming), `NatureFace` (natural face shape), `VFace` (V-shape face), `EnlargeEye` (eye enlargement), `EyeLighten` (eye brightening), `RemoveEyeBags` (eye bag removal), `ThinNose` (nose slimming), `ToothWhiten` (teeth whitening), `FaceFeatureLipsLut` (lipstick, with optional color: `FaceFeatureLipsLut:50:#ff0000`), and 20+ other types |
| `--filter` | Filter effect, format `Type:Strength`. Types: `Dongjing` (Tokyo), `Qingjiaopian` (Light Film), `Meiwei` (Gourmet) |
| `--erase-detect` | Auto erasure type (multiple allowed): `logo` / `text` / `watermark` |
| `--erase-area` | Specify erasure region (pixel coordinates), format `x1,y1,x2,y2`, can be specified multiple times |
| `--erase-box` | Specify erasure region (percentage coordinates 0-1), format `x1,y1,x2,y2`, can be specified multiple times |
| `--erase-area-type` | Erasure region type: `logo` (default) / `text` |
| `--add-watermark` | Add blind watermark with specified text (max 4 bytes, approximately 1 Chinese character or 4 ASCII characters) |
| `--extract-watermark` | Extract blind watermark |
| `--remove-watermark` | Remove blind watermark |
| `--resize-percent` | Percentage scale factor (e.g., `2.0` for 2x enlargement) |
| `--resize-mode` | Resize mode: `percent` / `mfit` / `lfit` / `fill` / `pad` / `fixed` |
| `--resize-width` / `--resize-height` | Target width/height (pixels) |
| `--resize-long-side` | Target long side (pixels) |
| `--resize-short-side` | Target short side (pixels) |
| `--definition` | Image processing template ID |
| `--schedule-id` | Orchestration scene ID (console preset AI capabilities), see the "Orchestration Scenario Overview" section below. **For outfit change use `mps_image_tryon.py`; for background fusion use `mps_image_bg_fusion.py`** |
| `--resource-id` | Resource ID (advanced option, for specific scenarios) |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-path` | Output file path template (e.g., `/output/{inputName}_processed.{format}`) |
| `--output-dir` | Output directory (e.g., `/output/image/`); if not specified, uses MPS default path |
| `--no-wait` | Submit task only, do not wait for result (default: auto-polling) |
| `--poll-interval` | Polling interval (seconds), default 5 |
| `--max-wait` | Maximum wait time (seconds), default 300 (5 minutes) |
| `--download-dir` | Download output files to specified local directory after task completion (default: only prints pre-signed URL) |
| `--compare [path]` | Automatically generate an effect comparison HTML page after task completion; optionally specify an output path, or omit to auto-name |
| `--verbose` / `-v` | Output detailed information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameters only, do not call API |

## Orchestration Scenario Overview (`--schedule-id`)

> The ScheduleIds below are **console-preset AI capabilities** provided by Tencent Cloud MPS. Usually you only need to provide the input image and `--schedule-id` — no other processing parameters are required (the orchestration template has the full pipeline preset internally).

| ScheduleId | Capability | Typical Triggers |
|:---:|------|------|
| `30000` | **AI Text Watermark Erasure** | erase text watermark / remove text watermark / remove watermark text |
| `30010` | **AI Outpainting (Image Extension)** | image outpainting / AI extension / image expansion / outpaint |
| `30030` | **AI Cutout** | AI cutout / smart cutout / cutout portrait / cutout subject / background removal (keep subject) |
| `30031` | **AI Foreground Extraction** | foreground extraction / extract subject / extract foreground |
| `30040` | **AI Image Restoration** | image restoration / old photo restoration / damage repair / scratch repair / portrait restoration |
| `30200` | **AI Image Understanding** | image understanding / image content recognition / AI vision / describe image content |

> ⚠️ Other business ScheduleIds use dedicated scripts: `30060` background fusion uses `mps_image_bg_fusion.py`; `30100/30101` outfit change uses `mps_image_tryon.py`.

## Mandatory Rules

- **Super-resolution selection rules**:
  - User says "upscale to 4K", "ultra HD", "upscale 3x or more", "HD restoration" → prefer `--advanced-sr` (advanced super-resolution), optionally with `--sr-width`/`--sr-height` or `--sr-long-side` to specify target dimensions
  - User says "2x upscale", "super-resolution", "improve resolution" (without specifying a factor or target size) → use `--super-resolution` (standard 2x super-resolution)
  - **The two super-resolution modes are mutually exclusive** — do not use `--super-resolution` and `--advanced-sr` simultaneously
- **Erasure scope boundary**: For erasing text/watermarks/logos in images, use `--erase-detect` or `--erase-area`; for **video** erasure, use `mps_erase.py` — do not mix them
- **Outfit change is prohibited with this script**: Image outfit change must use `mps_image_tryon.py`; `mps_imageprocess.py` does not support outfit change functionality (even using `--schedule-id 30100/30101` is incorrect)
- **Orchestration scenario (`--schedule-id`) usage rules**:
  - The AI capabilities below **must** be triggered via `--schedule-id`; do not manually combine processing parameters:
    - User says "image understanding / AI vision / describe image content" → `--schedule-id 30200`
    - User says "cutout / smart cutout / cutout subject" → `--schedule-id 30030`
    - User says "image restoration / old photo restoration / scratch repair" → `--schedule-id 30040`
    - User says "foreground extraction / extract subject" → `--schedule-id 30031`
    - User says "AI outpainting / image extension / outpaint" → `--schedule-id 30010`
    - User says "erase text watermark / remove watermark text in image" (when emphasizing AI smart erasure) → `--schedule-id 30000`
  - **Do not mix** `--schedule-id` with local image enhancement / erasure / beauty configuration parameters (the console orchestration template already defines the full pipeline)
  - Different business orchestrations use different scripts: **background fusion** → `mps_image_bg_fusion.py` (30060); **outfit change** → `mps_image_tryon.py` (30100/30101)

## Example Commands

```bash
# Super-resolution 2x upscale
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --super-resolution

# Advanced super-resolution to 4K
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-width 3840 --sr-height 2160

# Denoising + color enhancement + detail enhancement
python scripts/mps_imageprocess.py --url https://example.com/image.jpg \
    --denoise weak --color-enhance normal --sharp-enhance 0.8

# Comprehensive enhancement (overall quality improvement)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --quality-enhance normal

# Comprehensive enhancement + super-resolution (heavy restoration for low-quality images)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --quality-enhance strong --super-resolution

# Beauty (whitening + face slimming + eye enlargement)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg \
    --beauty Whiten:50 --beauty BeautyThinFace:30 --beauty EnlargeEye:40

# Auto erase watermark
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --erase-detect watermark

# Add blind watermark
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --add-watermark "MPS"

# Convert to WebP format + quality 80
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --format WebP --quality 80

# Filter (light film style, strength 70)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --filter Qingjiaopian:70

# Resize (aspect-fit within 800x600)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --resize-mode lfit --resize-width 800 --resize-height 600

# Resize (set long side to 1920, aspect ratio preserved)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --resize-long-side 1920

# === Orchestration Scenarios (console preset AI capabilities, only image + schedule-id required) ===
# AI Image Understanding (30200)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30200

# AI Cutout (30030)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30030

# AI Image Restoration (30040, old photo / scratch repair)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30040

# AI Foreground Extraction (30031)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30031

# AI Outpainting (30010)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30010

# AI Text Watermark Erasure (30000)
python scripts/mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30000

# Query image processing task status
python scripts/mps_get_image_task.py --task-id 1234567890-Image Task-80108cc3380155d98b2e3573a48a
```