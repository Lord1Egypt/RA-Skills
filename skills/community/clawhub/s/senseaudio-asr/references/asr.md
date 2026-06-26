# ASR Reference

## Table of Contents

- Endpoint summary
- Auth and secret handling
- Models and feature matrix
- HTTP transcription (`/v1/audio/transcriptions`)
- WebSocket realtime transcription (`/ws/v1/audio/transcriptions`)
- Audio analysis (`/v1/audio/analysis`)
- Records query (`/v1/audio/records`)
- Error handling

## Endpoint Summary

- HTTP transcription: `POST https://api.senseaudio.cn/v1/audio/transcriptions`
- WebSocket realtime: `wss://api.senseaudio.cn/ws/v1/audio/transcriptions`
- Audio analysis: `POST https://api.senseaudio.cn/v1/audio/analysis`
- Records query: `GET https://api.senseaudio.cn/v1/audio/records`

Official source in this repo:

- `/mnt/cache/wangke_fz/skills/SenseAudio开放平台.md`

## Auth and Secret Handling

- Read the credential from `SENSEAUDIO_API_KEY`.
- Send auth only as `Authorization: Bearer <API_KEY>`.
- Do not put API keys in URLs, query strings, logs, examples, or saved transcripts.
- The official records API documents an optional `api_key` query parameter, but this is sensitive and should be avoided unless the user explicitly needs that exact filter.
- Treat returned `api_key`, `audio`, `session_id`, and `trace_id` values as sensitive operational data.

## Models and Feature Matrix

Supported models:

- `sense-asr-lite`
- `sense-asr`
- `sense-asr-pro`
- `sense-asr-deepthink`

Feature summary from the official docs:

| Feature | lite | asr | pro | deepthink |
| --- | --- | --- | --- | --- |
| Basic recognition | ✅ | ✅ | ✅ | ✅ |
| HTTP `stream=true` | ❌ | ✅ | ✅ | ✅ |
| WebSocket realtime | ❌ | ❌ | ❌ | ✅ |
| Speaker diarization | ❌ | ✅ | ✅ | ❌ |
| Sentiment | ❌ | ✅ | ✅ | ❌ |
| Word / segment timestamps | ❌ | ✅ | ✅ | ❌ |
| Translation | ❌ | ✅ | ✅ | ✅ |
| Hotwords | ✅ | ❌ | ❌ | ❌ |
| ITN | ✅ | ✅ | ✅ | ❌ |
| Intelligent editing | ❌ | ❌ | ❌ | ✅ |
| Language control | ✅ | ✅ | ✅ | ❌ |

Important compatibility notes:

- `sense-asr-lite` does not support streaming or translation.
- `sense-asr` and `sense-asr-pro` support translation, diarization, sentiment, and timestamps.
- `max_speakers` is only documented for `sense-asr-pro`.
- `sense-asr-deepthink` supports translation and realtime use, but does not support `language`, diarization, sentiment, timestamps, `enable_itn`, or `enable_punctuation`.
- WebSocket realtime currently supports only `sense-asr-deepthink`.

## HTTP Transcription (`/v1/audio/transcriptions`)

Request type:

- `multipart/form-data`

Required fields:

- `file`: supported examples include `wav`, `mp3`, `ogg`, `flac`, `aac`, `m4a`, `mp4`; file size must be `<=10MB`
- `model`: `sense-asr-lite | sense-asr | sense-asr-pro | sense-asr-deepthink`

Optional fields:

- `language`: language code; auto-detect if omitted; unsupported on `sense-asr-deepthink`
- `response_format`: `json | text | verbose_json`
- `stream`: `true|false`; `lite` does not support it
- `enable_itn`: default `true`; `deepthink` does not support it
- `enable_punctuation`: default `false`; only `asr/pro`, not `deepthink`
- `enable_speaker_diarization`: default `false`; only `asr/pro`
- `max_speakers`: `1-20`; only documented for `sense-asr-pro`
- `enable_sentiment`: default `false`; only `asr/pro`
- `timestamp_granularities[]`: `word` or `segment`; only `asr/pro`
- `target_language`: translation target; unsupported on `lite`
- `hotwords`: comma-separated; only `lite`
- `recognize_mode`: `auto | record_only`; only documented for `deepthink` streaming mode

Language constraints:

- `language` is supported on `lite`, `asr`, and `pro`.
- `target_language` is supported on `asr`, `pro`, and `deepthink`.
- Do not send `language` with `sense-asr-deepthink`; use only `target_language` when translation is needed.

Response formats:

- `json`: returns top-level `text`
- `text`: returns plain text only
- `verbose_json`: may include `segments`, `speaker`, `sentiment`, `translation`, `words`
- `stream=true`: returns SSE (`text/event-stream`) with incremental `delta.text`

SSE constraints:

- Stream responses contain text deltas and terminal markers such as `finish_reason` / `[DONE]`.
- Official docs state stream mode does not return structured verbose information.

Verbose field gating:

- `speaker`: requires `enable_speaker_diarization`
- `sentiment`: requires `enable_sentiment`
- `translation`: requires `target_language`
- `words`: requires `timestamp_granularities[]=word`
- `segment`: requires `timestamp_granularities[]=segment`

## WebSocket Realtime Transcription (`/ws/v1/audio/transcriptions`)

Use WebSocket only for realtime audio streaming.

Supported model:

- `sense-asr-deepthink`

Message flow:

1. Connect and wait for `connected_success`
2. Send `task_start`
3. Receive `task_started`
4. Send binary audio chunks
5. Receive `result_final` events as VAD completes segments
6. Send `task_finish`
7. Receive `task_finished`
8. Handle `task_failed` as terminal failure

Client control message fields:

- `event`: `task_start | task_finish`
- `model`: required on `task_start`; currently `sense-asr-deepthink`
- `audio_setting`: required on `task_start`
- `vad_setting`: optional
- `transcription_setting`: optional

`audio_setting` requirements:

- `sample_rate=16000`
- `channel=1`
- `format=pcm`

Binary audio requirements:

- PCM signed 16-bit little-endian
- 16kHz
- mono

Optional `vad_setting` fields:

- `silence_duration` default `500`
- `min_speech_duration` default `300`
- `soft_max_duration` default `15000`
- `hard_max_duration` default `30000`
- `soft_silence_duration` default `300`
- `threshold` default `0.5`

Optional `transcription_setting` fields:

- `target_language`
- `recognize_mode`: `auto | record_only`

Server response shape:

- `event`: `connected_success | task_started | result_final | task_finished | task_failed`
- `session_id`
- `trace_id`
- `data` on `result_final`
- `base_resp.status_code`
- `base_resp.status_msg`

Common `result_final.data` fields in docs:

- `text`
- `is_final`
- `segment_id`
- `timestamp_end`

## Audio Analysis (`/v1/audio/analysis`)

- `POST` multipart form
- Required fields:
  - `model=sense-asr-check`
  - `file`

Response highlights:

- `audio_info.duration`
- `audio_info.format`
- `result.has_noise`
- `result.noise_score`
- `result.severity`
- `result.noise_types`
- `result.analysis`

## Records Query (`/v1/audio/records`)

- `GET` with Bearer auth
- Official optional query parameters:
  - `page`
  - `page_size`
  - `session_id`
  - `api_key`
- History retention is documented as up to 7 days after session end.

Safety rules for this endpoint:

- Prefer filtering by `session_id` when possible.
- Avoid sending `api_key` as a query parameter unless the user explicitly requires that provider-documented filter.
- Do not echo returned `api_key` values back to the user unless strictly necessary.
- Treat returned `audio` URLs as sensitive because they expose recorded session audio.

Response highlights:

- `total`
- `list[]`
- `list[].audio`
- `list[].points`
- `list[].session_id`
- `list[].session_start`
- `list[].session_end`
- `list[].text`

## Error Handling

HTTP errors documented for transcription:

- `400 invalid`
- `429 rate_limit_error`
- `500 internal_error`

WebSocket failures:

- Server emits `task_failed`
- Inspect `base_resp.status_code` and `base_resp.status_msg`
- Example from official docs: `2013 model is required`

Implementation checklist:

- Validate model-to-parameter compatibility before sending requests.
- Keep HTTP uploads at or below `10MB`.
- Enforce WS `pcm` / `16000Hz` / mono audio.
- Parse SSE separately from `json` and `verbose_json`.
- Do not expect structured verbose payloads in HTTP stream mode.
- Log identifiers only when operationally necessary and avoid exposing them in user-visible output.
