---
name: qwen-audio
description: "High-performance audio library with text-to-speech (TTS) and speech-to-text (STT)."
version: "0.0.4"
---

# Qwen-Audio

## Overview

Qwen-Audio is a high-performance audio processing library optimized. It delivers fast, efficient TTS and STT with support for multiple models, languages, and audio formats.

## Prerequisites

- Python 3.10+

### Environment checks

Before using any capability, verify that all items in `./references/env-check-list.md` are complete.

## Capabilities

### Voice Management

Voices are stored in the `./voices/` directory at the skill root level. Each voice has its own folder containing:
- `ref_audio.wav` - Reference audio file
- `ref_text.txt` - Reference text transcript
- `ref_instruct.txt` - Voice style description


#### Create a Voice
Create a reusable voice profile using VoiceDesign model. The `--instruct` parameter is required to describe the voice style:
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" voice create --text "This is a sample voice reference text." --instruct "A warm, friendly female voice with a professional tone." --id "my-voice-id"
```
Optional: `--id "my-voice-id"` to specify a custom voice ID.

**Returns (JSON):**
```json
{
  "id": "my-voice-id",
  "ref_audio": "/<qwen-audio-skill-path>/voices/my-voice-id/ref_audio.wav",
  "ref_text": "This is a sample voice reference text.",
  "instruct": "A warm, friendly female voice with a professional tone.",
  "duration": 3.456,
  "sample_rate": 24000,
  "success": true
}
```


#### List Voices
List all created voice profiles:
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" voice list
```

**Returns (JSON):**
```json
[
  {
    "id": "my-voice-id",
    "ref_audio": "/<qwen-audio-skill-path>/voices/my-voice-id/ref_audio.wav",
    "ref_text": "This is a sample voice reference text.",
    "instruct": "A warm, friendly female voice with a professional tone.",
    "duration": 3.456,
    "sample_rate": 24000
  }
]
```


### Text to Speech

#### TTS Voice Pre-check (Required)
Before any `tts` generation, always confirm the available voices first:

1. Run `voice list` to check the current voice profiles.
2. If the returned list is empty, stop and ask the user what kind of voice they want to create first. Offer style choices, for example:
   - Warm and friendly female narrator
   - Deep and steady male broadcast voice
   - Young and energetic neutral voice
   - Calm and professional customer-service voice
   Then run `voice create` only after the user confirms a style.
3. If the returned list is not empty, show the available voice `id` values and ask the user to confirm which one should be used as the `--ref_voice` reference id for generation.

Only run `tts` after this confirmation step is complete.

```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" tts --text "hello world" --output "/path/to/save.wav"
```
**Returns (JSON):**
```json
{
  "audio_path": "/path/to/save.wav",
  "duration": 1.234,
  "sample_rate": 24000,
  "success": true
}
```

### Voice Cloning
Clone any voice using a reference audio sample. Provide the wav file and its transcript:
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" tts --text "hello world" --output "/path/to/save.wav" --ref_audio "sample_audio.wav" --ref_text "This is what my voice sounds like."
```
ref_audio: reference audio to clone
ref_text: transcript of the reference audio


#### Use a Created Voice
After creating a voice, use it for TTS with the `--ref_voice` parameter. The instruct will be automatically loaded:
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" tts --text "New text to speak" --output "/path/to/save.wav" --ref_voice "my-voice-id" --instruct "Very happy and excited."
```
Optional: `--instruct` to emotion control.


### Automatic Speech Recognition (STT)
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" stt --audio "/sample_audio.wav" --output "/path/to/save.txt" --output-format txt
```
Test audio: https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav
output-format: "txt" | "ass" | "srt" | "all"

**Returns (JSON):**
```json
{
  "text": "transcribed text content",
  "duration": 10.5,
  "sample_rate": 16000,
  "files": ["/path/to/save.txt", "/path/to/save.srt"],
  "success": true
}
```
