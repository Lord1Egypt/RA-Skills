# Video Enhancement Parameters & Examples — `mps_enhance.py`

**Features**: Video quality enhancement, old film restoration, super resolution, audio separation/vocal extraction/accompaniment extraction, HDR, frame interpolation, audio denoising/volume balancing/audio beautification, etc.

## Two Usage Modes

> 1. **Template Mode** (Recommended): Use the `--template` parameter to specify a large model enhancement template ID (327001-327032), defaults to real-person scene
> 2. **Custom Parameter Mode**: Use `--preset`, `--diffusion-type`, and other parameters to customize enhancement configuration
>
> **Note**: The two modes are mutually exclusive. When using `--template`, other enhancement parameters will be ignored.

## Template ID Quick Reference

| Scene | 720P | 1080P | 2K | 4K |
|-------|------|-------|----|----|
| Real-Person (Real, face & text region protection) **Default** | 327001 | 327003 | 327005 | 327007 |
| Anime (Anime, anime line & color block enhancement) | 327002 | 327004 | 327006 | 327008 |
| Jitter Optimization (Jitter Opt, reduce inter-frame jitter) | 327009 | 327010 | 327011 | 327012 |
| Maximum Detail (Detail Max, maximize texture detail) | 327013 | 327014 | 327015 | 327016 |
| Face Fidelity (Face Fidelity, preserve facial features) | 327017 | 327018 | 327019 | 327020 |
| Old Film / Low-Quality Restoration (Old Film, comprehensive+face+scratch removal) | 327021 | 327022 | 327023 | 327024 |
| Real-Person Small Face Optimization (Real Small Face, small/distant face) | 327025 | 327026 | 327027 | 327028 |
| Anime Small Face Optimization (Anime Small Face, small/distant face) | 327029 | 327030 | 327031 | 327032 |

> ⚠️ **Important**: When the user mentions "face fidelity", "face-fidelity", or "preserve facial features", you MUST use the **Face Fidelity** row above (327017-327020), NOT the Real-Person row.

| Parameter | Description |
|------|------|
| `--local-file` | Local file path, automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL address |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/video.mp4`, **recommended**) |
| `--template` | **Large model enhancement template ID** (template mode): `327001`-`327032` |
| `--preset` | Large model enhancement preset (custom mode): `diffusion` / `comprehensive` / `artifact` |
| `--diffusion-type` | Diffusion enhancement strength: `weak` / `normal` / `strong` |
| `--comprehensive-type` | Comprehensive enhancement strength: `weak` / `normal` / `strong` |
| `--artifact-type` | De-artifact strength: `weak` / `strong` |
| `--scene-type` | Enhancement scene: `common` / `AIGC` / `short_play` / `short_video` / `game` / `HD_movie_series` / `LQ_material` / `lecture` |
| `--super-resolution` | Enable super resolution (2x, cannot be used simultaneously with large model enhancement) |
| `--sr-type` | Super resolution type: `lq` (low quality with noise, default) / `hq` (high quality) |
| `--sr-size` | Super resolution multiplier, currently only supports `2` (default 2) |
| `--denoise` | Enable video denoising (cannot be used simultaneously with large model enhancement) |
| `--denoise-type` | Denoising strength: `weak` (default) / `strong` |
| `--color-enhance` | Enable color enhancement |
| `--color-enhance-type` | Color enhancement strength: `weak` (default) / `normal` / `strong` |
| `--low-light-enhance` | Enable low-light enhancement |
| `--scratch-repair` | Scratch repair strength (float 0.0-1.0), suitable for old film restoration |
| `--hdr` | Enable HDR enhancement, options: `HDR10` / `HLG` |
| `--frame-rate` | Enable frame interpolation, target frame rate (Hz), e.g., `60` |
| `--audio-denoise` | Enable audio denoising |
| `--audio-separate` | Audio separation: `vocal` (extract vocals) / `background` (extract background sound) / `accompaniment` (extract accompaniment). **No default value, must be explicitly specified by the user, do not guess** |
| `--volume-balance` | Enable volume balancing |
| `--volume-balance-type` | Volume balancing type: `loud Norm` (loudness normalization, default) / `gain Control` |
| `--audio-beautify` | Enable audio beautification (noise removal + sibilance suppression) |
| `--codec` | Output video codec: `h264` / `h265` (default) / `h266` / `av1` / `vp9` |
| `--width` | Output video width/long side (pixels) |
| `--height` | Output video height/short side (pixels), `0` means scale proportionally |
| `--bitrate` | Output video bitrate (kbps), `0` means automatic |
| `--fps` | Output video frame rate (Hz), `0` means keep original |
| `--container` | Output container format: `mp4` (default) / `hls` / `flv` |
| `--audio-codec` | Output audio codec: `aac` (default) / `mp3` / `copy` |
| `--audio-bitrate` | Output audio bitrate (kbps), default `128` |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-dir` | Output directory, default `/output/enhance/` |
| `--output-object-path` | Output file path, e.g., `/output/{inputName}_enhance.{format}` |
| `--no-wait` | Submit task only, do not wait for result (default is automatic polling) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 (30 minutes) |
| `--download-dir` | Download output file to specified local directory after task completion (default only prints pre-signed URL) |
| `--compare [path]` | Automatically generate an effect comparison HTML page after task completion; optionally specify an output path, or omit to auto-name |
| `--notify-url` | Task completion callback URL (optional) |
| `--verbose` / `-v` | Output verbose information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameters only, do not call API |

## Mandatory Rules

- **Audio Separation Follow-up Rule**: Only when the user **has not specified at all** which audio track to separate (e.g., only says "extract audio track" or "audio separation"), ask: "Which audio track would you like to extract? Vocals (vocal), accompaniment (accompaniment), or background sound (background)?"
- **Generate Command Directly When Intent Is Clear**: If the user says "separate vocals and background music", the intent is already clear (vocal + accompaniment), directly generate **two separate commands** with `--audio-separate vocal` and `--audio-separate accompaniment` respectively, do not ask follow-up questions.
- **Default to Real-Person Template for Video Enhancement**: When using template mode, if the user does not specify the video type (Real-Person / Anime / Jitter Optimization / Maximum Detail / Face Fidelity), **default to the real-person template** (720P→327001, 1080P→327003, 2K→327005, 4K→327007), generate the command directly without asking; if the user explicitly specifies a video type, use the corresponding template row — e.g., "face fidelity" → Face Fidelity row (327017/327018/327019/327020), "anime" → Anime row (327002/327004/327006/327008), etc.
- Audio separation and quality enhancement are mutually exclusive; `--audio-separate` and `--template`/`--preset` cannot be used simultaneously.

## Example Commands

```bash
# ===== Large Model Enhancement Templates (Recommended, Use First) =====

# Real-person scene - Upscale to 1080P (recommended for real-person footage)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327003

# Real-person scene - Upscale to 4K (ultra-HD restoration)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327007

# Anime scene - Upscale to 1080P
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327004

# Anime scene - Upscale to 4K (recommended for anime video ultra-clear restoration)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327008

# Jitter optimization - Upscale to 1080P (reduce inter-frame jitter and texture flickering)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327010

# Maximum detail - Upscale to 4K (ultimate detail restoration)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327016

# Face fidelity - Upscale to 1080P (recommended for portrait/photoshoot/interview videos)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327018

# ===== Custom Parameter Mode =====

# Large model enhancement (strongest effect)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset diffusion --diffusion-type strong

# Comprehensive enhancement (balanced effect and efficiency)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset comprehensive --comprehensive-type normal

# De-artifact (repair artifacts caused by compression)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --preset artifact --artifact-type strong

# Super resolution + denoising + color enhancement
python scripts/mps_enhance.py --url https://example.com/video.mp4 --super-resolution --denoise --color-enhance

# HDR + frame interpolation 60fps
python scripts/mps_enhance.py --url https://example.com/video.mp4 --hdr HDR10 --frame-rate 60

# ===== Audio Separation =====

# Extract vocals (remove background music)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate vocal

# Extract background sound (remove vocals)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate background

# Extract accompaniment (remove vocals, keep music)
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-separate accompaniment

# Audio enhancement: denoising + volume balancing + beautification
python scripts/mps_enhance.py --url https://example.com/video.mp4 --audio-denoise --volume-balance --audio-beautify

# ===== Output Encoding Control =====

# Enhanced output as H265 + 1080P + specified bitrate
python scripts/mps_enhance.py --url https://example.com/video.mp4 --super-resolution \
    --codec h265 --width 1920 --height 1080 --bitrate 4000

# Submit asynchronously then query task status
python scripts/mps_enhance.py --url https://example.com/video.mp4 --template 327003 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```