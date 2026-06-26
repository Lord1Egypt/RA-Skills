# Image Inpainting Parameters & Examples — `mps_image_repaint.py`

**Function**: Calls the MPS `ProcessImage` API to initiate an image inpainting task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path or downloads the result locally.

Applicable scenarios: partial product image editing, ad creative retouching, defect removal and repainting, scene replacement, creative visual editing, etc.

---

## Parameter Description

### Input Parameters (Source Image)

| Parameter | Description |
|-----------|-------------|
| `--url` | Source image URL (choose one from `--url`, `--cos-input-key`, and `--local-file`) |
| `--cos-input-key` | Source image COS object key (e.g. `/input/photo.jpg`) |
| `--local-file` | Local source image path (automatically uploaded to COS before processing) |
| `--cos-input-bucket` | Input COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cos-input-region` | Input COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

### Input Parameters (Mask Image)

| Parameter | Description |
|-----------|-------------|
| `--mask-url` | Mask image URL (required, choose one from `--mask-url` and `--mask-cos-key`) |
| `--mask-cos-key` | Mask image COS object key (required, choose one from `--mask-url` and `--mask-cos-key`) |
| `--mask-cos-bucket` | Mask image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--mask-cos-region` | Mask image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify one of `--url`, `--cos-input-key`, or `--local-file` for the source image. You must also specify either `--mask-url` or `--mask-cos-key` for the mask image.

### Task-Specific Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompt` | — (**required**) | Editing instruction describing what should be generated in the masked area (for example, `"blue sky"` or `"a red rose"`) |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/repaint/` | Output directory |
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

1. **The mask image must be in RGBA format (with an Alpha channel)**. The Alpha channel marks the repaint region (`Alpha=255` means repaint, `Alpha=0` means keep unchanged).
2. **`--prompt` is required** and describes what should be generated in the masked region; omitting it causes the script to exit with an error.
3. The mask image is passed in `AddOnParameter` through `ImageSet` with `Type="mask"`.
4. `ScheduleId=30061`.
5. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
6. To manually query repaint task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: source image URL + mask image URL
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "blue sky and white clouds"

# Local source image + URL mask image
python scripts/mps_image_repaint.py \
    --local-file /tmp/room.jpg \
    --mask-url "https://example.com/mask.png" \
    --prompt "a green plant"

# COS source image + COS mask image
python scripts/mps_image_repaint.py \
    --cos-input-key "/input/scene.jpg" \
    --mask-cos-key "/input/mask.png" \
    --prompt "a white cat"

# Mask image from a non-default Bucket
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-cos-key "/masks/area.png" \
    --mask-cos-bucket mybucket-125xxx \
    --mask-cos-region ap-shanghai \
    --prompt "red flowers"

# Custom output path
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "wooden floor" \
    --output-path "/output/repaint/custom_result.jpg"

# Submit task only without waiting for result
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "green grass" \
    --no-wait

# Download result to a local directory after completion
python scripts/mps_image_repaint.py \
    --url "https://example.com/photo.jpg" \
    --mask-url "https://example.com/mask.png" \
    --prompt "marble texture" \
    --download-dir /tmp/results/

# Manually query repaint task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-fGHI6789JK0123",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:12Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/repaint/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/repaint/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/repaint/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit an inpainting task with `ScheduleId=30061`; the mask is passed through `AddOnParameter.ImageSet` with `Type="mask"` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
