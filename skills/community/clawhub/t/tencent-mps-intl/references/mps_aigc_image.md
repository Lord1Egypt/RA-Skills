# AIGC Image Generation Parameters & Examples — `mps_aigc_image.py`

**Features**: AI image generation, supporting text-to-image, image-to-image, and 3D panoramic image, with Hunyuan/GEM/Qwen/Vidu/Kling/OG model support.
> ⚠️ Generated images are stored for 12 hours by default. Please download them promptly.

## Parameter Reference

| Parameter | Description |
|------|------|
| `--prompt` | Image description text (max 1000 characters, required when no reference image is provided) |
| `--model` | Model: `Hunyuan` (default) / `GEM` / `Qwen` / `Vidu` / `Kling` / `OG` |
| `--model-version` | Model version: GEM `2.5`/`3.0`/`3.1`; Vidu `q2`; Kling `2.1`/`O1`/`3.0`/`3.0-Omni`; OG `image2_low`/`image2_medium`/`image2_high` |
| `--scene-type` | Scene-based image generation (Hunyuan only): `3d_panorama` (panoramic image) |
| `--negative-prompt` | Negative prompt |
| `--enhance-prompt` | Enable prompt enhancement |
| `--image-url` | Reference image URL (can be specified multiple times, GEM supports up to 3 images) |
| `--image-ref-type` | Reference image type (in order across all sources — `--image-url` / `--image-cos-key` / `--image-local`): `asset` (content reference) / `style` (style reference) |
| `--image-cos-bucket` | COS Bucket of the reference image (can be specified multiple times). Script auto-generates a presigned URL and passes it to the API |
| `--image-cos-region` | COS Region of the reference image (can be specified multiple times) |
| `--image-cos-key` | COS Key of the reference image (can be specified multiple times) |
| `--image-local` | **Local reference image path** (can be specified multiple times). Script auto-uploads to COS (`aigc_input/` directory), generates a presigned URL, and passes it to the API. Requires `TENCENTCLOUD_COS_BUCKET` or `--cos-bucket-name`. Supports jpeg/png/webp |
| `--additional-parameters` | Additional parameters (JSON string, model-specific extension parameters) |
| `--aspect-ratio` | Aspect ratio (e.g., `16:9`, `1:1`). Supported: `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `--resolution` | Resolution: `720P` / `1080P` / `2K` / `4K` |
| `--no-wait` | Submit the task only, without waiting for results |
| `--task-id` | Query the result of an existing task |
| `--cos-bucket-name` | COS Bucket for result storage (if not configured, MPS temporary storage is used for 12 hours) |
| `--cos-bucket-region` | COS Region for result storage |
| `--cos-bucket-path` | COS path prefix for result storage, default `/output/aigc-image/` |
| `--download-dir` | Download generated images to a specified local directory after task completion (by default, only pre-signed URLs are printed) |
| `--operator` | Operator name (optional) |
| `--poll-interval` | Polling interval (seconds), default 5 |
| `--max-wait` | Maximum wait time (seconds), default 300 |
| `--verbose` / `-v` | Output detailed information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameters only, do not call the API |

## Mandatory Rules

- **The AIGC image generation API only supports `ImageUrl`** for reference images — `CosInputInfo` is not supported. When using `--image-cos-key`, the script automatically generates a presigned URL and passes it to the API (requires `TENCENTCLOUD_SECRET_ID/KEY`; signing is only needed for private-read buckets).
- When using `--image-local`, the script first uploads the file to COS (`aigc_input/` directory), then generates a presigned URL and passes it to the API. Requires `TENCENTCLOUD_COS_BUCKET` and `TENCENTCLOUD_SECRET_ID/KEY`.
- When the user provides bucket/region/key, all three parameters must be passed in completely; none may be omitted.

```bash
# COS image-to-image (script auto-converts COS Key to presigned URL before passing to API)
python scripts/mps_aigc_image.py --prompt "city night scene" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/ref.jpg

# Local file image-to-image (auto-uploaded to COS then passed to API)
python scripts/mps_aigc_image.py --prompt "city night scene" \
    --image-local /tmp/ref.jpg

# Local file with ref-type
python scripts/mps_aigc_image.py --model GEM --model-version 3.0 \
    --prompt "generate with style reference" \
    --image-local /tmp/style.jpg --image-ref-type style

# Multiple local files (GEM supports up to 3)
python scripts/mps_aigc_image.py --model GEM --model-version 3.0 \
    --prompt "blend styles" \
    --image-local /tmp/a.jpg --image-ref-type asset \
    --image-local /tmp/b.jpg --image-ref-type style
```

## Example Commands

```bash
# Text-to-image (Hunyuan default)
python scripts/mps_aigc_image.py --prompt "a cute orange tabby cat napping in the sunshine"

# GEM 3.1 + negative prompt + 16:9 + 2K
python scripts/mps_aigc_image.py --prompt "cyberpunk city night scene" --model GEM --model-version 3.1 \
    --negative-prompt "people" --aspect-ratio 16:9 --resolution 2K

# Vidu q2 text-to-image
python scripts/mps_aigc_image.py --prompt "lake reflection under a starry sky" --model Vidu --model-version q2

# Kling 3.0 text-to-image
python scripts/mps_aigc_image.py --prompt "cyberpunk city night with neon lights" --model Kling --model-version 3.0

# OG image2_high text-to-image (high quality)
python scripts/mps_aigc_image.py --prompt "realistic landscape painting" --model OG --model-version image2_high

# OG image2_low text-to-image (fast generation)
python scripts/mps_aigc_image.py --prompt "cartoon style kitten" --model OG --model-version image2_low

# Hunyuan 3D panoramic image
python scripts/mps_aigc_image.py --prompt "tropical rainforest panorama" --model Hunyuan --scene-type 3d_panorama

# Image-to-image (reference image + description)
python scripts/mps_aigc_image.py --prompt "transform this photo into an oil painting style" \
    --image-url https://example.com/photo.jpg

# GEM multi-image reference (supports asset/style reference types)
python scripts/mps_aigc_image.py --prompt "blend these elements" --model GEM \
    --image-url https://example.com/img1.jpg --image-ref-type asset \
    --image-url https://example.com/img2.jpg --image-ref-type style

# Submit task only without waiting
python scripts/mps_aigc_image.py --prompt "product poster" --no-wait

# Query task result
python scripts/mps_aigc_image.py --task-id abc123def456-aigc-image-20260328112000
```