---
name: text-to-podcast
version: 1.0.0
description: 将文本转换为播客音频（使用 TTS）
author: 小叮当
tags:
  - tts
  - audio
  - podcast
  - text-to-speech
---

# Text to Podcast - 文本转播客

快速将文章、脚本转换为高质量播客音频。

## 功能

- 🎙️ **TTS 转换**：使用 OpenAI TTS API（或系统 TTS）
- 🎵 **多种声音**：alloy, echo, fable, onyx, nova, shimmer
- ⚡ **批量处理**：一次转换多个文本文件
- 📦 **输出格式**：MP3（高质量 24kHz）
- 🎚️ **音量/速度**：可调节语速
- 👀 **预览模式**：只生成前10秒试听
- ↩️ **撤销**：自动备份原始文本

## 快速开始

### 安装

```bash
clawhub install text-to-podcast
cd ~/.openclaw/workspace/skills/text-to-podcast
./install.sh
```

### 配置

```bash
export OPENAI_API_KEY="your-key"
```

### 使用

```bash
# 单个文件
text-to-podcast convert script.md --voice alloy --output podcast.mp3

# 批量
text-to-podcast batch ./scripts/ --output ./podcasts/

# 预览（10秒）
text-to-podcast convert script.md --preview

# 调整语速
text-to-podcast convert script.md --speed 1.2
```

## 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `input` | 路径 | 是 | 输入文本文件 |
| `--voice` | 选项 | 否 | 声音：alloy/echo/fable/onyx/nova/shimmer（默认：alloy） |
| `--output` | 路径 | 否 | 输出MP3文件 |
| `--speed` | 浮点数 | 否 | 语速倍数（0.5-2.0，默认：1.0） |
| `--preview` | 布尔 | 否 | 预览模式（只生成前10秒） |
| `--model` | 选项 | 否 | TTS 模型：tts-1/tts-1-hd（默认：tts-1） |

## 声音选择

- **alloy**：中性，适合新闻、访谈
- **echo**：温暖，适合故事、播客
- **fable**：清晰，适合教育内容
- **onyx**：低沉，适合深度内容
- **nova**：轻快，适合娱乐、轻松话题
- **shimmer**：空灵，适合冥想、放松

## 使用场景

- 文章转播客（多平台内容再利用）
- 脚本试听（内容创作前测试）
- 快速生成音频内容
- 与 content-researcher + ai-content-tailor 配合形成完整工作流

## License

MIT