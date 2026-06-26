---
name: voice-transcriber-toolkit
description: Voice-to-Text Transcription Toolkit - 语音识别转文字，支持Whisper/Vosk引擎，批量处理，字幕导出 | Speech recognition & transcription with Whisper/Vosk engines, batch processing, subtitle export
metadata:
  openclaw:
    requires:
      bins: ["python3", "ffmpeg"]
    install:
      - id: python-deps
        kind: python
        requirements: "requirements.txt"
      - id: ffmpeg
        kind: apt
        packages: ["ffmpeg"]
---

# Voice Transcriber Toolkit

## 功能

- **Transcribe** — 单文件/批量音频转文字 (Whisper/Vosk)
- **Convert** — 音频格式转换 (ffmpeg)
- **Export** — 导出 SRT/VTT 字幕
- **Info** — 音频文件元信息提取

## 使用

```python
from scripts.voice_transcriber import VoiceTranscriber, AudioConverter

transcriber = VoiceTranscriber(engine="whisper", model_size="base")

# 单文件转录
result = transcriber.transcribe("meeting.mp3", language="zh")
print(result["text"])

# 批量转录
results = transcriber.transcribe_batch(["file1.mp3", "file2.wav"])

# 导出字幕
srt = transcriber.export_subtitles(result, "srt")

# 音频转换
converter = AudioConverter()
converter.convert_to_wav("input.m4a", "output.wav")
```

## CLI

```bash
python3 scripts/voice_transcriber.py
```
