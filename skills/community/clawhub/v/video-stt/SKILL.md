---
name: video-stt
description: "Extract audio from video URLs and transcribe using STT (Speech-to-Text). Supports local Whisper or cloud APIs. Use when: user provides a video URL and wants to know what is being said, transcribing YouTube videos, podcasts, or any video with audio."
metadata:
  {
    "openclaw": { "emoji": "🎬" },
    "version": "1.0.0",
  }
---

# Video STT Skill

从视频 URL 提取音频并转换为文字 (Speech-to-Text)

## 环境要求

- **yt-dlp** - 下载视频/音频
- **ffmpeg** - 提取音频
- **Python** - 使用 uv 虚拟环境

## 快速开始

```bash
# 进入脚本目录
cd ~/.openclaw/workspace/skills/video-stt/scripts

# 运行转录
bash stt.sh "视频URL"
```

## 使用方法

```bash
# 基本用法
bash stt.sh "https://youtube.com/watch?v=xxx"

# 指定输出文件
bash stt.sh "https://youtube.com/watch?v=xxx" -o output.txt

# 使用本地 Whisper 模型
bash stt.sh "https://youtube.com/watch?v=xxx" --local

# 使用云端 API
bash stt.sh "https://youtube.com/watch?v=xxx" --api openai
```

## 支持的模型

### 本地 (免费)
- tiny - 最快，质量一般
- base - 平衡
- small - 较好
- medium - 很好
- large - 最佳（需要更多内存）

### 云端 API
- OpenAI Whisper API
- Azure Speech
- Google Speech

## 输出格式

默认输出纯文本，可选：
- `.txt` - 纯文本
- `.srt` - 字幕格式
- `.vtt` - WebVTT 字幕
- `.json` - 带时间戳的 JSON

## 环境变量

```bash
# OpenAI (如果使用云端)
export OPENAI_API_KEY="sk-xxx"

# 或者使用硅基流动 (更便宜)
export SILICONFLOW_API_KEY="xxx"
```

## 示例

```bash
# 转录 YouTube 视频
bash stt.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 指定模型
bash stt.sh "https://youtube.com/watch?v=xxx" --model medium

# 保存为 SRT
bash stt.sh "https://youtube.com/watch?v=xxx" --format srt
```

## Python 依赖

使用 uv 管理 Python 环境：
```bash
# 创建虚拟环境
uv venv
uv pip install yt-dlp whisper ffmpeg-python

# 运行
uv run python stt.py "视频URL"
```
