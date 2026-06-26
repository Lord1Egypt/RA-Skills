---
name: tencent-cos-uploader
description: 使用腾讯云 COS Python SDK 上传指定本地文件到目标 Bucket，并生成可用于查看和下载的预签名访问链接。用户提到 COS、对象存储、Bucket、上传文件、临时分享链接、签名 URL、下载直链时使用此 skill。
---

# Tencent COS Uploader

## Overview

Use Tencent COS Python SDK to upload a local file and return presigned URLs for browser preview and file download.

## Prerequisites

1. Install dependency:

```bash
pip install cos-python-sdk-v5
```

2. Prepare COS credentials (env vars preferred):

- `COS_SECRET_ID`
- `COS_SECRET_KEY`
- `COS_REGION`
- `COS_BUCKET`
- `COS_SESSION_TOKEN` (optional, for temporary credentials)

## Workflow

1. Confirm required inputs:
   - `region` (from `--region` or env)
   - `bucket` (from `--bucket` or env)
   - `--file` local file path
   - `--key` object key in bucket (default is filename)
2. Run the script:

```bash
python3 scripts/cos_upload_and_presign.py \
  --region ap-guangzhou \
  --bucket my-bucket-1250000000 \
  --file /absolute/path/to/file.pdf \
  --key reports/2026/file.pdf \
  --expires 3600
```

3. Return JSON output containing:
   - `view_url`: GET presigned URL for viewing
   - `download_url`: presigned URL with `attachment` disposition
   - `upload_result`: SDK upload response

## Script Parameters

- `--region` COS region, optional if `COS_REGION` exists
- `--bucket` bucket name with appid suffix, optional if `COS_BUCKET` exists
- `--file` local file path to upload, required
- `--key` object key in bucket, optional
- `--expires` URL expiration seconds, default `3600`
- `--secret-id` optional if `COS_SECRET_ID` exists
- `--secret-key` optional if `COS_SECRET_KEY` exists
- `--session-token` optional if `COS_SESSION_TOKEN` exists
- `--scheme` `https` or `http`, default `https`
- `--download-filename` custom filename for download prompt (optional)

## Notes

- Keep `expires` as short as practical to reduce link leakage risk.
- `download_url` is generated via `get_presigned_download_url`; `view_url` is generated via `get_presigned_url(Method='GET')`.
- If `--key` is omitted, the script uses the source filename as object key.
