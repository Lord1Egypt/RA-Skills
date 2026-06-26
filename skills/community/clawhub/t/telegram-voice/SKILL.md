---
name: voice
description: Voice communication via Telegram. Automatically transcribes incoming voice messages using faster-whisper and replies with TTS voice. Use for all voice-related interactions on Telegram.
---

# Voice Communication

This skill enables voice communication on Telegram:
1. **Receive**: Transcribe voice messages using faster-whisper
2. **Reply**: Send voice replies using TTS

## Incoming Voice (Automatic)

When receiving voice messages (.ogg files), use faster-whisper to transcribe:

```python
from faster_whisper import WhisperModel

model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe('<file_path>', language='zh')
result = ''.join([s.text for s in segments])
```

## Outgoing Voice (TTS)

Use the tts tool to send voice replies:

```json
{
  "action": "send",
  "channel": "telegram", 
  "message": "<text>",
  "asVoice": true
}
```

Or use the tts tool directly:

```json
{
  "channel": "telegram",
  "text": "<text to speak>"
}
```

## Language

- Input: Auto-detect or specify language (zh for Chinese)
- Output: Match user's language preference

## Requirements

- faster-whisper: `pip install faster-whisper`
- TTS already configured in OpenClaw
