# Video Deduplication Parameters & Examples — `mps_dedupe.py`

**Function**: Video Deduplication (Video Remake), modifying video frames to bypass platform duplicate content detection.
> **Core Mechanism**: `AI Analysis Task.Definition=29` + `Extended Parameter(vremake.mode)`.
> The script **automatically polls and waits for completion by default**; add `--no-wait` to submit only without waiting.
> Official Documentation: https://cloud.tencent.com/document/product/862/124394

## Supported Modes

| Mode | Description |
|------|-------------|
| `PicInPic` | Picture-in-Picture: shrinks the original video and embeds it in a new background |
| `BackgroundExtend` | Video Expansion: inserts extended frames at scene transitions |
| `VerticalExtend` | Vertical Extend (also known as "vertical fill"): adds padding content in the vertical direction. **Always use `VerticalExtend`, never `VerticalFill`** |
| `HorizontalExtend` | Horizontal Extend: adds padding content in the horizontal direction |

> **Default Mode**: When `--mode` is not specified, `PicInPic` is used automatically.
> **Fine-grained Control**: Each mode supports additional fine-grained parameters. If needed, please [contact Tencent Cloud](https://cloud.tencent.com/document/product/862/124394) for offline consultation to confirm specific configurations.

## Mandatory Rules

1. When the user says "video deduplication", "video anti-duplication", or "bypass duplicate detection", **this script must be used** (`mps_dedupe.py`), not `mps_vremake.py`.
2. The `--mode` parameter **can be omitted**, defaulting to `PicInPic` (Picture-in-Picture). If the user does not specify a mode, **use the default value directly without asking**.
3. If the user explicitly requests another mode, select accordingly: "vertical extend" or "vertical fill" → `VerticalExtend`, "horizontal extend" or "horizontal fill" → `HorizontalExtend`, "video expansion" or "background extend" → `BackgroundExtend`. **Always use the exact enum value from the mode table above.**

## Parameter Reference

| Parameter | Description |
|-----------|-------------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL (HTTP/HTTPS) |
| `--cos-input-key` | COS input file Key (e.g., `/input/video.mp4`, recommended) |
| `--cos-input-bucket` | COS Bucket name for the input file (defaults to environment variable) |
| `--cos-input-region` | COS Region for the input file (e.g., `ap-guangzhou`) |
| `--mode` | Deduplication mode (default `PicInPic`, see table above) |
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` environment variable) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` environment variable) |
| `--output-cos-dir` | COS output directory (default `/output/dedupe/`), must start and end with `/` |
| `--no-wait` | Async mode: submits the task only, returns TaskId, does not wait for results |
| `--json` | JSON format output |
| `--output-dir` | Save the result JSON to the specified directory |
| `--download-dir` | Download the output video to the specified local directory after task completion (if not specified, only prints the output path and pre-signed URL) |
| `--definition` | AI Analysis Task template ID (default `29`) |
| `--region` | Processing region (reads `TENCENTCLOUD_API_REGION` environment variable first, defaults to `ap-guangzhou`) |
| `--dry-run` | Print parameter preview only (including Extended Parameter), does not call the API |

## Example Commands

```bash
# Simplest usage (default PicInPic mode, automatically waits for completion)
python scripts/mps_dedupe.py --url https://example.com/video.mp4

# Vertical Fill deduplication
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode VerticalExtend

# Horizontal Fill deduplication
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode HorizontalExtend

# Video Expansion deduplication (COS input)
python scripts/mps_dedupe.py --cos-input-key /input/video.mp4 \
    --mode BackgroundExtend

# Local file (automatically uploaded to COS)
python scripts/mps_dedupe.py --local-file ./video.mp4

# Async submission (no waiting; use mps_get_video_task.py to query with the returned TaskId)
python scripts/mps_dedupe.py --url https://example.com/video.mp4 --no-wait

# Automatically download results to local after completion
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --download-dir /data/workspace/output/

# dry-run preview
python scripts/mps_dedupe.py --url https://example.com/video.mp4 \
    --mode BackgroundExtend --dry-run
```