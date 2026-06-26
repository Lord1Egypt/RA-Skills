# Precise Cutout Parameters & Examples — `mps_image_cutout.py`

**Function**: Calls the MPS `ProcessImage` API to initiate a precise image cutout task and outputs a transparent-background PNG image, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path or downloads the result locally.

Applicable scenarios: product cutout, portrait cutout, ID photo background removal, asset production, e-commerce compositing, etc.

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
| `--transparency-threshold` | `30` | Transparency threshold (int). Pixels below this value are treated as transparent |
| `--opaque-threshold` | `127` | Opaque threshold (int). Pixels above this value are treated as opaque |
| `--edge-sampling-step` | `5` | Edge sampling step (int). Smaller values produce finer edges but slower processing |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/cutout/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (returns TaskId and exits) |
| `--poll-interval` | Polling interval in seconds (default 5) |
| `--timeout` | Maximum wait time in seconds (default 300) |
| `--dry-run` | Preview the API request parameters without making an actual call |
| `--download-dir` | Download the result to the specified local directory after task completion |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **The output is a transparent-background PNG image**; non-transparent formats such as JPEG are not supported.
2. Cutout configuration is passed through `StdExtInfo.CutoutConfig`; `ScheduleId=30030`.
3. For **fine-edge objects** (such as hair strands or leaf gaps), it is recommended to reduce `--edge-sampling-step` (for example, to `2` or `3`) for more refined edge quality.
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query cutout task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: URL input, wait for result
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg"

# Local file input
python scripts/mps_image_cutout.py \
    --local-file /tmp/photo.jpg

# COS path input
python scripts/mps_image_cutout.py \
    --cos-input-key "/input/model.jpg"

# Fine-edge cutout (suitable for hair and other details)
python scripts/mps_image_cutout.py \
    --url "https://example.com/portrait.jpg" \
    --edge-sampling-step 2

# Adjust transparency thresholds
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --transparency-threshold 20 \
    --opaque-threshold 150

# Submit task only without waiting for result
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_cutout.py \
    --url "https://example.com/product.jpg" \
    --download-dir /tmp/results/

# Manually query cutout task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-aBCD1234EF5678",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:05Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/cutout/result.png",
      "cos_uri": "cos://mps-bucket-125xxx/output/cutout/result.png",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/cutout/result.png"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit a cutout task with `ScheduleId=30030`, configured through `StdExtInfo.CutoutConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
