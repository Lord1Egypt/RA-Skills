# StepFun Voice Selection

This skill targets `step-audio-r1.1` via Chat Completions, not the standalone
TTS APIs. Even so, voice selection matters because `step-audio-r1.1` requires
`audio.voice` whenever you request spoken output.

## Practical Rules

- For this skill, always pass a voice id when audio output is needed.
- The helper defaults to `wenrounansheng` because it was validated in real
  smoke tests.
- For production use, prefer explicit `--voice` instead of relying on the
  default.

## Relationship Between Audio Chat And TTS

- `step-audio-r1.1`: speech understanding + speech generation through Chat
  Completions
- `step-audio-2` / `step-audio-2-mini`: newer speech models with stronger
  end-to-end capabilities and tool calling
- `step-tts-2` / `step-tts-mini` / `step-tts-vivid`: dedicated TTS models for
  text-to-speech, richer emotional/style control, and voice cloning workflows

If the user wants advanced TTS controls such as emotion, style, speed, volume,
voice cloning, or standalone speech generation from plain text, prefer a
dedicated StepFun TTS skill instead of this chat-completions skill.

## Official Voice Guidance

According to StepFun audio-chat guidance:

- For `step-audio-2` models, docs show built-in voice ids including:
  - `wenrounansheng`
  - `qingchunshaonv`
  - `livelybreezy-female`
  - `elegantgentle-female`
- For `step-audio-r1.1` and `step-1o-audio`, docs direct you to query the
  voice-list endpoint to inspect available voice ids.

## Account-Level Voice Discovery

This skill provides:

```bash
python3 {baseDir}/scripts/stepfun_audio_chat.py --list-voices
```

That command queries StepFun's voice-list API and prints the custom/cloned
voices available to the current account, plus a short list of official voice
hints.

## Why This Skill Normalizes Input To WAV

The official docs mention WAV and MP3 input support. In real testing for this
skill, normalizing local input audio to WAV before embedding in
`input_audio.data` proved more reliable for `step-audio-r1.1`, so the helper
uses WAV normalization for compatibility.
