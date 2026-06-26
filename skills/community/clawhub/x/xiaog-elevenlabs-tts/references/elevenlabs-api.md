# ElevenLabs TTS API Reference

## Authentication

```http
xi-api-key: $ELEVENLABS_API_KEY
Content-Type: application/json
```

Base URL:

```text
https://api.elevenlabs.io
```

## List voices

```http
GET /v1/voices
```

Typical response fields used by this skill:

```json
{
  "voices": [
    {
      "voice_id": "...",
      "name": "Rachel",
      "category": "premade",
      "labels": {},
      "preview_url": "https://..."
    }
  ]
}
```

## HTTP streaming text-to-speech

Use when the complete text is available and low perceived latency matters.

```http
POST /v1/text-to-speech/{voice_id}/stream?output_format=mp3_44100_128&optimize_streaming_latency=2
```

Request body:

```json
{
  "text": "Text to speak",
  "model_id": "eleven_flash_v2_5",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0,
    "use_speaker_boost": false
  }
}
```

Response: raw audio bytes over chunked HTTP streaming. Measure TTFB as the time from request start to first non-empty audio chunk.

## WebSocket streaming guidance

Use WebSocket TTS when LLM output arrives incrementally and the audio should begin before the whole answer is known. The normal pattern is:

1. Open the ElevenLabs WebSocket TTS endpoint for the selected voice/model.
2. Send an initial payload with API key, voice settings, generation config, and first text chunk.
3. Send more text chunks as they are produced.
4. Send an end-of-stream marker / empty text per the current API contract.
5. Decode received audio chunks and append/play them in order.

Do not use the HTTP streaming script for incremental text; it is for complete text only.

## Output formats

Common values:

- `mp3_44100_128` — shareable default.
- `mp3_24000_48` — lower bandwidth.
- `pcm_16000`, `pcm_24000` — realtime playback/telephony pipelines.
- `opus_48000_64` — realtime/WebRTC-like pipelines.

## Latency tuning

`optimize_streaming_latency` values:

- `0`: default.
- `1`: normal optimization.
- `2`: strong optimization.
- `3`: maximum normal optimization.
- `4`: fastest, text normalizer off; may mispronounce numbers/dates.

Even if this parameter is marked deprecated in some docs, it may still be accepted by the API. Prefer model/output/streaming choices as the primary latency levers.

## Voice settings

- `stability`: higher is steadier/flatter; lower is more variable.
- `similarity_boost`: higher adheres more to the selected voice.
- `style`: expressive style strength; keep low for realtime dialogue.
- `use_speaker_boost`: improves similarity but adds compute/latency; default off for low-latency use.

## Troubleshooting

- `401/403`: missing/wrong key, revoked key, account access issue, or ElevenLabs abuse/free-tier restriction such as `detected_unusual_activity`; in that case voice listing may work while synthesis is blocked until the account/network/paid plan issue is resolved.
- `404 voice not found`: list voices and use the exact `voice_id`.
- `422/400`: model/output format not supported for the endpoint/account; retry with `eleven_flash_v2_5` and `mp3_44100_128`.
- Empty file: treat as failure; rerun and inspect HTTP error body.
- High TTFB: disable speaker boost, use Flash model, use streaming endpoint, shorten first text chunk, or switch to PCM for realtime pipelines.
