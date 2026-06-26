# US3 Uploader - 使用示例

## 自动上传工作流

当 AI 完成文件处理后，会自动上传到 US3 并提供下载链接：

### 示例 1：处理图片后上传

```bash
# 1. 处理图片（例如：压缩、裁剪等）
convert input.jpg -resize 800x600 /tmp/processed_image.jpg

# 2. 自动上传到 US3
python3 scripts/upload_to_us3.py /tmp/processed_image.jpg

# 输出示例：
# Uploading processed_image.jpg to US3...
#   Bucket: your-bucket
#   Remote name: 20260205_153025_a3b4c5d6e7f8g9h0.jpg
#   File size: 0.50MB
#
# ✓ Upload successful!
#
# 📋 Download URL (valid for 7 days):
# https://your-bucket.cn-sh2.ufileos.com/20260205_153025_a3b4c5d6e7f8g9h0.jpg?UCloudPublicKey=...&Signature=...&Expires=...
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📥 下载链接（7天内有效）：
# https://your-bucket.cn-sh2.ufileos.com/20260205_153025_a3b4c5d6e7f8g9h0.jpg?UCloudPublicKey=...&Signature=...&Expires=...
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 示例 2：生成 PDF 报告后上传

```bash
# 1. 生成 PDF 报告
pandoc report.md -o /tmp/monthly_report.pdf

# 2. 自动上传
python3 scripts/upload_to_us3.py /tmp/monthly_report.pdf
```

### 示例 3：批量上传文件

```bash
# 上传多个文件
for file in /tmp/processed_*.jpg; do
    python3 scripts/upload_to_us3.py "$file"
done
```

## 文件名格式说明

- **旧格式**（完整原文件名）：`20260204_153025_screenshot.jpg`
- **新格式**（时间戳+MD5）：`20260205_153025_a3b4c5d6e7f8g9h0.jpg`

新格式的优点：
- ✅ 时间戳便于按时间排序
- ✅ MD5 哈希确保唯一性（相同文件相同哈希）
- ✅ 避免文件名过长问题
- ✅ 防止特殊字符导致的路径问题
- ✅ 去重检测（相同内容的文件有相同 MD5）

## 下载链接特性

1. **有效期**：7天（604800秒）
2. **签名验证**：URL 包含 UCloud 签名，确保安全
3. **强制下载**：设置 `Content-Disposition` 头，点击直接下载而非预览
4. **原文件名**：下载时使用原始文件名，而非时间戳名称

## AI 使用指南

当 AI 需要给用户提供文件时：

1. **处理文件**（如果需要）
2. **上传到 US3**：
   ```bash
   python3 scripts/upload_to_us3.py <file_path>
   ```
3. **提取并发送下载链接**：
   - 从输出中找到最后的分隔线区域
   - 复制完整的 URL
   - 直接发送给用户

示例回复格式：
```
搞定！图片已处理完成（390KB → 28KB）

下载链接（7天有效）：
https://your-bucket.cn-sh2.ufileos.com/20260205_153025_a3b4c5d6e7f8g9h0.jpg?UCloudPublicKey=...&Signature=...&Expires=...
```

## 环境变量配置

确保已设置以下环境变量：

```bash
export US3_PUBLIC_KEY='your-public-key'
export US3_PRIVATE_KEY='your-private-key'
export US3_BUCKET='your-bucket-name'
export US3_ENDPOINT='cn-sh2.ufileos.com'  # 可选，默认值
export US3_MAX_FILE_SIZE_MB='50'          # 可选，默认 50MB
```
