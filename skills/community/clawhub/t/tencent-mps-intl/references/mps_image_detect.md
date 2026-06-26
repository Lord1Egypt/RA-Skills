# Object Detection & Description Parameters & Examples — `mps_image_detect.py`

**Function**: Calls the MPS image task API to initiate an object detection and object description task, polls for results via `DescribeImageTaskDetail`, and returns detection data (bounding boxes, descriptions, and optional cutouts).

Applicable scenarios: product localization, object recognition and description in images, automatic annotation, object crop extraction, etc.

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
| `--prompt` | — | Target description prompt for detection (can be specified multiple times); at least one of `--prompt` or `--point` is required |
| `--point` | — | Point coordinate in `"X,Y"` format (can be specified multiple times); at least one of `--prompt` or `--point` is required |
| `--top-k` | `1` | Maximum number of detections returned for each prompt/point (1–20) |
| `--confidence-threshold` | `0.5` | Confidence threshold (0–1). Results below this threshold are filtered out |
| `--describe` | — | Enable object description generation for each detection result |
| `--return-cutout` | — | Enable cutout output for each detection result |
| `--prompt-language` | — | Prompt language: `zh` / `en` |
| `--description-language` | — | Description output language: `zh` / `en` |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/object-detect/` | Output directory |
| `--output-path` | — | Custom output path (must include file extension) |

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (returns TaskId and exits) |
| `--poll-interval` | Polling interval in seconds (default 5) |
| `--timeout` | Maximum wait time in seconds (default 300) |
| `--dry-run` | Preview the API request parameters without making an actual call |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **At least one of `--prompt` or `--point` is required**; if both are omitted, the script exits with an error.
2. Detection configuration is passed through `StdExtInfo.ObjectDetectDescribeConfig` (no fixed `ScheduleId`; it runs as an ImageTask).
3. **The output JSON contains a `Detections` array**, where each item includes bounding box coordinates, confidence score, description (if enabled), and cutout path (if enabled).
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query detection task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: prompt-based detection
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "cat"

# Multi-object detection (multiple prompts)
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "cat" \
    --prompt "dog"

# Point-based detection
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --point "320,240"

# Multiple points
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --point "100,200" \
    --point "500,300"

# Increase return count and lower confidence threshold
python scripts/mps_image_detect.py \
    --url "https://example.com/crowd.jpg" \
    --prompt "person" \
    --top-k 10 \
    --confidence-threshold 0.3

# Enable object description
python scripts/mps_image_detect.py \
    --url "https://example.com/product.jpg" \
    --prompt "product" \
    --describe \
    --description-language en

# Enable cutout output
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "car" \
    --return-cutout

# Local file + full parameters
python scripts/mps_image_detect.py \
    --local-file /tmp/photo.jpg \
    --prompt "face" \
    --top-k 5 \
    --describe \
    --return-cutout \
    --prompt-language en \
    --description-language en

# Submit task only without waiting for result
python scripts/mps_image_detect.py \
    --url "https://example.com/scene.jpg" \
    --prompt "cat" \
    --no-wait

# Manually query detection task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-eFGH5678IJ9012",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:06Z",
  "Detections": [
    {
      "Label": "cat",
      "Confidence": 0.92,
      "BoundingBox": {
        "X": 120,
        "Y": 80,
        "Width": 200,
        "Height": 180
      },
      "Description": "An orange cat is resting on a sofa.",
      "CutoutPath": "/output/object-detect/cutout_0.png"
    }
  ]
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit an object detection task configured through `StdExtInfo.ObjectDetectDescribeConfig` |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
