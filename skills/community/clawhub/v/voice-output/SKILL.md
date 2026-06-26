---
name: voice-output
description: Use when Tony says voice reply or asks to speak. Speaks the response aloud via Doubao TTS to MOMAX BS6.
---

# voice-output skill

Speaks responses aloud when Tony requests voice reply.

## Trigger conditions

When Tony says:
- 「语音回复」
- 「用话说」
- 「voice reply」
- 「语音」
- Or any similar request to hear the response

## How to trigger

1. Generate the full text response
2. Call voice_speak.py to speak it aloud:

```bash
python3 /Users/tony/.openclaw/workspace/skills/voice-output/scripts/voice_speak.py "text to speak"
```

## Default voice

- Model: zh_female_xiaohe_uranus_bigtts (小何)
- TTS: Doubao TTS 2.0
- Player: afplay (routes to MOMAX BS6)

## Dependencies

- Python3 (urllib, base64 built-in)
- afplay (macOS built-in)
- Doubao TTS credentials (APPID: 8982709936)
