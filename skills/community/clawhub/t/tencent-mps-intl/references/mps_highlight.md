# Highlight Reel Parameters & Examples — `mps_highlight.py`

**Feature**: AI automatically extracts video highlight clips (highlight reels), supporting VLOG, short drama, football, basketball, custom, and other scenarios.
> **Core Mechanism**: `AI Analysis Task.Definition=26` + `Extended Parameter(hht scenario parameters)`.
> The script **synchronously waits** for task completion by default; add `--no-wait` to only submit the task and return the TaskId.
> ⚠️ **Only supports offline files, not live streams**; Extended Parameter must be selected from preset scenarios — **do not assemble manually**.

## Preset Scenarios

| Scenario Value | Description | Billing Version | Supports --top-clip |
|--------|------|---------|----------------|
| `vlog` | VLOG, scenery, drone videos | Large Model Edition | ✅ |
| `vlog-panorama` | Panoramic camera (with panoramic optimization enabled) | Large Model Edition | ✅ |
| `short-drama` | Short dramas, TV series — extracts protagonist appearances / BGM highlights | Large Model Edition | ❌ |
| `football` | Football matches — recognizes shots/goals/red & yellow cards/replays | Advanced Edition | ❌ |
| `basketball` | Basketball matches | Advanced Edition | ❌ |
| `custom` | Custom scenario — supports `--prompt` and `--scenario` | Large Model Edition | ✅ |

## Parameter Description

| Parameter | Description |
|------|------|
| `--local-file` | Local file path; automatically uploaded to COS before processing (mutually exclusive with `--cos-input-*`) |
| `--url` | Input video URL (HTTP/HTTPS) |
| `--cos-input-bucket` | Input COS Bucket name (used with `--cos-input-region`/`--cos-input-key`, recommended) |
| `--cos-input-region` | Input COS Bucket region (e.g., `ap-guangzhou`) |
| `--cos-input-key` | Input COS object key (e.g., `/input/video.mp4`, **recommended**) |
| `--scene` | **Required**. Preset scenario (see table above) |
| `--prompt` | Custom scenario description (only effective with `--scene custom`, optional) |
| `--scenario` | Custom scenario name (only effective with `--scene custom`, optional) |
| `--top-clip` | Maximum number of highlight clips to output (only available for `vlog` / `vlog-panorama` / `custom` scenarios, default 5) |
| `--output-bucket` | Output COS Bucket |
| `--output-region` | Output COS Region |
| `--output-dir` | Output directory, default `/output/highlight/` |
| `--output-object-path` | Output file path template, e.g., `/output/{inputName}_highlight.{format}` |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, default `ap-guangzhou`) |
| `--notify-url` | Task completion callback URL |
| `--no-wait` | Only submit the task without waiting for results (exits after returning TaskId) |
| `--poll-interval` | Polling interval (seconds), default 10 |
| `--max-wait` | Maximum wait time (seconds), default 1800 (highlight reel extraction takes longer) |
| `--download-dir` | Download output files to the specified local directory after task completion (by default, only prints pre-signed URLs) |
| `--dry-run` | Only print parameter preview without calling the API |
| `--verbose` / `-v` | Output detailed information |

## Mandatory Rules

- `--scene` is **required**; the value must be one of the preset enums: `vlog` | `vlog-panorama` | `short-drama` | `football` | `basketball` | `custom`
  - When the user mentions keywords like "basketball" / "football" / "short drama" / "VLOG", map directly to the corresponding `--scene` without further confirmation
  - **If the user does not mention any type keyword**: use `--scene custom` and generate the command directly with an appropriate `--prompt` based on the user's description. Do not ask the user to choose a scene.
- `--top-clip` is only allowed in `vlog` / `vlog-panorama` / `custom` scenarios
- `--prompt` and `--scenario` only take effect with `--scene custom`, but neither is required
- Do not generate Extended Parameter fields or values outside the preset table
- ⚠️ This script **only supports processing offline files, not live streams** (live streams require direct MPS API calls)

## Example Commands

```bash
# Football match highlight reel
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football

# Basketball match
python scripts/mps_highlight.py --cos-input-key /input/basketball.mp4 --scene basketball

# Short drama / TV series highlights
python scripts/mps_highlight.py --cos-input-key /input/drama.mp4 --scene short-drama

# VLOG panoramic camera
python scripts/mps_highlight.py --url https://example.com/vlog.mp4 --scene vlog-panorama

# Regular VLOG (specify max 10 output clips)
python scripts/mps_highlight.py --cos-input-key /input/vlog.mp4 --scene vlog --top-clip 10

# Custom scenario (with prompt and scenario)
python scripts/mps_highlight.py --url https://example.com/skiing.mp4 \
    --scene custom --prompt "Skiing scenario, output character highlights" --scenario "skiing"

# Custom scenario + specify clip count
python scripts/mps_highlight.py --url https://example.com/skiing.mp4 \
    --scene custom --prompt "Skiing scenario" --scenario "skiing" --top-clip 8

# Only submit task without waiting for results
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football --no-wait

# Dry Run (preview request parameters)
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football --dry-run

# Query task status
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx
```