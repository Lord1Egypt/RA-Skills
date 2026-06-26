---
name: wecom-voice
version: 1.0.0
description: Send native voice messages to WeCom using Windows TTS. Converts text to speech and sends as voice message (not audio file).
emoji: 🔊
tags:
  - wecom
  - voice
  - tts
  - windows
  - speech
metadata:
  openclaw:
    triggers:
      - "发语音"
      - "语音消息"
      - "voice message"
  clawhub:
    shortDescription: Send voice messages to WeCom
    longDescription: |
      Send native voice messages to WeCom (企业微信) using Windows TTS.
      Converts text to speech and sends as AMR format (WeCom native voice).
      
      Requirements:
      - Windows with System.Speech (built-in)
      - FFmpeg in PATH
      
      Workflow:
      1. Generate WAV using Windows TTS (Microsoft Huihui)
      2. Convert to AMR (8000Hz, 12.2kbit/s - WeCom native format)
      3. Send from media/inbound directory
---

# WeCom Voice Message Sender

Send native voice messages to WeCom (企业微信) using Windows TTS.

## Usage

```bash
# Basic
node scripts/send-voice.cjs "要说的内容"

# Specify target user
node scripts/send-voice.cjs "Hello" FanQi
```

## How it works

1. **TTS**: Uses Windows System.Speech (Microsoft Huihui voice)
2. **Convert**: FFmpeg converts WAV to AMR (WeCom native voice format)
3. **Send**: OpenClaw CLI sends from `media/inbound` directory

## Technical Details

- **TTS Voice**: Microsoft Huihui Desktop (中文)
- **AMR Format**: 8000Hz, mono, 12.2kbit/s
- **Directory**: Must send from `~/.openclaw/media/inbound`

## Files

- `SKILL.md` - This file
- `scripts/send-voice.cjs` - Main script