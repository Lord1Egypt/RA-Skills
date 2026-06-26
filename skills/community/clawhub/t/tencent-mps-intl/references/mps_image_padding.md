# Image Outpainting Parameters & Examples — `mps_image_padding.py`

**Function**: Calls the MPS `ProcessImage` API to initiate an image outpainting / canvas expansion task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path or downloads the result locally.

Applicable scenarios: e-commerce main image expansion, social media cover adaptation, portrait-to-landscape conversion, poster canvas expansion, etc.

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|-----------|-------------|
| `--url` | Input image URL (choose one from `--url`, `--cos-input-key`, and `--local-file`) |
| `--cos-input-key` | Input image COS object key (e.g. `/input/photo.jpg`) |
| `--local-file` | Local image path (automatically uploaded to COS before processing) |
| `--cos-input-bucket` | Input COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cos-input-region` | Input COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify one of `--url`, `--cos-input-key`, or `--local-file` as the input source.

### Task-Specific Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--aspect-ratio` | — | Target aspect ratio (string, such as `"16:9"`, `"1:1"`, `"9:16"`) |
| `--image-width` | — | Target width in pixels (int) |
| `--image-height` | — | Target height in pixels (int) |

> **Note**: At least one of `--aspect-ratio`, `--image-width`, or `--image-height` must be specified.

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/padding/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (returns TaskId and exits) |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 600) |
| `--dry-run` | Preview the API request parameters without making an actual call |
| `--download-dir` | Download the result to the specified local directory after task completion |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **At least one outpainting parameter is required**: `--aspect-ratio`, `--image-width`, and `--image-height` cannot all be empty.
2. **Output size around the 1K range is recommended** (such as 1024×1024). Resolutions above 2K are not recommended because they may reduce generation quality or cause timeouts.
3. Outpainting configuration is passed through `AddOnParameter.OutputConfig`; `ScheduleId=30010`.
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query outpainting task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: expand to 16:9 by aspect ratio
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9"

# Convert portrait image to landscape
python scripts/mps_image_padding.py \
    --url "https://example.com/vertical.jpg" \
    --aspect-ratio "16:9"

# Specify target width and height in pixels
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --image-width 1920 --image-height 1080

# Specify only target width
python scripts/mps_image_padding.py \
    --local-file /tmp/product.jpg \
    --image-width 1024

# Local file input, square canvas
python scripts/mps_image_padding.py \
    --local-file /tmp/product.jpg \
    --aspect-ratio "1:1"

# COS path input
python scripts/mps_image_padding.py \
    --cos-input-key "/input/banner.jpg" \
    --aspect-ratio "21:9"

# Submit task only without waiting for result
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9" \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_padding.py \
    --url "https://example.com/photo.jpg" \
    --aspect-ratio "16:9" \
    --download-dir /tmp/results/

# Manually query outpainting task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-bCDE2345FG6789",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:15Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/padding/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/padding/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/padding/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit an outpainting task with `ScheduleId=30010`, configured through `AddOnParameter.OutputConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
