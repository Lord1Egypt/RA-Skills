# Query Task Parameters & Examples — `mps_get_video_task.py` / `mps_get_image_task.py`

## Query Audio/Video Tasks — `mps_get_video_task.py`

Applicable to tasks submitted via `ProcessMedia` (TaskId format: `1234567890-WorkflowTask-xxxxxx`)

### Parameter Description

| Parameter | Description |
|------|------|
| `--task-id` | Task ID (required) |
| `--verbose` / `-v` | Output full JSON response (including all subtask details) |
| `--json` | Output raw JSON only, without formatted summary |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, defaults to `ap-guangzhou`) |

### Example Commands

```bash
# Query task status (concise output)
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a

# Verbose output (including subtask information)
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --verbose

# JSON format output (convenient for programmatic parsing)
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --json

# Specify region
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --region ap-beijing
```

---

## Query Image Tasks — `mps_get_image_task.py`

Applicable to tasks submitted via `ProcessImage`

### Parameter Description

| Parameter | Description |
|------|------|
| `--task-id` | Task ID (required) |
| `--verbose` / `-v` | Output full JSON response |
| `--json` | Output raw JSON only |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` environment variable first, defaults to `ap-guangzhou`) |

### Example Commands

```bash
# Query task status (concise output)
python scripts/mps_get_image_task.py --task-id 1234567890-Image Task-80108cc3380155d98b2e3573a48a

# Verbose output (including subtask information)
python scripts/mps_get_image_task.py --task-id 1234567890-Image Task-80108cc3380155d98b2e3573a48a --verbose

# JSON format output
python scripts/mps_get_image_task.py --task-id 1234567890-Image Task-80108cc3380155d98b2e3573a48a --json

# Specify region
python scripts/mps_get_image_task.py --task-id 1234567890-Image Task-80108cc3380155d98b2e3573a48a --region ap-beijing
```

## Mandatory Rules

1. **Must ask when task type is unknown**: When the user only says "query task xxx" without specifying the task type, you **must first ask** about the task type (audio/video, image, AIGC image generation, or AIGC video generation) — do not guess and call directly.
2. **AIGC tasks must not be queried with this script**: AIGC image/video generation tasks have their own dedicated query methods (`mps_aigc_image.py --task-id` / `mps_aigc_video.py --task-id`) and **must not** be queried using `mps_get_video_task.py` or `mps_get_image_task.py`.
3. **TaskId containing WorkflowTask does not indicate task type**: Both audio/video processing and image processing task IDs may contain `WorkflowTask` — you **cannot** determine the type based on this alone and must still ask the user.