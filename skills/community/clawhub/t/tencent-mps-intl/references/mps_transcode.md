# Transcoding Parameters & Examples — `mps_transcode.py`

**Features**: Video transcoding, compression, format conversion, supporting video codecs such as H264/H265/H266/AV1/VP9, as well as MP3/M4A audio-only format output.

## Parameter Reference

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL (HTTP/HTTPS) |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/video.mp4`, **recommended**) |
| `--codec` | Video encoding format: `h264` / `h265` / `h266` / `av1` / `vp9` |
| `--width` | Video width / long side (px), e.g., 1920, 1280 |
| `--height` | Video height / short side (px), 0 = scale proportionally |
| `--bitrate` | Video bitrate (kbps), 0 = auto |
| `--fps` | Video frame rate (Hz), 0 = keep original |
| `--container` | Container format: `mp4` / `hls` / `flv` / `mp3` / `m4a` |
| `--audio-codec` | Audio codec: `aac` / `mp3` / `copy` |
| `--audio-bitrate` | Audio bitrate (kbps) |
| `--compress-type` | Compression type: `ultra_compress` / `standard_compress` / `high_compress` / `low_compress` |
| `--scene-type` | Scene type: `normal` / `pgc` / `ugc` / `e-commerce_video` / `educational_video` / `materials_video` |
| `--notify-url` | Task completion callback URL |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-dir` | Output directory, default `/output/transcode/` |
| `--output-object-path` | Output file path template, e.g., `/output/{inputName}_transcode.{format}` |
| `--no-wait` | Submit task only, do not wait for result (default is auto-polling) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 (30 minutes) |
| `--download-dir` | Download output file to specified local directory after task completion (default is to print pre-signed URL only) |
| `--compare [path]` | Automatically generate an effect comparison HTML page after task completion; optionally specify an output path, or omit to auto-name |
| `--verbose` / `-v` | Output verbose information |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--dry-run` | Print parameters only, do not call API |

## Mandatory Rules

- **Default behavior**: When no encoding parameters are specified, the script uses the default template (H265 codec, MP4 container) — no need to ask, execute directly
- **Audio-only extraction**: When the user says "extract audio", "convert to MP3/M4A" → use `--container mp3` or `--container m4a`, no need to specify video codec parameters
- **Compression scenario selection**:
  - User says "maximum compression", "extreme compression", "bandwidth priority" → `--compress-type ultra_compress`
  - User says "balanced compression", "overall optimal" → `--compress-type standard_compress`
  - User says "bitrate priority", "control bitrate" → `--compress-type high_compress`
  - User says "quality priority", "archival" → `--compress-type low_compress`
- **Streaming scenario**: When the user says "HLS segmentation", "streaming playback" → use `--container hls`

## Example Commands

```bash
# Simplest usage: URL input + default template (TESHD-H265-MP4-1080P)
python scripts/mps_transcode.py --url https://example.com/video.mp4

# COS path input (recommended, use after local upload)
python scripts/mps_transcode.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou \
    --cos-input-key /input/video.mp4

# Custom parameters: H265 codec + 1080P + 3000kbps + 30fps
python scripts/mps_transcode.py --url https://example.com/video.mp4 \
    --codec h265 --width 1920 --height 1080 --bitrate 3000 --fps 30

# Maximum compression (ultra_compress): maximize bitrate reduction, ideal for bandwidth-sensitive scenarios
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type ultra_compress

# HLS segmentation (for streaming playback)
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container hls

# Overall optimal (standard_compress): balance between quality and bitrate
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type standard_compress

# Bitrate priority (high_compress): minimize bitrate while maintaining acceptable quality
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type high_compress

# Quality priority (low_compress): moderate compression while preserving quality, ideal for archival
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type low_compress

# Extract audio (convert to MP3)
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container mp3

# Extract audio (convert to M4A, high quality)
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container m4a --audio-bitrate 192

# Async submission then query task status
python scripts/mps_transcode.py --url https://example.com/video.mp4 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```