# Smallest AI — API Quick Reference

## Authentication

All requests require Bearer token authentication.

```
Authorization: Bearer <SMALLEST_API_KEY>
```

Get your key at https://waves.smallest.ai → API Key in left panel.

## TTS — Lightning v3.1 Model

### REST (Synchronous)

```
POST https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech
Content-Type: application/json
```

```json
{
  "text": "Hello world",
  "voice_id": "diana",
  "sample_rate": 24000,
  "speed": 1.0,
  "language": "en",
  "add_wav_header": true
}
```

**Response:** Binary audio data (WAV or PCM)

### WebSocket (Streaming)

```
wss://api.smallest.ai/waves/v1/lightning-v3.1/get_speech/stream
```

Send:
```json
{
  "voice_id": "diana",
  "text": "Streaming text",
  "language": "en",
  "sample_rate": 24000,
  "speed": 1.0
}
```

Receive:
```json
{
  "status": "processing",
  "data": { "audio": "<base64_chunk>" }
}
```

### Parameters

| Param           | Type    | Default | Range/Values                     |
|-----------------|---------|---------|----------------------------------|
| text            | string  | —       | Required. Max ~5000 chars        |
| voice_id        | string  | —       | Required. diana, vincent, etc.   |
| sample_rate     | int     | 24000   | 8000, 16000, 24000, 44100       |
| speed           | float   | 1.0     | 0.5 – 2.0                       |
| language        | string  | "en"    | ISO 639-1 code                   |
| add_wav_header  | bool    | false   | true = playable WAV              |

## STT — Pulse Model

### REST

```
POST https://api.smallest.ai/waves/v1/pulse/get_text
Content-Type: audio/wav
```

Query parameters:
- `model=pulse`
- `language=en`
- `diarize=true|false`
- `word_timestamps=true|false`
- `emotion_detection=true|false`

Body: Raw audio bytes

**Response:**
```json
{
  "transcription": "Hello world",
  "words": [
    {
      "word": "Hello",
      "start": 0.0,
      "end": 0.3,
      "speaker": 0,
      "confidence": 0.98
    }
  ]
}
```

### WebSocket (Streaming)

```
wss://api.smallest.ai/waves/v1/pulse/get_text
```

Send binary audio chunks, receive streaming transcription.

## Python SDK

```bash
pip install smallestai
```

```python
from smallestai.waves import WavesClient

client = WavesClient(api_key="YOUR_KEY")

# Synchronous TTS
client.synthesize(text="Hello", voice="diana", save_as="out.wav")

# Async TTS
audio = await client.synthesize("Hello", speed=1.5, sample_rate=16000)
```

## Error Codes

| HTTP Code | Meaning                    | Action                        |
|-----------|----------------------------|-------------------------------|
| 200       | Success                    | —                             |
| 400       | Bad request                | Check params, text length     |
| 401       | Unauthorized               | Check API key                 |
| 429       | Rate limited               | Wait and retry                |
| 500       | Server error               | Retry after a moment          |

## Pricing

| Plan     | Price    | TTS Hours | Voice Clones | STT             |
|----------|----------|-----------|--------------|-----------------|
| Free     | $0       | 30 min    | 0            | Limited          |
| Basic    | $5/mo    | 3 hours   | 1            | Included         |
| Premium  | $29/mo   | 24 hours  | 2            | Included         |

Full docs: https://waves-docs.smallest.ai
