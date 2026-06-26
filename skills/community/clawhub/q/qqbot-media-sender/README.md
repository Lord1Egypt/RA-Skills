# QQBot Media Sender

一键发送图片、视频、文件到 QQ 聊天窗口。

## 快速开始

### 安装

```bash
clawhub install qqbot-media-sender
```

### 基本用法

#### 1. 发送单张图片

```bash
qqbot-send-media /path/to/image.jpg
```

#### 2. 发送 PDF 文档

```bash
qqbot-send-media /path/to/document.pdf
```

#### 3. 批量发送图片

```bash
qqbot-send-media /path/to/images/ --type image
```

#### 4. 发送到 QQ 群

```bash
qqbot-send-media image.jpg --group 843812FF4BA524086B77B60886C38AB3
```

## 支持的标签

| 类型 | 标签 | 示例 |
|------|------|------|
| 图片 | `<qqimg>` | `<qqimg>/path/to/image.jpg</qqimg>` |
| 视频 | `<qqvideo>` | `<qqvideo>/path/to/video.mp4</qqvideo>` |
| 文件 | `<qqfile>` | `<qqfile>/path/to/file.pdf</qqfile>` |
| 语音 | `<qqvoice>` | `<qqvoice>/path/to/voice.mp3</qqvoice>` |

## 功能特性

- ✅ 支持图片、视频、文件发送
- ✅ 批量发送
- ✅ 自动检测文件类型
- ✅ 文件大小检查（最大 20MB）
- ✅ 发送间隔控制
- ✅ 实时进度显示

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--type` | 文件类型：image, video, file, auto | auto |
| `--group` | 目标 QQ 群号 | 私聊 |
| `--compress` | 是否压缩大文件 | false |
| `--max-size` | 最大文件大小 (MB) | 20 |
| `--delay` | 发送间隔 (ms) | 1000 |

## 示例

### 发送工作区所有 PDF

```bash
qqbot-send-media ~/.openclaw/workspace/*.pdf
```

### 发送截图到群组

```bash
qqbot-send-media /tmp/screenshot.png --group 843812FF4BA524086B77B60886C38AB3
```

### 批量发送图片（带间隔）

```bash
qqbot-send-media /photos/ --type image --delay 2000
```

## 支持的文件格式

### 图片
- JPG/JPEG, PNG, GIF, WebP, BMP

### 视频
- MP4, AVI, MOV, WMV

### 文档
- PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, TXT, ZIP

## 故障排除

### 发送失败
- 检查文件路径是否正确
- 检查文件大小是否超过 20MB
- 检查 QQBot 服务是否运行

### 图片无法显示
- 确保使用 `<qqimg>` 标签
- 检查文件扩展名
- 尝试转换为 JPG 格式

## 许可证

MIT
