---
name: stt-simple
description: >
  Local speech-to-text using OpenAI Whisper. Use when the user needs to: (1) transcribe
  audio files to text, (2) convert voice messages to written content, (3) process
  recordings in 99+ languages. Supports tiny/base/small/medium/large models. One-command
  installation with auto model download. Multi-Agent support with session isolation.
---

# STT Simple - Local Speech-to-Text

## 🎯 触发场景 / Trigger Scenarios

使用此技能当用户需要 / Use this skill when user needs to:

1. **转录音频文件 / Transcribe audio files** - 将 .ogg, .wav, .mp3 等格式转为文字 / Convert .ogg, .wav, .mp3 to text
2. **处理语音消息 / Process voice messages** - WhatsApp/Telegram 语音消息转文字 / Voice message to text
3. **多语言识别 / Multi-language recognition** - 支持中文、英文、日文等 99+ 语言 / Supports Chinese, English, Japanese, etc. (99+ languages)
4. **批量转录 / Batch transcription** - 处理多个音频文件 / Process multiple audio files
5. **多 Agent 协作 / Multi-Agent collaboration** - 多个 Agent 同时转录，输出隔离 / Multiple Agents transcribe simultaneously with isolated outputs

---

## 🚀 执行流程 / Execution Flow

### 1️⃣ 检查安装状态 / Check Installation

```bash
/root/.openclaw/venv/stt-simple/bin/whisper --version
```

如果未安装，先运行安装脚本 / If not installed, run install script first:
```bash
/root/.openclaw/workspace/skills/stt-simple/scripts/install.sh
```

### 2️⃣ 选择模型 / Model Selection

| 模型 / Model | 大小 / Size | 速度 / Speed | 精度 / Accuracy | 推荐场景 / Recommended For |
|------|------|------|------|------|
| `tiny` | 39MB | ⚡⚡⚡ | ⭐⭐⭐ | 快速测试 / Quick testing |
| `base` | 74MB | ⚡⚡ | ⭐⭐⭐⭐ | 日常使用 / Daily use |
| `small` | 244MB | ⚡ | ⭐⭐⭐⭐⭐ | **默认推荐 / Default** |
| `medium` | 769MB | 🐌 | ⭐⭐⭐⭐⭐ | 高精度需求 / High accuracy |
| `large` | 1.5GB | 🐌🐌 | ⭐⭐⭐⭐⭐+ | 最佳质量 / Best quality |

### 3️⃣ 执行转录 / Execute Transcription

**方法 A: 使用 Whisper 命令行 / Use Whisper CLI**
```bash
/root/.openclaw/venv/stt-simple/bin/whisper <audio_file> --model small --language Chinese
```

**方法 B: 使用 Python 脚本（推荐支持多 Agent） / Use Python Script (Recommended for Multi-Agent)**
```bash
# Without session isolation / 无会话隔离
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  <audio_file> small zh

# With session isolation / 带会话隔离（多 Agent 场景）
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  <audio_file> small zh agent-main-whatsapp
```

### 4️⃣ 输出位置 / Output Location

- **文本输出 / Text output**: `/root/.openclaw/workspace/stt_output/<session_id>/<filename>_<timestamp>.txt`
- **JSON 输出 / JSON output**: 包含时间戳和置信度（如需）/ Includes timestamps and confidence (if needed)

---

## 🌍 语言代码 / Language Codes

| 语言 / Language | 代码 / Code | 别名 / Alias |
|------|------|------|
| 中文 / Chinese | zh | Chinese |
| 英文 / English | en | English |
| 日文 / Japanese | ja | Japanese |
| 韩文 / Korean | ko | Korean |
| 法文 / French | fr | French |
| 德文 / German | de | German |
| 西班牙文 / Spanish | es | Spanish |

**自动检测 / Auto-detect**: 省略 `--language` 参数 / Omit `--language` parameter

---

## 📁 输出格式 / Output Formats

- `.txt` - 纯文本 / Plain text (default)
- `.json` - 完整结果（含时间戳、置信度）/ Full results (with timestamps, confidence)
- `.srt` - 字幕格式（视频用）/ Subtitle format (for videos)
- `.vtt` - WebVTT（网页用）/ WebVTT (for web)

---

## 🔧 故障排查 / Troubleshooting

### 检查安装 / Check Installation
```bash
/root/.openclaw/venv/stt-simple/bin/whisper --version
```

### 重新安装 / Reinstall
```bash
rm -rf /root/.openclaw/venv/stt-simple
/root/.openclaw/workspace/skills/stt-simple/scripts/install.sh
```

### 手动下载模型 / Manual Model Download
```bash
/root/.openclaw/venv/stt-simple/bin/python \
  -c "import whisper; whisper.load_model('small')"
```

---

## 📦 资源文件 / Resources

| 文件 / File | 路径 / Path | 用途 / Purpose |
|------|------|------|
| 安装脚本 / Install script | `scripts/install.sh` | 一键安装虚拟环境、依赖、模型 / One-click install venv, dependencies, models |
| Python 脚本 / Python script | `scripts/stt_simple.py` | 简化的转录 API，返回 JSON 结果 / Simplified transcription API with JSON output |

---

## 💡 使用示例 / Examples

### 示例 1: 转录中文语音消息 / Transcribe Chinese voice message
```bash
/root/.openclaw/venv/stt-simple/bin/whisper \
  /root/.openclaw/media/inbound/voice.ogg \
  --model small --language Chinese
```

### 示例 2: 转录英文会议录音 / Transcribe English meeting recording
```bash
/root/.openclaw/venv/stt-simple/bin/whisper \
  meeting.wav --model medium --language en
```

### 示例 3: 使用 Python API 获取 JSON 结果 / Use Python API for JSON output
```bash
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  audio.ogg small zh
```

### 示例 4: 多 Agent 场景 - 带会话隔离 / Multi-Agent with Session Isolation
```bash
# Jari (WhatsApp) - outputs to /root/.openclaw/workspace/stt_output/agent-jari-whatsapp/
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  voice_a.ogg small zh agent-jari-whatsapp

# Other Agent (Telegram) - outputs to /root/.openclaw/workspace/stt_output/agent-telegram/
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  voice_b.ogg small zh agent-telegram
```

---

## 🔐 多 Agent 支持 / Multi-Agent Support

### 为什么需要会话隔离 / Why Session Isolation?

当多个 Agent 同时使用 STT 功能时：
- 避免输出文件冲突 / Avoid output file conflicts
- 每个 Agent 可以追踪自己的转录结果 / Each Agent can track its own transcriptions
- 便于清理和管理 / Easier cleanup and management

### 会话 ID 命名建议 / Session ID Naming Suggestions

| Agent / 场景 | 推荐 session_id | 输出目录 / Output Directory |
|------|------|------|
| **Jari (WhatsApp)** | `agent-jari-whatsapp` | `stt_output/agent-jari-whatsapp/` |
| Eric (WhatsApp) | `agent-eric-whatsapp` | `stt_output/agent-eric-whatsapp/` |
| Telegram Agent | `agent-telegram` | `stt_output/agent-telegram/` |
| 临时会话 | `session-<uuid>` | `stt_output/session-<uuid>/` |
| 用户专属 | `user-<user_id>` | `stt_output/user-<user_id>/` |

### 输出文件命名规则 / Output File Naming

```
<audio_filename>_<unique_timestamp>.txt
```

例如 / For example:
- `voice_a_3f8b2c1d.txt`
- `meeting_9a4e7f2b.txt`

每个文件名包含唯一的时间戳后缀，即使同一音频多次转录也不会覆盖。
Each filename includes a unique timestamp suffix, preventing overwrites even for repeated transcriptions.

---

## ⚠️ 注意事项 / Notes

1. **CPU vs GPU**: 默认使用 CPU，FP16 会自动降级为 FP32 / Defaults to CPU, FP16 auto-downgrades to FP32
2. **首次运行 / First run**: 首次使用会下载模型（small 约 244MB）/ Downloads model on first use (~244MB for small)
3. **输出目录 / Output directory**: 结果保存在 `/root/.openclaw/workspace/stt_output/` / Results saved to `/root/.openclaw/workspace/stt_output/`
4. **隐私安全 / Privacy**: 所有处理在本地完成，音频文件不会上传 / All processing is local, audio files never uploaded
5. **多 Agent / Multi-Agent**: 建议使用 session_id 参数隔离输出 / Recommended to use session_id parameter for output isolation

---

## 🔑 默认配置 / Default Configuration

**当前会话标识符 / Current Session ID:**
```
agent-jari-whatsapp
```

**输出目录 / Output Directory:**
```
/root/.openclaw/workspace/stt_output/agent-jari-whatsapp/
```

**快速调用 / Quick Start:**
```bash
# 转录当前 WhatsApp 语音消息 / Transcribe current WhatsApp voice message
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/scripts/stt_simple.py \
  <audio_file> small zh agent-jari-whatsapp
```
