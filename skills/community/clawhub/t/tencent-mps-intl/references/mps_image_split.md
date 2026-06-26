# Storyboard / Grid Image Split Parameters & Examples — `mps_image_split.py`

**Function**: Calls the MPS `ProcessImage` API to initiate a storyboard split / grid image split task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS paths or downloads the result locally.

Applicable scenarios: AI drama storyboard splitting, comic panel splitting, long e-commerce image segmentation, storyboard extraction, etc.

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|-----------|-------------|
| `--url` | Input image URL (choose one from `--url`, `--cos-input-key`, and `--local-file`) |
| `--cos-input-key` | Input image COS object key (e.g. `/input/storyboard.jpg`) |
| `--local-file` | Local image path (automatically uploaded to COS before processing) |
| `--cos-input-bucket` | Input COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cos-input-region` | Input COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify one of `--url`, `--cos-input-key`, or `--local-file` as the input source.

### Task-Specific Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--process-index` | — | Process only the specified frame index (int, 0-based). If omitted, all frames are processed |
| `--erase-text` / `--no-erase-text` | enabled | Whether to erase text in the split frames (enabled by default) |
| `--model-sampling` | `0.1` | Model sampling parameter (float): `0.1` = AI drama storyboard, `1.0` = comic panels, `0.85` = e-commerce with preserved text |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/split/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (returns TaskId and exits) |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 300) |
| `--dry-run` | Preview the API request parameters without making an actual call |
| `--download-dir` | Download the result to the specified local directory after task completion |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. Storyboard configuration is passed through `StdExtInfo.StoryboardConfig`; `ScheduleId=30050`.
2. **This task may take a relatively long time** (about 127 seconds). Make sure `--timeout` is large enough, or use `--no-wait`.
3. **For e-commerce scenarios**, it is recommended to use `--no-erase-text --model-sampling 0.85` to preserve textual content.
4. `--model-sampling` value meanings: `0.1` is suitable for AI drama storyboards (erase text), `1.0` is suitable for comic panels (preserve line art), and `0.85` is suitable for e-commerce images (preserve text).
5. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
6. To manually query split task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: AI drama storyboard split (default parameters)
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg"

# Comic panel split
python scripts/mps_image_split.py \
    --url "https://example.com/manga_page.jpg" \
    --model-sampling 1.0

# E-commerce scenario: preserve text
python scripts/mps_image_split.py \
    --url "https://example.com/product_long.jpg" \
    --no-erase-text \
    --model-sampling 0.85

# Process only a specific frame (frame 0)
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --process-index 0

# Local file input
python scripts/mps_image_split.py \
    --local-file /tmp/comic.jpg \
    --model-sampling 1.0

# COS path input
python scripts/mps_image_split.py \
    --cos-input-key "/input/drama_board.jpg"

# Do not erase text
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --no-erase-text

# Submit task only without waiting for result (recommended for long-running tasks)
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_split.py \
    --url "https://example.com/storyboard.jpg" \
    --download-dir /tmp/results/

# Manually query split task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-gHIJ7890KL1234",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:02:07Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_0.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_0.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_0.jpeg"
    },
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_1.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_1.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_1.jpeg"
    },
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/split/frame_2.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/split/frame_2.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/split/frame_2.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit a storyboard split task with `ScheduleId=30050`, configured through `StdExtInfo.StoryboardConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
