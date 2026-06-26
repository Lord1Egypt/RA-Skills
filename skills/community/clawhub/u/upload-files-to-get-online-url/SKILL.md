---
name: cos-upload
description: Upload files to Tencent Cloud COS (Cloud Object Storage). Use when the user needs to upload images, documents, or any files to Tencent Cloud COS. Supports environment variables or command-line arguments for configuration. Automatically generates accessible URLs and signed URLs with 24-hour expiration.
---

# COS Upload

Upload files to Tencent Cloud COS (腾讯云对象存储) with automatic URL generation.

## Quick Start

### Method 1: Using Environment Variables

Set these environment variables:
```bash
export TENCENT_SECRET_ID=your-secret-id
export TENCENT_SECRET_KEY=your-secret-key
export TENCENT_COS_BUCKET=your-bucket-name
export TENCENT_COS_REGION=ap-guangzhou
export TENCENT_COS_PATH=uploads/  # optional
```

Then upload:
```bash
node cos-upload.js /path/to/file.png
```

### Method 2: Using Command Line Arguments

```bash
node cos-upload.js /path/to/file.png \
  --secret-id AKIDxxx \
  --secret-key xxx \
  --bucket my-bucket-1250000000 \
  --region ap-guangzhou \
  --path images/
```

## Output

On successful upload, returns:
- **Direct URL**: `https://{bucket}.cos.{region}.myqcloud.com/{key}`
- **Signed URL**: Pre-signed URL with 24-hour expiration (for private buckets)
- **COS Key**: The object key in the bucket

## Configuration Priority

1. Command line arguments (highest priority)
2. Environment variables
3. Default values

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TENCENT_SECRET_ID` | Yes | Tencent Cloud API Secret ID |
| `TENCENT_SECRET_KEY` | Yes | Tencent Cloud API Secret Key |
| `TENCENT_COS_BUCKET` | Yes | COS bucket name (e.g., `my-bucket-1250000000`) |
| `TENCENT_COS_REGION` | Yes | COS region (e.g., `ap-guangzhou`, `ap-nanjing`) |
| `TENCENT_COS_PATH` | No | Upload path prefix (default: `uploads/`) |

## Command Line Options

| Option | Description |
|--------|-------------|
| `--secret-id` | Tencent Cloud API Secret ID |
| `--secret-key` | Tencent Cloud API Secret Key |
| `--bucket` | COS bucket name |
| `--region` | COS region |
| `--path` | Upload path prefix |

## Notes

- Files are uploaded with auto-generated unique names: `upload_{timestamp}_{random}.{ext}`
- Supports all file types (images, documents, videos, etc.)
- Uses 5MB multipart upload threshold for large files
- Automatically generates both direct and pre-signed URLs
