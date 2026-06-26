# Erasure/Watermark Removal Parameters & Examples — `mps_erase.py`

**Function**: Subtitle removal, watermark erasure, face blurring, license plate blurring, and other visual element erasure/masking operations.
> ⚠️ This script is responsible for **erasing/masking visual elements on screen** and does not involve quality inspection. For quality inspection, use `mps_qualitycontrol.py`.

## Preset Templates

| Template ID | Description |
|-------------|-------------|
| `101` | Remove subtitles (default) |
| `102` | Remove subtitles + OCR extraction |
| `201` | Advanced watermark removal |
| `301` | Face blurring |
| `302` | Face + license plate blurring |

## Parameter Description

| Parameter | Description |
|-----------|-------------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL address |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/video.mp4`, **recommended**) |
| `--template` | Template ID (takes priority over custom parameters) |
| `--method` | Erasure method: `auto` (automatic) / `custom` (custom area) |
| `--model` | Erasure model: `standard` (standard) / `area` (area-based, suitable for decorative/shadow subtitles) |
| `--position` | Preset position: `fullscreen` / `top-half` / `bottom-half` / `center` / `left` / `right` |
| `--area` | Auto-erasure area (percentage coordinates `X1,Y1,X2,Y2`, range 0-1); can be specified multiple times |
| `--custom-area` | Custom area (`BEGIN,END,X1,Y1,X2,Y2`) |
| `--ocr` | Enable OCR subtitle extraction (boolean flag, write `--ocr` directly — **not** `--type ocr`) |
| `--subtitle-lang` | Subtitle language: `zh_en` (Chinese-English, default) / `multi` (multilingual) |
| `--subtitle-format` | Subtitle file format: `vtt` (default) / `srt` |
| `--translate` | Subtitle translation target language (**must enable `--ocr` simultaneously**). Supported: `zh`, `en`, `ja`, `ko`, `fr`, `es`, `it`, `de`, `tr`, `ru`, `pt`, `vi`, `id`, `ms`, `th`, `ar`, `hi` — 17 languages in total |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-dir` | Output directory, default `/output/erase/` |
| `--output-object-path` | Output file path, e.g., `/output/{inputName}_erase.{format}` |
| `--no-wait` | Submit task only, do not wait for results (auto-polling by default) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 (30 minutes) |
| `--download-dir` | Download output files to the specified local directory after task completion (by default, only prints pre-signed URLs) |
| `--verbose` / `-v` | Output detailed information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--notify-url` | Task completion callback URL (optional) |
| `--dry-run` | Print parameters only, do not call the API |

## Area Preset (--position) Description

| Preset Value | Description | Coordinate Range |
|--------------|-------------|------------------|
| `fullscreen` | Full screen | (0,0)-(0.9999,0.9999) |
| `top-half` | Top half of screen | (0,0)-(0.9999,0.5) |
| `bottom-half` | Bottom half of screen | (0,0.5)-(0.9999,0.9999) |
| `center` | Center of screen | (0.1,0.3)-(0.9,0.7) |
| `left` | Left side of screen | (0,0)-(0.5,0.9999) |
| `right` | Right side of screen | (0.5,0)-(0.9999,0.9999) |

## Mandatory Rules

> ⚠️ **Priority Note**: The following rules are listed in descending order of priority. When multiple rules match simultaneously, **use the rule with the lower number first**.

- **`mps_erase.py` has no `--type` parameter**: Never generate `--type ocr`, `--type watermark`, or similar. OCR is enabled via `--ocr` (flag) or `--template 102`, not a `--type` argument.
- **[Highest Priority — Entry Decision] First determine whether the user needs BOTH "remove subtitles" AND "extract subtitle text/OCR/recognize subtitles"**:
  - ✅ Yes → **Must and can only use `--template 102`**; the command **absolutely must not** contain `--template 101` or `--ocr` parameter (`--template 102` has built-in OCR functionality, no need to add `--ocr` separately)
  - ✅ No (only remove subtitles, no text extraction) → Use `--template 101`, must not be omitted
- **Subtitle removal scenario (remove only, no text extraction) must explicitly include `--template 101`**; must not be omitted (even though it is the default value, it must be written in the command)
- **Face blurring scenario must include `--template 301`**
- **Face + license plate blurring scenario must include `--template 302`**
- **Advanced watermark removal must include `--template 201`**

## Example Commands

```bash
# Auto-erase subtitles in the lower-center area (template 101, must be explicitly specified)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 101

# Remove subtitles and extract OCR subtitles (template 102)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 102

# Advanced watermark removal (template 201)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 201

# Face blurring (template 301)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 301

# Face and license plate blurring (template 302)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 302

# Aggressive erasure (area model, suitable for decorative/shadow subtitles)
python scripts/mps_erase.py --url https://example.com/video.mp4 --model area

# Use area preset — subtitles in the top half
python scripts/mps_erase.py --url https://example.com/video.mp4 --position top-half

# Use area preset — subtitles in the bottom half
python scripts/mps_erase.py --url https://example.com/video.mp4 --position bottom-half

# Custom area (top 0-25% of the frame)
python scripts/mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.25

# Multi-area erasure (subtitles at both top and bottom)
python scripts/mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.15 --area 0,0.75,1,1

# Remove subtitles + OCR extraction + translate to English (must use --template 102)
python scripts/mps_erase.py --url https://example.com/video.mp4 --template 102 --translate en

# Query existing task results
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --verbose

# Query task and download results locally
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --download-dir ./output/
