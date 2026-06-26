# vod_process_image — Parameters & Examples

> This file corresponds to the script: `scripts/vod_process_image.py`
>
> Supported subcommands: `super-resolution` (image super-resolution enhancement), `understand` (image understanding)

### ⚠️ Common Parameter Mistakes

| Incorrect Usage | Correct Usage | Notes |
|---------|---------|------|
| `vod_process_image_async.py --url ...` | `vod_process_image.py super-resolution --file-id ...` | `vod_process_image_async.py` does not exist, nor does an `async` subcommand. Use `super-resolution` for upscaling and `understand` for image understanding |
| `vod_process_image.py async --template-id 7` | `vod_process_image.py super-resolution --template-id 7` | There is no `async` subcommand; use `super-resolution --template-id` directly to specify a template |
| `--priority 5` | `--tasks-priority 5` | **🚨 The task priority parameter is `--tasks-priority`, not `--priority`** |

## Parameter Reference

### super-resolution Parameters (Image Super-Resolution Enhancement)

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--file-id` | string | ✅ | Image file FileId (required) |
| `--sub-app-id` | int | - | VOD sub-application ID (required for accounts created after 2023-12-25; can also be set via the environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--mode` | enum | - | Super-resolution mode: `percent` (multiplier upscale, default) / `fixed` (fixed resolution) / `aspect` (aspect-ratio fit) |
| `--percent` | float | - | Upscale multiplier (valid when `mode=percent`, default 2.0) |
| `--width` | int | - | Target width (valid when `mode=fixed` or `mode=aspect`) |
| `--height` | int | - | Target height (valid when `mode=fixed` or `mode=aspect`) |
| `--sr-type` | enum | - | Super-resolution type: `standard` (general upscaling, faster) / `super` (advanced upscaling, better quality, default) |
| `--output-format` | enum | - | Output format: `JPEG` / `PNG` / `BMP` / `WebP` |
| `--quality` | int | - | Output image quality (valid for JPEG/WebP, range 1–100) |
| `--template-id` | int | - | Directly specify an existing super-resolution template ID (mutually exclusive with `--mode`, `--percent`, etc.) |
| `--template-name` | string | - | Custom template name (used when creating a new template) |
| `--template-comment` | string | - | Custom template description |
| `--session-id` | string | - | Deduplication identifier (requests with the same ID within three days will return an error) |
| `--tasks-priority` | int | - | Task priority (−10 to 10) |
| `--region` | string | - | Region (default `ap-guangzhou`) |
| `--no-wait` | flag | - | Submit the task only without waiting for the result (waits automatically by default) |
| `--max-wait` | int | - | Maximum wait time in seconds (default 300) |
| `--json` | flag | - | Output in JSON format |
| `--dry-run` | flag | - | Preview request parameters without actually executing |

> The target resolution must not exceed 4096×4096.

---

### understand Parameters (Image Understanding)

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--file-id` | string | - | Image file FileId (one of `--file-id`, `--url`, or `--base64` is **required**) |
| `--url` | string | - | Image URL (one of `--file-id`, `--url`, or `--base64` is **required**) |
| `--base64` | string | - | Base64-encoded image (one of `--file-id`, `--url`, or `--base64` is **required**; file must be <4 MB) |
| `--sub-app-id` | int | ✅ | VOD sub-application ID (required; can also be set via the environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--prompt` | string | - | Custom prompt (default: "Describe this image") |
| `--model` | string | - | Model: `gemini-2.5-flash` / `gemini-2.5-flash-lite` / `gemini-2.5-pro` / `gemini-3-flash` / `gemini-3-pro` |
| `--output-name` | string | - | Output file name |
| `--class-id` | int | - | Category ID |
| `--expire-time` | string | - | Expiration time (ISO 8601 format, e.g. `2025-12-31T23:59:59Z`) |
| `--session-id` | string | - | Deduplication identifier; requests with the same ID within three days will return an error |
| `--session-context` | string | - | Source context; passes through user request information |
| `--tasks-priority` | int | - | Task priority (−10 to 10) |
| `--ext-info` | string | - | Extended information (JSON string, e.g. to specify a model name) |
| `--region` | string | - | Region (default `ap-guangzhou`) |
| `--no-wait` | flag | - | Submit the task only without waiting for the result (waits automatically by default) |
| `--max-wait` | int | - | Maximum wait time in seconds (default 120) |
| `--json` | flag | - | Output in JSON format |
| `--dry-run` | flag | - | Preview request parameters without actually executing |

---

## Usage Examples

### super-resolution Examples

```bash
# Default 2× advanced super-resolution (waits for completion automatically)
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id>

# Fixed-resolution upscale to 1920x1080, JPEG output
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --mode fixed --width 1920 --height 1080 --output-format JPEG

# 3× standard super-resolution, PNG output, with specified image quality
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --percent 3.0 --sr-type standard --output-format PNG --quality 90

# No wait — return task ID immediately
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --json
```

### understand Examples

```bash
# Image understanding (default prompt)
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154

# Image understanding with a custom prompt
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154 \
    --prompt "Describe the facial expressions and actions of the people in the image"

# URL input + specify model
python scripts/vod_process_image.py understand \
    --url "https://example.com/image.jpg" --sub-app-id 1500046154 \
    --model gemini-2.5-pro --prompt "Analyze the composition and color palette"

# No wait (return task ID immediately)
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154 \
    --json
```

---

## API Interfaces

| Feature | API Interface | Documentation |
|------|---------|---------|
| Image super-resolution (create template) | `CreateProcessImageAsyncTemplate` | https://cloud.tencent.com/document/product/266/127862 |
| Image super-resolution (submit task) / Image understanding / Async processing | `ProcessImageAsync` | https://cloud.tencent.com/document/api/266/127858 |