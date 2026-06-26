# Change-Model Parameters & Examples — `mps_image_changemodel.py`

**Function**: Based on a **source model image** and a **garment image**, calls the MPS `ProcessImage` API to initiate a change-model / body-shape transformation task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path or downloads the result locally.

Applicable scenarios: e-commerce model replacement, showcasing the same outfit on different body types, cross-body try-on previews, advertising asset customization, etc.

---

## Parameter Description

### Input Parameters (Source Image)

| Parameter | Description |
|-----------|-------------|
| `--url` | Source image URL (choose one from `--cos-input-key`, `--local-file`, and `--url`) |
| `--cos-input-key` | Source image COS object key (e.g. `/input/model.jpg`) |
| `--cos-input-bucket` | Source image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cos-input-region` | Source image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |
| `--local-file` | Local source image path (automatically uploaded to COS before processing) |

### Input Parameters (Garment Image)

| Parameter | Description |
|-----------|-------------|
| `--garment-url` | Garment image URL (required, choose one from `--garment-url` and `--garment-cos-key`) |
| `--garment-cos-key` | Garment image COS object key (required, choose one from `--garment-url` and `--garment-cos-key`) |
| `--garment-cos-bucket` | Garment image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--garment-cos-region` | Garment image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify one of `--url`, `--cos-input-key`, or `--local-file` for the source image. You must also specify either `--garment-url` or `--garment-cos-key` for the garment image.

### Task-Specific Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--body-shape` | `hourglass` | Target body shape: `hourglass` / `rectangle` / `plus-size` / `apple` / `pear` |
| `--precision-scale` | `1.0` | Precision scale (float, 0.01–2.0). Higher values improve accuracy but increase processing time |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/changemodel/` | Output directory |
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

1. **A garment image is required**: you must specify either `--garment-url` or `--garment-cos-key`, otherwise the script exits with an error.
2. Change-model configuration is passed through `StdExtInfo.ChangeGarmentModelConfig`; the garment image is passed through `AddOnParameter.ImageSet` with `Type="garment"`; `ScheduleId=30110`.
3. **Larger `--precision-scale` values improve detail accuracy but slow processing**: the default `1.0` is suitable for most cases; for detail-sensitive scenarios, you can increase it to `1.5–2.0`, but processing time may double.
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query change-model task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: source image URL + garment image URL (default body shape: hourglass)
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg"

# Set target body shape to pear
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --body-shape pear

# Plus-size body shape
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/coat.jpg" \
    --body-shape plus-size

# Increase precision for detail-sensitive scenarios
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --precision-scale 1.5

# Local source image + COS garment image
python scripts/mps_image_changemodel.py \
    --local-file /tmp/model.jpg \
    --garment-cos-key "/input/garment.jpg"

# COS source image + COS garment image
python scripts/mps_image_changemodel.py \
    --cos-input-key "/input/model.jpg" \
    --garment-cos-key "/input/garment.jpg"

# Garment image from a non-default Bucket
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-cos-key "/clothes/summer_dress.jpg" \
    --garment-cos-bucket mybucket-125xxx \
    --garment-cos-region ap-shanghai

# Submit task only without waiting for result
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_changemodel.py \
    --url "https://example.com/model.jpg" \
    --garment-url "https://example.com/dress.jpg" \
    --download-dir /tmp/results/

# Manually query change-model task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-hIJK8901LM2345",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:18Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/changemodel/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/changemodel/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/changemodel/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit a change-model task with `ScheduleId=30110`, configured through `StdExtInfo.ChangeGarmentModelConfig` + `AddOnParameter.ImageSet` (`Type="garment"`) |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
