# Image Try-On Parameters & Examples — `mps_image_tryon.py`

**Function**: Based on a **model image** and a **clothing image**, calls the MPS `ProcessImage` API to initiate an AI try-on task, polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path.

Applicable scenarios: e-commerce clothing try-on, product showcase image generation, advertising creative asset generation, clothing effect preview, etc.

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|-----------|-------------|
| `--model-url` | Model image URL (mutually exclusive with `--model-cos-key`) |
| `--model-cos-key` | Model image COS object key (e.g., `/input/model.jpg`), mutually exclusive with `--model-url` |
| `--model-cos-bucket` | Model image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--model-cos-region` | Model image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |
| `--cloth-url` | Clothing image URL, can be specified 1–2 times; can be mixed with `--cloth-cos-key` |
| `--cloth-cos-key` | Clothing image COS object key, can be specified 1–2 times; can be mixed with `--cloth-url` |
| `--cloth-cos-bucket` | Clothing image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--cloth-cos-region` | Clothing image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify either `--model-url` or `--model-cos-key` for the model image; at least one clothing image must be specified (`--cloth-url` or `--cloth-cos-key`). They can be mixed — for example, using a URL for the model image and COS for the clothing image.

### Try-On Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--schedule-id` | `30100` | Try-on scene ID: `30100` = regular clothing, `30101` = underwear |
| `--ext-prompt` | — | Additional prompt, can be specified multiple times (e.g., `"shirt buttons open"`) |
| `--random-seed` | — | Random seed; a fixed seed produces consistent style |
| `--resource-id` | — | Optional resource ID (business-specific resource) |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/tryon/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |
| `--format` | `JPEG` | Output format: `JPEG` / `PNG` |
| `--image-size` | `2K` | Output size: `1K` / `2K` / `4K` |
| `--quality` | `85` | Output quality 1–100 |

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (exits after returning TaskId) |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 600) |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **`--schedule-id 30101` (underwear scene) only accepts 1 clothing image** — passing multiple images will cause an error and exit.
2. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read files from the corresponding Bucket.
3. Task `Status=FINISH` does not necessarily mean success — you must also check whether `ErrMsg` is empty.
4. The script waits for task completion by default; to only submit and obtain the TaskId, add `--no-wait`.
5. To manually check try-on task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: model image + 1 clothing image (URL, wait for result)
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# Model image using COS path input
python scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# Both model image and clothing image using COS path input (using default Bucket from environment variables)
python scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-cos-key "/input/cloth.jpg"

# Clothing image using COS with a non-default Bucket
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-cos-key "/input/cloth.jpg" \
    --cloth-cos-bucket mybucket-125xxx --cloth-cos-region ap-shanghai

# Multiple clothing images (front + back, improves try-on quality)
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth-front.jpg" \
    --cloth-url "https://example.com/cloth-back.jpg"

# Underwear scene (only supports 1 clothing image)
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/underwear.jpg" \
    --schedule-id 30101

# Additional prompt + fixed random seed
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --ext-prompt "shirt buttons open" \
    --random-seed 48

# Specify output format and size
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --format PNG --image-size 4K

# Submit task only without waiting for result (returns TaskId)
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --no-wait

# Manually check try-on task status
python scripts/mps_get_image_task.py --task-id <TaskId>

# Download try-on result to local after task completion
# Step 1: run try-on task (result is saved to COS output path)
python scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"
# Step 2: download output from COS to local file
python scripts/mps_cos_download.py \
    --cos-input-key /output/tryon/result.jpeg \
    --local-file /tmp/tryon_result.jpg
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-b8dac8f326214464acef88afef9002d4",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T01:02:51Z",
  "FinishTime": "2025-05-21T01:02:52Z",
  "Outputs": [
    {
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/tryon/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/tryon/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/tryon/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit a try-on task with `ScheduleId=30100` (regular clothing) or `30101` (underwear) |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)