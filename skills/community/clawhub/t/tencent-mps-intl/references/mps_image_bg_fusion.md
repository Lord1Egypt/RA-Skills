# Image Background Fusion/Generation Parameters & Examples — `mps_image_bg_fusion.py`

**Function**: Based on a **subject image (foreground/product/main image)** and a **background image**, calls the MPS `ProcessImage` API to initiate an AI background fusion task,
or passes only the subject image + Prompt description to automatically generate a brand-new background (background generation mode).
Polls for results via `DescribeImageTaskDetail`, and finally returns the output COS path.

Use cases: E-commerce product image background replacement, advertising material background generation, product display scene customization, marketing creative image production, etc.

---

## Two Usage Modes

| Mode | Background Image Provided? | `--prompt` Purpose | Typical Scenario |
|------|------------|----------------|---------|
| **Background Fusion** | Yes (`--bg-url` or `--bg-cos-key`) | Additional requirement description for the fusion result (e.g., "Replace the leaves in the background with yellow"), optional | Fuse product image into a specified scene |
| **Background Generation** | No (no background image provided) | Full description for generating the background (e.g., "Minimalist white marble tabletop, soft natural light"), **required** | Generate a brand-new background from text |

---

## Parameter Description

### Input Parameters

| Parameter | Description |
|------|------|
| `--subject-url` | Subject image (foreground/product/main) URL (mutually exclusive with `--subject-cos-key`, **choose one**) |
| `--subject-cos-key` | Subject image COS object key (e.g., `/input/product.jpg`), mutually exclusive with `--subject-url` |
| `--subject-cos-bucket` | Subject image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--subject-cos-region` | Subject image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |
| `--bg-url` | Background image URL; if not provided, switches to background generation mode (mutually exclusive with `--bg-cos-key`, **choose one**) |
| `--bg-cos-key` | Background image COS object key (e.g., `/input/bg.jpg`), mutually exclusive with `--bg-url` |
| `--bg-cos-bucket` | Background image COS Bucket (defaults to `TENCENTCLOUD_COS_BUCKET`) |
| `--bg-cos-region` | Background image COS Region (defaults to `TENCENTCLOUD_COS_REGION`) |

> **Note**: You must specify either `--subject-url` or `--subject-cos-key` for the subject image; the background image is optional — omitting it activates background generation mode.

### Fusion/Generation Parameters

| Parameter | Default | Description |
|------|--------|------|
| `--prompt` | — | Background description or fusion requirement prompt; can be specified multiple times; **required in background generation mode** |
| `--random-seed` | — | Random seed; a fixed seed produces consistent style results |
| `--resource-id` | — | Optional resource ID (business-specific dedicated resource) |

### Output Parameters

| Parameter | Default | Description |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/bgfusion/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |
| `--format` | `JPEG` | Output format: `JPEG` / `PNG` |
| `--image-size` | `2K` | Output size: `1K` / `2K` / `4K` |
| `--quality` | `85` | Output quality 1-100 |

### Task Control

| Parameter | Description |
|------|------|
| `--no-wait` | Submit the task only without waiting for results (exits after returning TaskId) |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 600) |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **`--prompt` is required in background generation mode (when no background image is provided)**; omitting it will cause an error and exit.
2. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read files from the corresponding Bucket.
3. Task `Status=FINISH` does not necessarily mean success — you must also check whether `ErrMsg` is empty.
4. The script waits for task completion by default; to only submit and obtain the TaskId, add `--no-wait`.
5. To manually query background fusion/generation task status, use `mps_get_image_task.py` — do NOT use `mps_get_video_task.py`.
6. Only **1** background image can be provided (`--bg-url` or `--bg-cos-key`, choose one — multiple background images are not supported).

---

## Example Commands

```bash
# Background fusion: subject image + background image (URL, wait for result)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-url "https://example.com/background.jpg"

# Background fusion + additional Prompt (extra requirements for the fusion result)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-url "https://example.com/background.jpg" \
    --prompt "Replace the leaves in the background with yellow"

# Background generation: subject image only + Prompt (no background image)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "Minimalist white marble tabletop, soft natural light"

# Subject image using COS path input
python scripts/mps_image_bg_fusion.py \
    --subject-cos-key "/input/product.jpg" \
    --bg-url "https://example.com/background.jpg"

# Subject image + background image both using COS path input (using default Bucket from environment variables)
python scripts/mps_image_bg_fusion.py \
    --subject-cos-key "/input/product.jpg" \
    --bg-cos-key "/input/background.jpg"

# Background image COS input, specifying a non-default Bucket
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --bg-cos-key "/input/bg.jpg" \
    --bg-cos-bucket mybucket-125xxx --bg-cos-region ap-shanghai

# Background generation + fixed random seed (reproducible results)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "Modern minimalist living room background" \
    --random-seed 42

# Specify output format and size
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "Outdoor lawn, bright sunshine" \
    --format PNG --image-size 4K

# Submit task only, do not wait for result (returns TaskId)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "Minimalist white marble tabletop" \
    --no-wait

# Manually query background fusion/generation task status
python scripts/mps_get_image_task.py --task-id <TaskId>

# Download background fusion result to local after task completion
# Step 1: run background fusion task (result is saved to COS output path)
python scripts/mps_image_bg_fusion.py \
    --subject-url "https://example.com/product.jpg" \
    --prompt "Minimalist white marble tabletop"
# Step 2: download output from COS to local file
python scripts/mps_cos_download.py \
    --cos-input-key /output/bgfusion/result.jpeg \
    --local-file /tmp/bgfusion_result.jpg
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
      "path": "/output/bgfusion/result.jpeg",
      "cos_uri": "cos://mps-bucket-125xxx/output/bgfusion/result.jpeg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/bgfusion/result.jpeg"
    }
  ]
}
```

---

## API Reference

| API | Description |
|------|------|
| `ProcessImage` | Submit background fusion/generation task, `ScheduleId=30060` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official Documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)