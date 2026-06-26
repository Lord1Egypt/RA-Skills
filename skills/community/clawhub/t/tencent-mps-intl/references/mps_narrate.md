# AI Narration Remix Parameters & Examples — `mps_narrate.py`

**Function**: Input the original short drama video, and automatically complete narration script generation, AI voiceover, and subtitle removal in one stop, outputting a new video with narration.
> **Core Mechanism**: `AI Analysis Task.Definition=35` + `Extended Parameter(reelProcessType=narrate + scene parameters)`.
> The script **synchronously waits** for task completion by default; add `--no-wait` to only submit the task and return the TaskId.

## Preset Scenes

| Scene Value | Description | Erasure Setting |
|-------------|-------------|-----------------|
| `short-drama` | Short drama video with on-screen subtitles (default) | Erasure enabled |
| `short-drama-no-erase` | Short drama video without on-screen subtitles | Erasure disabled |

**Scene Selection Rules**:
- User says "has subtitles" / "with hardcoded subtitles" → use `short-drama`
- User says "no subtitles" / "original has no subtitles" / "don't erase" → use `short-drama-no-erase`

## Parameter Description

| Parameter | Description |
|-----------|-------------|
| `--local-file` | Local file path (first episode video), automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Input video URL (HTTP/HTTPS), first episode video |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object Key (e.g., `/input/video.mp4`, **recommended**) |
| `--extra-urls` | URL list for episode 2 and beyond (in order; resolution must match the first episode) |
| `--scene` | **Required**. Preset scene: `short-drama` / `short-drama-no-erase` |
| `--output-count` | Number of output videos, default 1, maximum 5 |
| `--output-bucket` | Output COS Bucket |
| `--output-region` | Output COS Region |
| `--output-dir` | Output directory, default `/output/narrate/` |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--notify-url` | Task completion callback URL |
| `--no-wait` | Submit task only, do not wait for results (exits after returning TaskId) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 |
| `--download-dir` | Download output files to the specified local directory after task completion (by default, only prints pre-signed URLs) |
| `--dry-run` | Print parameter preview only, do not call the API |
| `--verbose` / `-v` | Output detailed information |

> ⚠️ **Custom scripts not supported**: Custom narration scripts (`ScriptUrls`) are not supported as input; only MPS auto-generation is supported.
> ⚠️ **Multi-episode video resolution**: When appending multi-episode videos with `--extra-urls`, all videos must have the same resolution.

## Mandatory Rules

- `--scene` is **required**, and the value must be one of the preset enums: `short-drama` | `short-drama-no-erase`
  - When the user says "has subtitles" / "with hardcoded subtitles" → choose `short-drama` (includes erasure)
  - When the user says "no subtitles" / "original has no subtitles" / "don't erase" → choose `short-drama-no-erase`
  - **When the user does not specify the subtitle situation, you must ask first**: "Does the video contain hardcoded subtitles? Choose `short-drama` for videos with subtitles (auto subtitle erasure), or `short-drama-no-erase` for videos without subtitles." Do not guess and execute directly.
- For multi-episode videos, use `--url`/`--cos-input-key` for the first episode, and append subsequent episodes with `--extra-urls` in order
- Passing `ScriptUrls` related parameters is prohibited (custom script input is not supported)

## Example Commands

```bash
# Single episode short drama narration (with erasure by default)
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama

# COS object input
python scripts/mps_narrate.py --cos-input-key /input/drama.mp4 --scene short-drama

# Original video has no subtitles, disable erasure
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama-no-erase

# Multi-episode video combined narration (first episode with --url, subsequent episodes with --extra-urls)
python scripts/mps_narrate.py \
    --url https://example.com/ep01.mp4 \
    --extra-urls https://example.com/ep02.mp4 https://example.com/ep03.mp4 \
    --scene short-drama

# Output 3 different versions of the video
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --output-count 3

# Async submission (do not wait for results)
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --no-wait

# Dry Run (preview Extended Parameter)
python scripts/mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --dry-run

# Query task status
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx
```