# Image Try-On Parameters and Examples — `mps_image_tryon.py`

**Feature**: Based on a **model image** and **clothing image(s)**, calls the MPS `ProcessImage` API to initiate an AI try-on task (`ImageTask.AiTryOnConfig`),
polls via `DescribeImageTaskDetail` for results, and returns the output path or presigned download URL.

Applicable scenarios: E-commerce clothing try-on, product display image generation, ad creative material generation, clothing effect preview, etc.

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|------|------|
| `--model-url` | Model image URL (**mutually exclusive** with `--model-cos-key`) |
| `--model-cos-key` | Model image COS object Key (e.g., `/input/model.jpg`), mutually exclusive with `--model-url` |
| `--model-cos-bucket` | Model image COS Bucket (default reads `TENCENTCLOUD_COS_BUCKET`) |
| `--model-cos-region` | Model image COS Region (default reads `TENCENTCLOUD_COS_REGION`) |
| `--cloth-url` | Clothing image URL, can be repeated 1-4 times; can be mixed with `--cloth-cos-key` |
| `--cloth-cos-key` | Clothing image COS object Key, can be repeated 1-4 times; can be mixed with `--cloth-url` |
| `--cloth-cos-bucket` | Clothing image COS Bucket (default reads `TENCENTCLOUD_COS_BUCKET`) |
| `--cloth-cos-region` | Clothing image COS Region (default reads `TENCENTCLOUD_COS_REGION`) |

> **Note**: The model image must specify one of `--model-url` or `--model-cos-key`; 1-4 clothing images (`--cloth-url` or `--cloth-cos-key`). Both can be mixed, e.g., URL for model image and COS for clothing image.

### Try-On Parameters

| Parameter | Default | Description |
|------|--------|------|
| `--model` | `WAND-tryon-1.0-flash` | Try-on model: `WAND-tryon-1.0-lite` (lightweight) / `WAND-tryon-1.0-flash` (fast) / `WAND-tryon-1.0-pro` (professional) |
| `--prompt` | — | Try-on instruction (optional; uses built-in default when empty) |
| `--resource-id` | — | Optional resource ID (business-side exclusive resource) |

### Output Parameters

| Parameter | Default | Description |
|------|--------|------|
| `--resolution` | `1K` | Output resolution: `1K` / `2K` / `4K` |
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/tryon/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |

### Task Control

| Parameter | Description |
|------|------|
| `--no-wait` | Only submit task, do not wait for result (exit after returning TaskId) |
| `--dry-run` | Only print request parameters, do not actually call the API |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 600) |
| `--region` | MPS API access region (default reads `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **1-4 clothing images**; more than 4 will cause an error and exit.
2. URL input must be publicly accessible; COS input requires that the MPS service has permission to read files in the corresponding Bucket.
3. Task `Status=FINISH` does not equal success; you must also check whether `ErrMsg` is empty.
4. The script waits for task completion by default; if you only need to submit and get TaskId, add `--no-wait`.
5. Use `mps_get_image_task.py` to manually query try-on task status; do not use `mps_get_video_task.py`.
6. The new API uses `ImageTask.AiTryOnConfig`; `ScheduleId` is no longer used to distinguish scenarios.

---

## Example Commands

```bash
# Minimal usage: model image + 1 clothing image (URL, default COS output)
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# Specify model
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --model WAND-tryon-1.0-pro

# Model image using COS path input
python3 scripts/mps_image_tryon.py \
    --model-cos-key "/input/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg"

# Multiple clothing images (1-4 images)
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth-front.jpg" \
    --cloth-url "https://example.com/cloth-back.jpg"

# Additional prompt
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --prompt "Change the shirt to red"

# Specify resolution + model
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --model WAND-tryon-1.0-pro --resolution 4K

# Submit task only, do not wait for result
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --no-wait

# Specify COS output Bucket and directory
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --output-bucket mybucket-125xxx --output-region ap-shanghai \
    --output-dir /custom/output/

# Preview request parameters (do not actually submit)
python3 scripts/mps_image_tryon.py \
    --model-url "https://example.com/model.jpg" \
    --cloth-url "https://example.com/cloth.jpg" \
    --dry-run

# Manually query try-on task status
python3 scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

Task completion output JSON:

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
|------|------|
| `ProcessImage` | Submit AI try-on task, `ImageTask.AiTryOnConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
- [AiTryOnConfig Parameter Description](https://cloud.tencent.com/document/api/862/37615#AiTryOnConfig)
