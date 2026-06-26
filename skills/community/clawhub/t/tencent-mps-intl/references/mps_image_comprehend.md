# Image Comprehension Parameters & Examples — `mps_image_comprehend.py`

**Function**: Calls the MPS `ProcessImage` API to initiate an image comprehension / OCR / visual question answering task (Gemini family models), polls for results via `DescribeImageTaskDetail`, and returns text content (`Content`).

Applicable scenarios: image captioning, OCR text extraction, visual Q&A, product information extraction, document understanding, etc.

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
| `--prompt` | — (**required**) | Prompt or instruction, such as `"Describe this image"` or `"Extract all text from the image"` |
| `--model-name` | `Google/gemini-2.5-flash` | Model name (mutually exclusive with `--definition`) |
| `--definition` | — | Preset model ID (mutually exclusive with `--model-name`), see mapping below |
| `--temperature` | — | Sampling temperature that controls output randomness |
| `--top-p` | — | Top-P sampling parameter |
| `--top-k` | — | Top-K sampling parameter |

**DEFINITION_MAP (`--definition` values)**:

| Value | Corresponding Model |
|------|---------------------|
| `10000` | gemini-flash-lite |
| `10001` | gemini-flash |
| `10002` | gemini-flash-pro |
| `10003` | gemini-3-flash |
| `10004` | gemini-3-pro |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | Output COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | Output COS Region |
| `--output-dir` | `/output/comprehend/` | Output directory (used only if file output is involved) |

> **Note**: Image comprehension returns text `Content`, not an image file.

### Task Control

| Parameter | Description |
|-----------|-------------|
| `--no-wait` | Submit the task only without waiting for results (returns TaskId and exits) |
| `--poll-interval` | Polling interval in seconds (default 10) |
| `--timeout` | Maximum wait time in seconds (default 600) |
| `--dry-run` | Preview the API request parameters without making an actual call |
| `--region` | MPS API access region (defaults to `TENCENTCLOUD_API_REGION`, otherwise `ap-guangzhou`) |

---

## Mandatory Rules

1. **`--prompt` is required**; omitting it causes the script to exit with an error.
2. **`--definition` and `--model-name` are mutually exclusive** and cannot be specified together; if both are omitted, the default model is `Google/gemini-2.5-flash`.
3. `ScheduleId=30200`, and the output is text `Content` rather than an image file.
4. URL inputs must be publicly accessible; COS inputs require that the MPS service has permission to read from the corresponding Bucket.
5. To manually query image comprehension task status, use `mps_get_image_task.py` — do not use `mps_get_video_task.py`.

---

## Example Commands

```bash
# Simplest usage: describe image content
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "Describe the content of this image"

# OCR text extraction
python scripts/mps_image_comprehend.py \
    --url "https://example.com/document.jpg" \
    --prompt "Extract all text from the image"

# Visual question answering
python scripts/mps_image_comprehend.py \
    --local-file /tmp/product.jpg \
    --prompt "What are the brand and price of this product?"

# Specify model by definition
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "Describe the image content" \
    --definition 10004

# Specify model by name
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "Describe the image content" \
    --model-name "Google/gemini-2.5-flash"

# Adjust sampling parameters
python scripts/mps_image_comprehend.py \
    --url "https://example.com/creative.jpg" \
    --prompt "Describe this image in poetic language" \
    --temperature 0.8 --top-p 0.9

# COS path input
python scripts/mps_image_comprehend.py \
    --cos-input-key "/input/receipt.jpg" \
    --prompt "Extract the amount and date from this invoice"

# Submit task only without waiting for result
python scripts/mps_image_comprehend.py \
    --url "https://example.com/photo.jpg" \
    --prompt "Describe the image content" \
    --no-wait

# Manually query image comprehension task status
python scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## Output Example

JSON output after task completion:

```json
{
  "TaskId": "2600007696-WorkflowTask-cDEF3456GH7890",
  "Status": "FINISH",
  "CreateTime": "2025-05-21T10:00:00Z",
  "FinishTime": "2025-05-21T10:00:12Z",
  "Content": "This image shows an orange cat lying on a sunny windowsill, with a green garden in the background. The cat's eyes are half closed, and it looks very relaxed and comfortable."
}
```

---

## API Reference

| API | Description |
|-----|-------------|
| `ProcessImage` | Submit an image comprehension task with `ScheduleId=30200`, configured through prompt and model parameters |
| `DescribeImageTaskDetail` | Query task status and output results |

Official documentation:
- [Process Image](https://cloud.tencent.com/document/product/862/112896)
- [Describe Image Task Detail](https://cloud.tencent.com/document/api/862/118509)
