# vod_pull_upload — Parameters & Examples

> This file corresponds to the script: `scripts/vod_pull_upload.py`
>
> 🚨 **Mandatory Rule**: For URL pull uploads, it is **recommended and preferred** to use this dedicated script (no subcommand, parameters follow directly). `vod_upload.py` also has a `pull` subcommand available, but this dedicated script is recommended.

### ⚠️ Common Parameter Mistakes

| Incorrect Usage | Correct Usage | Notes |
|---------|---------|------|
| `vod_pull_upload.py pull --url ...` | `vod_pull_upload.py --url ...` | **No subcommand**, use `--url` directly |
| `vod_upload.py --url ...` | `vod_pull_upload.py --url ...` | Use the dedicated script `vod_pull_upload.py` for pull uploads |

### 📌 Media Name (`--media-name`) Inference Rules

> 🚨 **Mandatory Rule**: When the "media name" provided by the user is actually a URL (e.g., `https://example.com/video.mp4`), **do not ask for clarification** — automatically extract the filename from the end of the URL path as the media name (e.g., `video.mp4`) and generate the command directly.
>
> | User Input | Handling |
> |---------|---------|
> | `Specify media name https://example.com/video.mp4` | Automatically extract `video.mp4` as `--media-name` |
> | `Media name is https://example.com/my-clip.mp4` | Automatically extract `my-clip.mp4` as `--media-name` |
> | `Media name is "Product Promo Video"` | Use the name provided by the user directly |

## Parameter Reference

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--url` | string | ✅ | Media URL (required) |
| `--media-name` | string | - | Media name |
| `--media-type` | string | - | Media type (e.g., mp4, mp3; inferred automatically from URL by default) |
| `--cover-url` | string | - | Cover image URL |
| `--class-id` | int | - | Category ID (default 0) |
| `--procedure` | string | - | Task flow template name (automatically triggers a task flow after pull upload completes) |
| `--expire-time` | string | - | Expiration time (ISO 8601 format, e.g., `2025-12-31T23:59:59Z`) |
| `--storage-region` | string | - | Storage region (e.g., `ap-chongqing`) |
| `--tasks-priority` | int | - | Task priority (-10 to 10, default 0) |
| `--session-context` | string | - | Session context, passes through user request information (max 1000 characters) |
| `--session-id` | string | - | Deduplication identifier; requests with the same ID within three days will return an error (max 50 characters) |
| `--source-context` | string | - | Source context, passes through user request information (max 250 characters) |
| `--ext-info` | string | - | Reserved field, used for special purposes |
| `--media-storage-path` | string | - | Media storage path (must start with `/`; only available for sub-applications in FileID+Path mode) |
| `--sub-app-id` | int | - | VOD sub-application ID (required for accounts created after 2023-12-25; can also be set via the environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--app-name` | string | - | Fuzzy match sub-application by name/description (mutually exclusive with `--sub-app-id`) |
| `--region` | string | - | Region (default `ap-guangzhou`) |
| `--no-wait` | flag | - | Submit task only, do not wait for result (waits automatically by default) |
| `--max-wait` | int | - | Maximum wait time in seconds (default 600) |
| `--json` | flag | - | Output full response in JSON format |
| `--dry-run` | flag | - | Preview request parameters without actually executing |

---

## Usage Examples

#### Basic Pull Upload
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4"
```

#### Specify Media Name
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --media-name "Pulled Video"
```

#### Specify Media Type (when URL has no extension)
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video" \
    --media-type mp4
```

#### Specify Cover Image
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --cover-url "https://example.com/cover.jpg"
```

#### Automatically Trigger Task Flow After Pull Upload
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --procedure "My Procedure"
```

#### Wait for Task Completion
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \

```

#### Wait for Task Completion (Custom Timeout)
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
 \

```

#### Set Task Priority
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --tasks-priority 5
```

#### Deduplication Identifier (Prevent Duplicate Submissions)
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --session-id "my-unique-id-001"
```

#### JSON Output (with Wait for Result)
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
 \
    --json
```

#### dry-run Preview Parameters
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --media-name "Pulled Video" \
 \
    --dry-run
```

#### Pull HLS Stream
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.m3u8" \
    --media-name "HLS Stream"
```

---

## API Reference

| Feature | API | Documentation |
|------|---------|---------|
| URL Pull Upload | `PullUpload` | https://cloud.tencent.com/document/api/266/35575 |
| Query Task Status | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |