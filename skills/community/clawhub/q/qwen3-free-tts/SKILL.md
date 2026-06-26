---
name: free-tts-voice-cloning
name_zh: 免费文字转语音与克隆
description: 🆓 完全免费的本地文字转语音(TTS)与声音克隆技能。基于 Qwen3-TTS-1.7B 模型，支持 Apple Silicon，无需联网，保护隐私。可用于有声书制作、AI 角色配音、无障碍应用等场景。
description_en: 🆓 FREE local Text-to-Speech (TTS) & Voice Cloning skill. Based on Qwen3-TTS-1.7B model, Apple Silicon optimized, runs locally without internet, privacy protected.
categories: [audio, tts, voice-cloning, generative-ai, free, tools]
keywords: [免费语音合成, 免费声音克隆, 文字转语音, 免费TTS, TTS, Text-to-Speech, Voice Cloning, Qwen3-TTS, mlx-audio, Apple Silicon]
platforms: [macOS]
author: OpenClaw 社区
author_en: OpenClaw Community
license: MIT
price: free
---

# 🎤 免费文字转语音与克隆 (Free TTS & Voice Cloning)

🆓 **完全免费**的本地文字转语音(TTS)与声音克隆技能。无需 API Key，无需联网，无任何使用限制。支持**声音克隆**（10秒音频克隆任意声音）、**文字转语音**（12+内置声音）、**翻译配音**（配合翻译工具实现多语言配音）。

High-quality **100% FREE** local TTS voice synthesis and voice cloning skill. No API key required, no internet needed, unlimited usage. Supports **voice cloning**, **text-to-speech**, and **translation dubbing**.

## ✨ 功能特性

- **🆓 完全免费**: 无 API 费用，无调用限制，永久免费使用
- **🔊 高质量语音合成**: 基于 Qwen3-TTS-1.7B 模型，输出自然流畅
- **🎭 声音克隆**: 只需 10-30 秒参考音频，即可克隆任意声音
- **🎛️ 多声音模板**: 内置 12+ 种不同风格和特点的声音模板
- **⚡ Apple Silicon 优化**: 基于 MLX 框架，本地推理速度快
- **🌍 多语言支持**: 支持中文、英文、日文、韩文等多种语言
- **🔒 隐私保护**: 所有处理在本地运行，不上传任何数据到云端
- **📝 翻译配音**: 配合翻译工具可实现多语言翻译+配音工作流

## ✨ Features

- **🔊 High-Quality Synthesis**: Powered by Qwen3-TTS-1.7B model for natural-sounding speech
- **🎭 Voice Cloning**: Clone any voice with just 10-30 seconds of reference audio
- **🎛️ Multiple Voice Templates**: 12+ built-in voices with different styles and characteristics
- **⚡ Apple Silicon Optimized**: Built on MLX framework for fast local inference
- **🌍 Multi-Language Support**: Chinese, English, Japanese, Korean, and more
- **🔒 Privacy-First**: All processing runs locally, no data sent to cloud

## 📋 系统要求

| 项目 | 要求 |
|------|------|
| 芯片 | Apple Silicon (M1/M2/M3/M4) |
| 系统 | macOS 12.0+ |
| Python | 3.10+ |
| 内存 | 建议 8GB+ |
| 磁盘空间 | 约 3GB 用于模型文件 |

## 📋 Requirements

| Item | Requirement |
|------|-------------|
| Chip | Apple Silicon (M1/M2/M3/M4) |
| OS | macOS 12.0+ |
| Python | 3.10+ |
| RAM | 8GB+ recommended |
| Disk Space | ~3GB for model files |

## 🚀 快速安装

### 方法一：一键安装

```bash
chmod +x install_dependencies.sh && ./install_dependencies.sh
```

### 方法二：手动安装

```bash
# 1. 安装系统依赖
brew install python@3.10 ffmpeg

# 2. 安装 Python 包
python3.10 -m pip install mlx-audio
```

## 🚀 Quick Installation

### Method 1: One-Click Install

```bash
chmod +x install_dependencies.sh && ./install_dependencies.sh
```

### Method 2: Manual Installation

```bash
# 1. Install system dependencies
brew install python@3.10 ffmpeg

# 2. Install Python packages
python3.10 -m pip install mlx-audio
```

## 🎯 使用指南

### 1. 交互式演示

```bash
python3.10 voice_cloning_demo.py
```

### 2. 声音克隆 API

从参考音频文件克隆任意声音：

## 🎯 Usage Guide

### 1. Interactive Demo

```bash
python3.10 voice_cloning_demo.py
```

### 2. Voice Cloning API

Clone any voice from a reference audio file:

```python
from mlx_audio.tts.utils import load_model
from mlx_audio.tts.generate import generate_audio

# Load model (auto-downloads on first run, ~3GB)
model = load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit')

# Generate cloned voice
generate_audio(
    model=model,
    text="Your text content here, supports long-form generation",
    ref_audio="path/to/reference_audio.wav",  # 10-30 second voice sample
    lang_code="zh",                          # zh, en, ja, ko, etc.
    file_prefix="output_filename",           # Output: output_filename_000.wav
    max_tokens=3000                          # Prevent audio truncation
)
```

### 3. Built-in Voice Templates

Generate speech without reference audio using pre-built voices:

```python
from mlx_audio.tts.utils import load_model

model = load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit')

# Generate speech with built-in voice template
results = list(model.generate(
    text='Hello world, this is a text-to-speech test',
    voice='af_heart',      # Voice template code
    language='Chinese'     # Language
))

# Save audio file
with open('output.wav', 'wb') as f:
    for result in results:
        f.write(result.audio)
```

## 🎵 Built-in Voice Templates

| Code | Style | Gender |
|------|-------|--------|
| `af_heart` | Warm & Friendly | Female |
| `af_chat` | Conversational | Female |
| `af_narration` | Storytelling | Female |
| `af_emo` | Expressive | Female |
| `am_adventure` | Adventurous | Male |
| `am_broadcast` | Professional | Male |
| `am_chat` | Conversational | Male |
| `am_narration` | Storytelling | Male |
| `am_emo` | Expressive | Male |
| `us_af` | American English | Female |
| `us_am` | American English | Male |
| `cn_am` | Chinese Mandarin | Male |
| `jp_af` | Japanese | Female |

## 📝 Best Practices

### Reference Audio Preparation

1. **Duration**: 10-30 seconds of clear human speech
2. **Format**: WAV format, mono, 16kHz/24kHz
3. **Environment**: Quiet room, no background noise
4. **Content**: Natural conversational speech, avoid extreme emotions

### Quality Optimization

```python
# Recommended parameters for best quality
generate_audio(
    model=model,
    text="Your text here",
    ref_audio="reference.wav",
    lang_code="zh",
    file_prefix="output",
    max_tokens=3000,        # Increase for longer text
    temperature=0.8,        # Diversity control (0.5-1.0)
    repetition_penalty=1.1  # Reduce repetition
)
```

### Batch Generation

```python
# Batch processing example
texts = [
    "First paragraph text",
    "Second paragraph text",
    "Third paragraph text",
]

for i, text in enumerate(texts):
    generate_audio(
        model=model,
        text=text,
        ref_audio="reference_audio.wav",
        lang_code="zh",
        file_prefix=f"batch_{i:03d}",
        max_tokens=3000
    )
    print(f"Generated: batch_{i:03d}_000.wav")
```

## 🔧 Troubleshooting

### Common Issues

**Q: Audio gets truncated?**
```python
# Increase max_tokens parameter
generate_audio(..., max_tokens=5000)
```

**Q: Slow model download?**
```bash
# Use Hugging Face mirror
export HF_ENDPOINT=https://hf-mirror.com
python3.10 your_script.py
```

**Q: Poor cloning quality?**
- Ensure reference audio is clear with no background noise
- Optimal reference duration: 15-25 seconds
- Try different reference audio recordings
- Match text style to reference voice style

**Q: Python version issues?**
```bash
# Verify Python 3.10 path
which python3.10
/opt/homebrew/bin/python3.10  # Confirm path

# Use full path to call
/opt/homebrew/bin/python3.10 your_script.py
```

## ⚖️ Legal Notice & Disclaimer

### Important Legal Information

This skill is intended **for legal and ethical use only**. By using this skill, you agree to the following terms:

#### 1. Voice Cloning Ethics
- **Only clone voices that you own** or have **explicit written permission** to clone
- **Do not** use this skill to impersonate others without consent
- **Do not** use this skill for fraudulent, deceptive, or malicious purposes
- Respect privacy rights and obtain proper authorization for all voice data you process

#### 2. Copyright Compliance
- Ensure you have the legal right to use and reproduce any text content converted to speech
- Generated audio content may be subject to copyright laws in your jurisdiction
- Users are solely responsible for complying with all applicable copyright regulations

#### 3. Compliance with Laws
- Users must comply with **all local, state, and federal laws** regarding:
  - Voice synthesis and recording
  - Data privacy and protection
  - Intellectual property rights
  - Biometric information laws (where applicable)
- This skill may be subject to specific regulations in certain jurisdictions

#### 4. No Warranty & Limitation of Liability
```
THIS SKILL IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```

#### 5. Responsible Use Guidelines

✅ **Permitted Uses** (Proper Authorization Required Where Noted):
- Personal voice cloning for personal use
- Creating audiobooks from content you own or have rights to
- Voice assistants and accessibility applications
- AI character voices for games or animations (with original voice design)
- Educational and research purposes
- Dubbing content you own or have licensed

❌ **Prohibited Uses**:
- Cloning voices without explicit written consent
- Creating deepfakes for deceptive purposes
- Impersonating individuals or entities
- Generating harmful, illegal, or misleading content
- Violating privacy rights or data protection laws
- Any use that could cause harm to individuals or society

---

**中文法律声明**: 本技能仅用于合法合规用途。使用本技能即表示您同意：仅克隆您拥有或已获得明确书面授权的声音；遵守所有适用的版权和隐私法规；对使用本技能产生的任何后果承担全部责任。禁止将本技能用于欺诈、冒充或任何非法目的。

## 📄 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome! Feel free to contribute to this skill.

---

**Keywords**: TTS, Text-to-Speech, Voice Cloning, Qwen3, Qwen3-TTS, mlx-audio, Apple Silicon, Local Deployment, Audiobooks, Dubbing, Generative AI
