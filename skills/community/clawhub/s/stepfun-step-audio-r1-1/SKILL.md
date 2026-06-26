---
name: stepfun-step-audio-r1-1
description: Use StepFun Chat Completions with model step-audio-r1.1 for non-streaming speech turns that can send text with optional local audio input and save the returned audio, transcript, and raw response object.
metadata:
  openclaw:
    emoji: "🔊"
    requires:
      bins: ["python3"]
      env: ["STEPFUN_API_KEY", "STEP_API_KEY"]
    primaryEnv: "STEPFUN_API_KEY"
---

# StepFun step-audio-r1.1

Call StepFun's `POST /v1/chat/completions` endpoint with `stream: false` and
`model: step-audio-r1.1`.

Use this skill when the user explicitly wants StepFun audio generation,
speech-style replies through the Chat API, a standard non-streaming chat
completion object, or local audio input encoded as `input_audio`.

Do not use this skill for realtime duplex voice sessions. Use StepFun Realtime
API instead when the user wants low-latency live conversation.

`step-audio-r1.1` does not support tool call. If the user needs tool calling,
prefer `step-audio-2` instead of this skill.

## Quick Start

Text in, audio out:

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py \
  --prompt "用中文介绍一下苏州的春天，语气自然一点。" \
  --voice wenrounansheng \
  --format wav
```

Check available voice ids before a run:

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py \
  --list-voices
```

Text + local audio in, audio out:

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py \
  --prompt "听完这段语音后，总结重点，并用更简洁的话复述。" \
  --input-audio /path/to/input.wav \
  --voice wenrounansheng \
  --format wav
```

Build and inspect the non-streaming request without sending it:

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py \
  --prompt "测试 step-audio-r1.1 非流式 payload" \
  --dry-run \
  --print-json
```

## What The Script Produces

The helper writes a fresh output directory for each run unless `--output-dir`
is provided. Typical files are:

- `request.json`: saved only for `--dry-run`
- `response.json`: full non-streaming response object
- `response.<format>`: decoded audio from `choices[0].message.audio.data`
- `transcript.txt`: `choices[0].message.audio.transcript`
- `content.txt`: textual assistant content when present

## Common Flags

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py --help
```

Important flags:

- `--prompt`: user text to send with the request
- `--input-audio`: local audio file that will be base64-encoded into
  `input_audio`; non-WAV files are converted to WAV first when `ffmpeg` or
  `afconvert` is available
- `--system`: optional system instruction
- `--voice`: output voice name
- `--list-voices`: query StepFun for account-level custom/cloned voices and
  print a few official voice hints
- `--format`: non-streaming output audio format; this skill uses `wav`
- `--no-audio-output`: request text-only output while still using the Chat API
- `--temperature`: optional sampling override
- `--max-tokens`: optional generation cap
- `--print-json`: echo request or response JSON to stdout
- `--dry-run`: build payload and stop before the network call

## Configuration

Set `STEPFUN_API_KEY` in the environment, or inject it through OpenClaw skill
config:

```json5
{
  skills: {
    entries: {
      "stepfun-step-audio-r1-1": {
        env: {
          STEPFUN_API_KEY: "STEP_KEY_HERE",
        },
      },
    },
  },
}
```

The script still accepts `STEP_API_KEY` as a legacy alias for backward
compatibility, but the official name is `STEPFUN_API_KEY`.

Optional environment variables:

- `STEP_API_BASE_URL`: overrides the default `https://api.stepfun.com`

Input audio note:

- StepFun expects `input_audio.data` in `data:audio/wav;base64,...` format
- Official docs mention WAV and MP3 input support
- This script normalizes local input to WAV for maximum compatibility
- If you pass `m4a`, `mp3`, `aiff`, or similar, this script will try to convert
  to WAV via `ffmpeg` or macOS `afconvert`
- The normalized `input_audio` payload must stay within StepFun's 10MB base64
  limit

Voice selection note:

- `step-audio-r1.1` needs `audio.voice` whenever you request audio output
- The script defaults to `wenrounansheng`, which was validated in real smoke
  tests for this skill
- For production use, prefer passing `--voice` explicitly
- Use `--list-voices` to inspect account-level custom/cloned voice ids
- Read [references/stepfun-voices.md](references/stepfun-voices.md) for how
  `step-audio-r1.1`, `step-audio-2`, and `step-tts-*` differ in voice usage

## Workflow

1. Confirm the user wants StepFun `step-audio-r1.1` through Chat API.
2. Choose whether the turn is text-only or text plus local audio input.
3. Run the helper script with `stream: false`.
4. Return the saved transcript, the audio file path, and any important response
   fields to the user.

## Reference

Read [references/stepfun-chat-api.md](references/stepfun-chat-api.md) when you
need the exact request shape, supported audio fields, or the non-streaming
response layout. Read [references/stepfun-voices.md](references/stepfun-voices.md)
when you need voice-selection guidance.
