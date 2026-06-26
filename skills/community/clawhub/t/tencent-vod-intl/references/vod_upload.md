# vod_upload — Parameters & Examples

> This file corresponds to the script: `scripts/vod_upload.py`
>
> 🚨 **Mandatory Rule**: Use `vod_upload.py upload` for local file uploads; for URL pull uploads, it is **recommended and preferred** to use the dedicated script `vod_pull_upload.py` (no subcommand, pass parameters directly). `vod_upload.py` also has a `pull` subcommand available, but the dedicated script is recommended.

### ⚠️ Common Parameter Mistakes

| Incorrect Usage | Correct Usage | Notes |
|---------|---------|------|
| `--media-type image` | (omit `--media-type`) | Media type is automatically inferred from the file extension |
| `--url ...` | `vod_pull_upload.py --url ...` | Use the dedicated script `vod_pull_upload.py` for pull uploads |
| (no category specified during upload) | `upload --file xxx.mp4 --class-id <category-ID>` | **Must include `--class-id` when specifying a media category**; defaults to 0 (other categories) |

## Parameter Reference

### Common Parameters

| Parameter | Type | Description |
|------|------|------|
| `--region` | string | Region, default `ap-guangzhou` |
| `--sub-app-id` | int | VOD sub-application ID (required for applications created after 2023-12-25; can also be set via the environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--app-name` | string | Fuzzy-match sub-application by name/description (mutually exclusive with `--sub-app-id`) |
| `--json` | flag | Output full response in JSON format |
| `--dry-run` | flag | Preview parameters without calling the API |
| `--verbose` | flag | Display detailed upload information |

### upload Parameters (Local File Upload)

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--file` | path | ✅ | Local file path (required) |
| `--media-name` | string | - | Media name (defaults to the filename without extension) |
| `--media-type` | string | - | Media type (e.g., mp4, mp3, jpg; automatically inferred from the file extension by default) |
| `--cover-file` | path | - | Local cover image file path |
| `--cover-type` | string | - | Cover type (e.g., jpg, png; inferred from the cover file extension by default) |
| `--class-id` | int | - | Category ID (default 0) |
| `--procedure` | string | - | Task flow template name (automatically initiates a task flow after upload completes) |
| `--expire-time` | string | - | Expiration time (ISO 8601 format, e.g., `2025-12-31T23:59:59Z`) |
| `--storage-region` | string | - | Storage region (e.g., `ap-chongqing`) |
| `--source-context` | string | - | Source context (pass-through user request info, max 250 characters) |
| `--concurrent-upload-number` | int | - | Number of concurrent multipart uploads (effective for large files) |
| `--media-storage-path` | string | - | Media storage path (must start with `/`; only available for sub-applications in FileID+Path mode) |

### Supported Media Types

**Video formats**: mp4, flv, avi, mkv, mov, wmv, webm, ts, m3u8, mpg, mpeg

**Audio formats**: mp3, aac, flac, wav, ogg, m4a, wma

**Image formats**: jpg, jpeg, png, gif, bmp, webp

### API Mapping

| Feature | API | Documentation |
|------|---------|---------|
| Apply for upload | `ApplyUpload` | https://cloud.tencent.com/document/api/266/31767 |
| Confirm upload | `CommitUpload` | https://cloud.tencent.com/document/api/266/31766 |
| URL pull upload | `PullUpload` | https://cloud.tencent.com/document/api/266/35575 |
| Query task status | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |

### Upload Process

#### Local File Upload Process
1. Call `ApplyUpload` to obtain temporary credentials and storage information (StorageBucket, StorageRegion, MediaStoragePath, VodSessionKey)
2. Use the COS SDK to upload the file to the specified path
3. Call `CommitUpload` to confirm the upload; returns FileId and playback URL

### Error Code Reference

| Error Type | Cause | Recommended Action |
|---------|------|---------|
| File not found | Incorrect local file path | Verify the file path is correct |
| Apply upload failed | Invalid parameters or insufficient permissions | Check parameters such as Media Type and Sub AppId |
| COS upload failed | Temporary credentials expired or network issue | Temporary credentials typically have a short validity period (< 1 hour); re-apply as needed |
| Confirm upload failed | Invalid VodSessionKey | Use the VodSessionKey returned by Apply Upload |

### pull Parameters (URL Pull Upload — Recommended: use vod_pull_upload.py)

> 💡 `vod_upload.py pull` and `vod_pull_upload.py` provide identical functionality. The dedicated script `vod_pull_upload.py` is recommended (no subcommand required); parameters are exactly the same. See `vod_pull_upload.md` for details.

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--url` | string | ✅ | Media URL (required) |
| `--media-name` | string | - | Media name |
| `--media-type` | string | - | Media type (e.g., mp4, mp3; automatically inferred from the URL by default) |
| `--cover-url` | string | - | Cover image URL |
| `--class-id` | int | - | Category ID (default 0) |
| `--procedure` | string | - | Task flow template name |
| `--expire-time` | string | - | Expiration time (ISO 8601 format) |
| `--storage-region` | string | - | Storage region (e.g., `ap-chongqing`) |
| `--tasks-priority` | int | - | Task priority (-10 to 10, default 0) |
| `--session-context` | string | - | Session context (pass-through user request info, max 1000 characters) |
| `--session-id` | string | - | Deduplication identifier (max 50 characters; the same ID within three days returns an error) |
| `--ext-info` | string | - | Reserved field; use only for special purposes |
| `--source-context` | string | - | Source context (pass-through user request info, max 250 characters) |
| `--media-storage-path` | string | - | Media storage path (must start with `/`; only available for sub-applications in FileID+Path mode) |
| `--sub-app-id` | int | - | VOD sub-application ID (can also be set via the environment variable `TENCENTCLOUD_VOD_SUB_APP_ID`) |
| `--app-name` | string | - | Fuzzy-match sub-application by name/description (mutually exclusive with `--sub-app-id`) |
| `--region` | string | - | Region (default `ap-guangzhou`) |
| `--no-wait` | flag | - | Submit the task only without waiting for the result (waits automatically by default) |
| `--max-wait` | int | - | Maximum wait time in seconds (default 600) |
| `--json` | flag | - | Output full response in JSON format |
| `--dry-run` | flag | - | Preview request parameters without executing |

---

## Usage Examples

### Local File Upload

#### Basic Upload (Auto-infer Media Type)
```bash
python scripts/vod_upload.py upload --file /path/to/video.mp4
```

#### Specify Media Name
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-name "My Highlight Video"
```

#### Specify Media Type
```bash
python scripts/vod_upload.py upload \
    --file video.mov \
    --media-type mp4 \
    --media-name "Format Conversion"
```

#### Upload with Cover Image
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --cover-file /path/to/cover.jpg
```

#### Specify Category
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --class-id 10
```

#### Automatically Trigger Task Flow After Upload
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --procedure "Long Video Preset"
```

#### Specify StorageRegion
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --storage-region ap-beijing
```

#### Specify Storage Path (FileID+Path Mode Only)
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-storage-path "/videos/2026-03/my-video.mp4"
```

#### Pass Through Context Information
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --source-context "client:app_v1"
```

#### JSON Output
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --json
```

#### Verbose Output
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --verbose
```

#### dry-run Preview Parameters
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-name "My Video" \
    --dry-run
```

---

### Different Media Type Examples

#### Upload Audio File
```bash
python scripts/vod_upload.py upload \
    --file /path/to/audio.mp3 \
    --media-name "Background Music"
```

#### Upload Image File
```bash
python scripts/vod_upload.py upload \
    --file /path/to/image.jpg \
    --media-name "Cover Image"
```

---

### Advanced Usage

#### Batch Upload (Using Shell Loop)
```bash
for f in /path/to/videos/*.mp4; do
    python scripts/vod_upload.py upload --file "$f"
done
```

#### Upload and Save Result to File
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --json > upload_result.json
```

#### Conditionally Check Upload Success
```bash
RESULT=$(python scripts/vod_upload.py upload --file video.mp4 --json)
FILE_ID=$(echo "$RESULT" | jq -r '.commit.FileId')
if [ "$FILE_ID" != "null" ]; then
    echo "Upload successful, FileId: $FILE_ID"
else
    echo "Upload failed"
fi
```

> 🚨 **For URL pull uploads, use `vod_pull_upload.py`**. See `vod_pull_upload.md` for parameter details.