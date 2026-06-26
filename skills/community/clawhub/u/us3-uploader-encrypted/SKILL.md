---
name: us3-uploader
description: |
  Upload files to UCloud US3 (UFile) object storage and generate download URLs.
  当用户需要：上传文件、发送文件、分享文件、生成文件链接、把文件发给用户、导出文件、
  生成PDF/图片/文档后发送、任何文件产出需要给用户时，必须使用此 skill。
  沙箱内的文件用户无法直接访问，必须上传到 US3 生成下载链接。
metadata: |
  {
    "openclaw": {
      "always": true
    }
  }
---

# US3 Uploader

> [!CAUTION]
> **强制要求 - 文件产出必须上传！**
>
> 如果任务产出的内容是**任何类型的文件**，包括但不限于：
> - 图片（截图、生成的图片、处理后的图片等）
> - 视频（录制、剪辑、转码后的视频等）
> - PDF（生成的报告、转换的文档等）
> - 其他文档（Word、Excel、PPT、代码压缩包等）
>
> **必须执行以下步骤：**
> 1. 使用 `python3 scripts/upload_to_us3.py <文件路径>` 上传到 US3
> 2. 将生成的下载链接发送给用户
>
> **禁止：** 只告诉用户"文件已保存在 /tmp/xxx"或本地路径。沙箱环境中的文件用户**完全无法访问**，必须上传后提供链接！

## Overview

Upload files to UCloud US3 (UFile) object storage using the official Python SDK and automatically generate download URLs with authentication signatures.

## Quick Start

### 1. Set Environment Variables

```bash
export US3_PUBLIC_KEY='your-public-key'
export US3_PRIVATE_KEY='your-private-key'
export US3_BUCKET='bucket-name.region.ufileos.com'  # full domain format (e.g., my-bucket.cn-bj.ufileos.com)
export US3_MAX_FILE_SIZE_MB='50'  # optional, defaults to 50MB
```

**Note:** If your `US3_BUCKET` contains the full domain (with dots), the endpoint will be automatically extracted. You don't need to set `US3_ENDPOINT` separately.

### 2. Upload a File

```bash
python3 scripts/upload_to_us3.py <file_path>
```

## Features

- **Timestamp and MD5-based filename**: Files are uploaded with format `YYYYMMDD_HHMMSS_md5hash.ext` (e.g., `20260205_153025_a3b4c5d6e7f8g9h0.jpg`)
- **File size limit**: Configurable max size (default 50MB), rejects larger files
- **Signed download URLs**: Valid for 7 days with authentication
- **Auto-install SDK**: Installs ufile SDK if not present
- **Force download**: Sets Content-Disposition to download (not preview)
- **Direct URL output**: Provides complete download URL directly to users

## Output Format

The upload script will output the download URL directly for easy sharing:

```
Uploading screenshot.png to US3...
  Bucket: my-bucket
  Remote name: 20260205_153025_a3b4c5d6e7f8g9h0.png
  File size: 2.50MB

✓ Upload successful!

📋 Download URL (valid for 7 days):
https://my-bucket.cn-sh2.ufileos.com/20260205_153025_a3b4c5d6e7f8g9h0.png?...signature...

ℹ️  Note:
   - Click to download file directly (not preview)
   - URL contains authentication signature (required by US3)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 下载链接（7天内有效）：
https://my-bucket.cn-sh2.ufileos.com/20260205_153025_a3b4c5d6e7f8g9h0.png?...signature...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Getting UCloud Credentials

1. Log in to UCloud Console: https://console.ucloud.cn
2. Navigate to **API 密钥** (API Keys)
3. Create or view API keys
4. Copy Public Key and Private Key

### Create a Bucket

1. Go to **对象存储 US3**
2. Click **创建存储空间** (Create Bucket)
3. Enter unique bucket name
4. Select region (e.g., 上海 Shanghai)
5. Note the bucket endpoint

## Common Endpoints

- Beijing: `cn-bj.ufileos.com`
- Shanghai: `cn-sh2.ufileos.com`
- Guangzhou: `cn-gd.ufileos.com`
- Hong Kong: `hk.ufileos.com`

## Security Notes

- ⚠️ Never commit credentials to version control
- Keep API keys secure and private
- Rotate API keys periodically
