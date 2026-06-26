---
name: QQBot Media Sender
slug: qqbot-media-sender
description: "一键发送图片/视频/文件到 QQ，支持批量发送和自动压缩"
type: skill
version: 1.0.0
author: Lin
license: MIT
---

# QQBot Media Sender

一键发送图片、视频、文件到 QQ 聊天窗口，支持批量发送和自动压缩。

## 功能特性

- ✅ **图片发送**：支持 jpg, png, gif, webp 等格式
- ✅ **视频发送**：支持 mp4, avi, mov 等格式
- ✅ **文件发送**：支持 pdf, docx, xlsx, zip 等格式
- ✅ **批量发送**：一次发送多个文件
- ✅ **自动压缩**：大文件自动压缩（可选）
- ✅ **进度显示**：实时显示发送进度

## 使用方法

### 发送单张图片

```bash
# 使用标签直接发送
<qqimg>/path/to/image.jpg</qqimg>
```

### 发送单个文件

```bash
# 使用标签直接发送
<qqfile>/path/to/document.pdf</qqfile>
```

### 批量发送

```bash
# 发送目录下所有图片
qqbot-send-media /path/to/images/ --type image

# 发送指定文件列表
qqbot-send-media file1.pdf file2.pdf file3.pdf

# 发送到指定 QQ 群
qqbot-send-media /path/to/file.jpg --group 843812FF4BA524086B77B60886C38AB3
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--type` | 文件类型：image, video, file, auto | auto |
| `--group` | 目标 QQ 群号 | 私聊 |
| `--compress` | 是否压缩大文件 | false |
| `--max-size` | 最大文件大小 (MB) | 20 |
| `--delay` | 发送间隔 (ms) | 1000 |

## 示例

### 示例 1: 发送工作区所有 PDF

```bash
qqbot-send-media ~/.openclaw/workspace/*.pdf --type file
```

### 示例 2: 发送图片到指定群组

```bash
qqbot-send-media /tmp/screenshot.png --group 843812FF4BA524086B77B60886C38AB3
```

### 示例 3: 批量发送并压缩

```bash
qqbot-send-media /photos/ --type image --compress --max-size 10
```

## 自动压缩规则

- 图片 > 5MB: 自动压缩到 80% 质量
- 视频 > 10MB: 提示并建议压缩
- 文件 > 20MB: 自动分割或拒绝

## 支持的文件格式

### 图片
- ✅ JPG/JPEG
- ✅ PNG
- ✅ GIF
- ✅ WebP
- ✅ BMP

### 视频
- ✅ MP4
- ✅ AVI
- ✅ MOV
- ✅ WMV

### 文档
- ✅ PDF
- ✅ DOC/DOCX
- ✅ XLS/XLSX
- ✅ PPT/PPTX
- ✅ TXT
- ✅ ZIP

## 故障排除

### 问题：发送失败

**解决方案：**
1. 检查文件路径是否正确
2. 检查文件大小是否超过 20MB
3. 检查 QQBot 服务是否运行

### 问题：图片无法显示

**解决方案：**
1. 确保使用 `<qqimg>` 标签
2. 检查文件扩展名是否正确
3. 尝试转换为 JPG 格式

## 技术细节

### 标签格式

```
<qqimg>路径</qqimg>   - 图片
<qqvideo>路径</qqvideo> - 视频
<qqfile>路径</qqfile>  - 文件
<qqvoice>路径</qqvoice> - 语音
```

### API 调用

```javascript
// 内部调用示例
const payload = {
  type: 'media',
  mediaType: 'image',
  source: 'file',
  path: '/absolute/path/to/file.jpg'
};
```

## 许可证

MIT
