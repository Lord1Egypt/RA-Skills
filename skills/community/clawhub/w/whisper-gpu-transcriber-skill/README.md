# 🎙️ Whisper GPU Audio Transcriber

Convert audio files to SRT subtitles using local Whisper models — **completely free**, offline, and GPU accelerated.

## ✨ Features

- **100% Free** — Local execution, no API costs, alternative to paid subtitle services
- **GPU Accelerated** — Automatic detection and usage of Intel XPU / NVIDIA CUDA / AMD ROCm / Apple Metal
- **Smart Adaptation** — Automatically selects optimal parameters (e.g., disables FP16 for Intel XPU)
- **High Accuracy** — Supports Whisper Turbo model for balanced speed and quality

## 📦 Use Cases

- Content creation (YouTube, Bilibili, TikTok, etc.)
- Meeting transcription
- Podcast/course subtitles
- Stream replay organization

## 🚀 Quick Start

### Install Dependencies

```bash
pip install openai-whisper
```

Install PyTorch matching your hardware:

```bash
# Intel GPU
pip install torch==2.10.0+xpu

# NVIDIA GPU
pip install torch --index-url https://download.pytorch.org/whl/cu121

# CPU
pip install torch
```

### Usage

After installing this Skill, simply tell the AI:

```
Convert xxx.mp3 to SRT subtitles
```

Or specify the full path:

```
Convert /path/to/audio.mp3 to SRT subtitles
```

### Advanced Usage

```
Convert xxx.mp3 to English subtitles using large-v3-turbo model
Convert xxx.mp3 to subtitles, language is Japanese
```

## 🎬 Supported Subtitle Platforms

The generated `.srt` subtitle files can be used directly in these platforms:

### Video Editing Software
| Software | Support |
|----------|---------|
| **剪映 (Jianying)** | ✅ Full support, editable styles after import |
| **Adobe Premiere Pro** | ✅ Native support |
| **DaVinci Resolve** | ✅ Native support |
| **Final Cut Pro** | ✅ Native support (via plugin) |
| **CapCut (Desktop)** | ✅ Full support |

### Media Players
| Player | Support |
|--------|---------|
| **PotPlayer** | ✅ Auto-loads same-named SRT files |
| **VLC Media Player** | ✅ Auto-loads same-named SRT files |
| **IINA (macOS)** | ✅ Auto-loads same-named SRT files |
| **MPV** | ✅ Auto-loads same-named SRT files |
| **QQ Player** | ✅ Auto-loads same-named SRT files |

### Online Platforms
| Platform | Support | Notes |
|----------|---------|-------|
| **Bilibili** | ✅ Upload with subtitles | Direct SRT upload supported |
| **YouTube** | ✅ Creator Studio | Subtitle track upload supported |
| **TikTok (Douyin)** | ✅ Via Jianying | Cannot upload SRT directly, import via Jianying |
| **WeChat Channels** | ⚠️ Conversion needed | May require format conversion |
| **Xigua Video** | ✅ Like Bilibili | SRT format supported |

### Subtitle Editing Tools
| Tool | Purpose |
|------|---------|
| **Subtitle Edit** | Professional subtitle editing, SRT support |
| **Aegisub** | Anime subtitle production |
| **Arctime** | Domestic subtitle editing software |
| **Notepad++** | Simple text editing |

> 💡 **Tip**: Most platforms automatically load `.srt` files with the same name as the video file. For example, `video.mp4` will automatically load `video.srt`.

## 🖥️ Supported GPU Acceleration

| Device | Acceleration | FP16 | Notes |
|--------|-------------|------|-------|
| Intel Arc Series | XPU | ❌ Auto-disabled | Requires PyTorch XPU version |
| NVIDIA GPUs | CUDA | ✅ Auto-enabled | Recommended for RTX 30/40 series |
| AMD GPUs | ROCm | ✅ Auto-enabled | Best support on Linux |
| Apple M1/M2/M3 | Metal | ✅ Auto-enabled | Native macOS support |
| No GPU | CPU | ❌ Auto-disabled | Fallback option |

## 📊 Supported Whisper Models

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|----------------|
| `tiny` | 39M | Fastest | Low | Quick preview |
| `base` | 74M | Fast | Medium | Daily use |
| `small` | 244M | Medium | Medium | Balanced choice |
| `medium` | 769M | Slow | High | High-quality needs |
| `turbo` | 809M | Medium | High | ✅ **Default recommended** |
| `large-v3` | 1550M | Slowest | Highest | Professional needs |
| `large-v3-turbo` | 1550M | Slow | Highest | Professional needs |

## ⚙️ Execution

AI will execute the `scripts/transcribe.py` script in your project directory, which will:

1. Automatically detect available GPU devices and select optimal acceleration
2. Load Whisper model (default: `turbo`)
3. Transcribe audio to SRT format
4. Save output in the same directory as the audio

## 📝 Notes

- First run will auto-download the model file (turbo ~1.5GB)
- Models cache in `~/.cache/whisper` by default, can use symlink/Junction to redirect
- Intel XPU requires Intel Arc GPU + matching PyTorch version
- China users: If model download fails, manually download from mirror sites and place in `~/.cache/whisper/`

## 🔧 Requirements

- Python 3.8+
- PyTorch (version matching your hardware)
- openai-whisper

## 📄 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 🇨🇳 中文文档

[README_ZH.md](README_ZH.md) - Complete documentation in Chinese / 完整的中文文档
