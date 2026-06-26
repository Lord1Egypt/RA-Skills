---
name: xia-zhuan-audio
description: 🎵 音视频格式转换与处理工具箱。基于 FFmpeg + Whisper AI，支持：格式转换、视频提取音频、合并、分割、压缩、查看信息、音频转文字。
license: MIT
metadata:
  homepage: "https://github.com/luis12123899/xia-zhuan-audio"
  emoji: "🎵"
  requires:
    bins:
      - ffmpeg
    env:
      - XZA_FFMPEG
      - XZA_FFPROBE
      - XZA_SCRIPTDIR
      - XZA_MODELDIR
      - HF_ENDPOINT
---

# 虾转音频 (xia-zhuan-audio)

## 功能列表

| # | 功能 | 说明 |
|---|------|------|
| 1 | 格式转换 | m4a→mp3, wav→flac, ape→flac, aac→mp3 等，支持 20+ 格式 |
| 2 | 视频提取音频 | mp4/mkv/avi/flv → mp3/aac/wav 等 |
| 3 | 合并音频 | 将多个音频拼接成一个文件 |
| 4 | 分割音频 | 按时间范围截取片段 |
| 5 | 压缩音频 | 减小文件体积（64k/128k/192k） |
| 6 | 查看音频信息 | 时长 / 码率 / 采样率 / 声道 / 元数据 |
| 7 | 音频转文字 | Whisper AI 自动转录，支持 txt / srt / vtt / json |

## 支持的格式

**音频格式：** mp3, wav, flac, aac, m4a, ogg, wma, aiff, opus, ape, alac
**视频格式：** mp4, mkv, avi, mov, flv, wmv, webm

## 环境变量配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `XZA_FFMPEG` | FFmpeg/FFprobe 路径 | 系统 PATH 中查找 |
| `XZA_FFPROBE` | FFprobe 路径 | 从 XZA_FFMPEG 推断 |
| `XZA_SCRIPTDIR` | 脚本目录 | 自动检测 |
| `XZA_MODELDIR` | Whisper 模型保存目录 | 技能目录下的 whisper_models |
| `HF_ENDPOINT` | HuggingFace 模型下载源 | https://huggingface.co（官方）|

## 依赖

- **FFmpeg** — 系统已有或从 https://ffmpeg.org 下载，并在 PATH 中可用
- **Python** — 系统已有（用于音频转文字）
- **faster-whisper** — 运行 `pip install faster-whisper` 安装

### Whisper 模型安全说明

模型通过 HuggingFace 官方源下载（默认），如需使用国内镜像：
```bash
set HF_ENDPOINT=https://hf-mirror.com
```

## 使用方式

### 通过 OpenClaw 对话触发（推荐）

直接用自然语言描述需求，例如：
- "把这段 m4a 转成 mp3"
- "把这个视频的音频提取出来"
- "把这几个音频合并成一个"
- "把这段音频 1:30 到 2:45 的部分截出来"
- "压缩这个音频，128kbps"
- "查看这个音频的信息"
- "把这段录音转成文字"

### 通过命令行直接调用

```bash
# 格式转换
node audio-forge.js convert <输入> <输出格式> [--bitrate 192k]

# 视频提取音频
node audio-forge.js extract <视频> [输出格式] [--bitrate 192k]

# 合并音频
node audio-forge.js merge <文件1> <文件2> [...] <输出>

# 分割音频
node audio-forge.js split <输入> <开始时间> <结束时间>

# 压缩音频
node audio-forge.js compress <输入> [--quality low|medium|high]

# 查看音频信息
node audio-forge.js info <音频文件>

# 音频转文字（Whisper）
python transcribe.py <音频/视频文件> [--model small] [--language zh] [--format txt] [--device auto]
```

## 音频转文字 - Whisper 模型

| 模型 | 精度 | 速度 | 首次下载 |
|------|------|------|----------|
| tiny | 较低 | 最快 | ~75MB |
| base | 标准 | 快 | ~150MB |
| small | 良好 | 较快 | ~460MB |
| medium | 很好 | 较慢 | ~1.5GB |
| large | 最高 | 最慢 | ~3GB |

## 安装

```bash
openclaw skill install xia-zhuan-audio
```

或直接把 `xia-zhuan-audio` 文件夹放入 `~/.openclaw/workspace/skills/` 目录。

---

创建：2026-04-11 | 作者：@luis12123899
