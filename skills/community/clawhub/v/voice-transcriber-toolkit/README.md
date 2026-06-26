# Voice Transcriber Toolkit

> 中英文双语 | Bilingual Documentation

---

## English

A comprehensive voice-to-text transcription toolkit supporting multiple engines (OpenAI Whisper, Vosk), batch processing, and subtitle generation.

### Features

- **Multiple Engines** — OpenAI Whisper (local), Vosk (offline)
- **Batch Processing** — transcribe multiple files at once
- **Format Support** — WAV, MP3, M4A, FLAC, OGG, WEBM
- **Subtitle Export** — SRT and WebVTT formats
- **Audio Conversion** — convert any format to WAV via ffmpeg
- **Language Auto-detect** — or specify language explicitly

### Quick Start

```python
from scripts.voice_transcriber import VoiceTranscriber

transcriber = VoiceTranscriber(engine="whisper", model_size="base")
result = transcriber.transcribe("audio.mp3", language="en")
print(result["text"])

# Export subtitles
srt = transcriber.export_subtitles(result, "srt")
with open("output.srt", "w") as f:
    f.write(srt)
```

## 中文

综合语音识别转文字工具包，支持多种引擎（OpenAI Whisper、Vosk）、批量处理和字幕生成。

### 功能特性

- **多引擎支持** — OpenAI Whisper（本地）、Vosk（离线）
- **批量处理** — 一次性转录多个文件
- **格式支持** — WAV、MP3、M4A、FLAC、OGG、WEBM
- **字幕导出** — SRT 和 WebVTT 格式
- **音频转换** — 通过 ffmpeg 将任意格式转为 WAV
- **语言自动检测** — 或显式指定语言

### 快速开始

```python
from scripts.voice_transcriber import VoiceTranscriber

transcriber = VoiceTranscriber(engine="whisper", model_size="base")
result = transcriber.transcribe("audio.mp3", language="zh")
print(result["text"])

# 导出字幕
srt = transcriber.export_subtitles(result, "srt")
with open("output.srt", "w") as f:
    f.write(srt)
```

### 安装依赖

```bash
pip install -r requirements.txt
# 同时需要安装 ffmpeg:
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

### 运行测试

```bash
python3 -m pytest tests/ -v
```
