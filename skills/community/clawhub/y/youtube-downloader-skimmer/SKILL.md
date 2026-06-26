---
name: "youtube-downloader-skimmer"
slug: "youtube-downloader-skimmer"
description: "下载 YouTube 视频并自动剪辑关键片段"
version: "1.0.0"
author: "OpenClaw User"
license: "MIT"
tags: ["youtube", "download", "video", "clip", "automation"]
---

# YouTube Video Downloader & Skimmer

**功能**：下载 YouTube 视频并自动剪辑关键片段

## 使用方式

### 基础用法
```
youtube-downloader-skimmer "YouTube 视频 URL"
```

### 高级用法
```
youtube-downloader-skimmer "URL" --chapters "章节 1:0-60,章节 2:60-180"
youtube-downloader-skimmer "URL" --output-format "mp4,mp3"
youtube-downloader-skimmer "URL" --quality "best"
```

## 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | YouTube 视频 URL（必填） | - |
| `--chapters` | 自定义章节时间范围 | 自动检测（如有） |
| `--output-format` | 输出格式：mp4, mp3, 或两者 | mp4 |
| `--quality` | 视频质量：best, 1080p, 720p, 480p | best |
| `--send-to` | 发送平台：qq, telegram | qq |
| `--delete-raw` | 删除原始视频 | true |
| `--output-dir` | 输出目录 | `/tmp/openclaw/` |

## 工作流程

1. **检测章节**：自动获取 YouTube 视频章节信息（如有）
2. **下载安装**：使用 yt-dlp 下载视频
3. **剪辑片段**：按章节或手动指定时间剪辑
4. **文件交付**：发送到指定平台
5. **清理文件**：可选删除原始视频

## 示例

### 下载并剪辑所有章节
```
youtube-downloader-skimmer "https://www.youtube.com/watch?v=xxx"
```

### 指定章节时间范围
```
youtube-downloader-skimmer "https://www.youtube.com/watch?v=xxx" \\
  --chapters "介绍：0-60,Sora 评测：60-300,Kling 评测：300-540"
```

### 下载为 MP3 音频
```
youtube-downloader-skimmer "https://www.youtube.com/watch?v=xxx" \\
  --output-format mp3
```

### 指定质量并发送到 Telegram
```
youtube-downloader-skimmer "https://www.youtube.com/watch?v=xxx" \\
  --quality 1080p \\
  --send-to telegram
```

## 依赖要求

- Python 3.x
- yt-dlp (`pip install yt-dlp`)
- ffmpeg

## 注意事项

- YouTube 视频需可公开访问
- 某些视频可能没有章节信息
- 长视频下载可能需要较长时间
- 需要网络连接

## 输出文件命名

```yaml
格式：clip_编号_章节名称.mp4
示例：
- clip_01_Introduction.mp4
- clip_02_Sora_2.mp4
- clip_03_Kling_2.6.mp4
```

---

*技能版本：1.0.0*
*创建日期：2026-04-04*
