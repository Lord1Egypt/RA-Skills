# Audio Models

## Text-to-Speech (TTS)

| Model ID | Description |
|----------|-------------|
| `elevenlabs/eleven_multilingual_v2` | 29 languages, highest quality |
| `elevenlabs/sound_generation` | Sound effects |
| `minimax/speech-01-turbo` | Chinese optimized |
| `openai/tts-1` | Standard quality |
| `openai/tts-1-hd` | HD quality |
| `replicate/lucataco/xtts-v2` | XTTS v2 |

## Speech-to-Text (STT)

| Model ID | Description |
|----------|-------------|
| `openai/whisper-1` | Audio transcription |

## Music Generation

| Model ID | Description |
|----------|-------------|
| `replicate/elevenlabs/music` | High quality with natural vocals |
| `replicate/google/lyria-2` | DeepMind's advanced music AI |
| `replicate/meta/musicgen` | Open-source, diverse styles |
| `replicate/stability-ai/stable-audio-2.5` | Up to 3 minutes |

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "minimax/speech-01-turbo", "inputs": {"text": "Hello world", "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0}}}'
```
