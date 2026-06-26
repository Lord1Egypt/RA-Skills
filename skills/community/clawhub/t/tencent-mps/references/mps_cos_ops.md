# COS 文件操作参数与示例 — `mps_cos_upload.py` / `mps_cos_download.py` / `mps_cos_list.py`

## COS 文件上传 — `mps_cos_upload.py`

### 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` / `-f` | 本地文件路径（必填）|
| `--cos-input-key` / `-k` | COS 对象键（Key），如 `input/video.mp4`（**可选**，省略时自动使用 `input/<本地文件名>`）|
| `--bucket` / `-b` | COS Bucket 名称（默认使用环境变量 `TENCENTCLOUD_COS_BUCKET`）|
| `--region` / `-r` | COS Bucket 区域（默认使用环境变量 `TENCENTCLOUD_COS_REGION`）|
| `--secret-id` | 腾讯云 SecretId（默认使用环境变量）|
| `--secret-key` | 腾讯云 SecretKey（默认使用环境变量）|
| `--verbose` / `-v` | 显示详细日志（文件大小、Bucket、Region、Key、ETag、URL 等）|

### 示例命令

```bash
# 最简用法：省略 --cos-input-key，自动使用 input/<文件名> 作为 COS Key
python scripts/mps_cos_upload.py --local-file ./video.mp4
# 等价于：--cos-input-key input/video.mp4

# 手动指定 cos-input-key
python scripts/mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4

# 显示详细日志
python scripts/mps_cos_upload.py --local-file ./video.mp4 --verbose

# 指定 bucket 和 region（覆盖环境变量）
python scripts/mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4 \
    --bucket mybucket-125xxx --region ap-guangzhou

# 上传图片文件
python scripts/mps_cos_upload.py --local-file ./photo.jpg --verbose
```

---

## COS 文件下载 — `mps_cos_download.py`

> ⚠️ **参数名注意**：
> - 下载脚本的 COS 路径参数是 `--cos-input-key`（与上传脚本一致）
> - 本地保存路径参数是 `--local-file`，**不是** `--local-path`

### 参数说明

| 参数 | 说明 |
|------|------|
| `--cos-input-key` / `-k` | COS 对象键（Key），如 `output/result.mp4`（**必填**）|
| `--local-file` / `-f` | 本地保存路径（**可选**，省略时自动保存为 `./<cos-input-key 文件名>`），建议保存到 `/data/workspace/` 下（注意：是 `--local-file` 而非 `--local-path`）|
| `--bucket` / `-b` | COS Bucket 名称（默认使用环境变量）|
| `--region` / `-r` | COS Bucket 区域（默认使用环境变量）|
| `--secret-id` | 腾讯云 SecretId（默认使用环境变量）|
| `--secret-key` | 腾讯云 SecretKey（默认使用环境变量）|
| `--verbose` / `-v` | 显示详细日志（Bucket、Region、Key、本地路径、文件大小、URL 等）|

### 示例命令

```bash
# 最简用法：省略 --local-file，自动保存为 ./<文件名>
python scripts/mps_cos_download.py --cos-input-key output/result.mp4
# 等价于：--local-file ./result.mp4

# 手动指定 local-file
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4

# 显示详细日志
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --verbose

# 下载到工作目录（推荐路径）
python scripts/mps_cos_download.py --cos-input-key output/enhanced.mp4 --local-file /data/workspace/enhanced.mp4 --verbose

# 指定 bucket 和 region（覆盖环境变量）
python scripts/mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4 \
    --bucket mybucket-125xxx --region ap-guangzhou
```

---

## COS 文件列表 — `mps_cos_list.py`

### 参数说明

| 参数 | 说明 |
|------|------|
| `--prefix` / `-p` | 路径前缀，用于过滤指定目录（如 `output/transcode/`），默认为空（根目录）|
| `--search` / `-s` | 文件名搜索关键字，支持模糊匹配（不区分大小写）|
| `--exact` | 精确匹配模式，只返回文件名完全匹配的文件 |
| `--limit` / `-l` | 最大返回文件数量（默认 1000，最大 1000）|
| `--bucket` / `-b` | COS Bucket 名称（默认使用环境变量）|
| `--region` / `-r` | COS Bucket 区域（默认使用环境变量）|
| `--show-url` | 显示文件完整 URL |
| `--verbose` / `-v` | 显示详细日志 |

### 示例命令

```bash
# 列出 Bucket 根目录下的所有文件
python scripts/mps_cos_list.py

# 列出指定路径下的文件
python scripts/mps_cos_list.py --prefix output/transcode/

# 模糊搜索文件名包含 "video" 的文件
python scripts/mps_cos_list.py --prefix output/ --search video

# 精确匹配文件名
python scripts/mps_cos_list.py --prefix output/ --search "result.mp4" --exact

# 显示文件完整 URL
python scripts/mps_cos_list.py --prefix output/ --show-url

# 限制返回数量
python scripts/mps_cos_list.py --prefix output/ --limit 50

# 列出增强后的结果文件并显示 URL
python scripts/mps_cos_list.py --prefix /output/enhance/ --show-url --limit 20
```

## 强制规则

1. **上传路径自动补全**：上传时若用户未指定 `--cos-input-key`，**不得询问用户**，直接省略即可，脚本自动使用 `input/<本地文件名>` 作为 COS Key。
2. **下载路径自动补全**：下载时若用户未指定 `--local-file`，**不得询问用户**，直接省略即可，脚本自动保存为 `./<文件名>`；如需保存到特定目录，推荐使用 `/data/workspace/<文件名>`。
3. **参数名不得混淆**：下载脚本的本地路径参数是 `--local-file`，**不是** `--local-path`，生成命令时必须使用正确参数名。
4. **Bucket/Region 自动读取**：`--bucket` 和 `--region` 默认从环境变量读取，**不得主动询问用户**，除非用户明确要求覆盖。
