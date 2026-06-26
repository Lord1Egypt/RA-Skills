# Multi-View Image Generation Parameters & Examples — `mps_image_multiview.py`

**Function**: Calls the MPS `ProcessImage` API to initiate a multi-view image generation task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path or downloads the result locally.

Applicable scenarios: 3D product showcase, multi-angle product preview, e-commerce detail page asset generation, virtual showroom display, etc.

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|-----------|-------------|
| `--url` | Input image URL (choose one from `--url`, `--cos-input-key`, and `--local-file`) |
| `--cos-input-key` | Input image COS object key (e.g. `/input/product.jpg`) |
| `--local-file` | Local image path (automatically uploaded to COS before processing) |
| `--cos-input-bucket` | Input COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cos-input-region` | Input COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify one of `--url`, `--cos-input-key`, or `--local-file` as the input source.

### Task-Specific Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--horizontal-angle` | `0` | Horizontal rotation angle (int, range: -180 to 180) |
| `--vertical-angle` | `0` | Vertical rotation angle (int, range: -30 to 60) |
| `--zoom` | `medium` | Zoom level: `wide` / `medium` / `close` |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/multiview/` | Output directory |
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

1. Multi-view configuration is passed through `StdExtInfo.MultiViewConfig`; `ScheduleId=30070`.
2. **Horizontal angle range restriction**: `--horizontal-angle` must be between `-180` and `180`; values outside this range cause an error.
3. **Vertical angle range restriction**: `--vertical-angle` must be between `-30` and `60`; values outside this range cause an error.
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query multi-view task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: default parameters (front view)
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg"

# Rotate horizontally by 45 degrees
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 45

# Top-down angle (vertical rotation by 30 degrees)
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --vertical-angle 30

# Combined rotation + close-up view
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle -90 \
    --vertical-angle 15 \
    --zoom close

# Wide shot view
python scripts/mps_image_multiview.py \
    --local-file /tmp/shoe.jpg \
    --horizontal-angle 180 \
    --zoom wide

# COS path input
python scripts/mps_image_multiview.py \
    --cos-input-key "/input/bag.jpg" \
    --horizontal-angle 60

# Submit task only without waiting for result
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 45 \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_multiview.py \
    --url "https://example.com/product.jpg" \
    --horizontal-angle 90 \
    --download-dir /tmp/results/

# Manually query multi-view task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-dEFG4567HI8901",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:10Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/multiview/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/multiview/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/multiview/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit a multi-view generation task with `ScheduleId=30070`, configured through `StdExtInfo.MultiViewConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
