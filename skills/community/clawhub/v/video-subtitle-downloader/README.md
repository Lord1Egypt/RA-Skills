# 🎬 Video Subtitle Downloader

> 一键下载 YouTube/B站 等1000+平台的视频字幕

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## ✨ 功能特点

- 🌐 **1000+平台支持** - YouTube, B站, Twitter, Vimeo, TED...
- 📝 **多格式导出** - SRT, JSON, TXT
- 🤖 **自动字幕下载** - 自动字幕 + 手动字幕
- ⚡ **GPU加速转录** - 支持 Whisper GPU 加速（可选）
- 📦 **批量处理** - 支持URL列表批量下载

## 🚀 快速开始

### 安装

```bash
pip install yt-dlp faster-whisper
```

### 下载单个视频字幕

```bash
python scripts/download_subtitle.py "https://www.youtube.com/watch?v=VIDEO_ID" --format srt
```

### 批量下载

创建 `urls.txt`：
```
# 视频URL列表
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.bilibili.com/video/BV1xx411c7XD
https://twitter.com/user/status/123456
```

运行：
```bash
python scripts/batch_download.py urls.txt --format json
```

## 📁 输出示例

```
subtitles/
├── Video Title 1.srt      # SRT格式（带时间轴）
├── Video Title 2.json     # JSON格式（结构化数据）
└── Video Title 3.txt      # TXT格式（纯文本）
```

## 💰 定价

| 套餐 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 每月5个视频 |
| 专业版 | ¥19/月 | 无限使用 + GPU加速 |
| 企业版 | ¥99/月 | API接口 + 批量处理 |

## 🔧 配置

### 字幕语言
```bash
# 指定语言
python scripts/download_subtitle.py "URL" --sub-langs "zh-CN,en"
```

### 输出路径
```bash
python scripts/download_subtitle.py "URL" --output "./my_subtitles"
```

## 📝 License

MIT License - 可以自由使用、修改、销售
