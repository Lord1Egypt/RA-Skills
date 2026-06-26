---
name: whisper-gpu-transcribe
description: Convert audio to SRT subtitles using OpenAI Whisper with automatic GPU acceleration for Intel XPU / NVIDIA CUDA / AMD ROCm / Apple Metal. Ideal for content creators as a free alternative to paid subtitle generation.
version: 1.0.2
metadata:
  openclaw:
    emoji: "🎙️"
    homepage: https://github.com/allanmeng/whisper-gpu-transcriber-skill
    requires:
      bins:
        - python
    install:
      - kind: pip
        package: openai-whisper
---

# 🎙️ Whisper GPU Audio Transcriber

Convert audio files to SRT subtitles using local Whisper models — **completely free**, offline, and GPU accelerated.

---

## Use Cases

- Content creation, free alternative to paid subtitle features (e.g., CapCut/剪映)
- Meeting recording to text
- Podcast/course subtitles

---

## Supported GPU Acceleration

| Device | Acceleration | FP16 |
|--------|-------------|------|
| Intel Arc Series | XPU | ❌ Auto disabled |
| NVIDIA GPUs | CUDA | ✅ Auto enabled |
| AMD GPUs | ROCm | ✅ Auto enabled |
| Apple M Series | Metal | ✅ Auto enabled |
| No GPU | CPU | ❌ Auto disabled |

---

## Usage

### Basic Usage

Place the audio file in your current working directory and tell the AI:

```
Convert xxx.mp3 to SRT subtitles
```

Or specify the full path directly:

```
Convert /path/to/audio.mp3 to SRT subtitles
```

### Advanced Usage

```
Convert xxx.mp3 to English subtitles using large-v3-turbo model

Convert xxx.mp3 to subtitles, language is Japanese
```

---

## Execution

AI will execute the `scripts/transcribe.py` script, which will:

1. Automatically detect available GPU and select optimal acceleration
2. Load Whisper model (default: `turbo`)
3. Transcribe audio to SRT format
4. Save output in the same directory as the audio

---

## Requirements

- Python 3.8+
- PyTorch (version matching your hardware)
  - Intel GPU: `pip install torch==2.10.0+xpu`
  - NVIDIA GPU: `pip install torch --index-url https://download.pytorch.org/whl/cu121`
  - CPU: `pip install torch`
- openai-whisper: Automatically installed via `pip install openai-whisper`

---

## Notes

- First run will auto-download the model file (turbo ~1.5GB)
- Models cache in `~/.cache/whisper` by default, use symlink/Junction to redirect to another disk
- Intel XPU requires Intel Arc GPU + matching PyTorch version

> **Tip for China users**: If model download fails, manually download from mirror sites and place in `~/.cache/whisper/`

---

## Supported Models

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 39M | Fastest | Low |
| `base` | 74M | Fast | Medium |
| `small` | 244M | Medium | Medium |
| `medium` | 769M | Slow | High |
| `turbo` | 809M | Medium | High ✅ Recommended |
| `large-v3` | 1550M | Slowest | Highest |
| `large-v3-turbo` | 1550M | Slow | Highest |

---
---

# 🎙️ Whisper GPU 音频转字幕

使用本地 Whisper 模型将音频文件转录为 SRT 字幕，**完全免费**，无需联网，支持 GPU 加速。

---

## 适用场景

- 自媒体视频制作，替代剪映付费字幕功能
- 会议录音转文字
- 播客/课程内容转字幕

---

## 支持的 GPU 加速

| 设备 | 加速方式 | FP16 |
|------|---------|------|
| Intel Arc 系列 | XPU | ❌ 自动禁用 |
| NVIDIA 显卡 | CUDA | ✅ 自动启用 |
| AMD 显卡 | ROCm | ✅ 自动启用 |
| Apple M 系列 | Metal | ✅ 自动启用 |
| 无独显 | CPU | ❌ 自动禁用 |

---

## 使用方法

### 基础用法

将音频文件放入当前工作目录，然后告诉 AI：

```
把 xxx.mp3 转成 SRT 字幕文件
```

或者直接指定路径：

```
把 /path/to/audio.mp3 转成 SRT 字幕
```

### 高级用法

```
把 xxx.mp3 用 large-v3-turbo 模型转成英文字幕

把 xxx.mp3 转成字幕，语言是日语
```

---

## 执行方式

AI 会调用 `scripts/transcribe.py` 脚本执行转录，脚本会：

1. 自动检测可用 GPU 设备并选择最优加速方式
2. 加载 Whisper 模型（默认 `turbo`）
3. 将音频转录为 SRT 格式字幕
4. 输出文件保存在与音频同目录

---

## 环境要求

- Python 3.8+
- PyTorch（版本需匹配硬件）
  - Intel GPU：`pip install torch==2.10.0+xpu`
  - NVIDIA GPU：`pip install torch --index-url https://download.pytorch.org/whl/cu121`
  - CPU：`pip install torch`
- openai-whisper：由 ClawHub 通过 `pip install openai-whisper` 自动安装

---

## 注意事项

- 首次运行会自动下载模型文件（turbo 约 1.5GB）
- 模型默认缓存在 `~/.cache/whisper`，可用软链接/Junction 指向其他磁盘
- Intel XPU 需要 Intel Arc 独显 + 对应版本 PyTorch

> **国内用户提示**：首次运行会自动下载模型，如下载失败可手动从镜像站下载后放入 `~/.cache/whisper/`

---

## 支持的模型

| 模型 | 大小 | 速度 | 准确度 |
|------|------|------|--------|
| `tiny` | 39M | 最快 | 低 |
| `base` | 74M | 快 | 中 |
| `small` | 244M | 中 | 中 |
| `medium` | 769M | 慢 | 高 |
| `turbo` | 809M | 中 | 高 ✅ 推荐 |
| `large-v3` | 1550M | 最慢 | 最高 |
| `large-v3-turbo` | 1550M | 慢 | 最高 |
