---
name: stt-simple
version: 1.0.0
description: >
  Simple local Speech-To-Text using Whisper. One-command install with auto model download.
  Supports 99+ languages.
homepage: https://openai.com/research/whisper
---

# Simple Local STT (Whisper)

一键安装本地语音识别，支持 99+ 语言。  
One-click local speech recognition supporting 99+ languages.

## 🚀 快速开始 / Quick Start

### 安装（首次使用）/ Installation (First Time)

```bash
# 自动安装虚拟环境 + 依赖 + 模型
# Auto-installs virtual env + dependencies + model
/root/.openclaw/workspace/skills/stt-simple/install.sh
```

### 使用 / Usage

```bash
# 命令行转换 / Command line conversion
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese

# Python API
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/stt_simple.py \
  audio.ogg small zh
```

## 📦 安装脚本详解 / Install Script Details

`install.sh` 自动完成 / automatically completes:

1. ✅ 创建虚拟环境 / Create virtual env: `/root/.openclaw/venv/stt-simple/`
2. ✅ 安装 / Install: `openai-whisper` + `ffmpeg`
3. ✅ 下载 Whisper small 模型（244MB）/ Download Whisper small model (244MB)
4. ✅ 创建输出目录 / Create output directory

## 🎯 模型选择 / Model Selection

| 模型 / Model | 大小 / Size | 速度 / Speed | 精度 / Accuracy | 场景 / Use Case |
|------|------|------|------|------|
| `tiny` | 39MB | ⚡⚡⚡ | ⭐⭐⭐ | 快速测试 / Quick testing |
| `base` | 74MB | ⚡⚡ | ⭐⭐⭐⭐ | 日常使用 / Daily use |
| `small` | 244MB | ⚡ | ⭐⭐⭐⭐⭐ | **推荐 / Recommended** |
| `medium` | 769MB | 🐌 | ⭐⭐⭐⭐⭐ | 高精度 / High accuracy |
| `large` | 1.5GB | 🐌🐌 | ⭐⭐⭐⭐⭐+ | 最佳质量 / Best quality |

## 🌍 语言代码 / Language Codes

- 中文 / Chinese：`zh` 或 `Chinese`
- 英文 / English：`en` 或 `English`
- 日文 / Japanese：`ja` 或 `Japanese`
- 自动检测 / Auto-detect：省略 `--language` / omit `--language`

## 📁 输出格式 / Output Formats

- `.txt` - 纯文本 / Plain text
- `.json` - 完整结果（含时间戳）/ Full results (with timestamps)
- `.srt` - 字幕格式 / Subtitle format
- `.vtt` - WebVTT

## 🔧 故障排查 / Troubleshooting

```bash
# 检查安装 / Check installation
/root/.openclaw/venv/stt-simple/bin/whisper --version

# 重新安装 / Reinstall
rm -rf /root/.openclaw/venv/stt-simple
/root/.openclaw/workspace/skills/stt-simple/install.sh
```
