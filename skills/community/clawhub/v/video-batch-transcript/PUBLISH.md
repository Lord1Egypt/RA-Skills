# Video Batch Transcript - ClawHub 发布说明

## 基本信息

- **技能名称**: video-batch-transcript
- **版本**: 1.0.0
- **发布日期**: 2026-03-05
- **分类**: 媒体处理 / 教育工具
- **标签**: video, transcript, youtube, bilibili, whisper, gpu, batch, notes

## 技能描述

通用视频批量转录工具 - 支持 1000+ 网站（B 站、YouTube、抖音、Twitch 等），使用 yt-dlp 批量下载视频音频，GPU 加速语音转文字（faster-whisper + CUDA），自动校正专业术语，生成结构化学习笔记。

### 核心功能

- 🌐 支持 1000+ yt-dlp 兼容网站
- 📥 批量下载视频/音频（单视频、合集、播放列表、频道）
- 🚀 GPU 加速转录（比 OpenAI Whisper 快 4-6 倍）
- 📝 自动生成结构化学习笔记
- 🔧 专业术语自动校正
- 💾 断点续传支持
- 📤 多格式导出（txt/md/docx）
- 🔐 支持需要登录的网站（cookies 配置）

## 支持的网站

### 国内平台
哔哩哔哩、抖音、快手、西瓜视频、腾讯视频、爱奇艺、优酷、微博视频、小红书

### 国际平台
YouTube、Vimeo、Dailymotion、Twitch、Twitter/X、Instagram、TikTok、Facebook

### 流媒体（需登录）
Netflix、Hulu、HBO、Disney+、Amazon Prime

### 音频平台
SoundCloud、Bandcamp、Spotify

### 教育平台
Coursera、edX、Udemy、Khan Academy、TED

**完整列表**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 安装要求

### 系统要求
- Python 3.8+
- ffmpeg（音频处理）
- NVIDIA GPU + CUDA（可选，用于 GPU 加速）

### Python 依赖
```bash
pip install yt-dlp faster-whisper pandas python-docx
```

### GPU 加速（可选）
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

## 使用示例

### 基础用法
```bash
# YouTube 视频
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/watch?v=xxx" \
  --output-dir "~/video-notes"

# B 站合集
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/collectiondetail?sid=xxx" \
  --output-dir "~/video-notes"
```

### GPU 加速
```bash
python scripts/batch_transcript.py \
  --url "xxx" \
  --device cuda \
  --model medium
```

### 使用 Cookies（需要登录的网站）
```bash
# 从浏览器获取 cookies
python scripts/batch_transcript.py \
  --url "https://youtube.com/watch?v=xxx" \
  --cookies-from-browser chrome
```

## 更新日志

### v1.0.0 (2026-03-05)
- 初始版本发布
- 支持 1000+ yt-dlp 兼容网站
- GPU 加速转录（faster-whisper）
- 结构化笔记生成
- 断点续传支持
- 多格式导出
- Cookies 登录支持
- 术语校正功能
- 并行处理支持

## 技术实现

### 核心组件
- **yt-dlp**: 视频/音频下载（支持 1000+ 网站）
- **faster-whisper**: GPU 加速语音识别
- **自定义脚本**: 批量处理、笔记生成、术语校正

### 性能优化
- GPU 加速（CUDA）
- 多进程并行处理
- 断点续传
- 智能缓存

## 发布元数据

```json
{
  "name": "video-batch-transcript",
  "version": "1.0.0",
  "description": "通用视频批量转录工具 - 支持 1000+ 网站，GPU 加速语音转文字",
  "category": "媒体处理",
  "tags": ["video", "transcript", "youtube", "bilibili", "whisper", "gpu", "batch", "notes"],
  "author": "OpenClaw Community",
  "license": "MIT",
  "python_version": ">=3.8",
  "gpu_support": true,
  "dependencies": [
    "yt-dlp>=2024.0.0",
    "faster-whisper>=1.0.0",
    "pandas>=2.0.0",
    "python-docx>=1.0.0"
  ],
  "optional_dependencies": {
    "gpu": ["torch>=2.0.0"]
  },
  "system_requirements": [
    "ffmpeg"
  ],
  "repository": "https://github.com/openclaw/skills/video-batch-transcript",
  "documentation": "https://github.com/openclaw/skills/video-batch-transcript/blob/main/README.md"
}
```

## 发布命令

```bash
# 发布到 ClawHub
cd /root/.openclaw/workspace/skills/video-batch-transcript
clawdhub publish --name video-batch-transcript --version 1.0.0
```

## 后续计划

- [ ] 飞书文档集成
- [ ] 更多输出格式（PDF、HTML）
- [ ] 多语言字幕支持
- [ ] 视频摘要生成
- [ ] 关键词提取
- [ ] 自动时间戳章节
- [ ] Web UI 界面

## 许可证

MIT License
