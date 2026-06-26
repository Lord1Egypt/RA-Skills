---
name: tts-cosyvoice
version: 1.0.0
description: "Text-to-Speech via Edge TTS (Microsoft Azure voices). Free, no API key needed, supports 100+ voices in 50+ languages including Chinese and English."
metadata: { "openclaw": { "emoji": "🔊", "requires": { "bins": ["python3"] } } }
tags: ["tts", "text-to-speech", "edge-tts", "voice", "audio"]
---

# Edge TTS — Text-to-Speech

Use to convert text to speech using Microsoft Edge's free TTS service. No API key required.

## Voices

### Chinese (Recommended)
| Voice | Gender | Style |
|-------|--------|-------|
| `zh-CN-XiaoxiaoNeural` | Female | Warm, natural (default) |
| `zh-CN-YunxiNeural` | Male | Young, casual |
| `zh-CN-YunjianNeural` | Male | Professional, news |
| `zh-CN-XiaoyiNeural` | Female | Cute, young |
| `zh-CN-YunyangNeural` | Male | News broadcaster |
| `zh-CN-XiaochenNeural` | Female | Child |
| `zh-TW-HsiaoChenNeural` | Female | Traditional Chinese |

### English
| Voice | Gender | Style |
|-------|--------|-------|
| `en-US-JennyNeural` | Female | Friendly (default) |
| `en-US-GuyNeural` | Male | Professional |
| `en-GB-SoniaNeural` | Female | British |

## Script

```bash
{baseDir}/scripts/tts.py --text "Hello world" --output /tmp/output.mp3
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--text` | (required) | Text to speak |
| `--voice` | zh-CN-XiaoxiaoNeural | Voice ID |
| `--output` | /tmp/tts_output.mp3 | Output file path |
| `--rate` | 0% | Speed adjustment (-50% to +100%) |
| `--pitch` | 0Hz | Pitch adjustment (-50Hz to +50Hz) |
| `--volume` | 0% | Volume adjustment (-100% to +100%) |
| `--file` | | Read text from file instead of --text |

### Examples

```bash
# Basic Chinese TTS
{baseDir}/scripts/tts.py --text "你好，我是Nova" --output /tmp/hello.mp3

# Male voice, faster speech
{baseDir}/scripts/tts.py --text "Hello world" --voice en-US-GuyNeural --rate +20% --output /tmp/fast.mp3

# Read from file
{baseDir}/scripts/tts.py --file script.txt --output /tmp/script.mp3
```

## Available Voices

List all voices:
```bash
{baseDir}/scripts/tts.py --list-voices zh
{baseDir}/scripts/tts.py --list-voices en
{baseDir}/scripts/tts.py --list-voices ja
```

## Dependencies

- `edge-tts` (pip install)
- No API key needed — uses Microsoft Edge's free TTS service
- Requires internet connection
