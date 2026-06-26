---
name: tencent-cos-ops
description: |
  腾讯云COS对象存储操作工具，用于上传、下载、列举和删除COS中的文件。触发场景：
  (1) 用户需要将本地文件上传到腾讯云COS对象存储
  (2) 用户需要从COS下载文件到本地
  (3) 用户需要按月管理COS中的文件（自动按YYYY/MM/前缀组织）
  (4) 用户需要列出或删除COS中的文件
  (5) 用户提到"腾讯云"、"COS"、"对象存储"、"上传文件到云存储"等关键词
---

# Tencent COS 操作

腾讯云COS对象存储操作工具，支持文件上传、下载、列表和管理。

## 环境配置

使用前需要设置以下环境变量：

```bash
export COS_SECRET_ID="你的SecretId"
export COS_SECRET_KEY="你的SecretKey"
export COS_REGION="ap-beijing"  # COS地域
export COS_BUCKET="examplebucket-1250000000"  # Bucket名称
```

## 快速使用

### 上传文件（按月自动管理）

```bash
python scripts/cos_ops.py upload /path/to/file.txt
```

默认按当前月份 `YYYY/MM/filename` 格式存储，例如 `2024/03/report.pdf`

### 指定目录上传

```bash
python scripts/cos_ops.py upload /path/to/file.txt --key "myfolder/report.pdf"
```

### 高级上传（分块上传，适合大文件）

```bash
python scripts/cos_ops.py upload /path/to/largefile.zip --advanced --part-size 10 --threads 20
```

### 下载文件

```bash
python scripts/cos_ops.py download "2024/03/report.pdf" /local/path/report.pdf
```

### 列出文件

```bash
# 列出所有文件
python scripts/cos_ops.py list

# 按前缀筛选
python scripts/cos_ops.py list --prefix "2024/03/"

# 指定bucket
python scripts/cos_ops.py list --prefix "logs/" --bucket "my-bucket-1250000000"
```

### 删除文件

```bash
python scripts/cos_ops.py delete "2024/03/report.pdf"
```

## Python脚本使用

在Python代码中直接调用：

```python
from cos_ops import upload_file, download_file, list_objects, delete_object

# 上传文件（自动按月管理）
upload_file('/path/to/file.txt')

# 指定对象键
upload_file('/path/to/file.txt', cos_key='custom/path/file.txt')

# 下载文件
download_file('2024/03/report.pdf', '/local/save/report.pdf')

# 列出文件
list_objects(prefix='2024/03/')

# 删除文件
delete_object('2024/03/report.pdf')
```

## 按月文件管理

脚本默认使用当前年月作为存储前缀，实现按月管理：

- 上传文件自动存储到 `YYYY/MM/` 目录下
- 例如：2024年3月上传的 `report.pdf` 会存储为 `2024/03/report.pdf`

## API参考

详细API文档请查看 [references/cos_api.md](references/cos_api.md)

### 常用API

| 方法 | 说明 |
|------|------|
| `upload_file()` | 简单上传，文件流方式 |
| `upload_file_advanced()` | 高级上传，自动分块 |
| `download_file()` | 下载文件到本地 |
| `list_objects()` | 列出对象 |
| `delete_object()` | 删除单个对象 |

## 版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-31 | 初始版本，支持上传、下载、列举、删除功能，按月文件管理 |
