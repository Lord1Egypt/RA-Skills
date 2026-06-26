# COS File Operation Parameters & Examples — `mps_cos_upload.py` / `mps_cos_download.py` / `mps_cos_list.py`

## COS File Upload — `mps_cos_upload.py`

### Parameter Description

| Parameter | Description |
|-----------|-------------|
| `--local-file` / `-f` | Local file path (required) |
| `--cos-input-key` / `-k` | COS object key, e.g., `input/video.mp4` (**optional**; when omitted, automatically uses `input/<local filename>`) |
| `--bucket` / `-b` | COS Bucket name (defaults to environment variable `TENCENTCLOUD_COS_BUCKET`) |
| `--region` / `-r` | COS Bucket region (defaults to environment variable `TENCENTCLOUD_COS_REGION`) |
| `--secret-id` | Tencent Cloud SecretId (defaults to environment variable) |
| `--secret-key` | Tencent Cloud Secret Key (defaults to environment variable) |
| `--verbose` / `-v` | Show detailed logs (file size, Bucket, Region, Key, ETag, URL, etc.) |

### Example Commands

```bash
# Simplest usage: omit --cos-input-key, automatically uses input/<filename> as COS Key
python scripts/mps_cos_upload.py --local-file ./video.mp4
# Equivalent to: --cos-input-key input/video.mp4

# Manually specify cos-input-key
python scripts/mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4

# Show detailed logs
python scripts/mps_cos_upload.py --local-file ./video.mp4 --verbose

# Specify bucket and region (overrides environment variables)
python scripts/mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4 \
    --bucket mybucket-125xxx --region ap-guangzhou

# Upload an image file
python scripts/mps_cos_upload.py --local-file ./photo.jpg --verbose
```

---

## COS File Download — `mps_cos_download.py`

> ⚠️ **Parameter Name Notice**:
> - The COS path parameter for the download script is `--cos-input-key` (consistent with the upload script)
> - The local save path parameter is `--local-file`, **not** `--local-path`

### Parameter Description

| Parameter | Description |
|-----------|-------------|
| `--cos-input-key` / `-k` | COS object key, e.g., `output/result.mp4` (**required**) |
| `--local-file` / `-f` | Local save path (**optional**; when omitted, automatically saves as `./<cos-input-key filename>`); recommended to save under `/data/workspace/` (note: it's `--local-file`, not `--local-path`) |
| `--bucket` / `-b` | COS Bucket name (defaults to environment variable) |
| `--region` / `-r` | COS Bucket region (defaults to environment variable) |
| `--secret-id` | Tencent Cloud SecretId (defaults to environment variable) |
| `--secret-key` | Tencent Cloud Secret Key (defaults to environment variable) |
| `--verbose` / `-v` | Show detailed logs (Bucket, Region, Key, local path, file size, URL, etc.) |

### Example Commands

```bash
# Simplest usage: omit --local-file, automatically saves as ./<filename>
python scripts/mps_cos_download.py --cos-input-key output/result.mp4
# Equivalent to: --local-file ./result.mp4

# Manually specify local-file
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4

# Show detailed logs
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --verbose

# Download to workspace directory (recommended path)
python scripts/mps_cos_download.py --cos-input-key output/enhanced.mp4 --local-file /data/workspace/enhanced.mp4 --verbose

# Specify bucket and region (overrides environment variables)
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4 \
    --bucket mybucket-125xxx --region ap-guangzhou
```

---

## COS File List — `mps_cos_list.py`

### Parameter Description

| Parameter | Description |
|-----------|-------------|
| `--prefix` / `-p` | Path prefix for filtering a specific directory (e.g., `output/transcode/`); defaults to empty (root directory) |
| `--search` / `-s` | Filename search keyword; supports fuzzy matching (case-insensitive) |
| `--exact` | Exact match mode; returns only files with an exactly matching filename |
| `--limit` / `-l` | Maximum number of files to return (default 1000, max 1000) |
| `--bucket` / `-b` | COS Bucket name (defaults to environment variable) |
| `--region` / `-r` | COS Bucket region (defaults to environment variable) |
| `--show-url` | Show full file URL |
| `--verbose` / `-v` | Show detailed logs |

### Example Commands

```bash
# List all files in the Bucket root directory
python scripts/mps_cos_list.py

# List files under a specific path
python scripts/mps_cos_list.py --prefix output/transcode/

# Fuzzy search for files with "video" in the filename
python scripts/mps_cos_list.py --prefix output/ --search video

# Exact match filename
python scripts/mps_cos_list.py --prefix output/ --search "result.mp4" --exact

# Show full file URLs
python scripts/mps_cos_list.py --prefix output/ --show-url

# Limit the number of returned results
python scripts/mps_cos_list.py --prefix output/ --limit 50

# List enhanced result files and show URLs
python scripts/mps_cos_list.py --prefix /output/enhance/ --show-url --limit 20
```

## Mandatory Rules

1. **Upload path auto-completion**: When uploading, if the user does not specify `--cos-input-key`, **do not ask the user**; simply omit it, and the script will automatically use `input/<local filename>` as the COS Key.
2. **Download path auto-completion**: When downloading, if the user does not specify `--local-file`, **do not ask the user**; simply omit it, and the script will automatically save as `./<filename>`; if saving to a specific directory is needed, the recommended path is `/data/workspace/<filename>`.
3. **Do not confuse parameter names**: The local path parameter for the download script is `--local-file`, **not** `--local-path`; the correct parameter name must be used when generating commands.
4. **Bucket/Region auto-read**: `--bucket` and `--region` default to reading from environment variables; **do not proactively ask the user** unless the user explicitly requests to override them.