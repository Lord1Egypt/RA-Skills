# AIGC Video Generation Parameters & Examples — `mps_aigc_video.py`

**Features**: AI video generation supporting text-to-video, image-to-video, and multi-shot storyboard generation with Hunyuan/Hailuo/Kling/Vidu/OS/GV/Mingmou/PixVerse models.
> ⚠️ Generated videos are stored for 12 hours by default. Please download them promptly.

## Parameter Reference

| Parameter | Description |
|-----------|-------------|
| `--prompt` | Video description text (max 2000 characters, required when no image is provided) |
| `--model` | Model: `Hunyuan` (default) / `Hailuo` / `Kling` / `Vidu` / `OS` / `GV` / `Mingmou` / `PixVerse` |
| `--model-version` | Model version. Kling: `1.6`/`2.0`/`2.1`/`2.5`/`O1`/`2.6`/`3.0`/`3.0-Omni`; Hailuo: `02`/`2.3`/`2.3-fast`; Vidu: `q2`/`q2-pro`/`q2-turbo`/`q3`/`q3-pro`/`q3-turbo`/`q3-mix`; GV: `3.1`/`3.1-fast`; PixVerse: `v5.6`/`v6`/`c1` |
| `--scene-type` | Scene type (strict model mapping): `motion_control` (Kling motion control) / `land2port` (Mingmou landscape-to-portrait) / `template_effect` (Vidu effect template) / `3d_scene` (Hunyuan 3D scene, automatically uses ModelVersion=3d_2.0) |
| `--multi-shot` | **Kling exclusive**. Enable multi-shot storyboard mode |
| `--multi-prompts-json` | **Kling exclusive**. Multi-shot configuration (JSON array), each shot contains `index`, `prompt`, `duration`. Limits: 1–6 shots, max 512 characters per prompt, total duration of all shots must equal the overall duration |
| `--negative-prompt` | Negative prompt |
| `--enhance-prompt` | Enable prompt enhancement |
| `--image-url` | Reference image (first frame) URL (single image, used for image-to-video) |
| `--last-image-url` | Reference image (last frame) URL (supported by some models, requires `--image-url` to be set as well) |
| `--image-cos-bucket` | COS Bucket for the first-frame image (script auto-generates presigned URL then passes as ImageUrl) |
| `--image-cos-region` | COS Region for the first-frame image |
| `--image-cos-key` | COS Key for the first-frame image |
| `--image-local` | **Local first-frame image path**, auto-uploaded to COS then passed as ImageUrl. Requires `TENCENTCLOUD_COS_BUCKET` or `--cos-bucket-name` |
| `--last-image-cos-bucket` | COS Bucket for the last-frame image (script auto-generates presigned URL then passes as LastImageUrl) |
| `--last-image-cos-region` | COS Region for the last-frame image |
| `--last-image-cos-key` | COS Key for the last-frame image |
| `--last-image-local` | **Local last-frame image path**, auto-uploaded to COS then passed as LastImageUrl. Requires `TENCENTCLOUD_COS_BUCKET` or `--cos-bucket-name` |
| `--ref-image-url` | Multi-image reference URL (can be specified multiple times, supported by GV/Vidu, max 3 images) |
| `--ref-image-type` | Multi-image reference type (in order across all sources — `--ref-image-url` / `--ref-image-cos-key` / `--ref-image-local`): `asset` (content reference) / `style` (style reference) |
| `--ref-image-cos-bucket` | COS Bucket for multi-image reference (can be specified multiple times, script auto-generates presigned URL) |
| `--ref-image-cos-region` | COS Region for multi-image reference (can be specified multiple times) |
| `--ref-image-cos-key` | COS Key for multi-image reference (can be specified multiple times) |
| `--ref-image-local` | **Local multi-image reference path** (can be specified multiple times), auto-uploaded to COS then passed as ImageUrl. Requires `TENCENTCLOUD_COS_BUCKET` or `--cos-bucket-name` |
| `--duration` | Video duration (seconds). Supported ranges per model:<br>- Hunyuan: default 5s<br>- Hailuo: 6s (default) / 10s<br>- Kling: 5s / 10s, default 5s<br>- Vidu: 1~10s, default 4s<br>- OS: 5s / 10s, default 5s<br>- GV: 5s / 10s, default 5s<br>- **PixVerse: any integer from 1~15s, default 5s** |
| `--resolution` | Resolution: `720P` / `1080P` / `2K` / `4K` |
| `--aspect-ratio` | Aspect ratio (e.g., `16:9`, `9:16`, `1:1`, `4:3`, `3:4`). **PixVerse supports 8**: `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `2:3` / `3:2` / `21:9` |
| `--quality` | Video quality (**PixVerse only**): `360p` / `540p` / `720p` / `1080p`. Passed via `ExtraParameters.Quality`; MPS backend maps it to PixVerse's native quality field |
| `--generate-audio` | Whether to generate sound effects (**PixVerse only**): `true` / `false`. Passed via `ExtraParameters.EnableAudio`; MPS backend maps it to PixVerse's `generate_audio_switch`. When enabled, PixVerse auto-generates ambient sound / audio matching the video content |
| `--no-logo` | Remove watermark (supported by Hailuo/Kling/Vidu) |
| `--enable-bgm` | Enable background music (supported by some model versions) |
| `--enable-audio` | Whether to generate audio for the video (supported by GV/OS, accepted values: `true`/`false`) |
| `--ref-video-url` | Reference video URL (Kling model only) |
| `--ref-video-type` | Reference video type: `feature` (feature reference) / `base` (video to be edited, default) |
| `--keep-original-sound` | Keep original audio: `yes` / `no` |
| `--ref-video-cos-bucket` | COS Bucket for reference video (can be specified multiple times) |
| `--ref-video-cos-region` | COS Region for reference video (can be specified multiple times) |
| `--ref-video-cos-key` | COS Key for reference video (can be specified multiple times, auto-generates pre-signed URL into VideoUrl) |
| `--off-peak` | Off-peak mode (Vidu only), task completes within 48 hours |
| `--additional-params` | Additional parameters in JSON format for model-specific extensions (e.g., Kling camera control) |
| `--no-wait` | Submit task only, do not wait for results |
| `--task-id` | Query the result of an existing task |
| `--cos-bucket-name` | COS Bucket for result storage (if not configured, MPS temporary storage is used for 12 hours) |
| `--cos-bucket-region` | COS Region for result storage |
| `--cos-bucket-path` | COS path prefix for result storage, default `/output/aigc-video/` |
| `--download-dir` | Download the generated video to a specified local directory after task completion (by default, only the pre-signed URL is printed) |
| `--operator` | Operator name (optional) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 |
| `--verbose` / `-v` | Output verbose information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameters only, do not call the API |

## ⚠️ Mandatory Rules (Violations will cause command execution to fail)

- **🚫 Reference video is supported by the Kling model only**: When the user requests a reference video (`--ref-video-url` or `--ref-video-cos-key`), **`--model Kling` must be used** — other models do not support reference video. If the user specifies another model with a reference video, **you must reject and inform** them that reference video is only supported by the Kling model and suggest switching to Kling.
- **🚫 SceneType strictly maps to model**: The `--scene-type` parameter **must** match the model exactly — **no mixing allowed**:
  - `motion_control` (motion control) → ⚠️ **Kling model only**
  - `land2port` (landscape-to-portrait) → ⚠️ **Mingmou model only**
  - `template_effect` (effect template) → ⚠️ **Vidu model only**
  - `3d_scene` (3D scene) → ⚠️ **Hunyuan model only** (automatically uses ModelVersion=3d_2.0)
  If the user specifies a mismatched combination (e.g., "Use Vidu model with motion control"), **you must reject and inform** them that the scene type is only supported by the corresponding model (e.g., "motion_control is only supported by Kling, please use Kling model instead").
- **Mingmou landscape-to-portrait (land2port) does NOT require an input video file**: This scene generates a portrait video from the prompt description alone — **do NOT ask the user for an input video source**. Simply use the `--prompt` parameter to generate the command.
- **PixVerse model — strict parameter validation**:
  - `--model-version` must be one of: `v5.6` / `v6` / `c1` (omit to let the backend choose)
  - `--aspect-ratio` must be one of 8: `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `2:3` / `3:2` / `21:9`
  - `--duration` must be an integer between 1 and 15 seconds
  - `--quality` must be one of: `360p` / `540p` / `720p` / `1080p` (passed via `ExtraParameters.Quality`, PixVerse only)
  - `--generate-audio` must be `true` / `false` (passed via `ExtraParameters.EnableAudio`; MPS backend maps it to PixVerse's `generate_audio_switch`; PixVerse only; when enabled, auto-generates sound effects matching the video)
  If the user requests PixVerse with `--multi-shot` or `--ref-video-url`, **you must reject** — those capabilities are Kling-only.
- **The AIGC video generation API only supports URL fields** (`ImageUrl`/`LastImageUrl`) for image inputs — `CosInputInfo` is not supported. When using `--image-cos-key` / `--last-image-cos-key` / `--ref-image-cos-key`, the script automatically generates a presigned URL and passes it to the API (requires `TENCENTCLOUD_SECRET_ID/KEY`).
- When the user provides bucket/region/key, all three parameters must be passed in full — none may be omitted.

```bash
# COS image-to-video (script auto-converts COS Key to presigned URL before passing to API)
python scripts/mps_aigc_video.py --prompt "Flowers swaying in the wind" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/scene.jpg
```

## Multi-Shot Storyboard (Kling Exclusive)

### Single-Shot Mode (System Auto-Split)
```bash
python scripts/mps_aigc_video.py --prompt "Travel diary, capturing beautiful moments" --model Kling --multi-shot
```

### Multi-Shot Mode (Custom Per Shot)
```bash
python scripts/mps_aigc_video.py --model Kling --multi-shot --duration 12 \
    --multi-prompts-json '[
      {"index": 1, "prompt": "At sunrise, viewing the city skyline from the hotel window", "duration": "3"},
      {"index": 2, "prompt": "Enjoying breakfast at a café, pedestrians on the street outside", "duration": "4"},
      {"index": 3, "prompt": "Walking in the park, sunlight filtering through the leaves", "duration": "5"}
    ]'
```

**Validation rules**: 1–6 shots; max 512 characters per prompt; each duration ≥ 1 second; total of all durations must equal the overall duration.

## Example Commands

```bash
# Text-to-video (Hunyuan default)
python scripts/mps_aigc_video.py --prompt "A cat stretching lazily in the sunlight"

# Kling 2.5 + 10s + 1080P + 16:9 + no watermark + BGM
python scripts/mps_aigc_video.py --prompt "Cyberpunk city" --model Kling --model-version 2.5 \
    --duration 10 --resolution 1080P --aspect-ratio 16:9 --no-logo --enable-bgm

# Image-to-video (first-frame image + description)
python scripts/mps_aigc_video.py --prompt "Bring the scene to life" \
    --image-url https://example.com/photo.jpg

# First & last frame video generation (GV model)
python scripts/mps_aigc_video.py --prompt "Transition animation" --model GV \
    --image-url https://example.com/start.jpg --last-image-url https://example.com/end.jpg

# GV multi-image reference video generation (supports asset/style reference types)
python scripts/mps_aigc_video.py --prompt "Generate video with blended styles" --model GV \
    --ref-image-url https://example.com/img1.jpg --ref-image-type asset \
    --ref-image-url https://example.com/img2.jpg --ref-image-type style

# Kling reference video + keep original audio
python scripts/mps_aigc_video.py --prompt "Stylize the video" --model Kling --model-version O1 \
    --ref-video-url https://example.com/video.mp4 --ref-video-type base --keep-original-sound yes

# Mingmou landscape to portrait (land2port scene does NOT require an input video file — just provide a prompt description)
python scripts/mps_aigc_video.py --prompt "Landscape to portrait conversion" --model Mingmou --scene-type land2port

# Kling reference video (COS path, auto-generates pre-signed URL)
python scripts/mps_aigc_video.py --prompt "Stylization" --model Kling --model-version O1 \
    --ref-video-cos-bucket mybucket-125xxx --ref-video-cos-region ap-guangzhou --ref-video-cos-key /input/video.mp4 \
    --ref-video-type base --keep-original-sound yes

# Vidu off-peak mode
python scripts/mps_aigc_video.py --prompt "Natural scenery" --model Vidu --off-peak

# === PixVerse model examples ===
# PixVerse v6 text-to-video (cinematic 21:9, 10 seconds, 1080p quality)
python scripts/mps_aigc_video.py --prompt "Cinematic city skyline shot" --model PixVerse --model-version v6 \
    --duration 10 --aspect-ratio 21:9 --quality 1080p

# PixVerse v6 text-to-video + auto-generated sound effects (rainy night ambience)
python scripts/mps_aigc_video.py --prompt "Rainy neon street, solitary walker" --model PixVerse --model-version v6 \
    --duration 15 --aspect-ratio 16:9 --quality 720p --generate-audio true

# PixVerse c1 image-to-video (short-form 9:16, 5 seconds, 540p quality)
python scripts/mps_aigc_video.py --prompt "Character walking slowly, hair blowing in the wind" \
    --model PixVerse --model-version c1 \
    --image-url https://example.com/first-frame.jpg --duration 5 --aspect-ratio 9:16 --quality 540p

# PixVerse c1 text-to-video (square 1:1, 3 seconds, 720p quality)
python scripts/mps_aigc_video.py --prompt "Close-up of coffee latte art" --model PixVerse --model-version c1 \
    --duration 3 --aspect-ratio 1:1 --quality 720p

# Submit task only without waiting
python scripts/mps_aigc_video.py --prompt "Promotional video" --no-wait

# Query task result
python scripts/mps_aigc_video.py --task-id abc123def456-aigc-video-20260328112000
```