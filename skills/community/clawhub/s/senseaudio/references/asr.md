# ASR Reference

## Table of Contents

- Endpoint summary
- Models and feature matrix
- HTTP transcription (`/v1/audio/transcriptions`)
- WebSocket realtime transcription
- Audio analysis (`/v1/audio/analysis`)
- Records query (`/v1/audio/records`)
- Language/translation constraints
- Error handling

## Endpoint Summary

- HTTP transcription: `POST https://api.senseaudio.cn/v1/audio/transcriptions`
- WebSocket realtime: `wss://api.senseaudio.cn/ws/v1/audio/transcriptions`
- Audio analysis: `POST https://api.senseaudio.cn/v1/audio/analysis`
- Records query: `GET https://api.senseaudio.cn/v1/audio/records`

Auth:

- `Authorization: Bearer <API_KEY>`

## Models and Feature Matrix

Supported models:

- `sense-asr-lite`
- `sense-asr`
- `sense-asr-pro`
- `sense-asr-deepthink`

Key constraints:

- `lite`: no streaming, no translation; supports hotwords.
- `asr`/`asr-pro`: support stream, diarization, sentiment, timestamps, translation.
- `deepthink`: supports stream and translation; no diarization/sentiment/timestamps; `language` unsupported.

## HTTP Transcription (`/v1/audio/transcriptions`)

Request type:

- `multipart/form-data`

Required fields:

- `file` (<=10MB per doc)
- `model`

Common optional fields:

- `language`
- `target_language`
- `response_format`: `json|text|verbose_json`
- `stream` (not for `lite`)
- `enable_itn`
- `enable_punctuation`
- `enable_speaker_diarization`
- `max_speakers`
- `enable_sentiment`
- `timestamp_granularities[]`: `word` / `segment`
- `hotwords` (lite only)
- `recognize_mode` (deepthink stream)

Response formats:

- JSON with `text`
- plain text
- verbose JSON with `segments`, `words`, etc.
- SSE for stream mode with incremental deltas

## WebSocket Realtime Transcription

Flow:

1. Connect, receive `connected_success`
2. Send `task_start` control message
3. Receive `task_started`
4. Send binary PCM chunks
5. Receive `result_final` events
6. Send `task_finish`
7. Receive `task_finished`

Control message highlights:

- `event`: `task_start` or `task_finish`
- `model`: currently documented as `sense-asr-deepthink`
- `audio_setting` required: `sample_rate=16000`, `channel=1`, `format=pcm`
- optional `vad_setting`
- optional `transcription_setting.target_language` and `recognize_mode`

Binary audio format:

- PCM signed 16-bit little-endian
- 16kHz
- mono

## Audio Analysis (`/v1/audio/analysis`)

- `POST` multipart form
- Required: `model=sense-asr-check`, `file`
- Returns audio info plus noise analysis fields:
  - `has_noise`
  - `noise_score`
  - `severity`
  - `noise_types`
  - `analysis`

## Records Query (`/v1/audio/records`)

- `GET` with optional filters: `page`, `page_size`, `session_id`, `api_key`
- Returns `total` and `list` records
- Doc states history retention up to 7 days after session end

## Language/Translation Constraints

- `language` supported on lite/asr/asr-pro
- `target_language` supported on asr/asr-pro/deepthink
- `deepthink` does not support `language`

When user requests language control with `deepthink`, map to `target_language` only.

## Error Handling

Documented generic HTTP errors for transcription:

- `400 invalid`
- `429 rate_limit_error`
- `500 internal_error`

WebSocket failures:

- server emits `task_failed` with `base_resp.status_code/status_msg`

Implementation checklist:

- Validate model-feature compatibility before request.
- Enforce audio format requirements for WS.
- Handle SSE `[DONE]` and WS terminal events.
- Log `session_id`/`trace_id` when present.

