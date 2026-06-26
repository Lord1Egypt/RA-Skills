---
name: STT Recognizer | STT 识别器
description: |
  语音转文字（Speech-to-Text / STT）工具。
  支持从麦克风录音，使用 Whisper（faster-whisper）在本地进行语音转文字，
  或通过 OpenAI 兼容 API 进行云端转写。
  触发词：录音、语音转文字、STT、语音识别、转写、录音转文字。
  适用平台：Linux / Windows / macOS。
---

# STT Recognizer | STT 识别器 🎤

将语音转换为文字，支持本地推理和 API 调用。

---

## 文件结构

```
技能目录（发布用）：
~/.openclaw/workspace/skills/stt-recognizer/
├── SKILL.md           # 本文档
├── _meta.json         # 元数据
├── .clawhub/          # ClawHub 源信息
└── scripts/           # 运行时脚本
    ├── download_models.sh      # 下载模型
    ├── record_audio.py         # 录音
    ├── transcribe.py          # 转写
    └── record_and_transcribe.py # 一键录音+转写

项目目录（运行时数据）：
~/.openclaw/workspace/projects/stt-recognizer/
├── requirements.txt   # Python 依赖
├── recordings/       # 录音文件
└── transcriptions/   # 转写结果

模型缓存（统一命名，技能专属）：
~/.cache/huggingface/modules/stt-recognizer/
├── small/        # small 模型（464MB，默认使用）
└── base/        # base 模型（约 142MB，可选）
```

---

## 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [录音脚本](#录音脚本)
4. [转写脚本](#转写脚本)
5. [模型管理](#模型管理)
6. [输出目录](#输出目录)
7. [环境变量](#环境变量)
8. [故障排查](#故障排查)

---

## 概述

### 支持的转写引擎

| 引擎 | 说明 | 优点 |
|------|------|------|
| `faster-whisper` | 本地 GPU/CPU 高效推理 | 快速、免费、无需网络 |
| `whisper` | OpenAI 原生 Whisper | 准确、完整功能 |
| `api` | OpenAI 兼容 API | 可用云端算力、支持大模型 |

### 支持的音频格式

- WAV (推荐，16-bit PCM)
- MP3
- OGG
- FLAC
- M4A

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
pip install -r requirements.txt --break-system-packages
```

### 2. 下载模型

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
bash scripts/download_models.sh base
```

### 3. 录音并转写

```bash
# 方式一：一键录音+转写（推荐）
python3 scripts/record_and_transcribe.py --duration 10

# 方式二：分开执行
# 录制 10 秒音频
python3 scripts/record_audio.py --duration 10

# 转写音频文件
python3 scripts/transcribe.py ~/.openclaw/workspace/projects/stt-recognizer/recordings/recording_xxx.wav
```

---

## 录音脚本

### record_and_transcribe.py ⭐ 推荐

一键录音并转写，适合快速使用：

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
python3 scripts/record_and_transcribe.py --duration 10 --language zh
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--duration` | 10 | 录音时长（秒） |
| `--language` | (自动) | 语言代码，留空自动检测 |
| `--model` | base | 模型大小 |
| `--engine` | faster-whisper | 转写引擎 |

### record_audio.py

从麦克风录制音频，输出 WAV 文件。

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
python3 scripts/record_audio.py \
    --duration 10 \
    --sample-rate 16000 \
    --channels 1
```

**参数说明**:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--duration` | 10 | 录音时长（秒） |
| `--sample-rate` | 16000 | 采样率（Hz），Whisper 推荐 16000 |
| `--channels` | 1 | 声道数，1=单声道 |
| `--list-devices` | - | 列出可用的音频设备 |
| `--output-dir` | projects/stt-recognizer/recordings | 输出目录 |
| `--filename` | auto | 输出文件名 |

**示例**:

```bash
# 列出所有音频设备
python3 scripts/record_audio.py --list-devices

# 录制 30 秒
python3 scripts/record_audio.py --duration 30 --filename my_voice.wav
```

---

## 转写脚本

### transcribe.py

将音频文件转写为文字。

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
python3 scripts/transcribe.py audio.wav
```

**参数说明**:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `audio_file` | (必需) | 要转写的音频文件路径 |
| `--model` | base | 模型名称或路径 |
| `--language` | (不填) | 语言代码，如 `zh`、`en`、`ja`。留空则自动检测 |
| `--task` | transcribe | `transcribe`（转写）或 `translate`（翻译为英文） |
| `--engine` | auto | 转写引擎：`auto`、`faster-whisper`、`whisper`、`api` |
| `--api-url` | (env) | API URL（API 模式） |
| `--api-key` | (env) | API 密钥（API 模式） |
| `--output-dir` | projects/stt-recognizer/transcriptions | 输出目录 |

**模型选择**:

| 模型 | 大小 | 内存需求 | 速度 | 精度 |
|------|------|----------|------|------|
| `tiny` | ~39M | ~1GB | 最快 | 较低 |
| `base` | ~74M | ~1GB | 快 | 中等 |
| `small` | ~244M | ~2GB | 中 | 较高 |
| `medium` | ~769M | ~5GB | 慢 | 高 |
| `large` | ~1550M | ~10GB | 最慢 | 最高 |

**示例**:

```bash
# 转写（自动检测语言，推荐）
python3 scripts/transcribe.py audio.wav

# 使用 small 模型转写中文
python3 scripts/transcribe.py audio.wav --model small --language zh

# 使用 small 模型并翻译成英文
python3 scripts/transcribe.py audio.wav --model small --task translate

# 使用 API 转写
python3 scripts/transcribe.py audio.wav \
    --engine api \
    --api-url https://api.openai.com/v1 \
    --api-key sk-xxx \
    --model whisper-1
```

---

## 模型管理

### 模型存放位置

模型统一存放在缓存位置，**按技能命名目录**，清晰不混乱：

```
~/.cache/huggingface/modules/stt-recognizer/
├── small/        # small 模型（464MB，当前使用）
└── base/        # base 模型（约 142MB）

# 模型文件结构示例：
~/.cache/huggingface/modules/stt-recognizer/small/
├── model.bin        # 462MB（实际模型）
├── tokenizer.json   # 2.2MB
├── config.json      # 2.4KB
└── vocabulary.txt   # 450KB
```

### 下载模型

首次使用需下载 Whisper 模型（存放在 HuggingFace 缓存，不占技能目录）：

```bash
cd ~/.openclaw/workspace/skills/stt-recognizer
bash scripts/download_models.sh base

# 可选模型大小: tiny, base, small, medium, large
bash scripts/download_models.sh small
```

### 模型搜索路径

脚本按以下顺序查找模型：
1. 环境变量 `STT_MODEL_PATH`
2. `~/.cache/huggingface/modules/`  ← 主要位置
3. `~/.openclaw/workspace/projects/stt-recognizer/models/`  ← 工作区备份

---

## 输出目录

运行结果统一保存在工作区的 `projects/stt-recognizer/` 目录下：

```
~/.openclaw/workspace/projects/stt-recognizer/
├── recordings/       # 原始录音文件 (record_audio.py)
│   └── recording_20260401_123456.wav
└── transcriptions/  # 转写结果 (transcribe.py)
    └── recording_20260401_123456.txt
```

---

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `OPENCLAW_WORKSPACE` | 工作区根目录 |
| `STT_MODEL_PATH` | Whisper 模型路径 |
| `STT_API_URL` | OpenAI 兼容 API URL |
| `STT_API_KEY` | API 密钥 |

**API 模式设置示例**:

```bash
export STT_API_URL=https://api.openai.com/v1
export STT_API_KEY=sk-your-key
```

---

## 故障排查

### 录音失败

**检查音频设备**:

```bash
python3 scripts/record_audio.py --list-devices
```

**解决方案**:
- Linux: 安装 `portaudio19-dev` 或 `libasound-dev`
- Windows: 安装 PyAudio wheel
- macOS: 可能需要给终端麦克风权限

**安装音频依赖**:

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev libasound-dev

# macOS
brew install portaudio

# 然后安装 PyAudio
pip install pyaudio

# 安装依赖
cd ~/.openclaw/workspace/skills/stt-recognizer
pip install -r requirements.txt --break-system-packages
```

### 转写速度慢

**使用 faster-whisper**（推荐，比原版快 2-4 倍）:

```bash
pip install faster-whisper
```

**降低模型大小**:

```bash
# 使用 tiny 模型（最快）
python3 scripts/transcribe.py audio.wav --model tiny
```

**使用 GPU**:

```bash
# 确认 CUDA 可用
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### 模型下载失败

```bash
# 使用镜像
export HF_ENDPOINT=https://hf-mirror.com

# 手动下载
python3 -c "from faster_whisper import download_model; download_model('base', output_dir='models/')"
```

### API 模式错误

- 确认 API URL 正确（包含 `/v1`）
- 确认 API Key 有效
- 检查网络连接

---

## 平台特定说明

### Linux
- **音频后端**: ALSA + PulseAudio
- **录音工具**: PyAudio 或 arecord
- **权限**: 确保用户在 `audio` 组
  ```bash
  sudo usermod -a -G audio $USER
  ```

### Windows
- **音频后端**: WASAPI / DirectSound
- **录音工具**: PyAudio
- **注意**: 部分驱动可能需要管理员权限

### macOS
- **音频后端**: Core Audio + AVFoundation
- **录音工具**: PyAudio
- **权限**: 系统偏好设置 → 安全性与隐私 → 麦克风 → 允许终端
- Apple Silicon 支持 MPS 加速

### GTX 10xx / Pascal 显卡兼容性
- GTX 10xx 系列（Pascal 架构）不支持高效的 float16
- 脚本已自动降级为 float32，不会报错但速度稍慢

## 目录结构

### 技能目录（发布用）

```
stt-recognizer/
├── SKILL.md           # 本文档
├── _meta.json         # 元数据
├── .clawhub/          # ClawHub 源信息
└── scripts/           # 运行时脚本
    ├── download_models.sh      # 下载模型
    ├── record_audio.py         # 录音脚本
    ├── transcribe.py           # 转写脚本
    └── record_and_transcribe.py # ⭐ 一键录音+转写
```

### 项目目录（运行时数据）

```
~/.openclaw/workspace/projects/stt-recognizer/
├── requirements.txt   # Python 依赖
├── recordings/        # 录音文件
└── transcriptions/   # 转写结果
```

### 模型缓存

```
~/.cache/huggingface/modules/stt-recognizer/
├── small/        # small 模型
└── base/        # base 模型
```

---

## 依赖

```
# requirements.txt
faster-whisper>=1.0.0
pyaudio>=0.2.14
openai>=1.0.0
numpy>=1.24.0
torch>=2.0.0
```
