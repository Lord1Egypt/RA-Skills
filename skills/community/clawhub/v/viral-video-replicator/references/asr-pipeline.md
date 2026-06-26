# ASR Transcription Pipeline

> **Role:** Defines TOS upload protocol and Seed-ASR-2.0 submit/poll API for speech-to-text.
> Load at: Step 3 (transcribing audio). Skip entirely if video has no speech.
> It does NOT replace execution — always run the actual ASR pipeline, never fabricate transcripts.

## TOS Audio Upload

### SDK
- Uses `tos` Python SDK (TosClientV2)
- Install: `pip install tos`

### Connection
```python
client = TosClientV2(
  ak=TOS_ACCESS_KEY,
  sk=TOS_SECRET_KEY,
  endpoint=f"tos-{TOS_REGION}.volces.com",
  region=TOS_REGION,
)
```

### Upload
- Key: `outfit-video/asr/{uuid}.wav`
- Content-Type: audio/wav
- Retry: up to 2 times with 1s delay
- Runs in thread pool (put_object is blocking)

### Presigned URL
- Method: GET
- Expires: 3600 seconds (1 hour)
- Returns signed URL for ASR access

## Seed-ASR-2.0 Transcription

### Base URL
`https://openspeech.bytedance.com/api/v3/auc/bigmodel`

### Submit Request
```
POST /submit
Headers:
  Content-Type: application/json
  x-api-key: {ASR_ACCESS_TOKEN}
  X-Api-Resource-Id: volc.seedasr.auc
  X-Api-Request-Id: {uuid}
  X-Api-Sequence: -1
Body:
  user.uid: "outfit-video"
  audio.url: {presigned_tos_url}
  audio.format: "wav"
  request:
    model_name: "bigmodel"
    enable_itn: true
    enable_punc: true
    enable_ddc: true
    show_utterances: true
    enable_speaker_info: true
    enable_emotion_detection: true
    enable_gender_detection: true
```

### Poll Request
```
POST /query
Headers: (same as submit, WITHOUT X-Api-Sequence)
Body: {}
```

### Status Codes (X-Api-Status-Code header)
- 20000000: completed -> extract result.text
- 20000001: processing, keep polling
- 20000002: processing, keep polling
- 20000003: silent audio, no transcript

### Polling Parameters
- Max wait: 120 seconds
- Poll interval: 3 seconds
- Network retry: exponential backoff, max 3 retries
- Backoff formula: `interval * 2^(retry-1)`
