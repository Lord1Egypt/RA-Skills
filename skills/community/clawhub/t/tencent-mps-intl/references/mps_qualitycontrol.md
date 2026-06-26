# Media Quality Control Parameters & Examples — `mps_qualitycontrol.py`

**Function**: Audio/video quality detection, supporting three modes: video quality inspection, playback compatibility detection, and audio quality inspection.
> ⚠️ "Quality detection", "blur", "screen corruption", "playback compatibility", "audio quality inspection" → Must use this script, do NOT use `mps_erase.py`.

## Quality Control Templates

| Template ID | Name | Use Case |
|---------|------|---------|
| `50` | Audio Detection | Audio quality / audio event detection |
| `60` | Format QC - Pro Edition (**Default**) | Image blur, screen corruption, frame damage, and other content issues |
| `70` | Content QC - Pro Edition | Playback stuttering, playback anomalies, playback compatibility issues |

## Parameter Description

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Video URL address |
| `--cos-input-key` | COS input file Key (e.g., `/input/video.mp4`, recommended) |
| `--cos-input-bucket` | COS Bucket name for the input file (defaults to environment variable) |
| `--cos-input-region` | COS Region for the input file (e.g., `ap-guangzhou`) |
| `--definition` | Quality control template ID (default `60`). `50`: Audio QC; `60`: Format QC (image blur/screen corruption, etc.); `70`: Content QC (playback compatibility) |
| `--no-wait` | Submit task only, do not wait for results (exits after returning TaskId) |
| `--json` | Output results in JSON format |
| `--output-bucket` | Output COS Bucket name (defaults to environment variable) |
| `--output-region` | Output COS Region (defaults to environment variable) |
| `--output-dir` | Output directory path (e.g., `/output/quality_control/`) |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, defaults to `ap-guangzhou`) |
| `--notify-url` | Task completion callback URL (optional) |
| `--dry-run` | Print parameters only, do not call the API |

## Mandatory Rules

- **You must select the corresponding template based on the user's described scenario**; do not arbitrarily use the default value:
  - User mentions "audio quality inspection", "noise detection", "silence detection", "audio event" → **Must use `--definition 50`**
  - User mentions "quality detection", "blur", "screen corruption", "frame damage", "video quality" → **Must use `--definition 60`** (default)
  - User mentions "playback compatibility", "stuttering", "playback anomaly", "playback failure" → **Must use `--definition 70`**
- If the user's description is ambiguous and the scenario cannot be determined, use the default value `60` and inform the user accordingly

## Example Commands

```bash
# Video quality inspection (default, template 60)
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4

# Specify video quality inspection template
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 60

# Playback compatibility inspection (template 70)
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70

# Audio quality inspection (template 50)
python scripts/mps_qualitycontrol.py --url https://example.com/audio.mp3 --definition 50

# COS input (recommended usage)
python scripts/mps_qualitycontrol.py --cos-input-key /input/video.mp4

# Async submission
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --no-wait

# Query existing task result (JSON format)
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx

# dry-run preview
python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70 --dry-run
```