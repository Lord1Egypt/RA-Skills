# Multi-Platform Export Specs Reference

Export one reel for every major short-form platform in one workflow.
Use `scripts/batch-export.sh` to run all exports at once.

---

## Platform Specs Comparison

| Platform           | Resolution  | FPS  | Max Duration | Max File Size | Codec      | Audio      |
|--------------------|-------------|------|--------------|---------------|------------|------------|
| Instagram Reels    | 1080×1920   | 30   | 90s          | 250 MB        | H.264      | AAC 44.1kHz|
| TikTok             | 1080×1920   | 30   | 60s (short)  | 287 MB        | H.264/H.265| AAC 44.1kHz|
| YouTube Shorts     | 1080×1920   | 30-60| 60s          | 256 MB        | H.264      | AAC 44.1kHz|
| Facebook Reels     | 1080×1920   | 30   | 90s          | 4 GB          | H.264      | AAC 44.1kHz|
| Snapchat Spotlight | 1080×1920   | 30-60| 60s          | 32 MB         | H.264      | AAC 44.1kHz|
| Pinterest Idea Pin | 1080×1920   | 30   | 60s          | 100 MB        | H.264      | AAC 44.1kHz|
| LinkedIn Video     | 1080×1920   | 30   | 30s (organic)| 200 MB        | H.264      | AAC 44.1kHz|
| Twitter/X          | 1080×1920   | 30-60| 2m 20s       | 512 MB        | H.264      | AAC 44.1kHz|

---

## Platform-Specific ffmpeg Export Commands

### Instagram Reels (Primary)
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 128k \
  -movflags +faststart \
  -t 90 \
  instagram_reel.mp4
```

### TikTok
```bash
# TikTok prefers slightly higher bitrate and H.265 option
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 192k \
  -movflags +faststart \
  -t 60 \
  tiktok.mp4
```

### YouTube Shorts
```bash
# YouTube Shorts allows up to 60fps — use 60fps for smoother look
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=60" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 -b:a 192k \
  -movflags +faststart \
  -t 60 \
  youtube_shorts.mp4
```

### Facebook Reels
```bash
# Facebook allows large files — use highest quality
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 192k \
  -movflags +faststart \
  -t 90 \
  facebook_reels.mp4
```

### Snapchat Spotlight
```bash
# Snapchat is strict on file size (32MB) — use higher CRF
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 128k \
  -movflags +faststart \
  -t 60 \
  snapchat.mp4
```

### Pinterest Idea Pin
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 128k \
  -movflags +faststart \
  -t 60 \
  pinterest.mp4
```

### LinkedIn Video
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -b:a 128k \
  -movflags +faststart \
  -t 30 \
  linkedin.mp4
```

---

## Platform-Specific Safe Zones (UI Overlay Areas)

Avoid placing important text/elements in these areas:

| Platform        | Top safe zone | Bottom safe zone | Side safe zones |
|-----------------|---------------|------------------|-----------------|
| Instagram Reels | Top 100px     | Bottom 350px     | 60px each side  |
| TikTok          | Top 80px      | Bottom 300px     | 40px each side  |
| YouTube Shorts  | Top 100px     | Bottom 280px     | 50px each side  |
| Snapchat        | Top 120px     | Bottom 250px     | 40px each side  |

**Safe zone content area for all platforms (conservative):**
- Top margin: 120px from top
- Bottom margin: 350px from bottom
- Side margins: 60px each side
- **Effective content area:** 960×1450px centered at 540,710

**Apply safe zone indicator overlay (for preview):**
```bash
# Draw safe zone rectangle (remove before final export)
ffmpeg -i video.mp4 -vf "
  drawbox=x=60:y=120:w=960:h=1450:color=yellow@0.3:t=3
" OUTPUT_FLAGS preview_safezone.mp4
```

---

## Aspect Ratio Variants

Sometimes you need landscape or square versions too:

### Square (1:1) — 1080×1080 (Instagram Feed / LinkedIn)
```bash
ffmpeg -i vertical_reel.mp4 \
  -vf "crop=1080:1080:0:420" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -movflags +faststart \
  square_1080.mp4
```

### Landscape (16:9) — 1920×1080 (YouTube / Facebook)
```bash
ffmpeg -i vertical_reel.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -movflags +faststart \
  landscape_1920.mp4
```

### 4:5 Portrait — 1080×1350 (Instagram Feed Portrait)
```bash
ffmpeg -i vertical_reel.mp4 \
  -vf "crop=1080:1350:0:285" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -ar 44100 -ac 2 -movflags +faststart \
  portrait_4x5.mp4
```

---

## File Size Estimation

Estimate output file size before encoding:

```
File size (MB) ≈ (bitrate in Mbps × duration in seconds) / 8

CRF 16 ≈ 8–15 Mbps
CRF 18 ≈ 5–10 Mbps
CRF 20 ≈ 3–7  Mbps
CRF 23 ≈ 2–5  Mbps
CRF 26 ≈ 1–3  Mbps

Example: 30s reel at CRF 18 ≈ 30 × 7 / 8 ≈ 26 MB
```

To check actual bitrate after encode:
```bash
ffprobe -v quiet -show_entries format=bit_rate -of csv output.mp4
```

---

## Thumbnail / Cover Frame Extraction

Each platform lets you set a cover frame — always choose the most visually striking frame.

```bash
# Extract frame at specific timestamp (e.g., 3.5 seconds)
ffmpeg -ss 3.5 -i output.mp4 -vframes 1 -q:v 2 thumbnail.jpg

# Extract best-quality frame (I-frame only)
ffmpeg -i output.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr -q:v 2 keyframe_%03d.jpg

# Batch extract frames every 2 seconds for manual selection
ffmpeg -i output.mp4 -vf fps=0.5 -q:v 2 frames/frame_%04d.jpg
```

Use `scripts/scene-detect.py` with `--thumbnail` flag to auto-select the sharpest, most visually interesting frame.

---

## Quality Check Commands

Run before uploading:

```bash
# Check resolution, codec, duration, fps
ffprobe -v quiet -print_format json -show_streams output.mp4 | python -c "
import json,sys
d = json.load(sys.stdin)
for s in d['streams']:
    if s.get('codec_type') == 'video':
        print(f'Resolution: {s[\"width\"]}x{s[\"height\"]}')
        print(f'Codec: {s[\"codec_name\"]}')
        print(f'FPS: {s[\"r_frame_rate\"]}')
        print(f'Duration: {s[\"duration\"]}s')
    if s.get('codec_type') == 'audio':
        print(f'Audio: {s[\"codec_name\"]} {s[\"sample_rate\"]}Hz')
"

# Check file size
ls -lh output.mp4 | awk '{print "File size: "$5}'
```
