# StepFun Chat API Notes

Official docs:

- https://platform.stepfun.com/docs/zh/api-reference/chat/chat-completion-create
- https://platform.stepfun.com/docs/zh/api-reference/chat/object

## Endpoint

- Method: `POST`
- URL: `https://api.stepfun.com/v1/chat/completions`

## Request Fields Used By This Skill

- `model`: set to `step-audio-r1.1`
- `messages`: normal chat messages
- `stream`: set to `false` so the API returns one complete response object
- `modalities`: use `["text", "audio"]` when spoken output is needed
- `audio`: include output audio settings such as `voice` and `format`
- `step-audio-r1.1`: does not support tool call
- `audio.voice`: required when spoken output is requested

For this skill, use the official env var name `STEPFUN_API_KEY`. The helper
script also accepts `STEP_API_KEY` as a backward-compatible alias.

For audio input, the user message can use an array of parts and include:

```json
{
  "type": "input_audio",
  "input_audio": {
    "data": "data:audio/wav;base64,..."
  }
}
```

Official docs list WAV and MP3 input support. In practice, this skill
normalizes local input to `data:audio/wav;base64,...` before sending. If the
local source file is not WAV, convert it before embedding.

## Non-Streaming Response Shape

The API returns the standard chat completion object documented at
`/chat/object`. This skill reads:

- `id`
- `model`
- `choices[0].finish_reason`
- `choices[0].message.content`
- `choices[0].message.audio.data`
- `choices[0].message.audio.transcript`
- `usage`

## Maintenance Notes

- The helper script keeps the API base URL configurable through
  `STEP_API_BASE_URL`.
- The helper script can query `GET /v1/audio/voices` through `--list-voices` to
  inspect account-level custom/cloned voice ids.
- The helper script enforces `wav` for non-streaming audio replies because this
  skill targets `stream: false`.
- The helper script rejects oversized input audio when the normalized data URL
  exceeds StepFun's documented 10MB base64 limit.
- If StepFun changes the exact audio response shape, update the extraction logic
  in `scripts/stepfun_audio_chat.py`.
- If StepFun later requires different voice names for `step-audio-r1.1`, change
  the script default or pass `--voice` explicitly.
