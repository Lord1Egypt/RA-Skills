# TTS Reference

## Table of Contents

- Endpoint summary
- Common auth and headers
- HTTP TTS (`/v1/t2a_v2`)
- SSE streaming behavior
- WebSocket TTS (`/ws/v1/t2a_v2`)
- Parameters and ranges
- Response parsing
- Best practices and errors

## Endpoint Summary

- HTTP/SSE endpoint: `POST https://api.senseaudio.cn/v1/t2a_v2`
- WebSocket endpoint: `wss://api.senseaudio.cn/ws/v1/t2a_v2`
- Auth: `Authorization: Bearer <API_KEY>`

## Common Auth and Headers

- `Authorization: Bearer <API_KEY>`
- `Content-Type: application/json`

## HTTP TTS (`/v1/t2a_v2`)

Core request fields:

- `model` (required): `SenseAudio-TTS-1.0` (doc also references clone dictionary requirement on `SenseAudio-TTS-1.5`)
- `text` (required): up to 10000 chars
- `stream` (boolean): controls stream mode
- `voice_setting` (required object): includes `voice_id` and optional tuning
- `audio_setting` (optional object)
- `dictionary` (optional array): only for clone voice use case per doc constraints

`<break>` pause syntax inside `text`:

- Format: `<break time=500>`
- Unit: ms
- Min: 100ms

## SSE Streaming Behavior

When `stream=true`, response is `text/event-stream`.

- Each chunk contains JSON under `data:`
- `data.status=1`: ongoing
- `data.status=2`: final chunk
- `extra_info` usually appears in the final chunk

## WebSocket TTS (`/ws/v1/t2a_v2`)

Required flow:

1. Connect and wait for `connected_success`
2. Send `task_start`
3. Wait for `task_started`
4. Send one or more `task_continue` with text
5. Send `task_finish`
6. Receive `task_finished` (or `task_failed`)

Important notes:

- Audio is returned as hex data.
- If no new event is sent for 120s after the last server return, server may disconnect.
- Keep strict event order; do not send `task_continue` before `task_started`.

## Parameters and Ranges

`voice_setting`:

- `voice_id` required
- `speed`: `[0.5, 2.0]`, default `1.0`
- `vol`: `[0, 10]` (or `(0,10]` in WebSocket section), default `1.0`
- `pitch`: `[-12, 12]`, default `0`

`audio_setting`:

- `format`: `mp3|wav|pcm|flac` (default `mp3`)
- `sample_rate`: `8000|16000|22050|24000|32000|44100` (default `32000`)
- `bitrate` (mp3): `32000|64000|128000|256000` (default `128000`)
- `channel`: `1|2` (default `2`)

## Response Parsing

Common fields:

- `data.audio`: hex string
- `data.status`: 1 (ongoing), 2 (done)
- `extra_info`: final audio metadata
- `base_resp.status_code` and `base_resp.status_msg`

Hex decoding examples:

- shell: `jq -r '.data.audio' response.json | xxd -r -p > output.mp3`
- Node: `Buffer.from(hex, 'hex')`
- Python: `bytes.fromhex(hex_str)`

Always guard against null/empty `data` in stream chunks.

## Best Practices and Errors

- Chunk long text into semantic units when using WebSocket incremental mode.
- Track `trace_id`/`session_id` for debugging.
- Handle `task_failed` explicitly and close connection cleanly.
- Retry transient network failures with bounded backoff.
- Validate params before sending to avoid `1001` (parameter error in TTS WS doc).

