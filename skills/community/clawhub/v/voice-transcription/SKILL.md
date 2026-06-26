---
name: voice-transcription
description: "语音转文本技能 - 基于 SiliconFlow API (SenseVoiceSmall/TeleSpeechASR)，支持四川话等多种方言识别"
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["python3", "curl"]
    install:
      - id: requirements
        kind: pip
        packages: ["requests"]
        label: "Install Python requests library"
---

# 🎙️ Voice Transcription - 语音转文本

基于 SiliconFlow API 的语音转文本技能，支持普通话、粤语、英语、日语、韩语等多种语言，对四川话等方言也有良好的识别能力。

## 模型说明

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| `FunAudioLLM/SenseVoiceSmall` | 轻量级，支持多语言+情感识别 | 日常对话、会议录音 |
| `TeleAI/TeleSpeechASR` | 电信自研，方言识别更强 | 四川话等方言语音 |

## 配置

设置环境变量 `SILICONFLOW_API_KEY` 或在调用时传入 `api_key` 参数。

```bash
export SILICONFLOW_API_KEY="your-api-key-here"
```

## 使用方法

### 命令行

```bash
# 转录音频文件（自动选择模型）
python3 scripts/transcribe.py audio.mp3

# 指定模型
python3 scripts/transcribe.py audio.mp3 --model TeleAI/TeleSpeechASR

# 指定 API Key
python3 scripts/transcribe.py audio.mp3 --api-key sk-xxx

# 输出到文件
python3 scripts/transcribe.py audio.mp3 --output result.txt
```

### 在对话中使用

当用户提供音频文件或提到"语音转文字"、"听一下这个录音"等时，使用此技能。

## 注意事项

- 音频文件限制：时长不超过 1 小时，文件大小不超过 50MB
- 支持格式：mp3, wav, m4a, flac, ogg, webm 等常见音频格式
- API 免费额度：SiliconFlow 提供一定的免费调用额度
