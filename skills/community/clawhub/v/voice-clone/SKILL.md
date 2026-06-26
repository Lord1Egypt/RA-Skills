---
name: senseaudio-voice-cloner
description: Guide users through SenseAudio platform voice cloning, then generate TTS with cloned `voice_id` values. Use when users want to clone voices, manage cloned voice slots, or synthesize audio with a cloned voice.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - python3
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
    install:
      - kind: uv
        package: requests
      - kind: uv
        package: pydub
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
homepage: https://senseaudio.cn
source: https://github.com/anthropics/skills
---

# SenseAudio Voice Cloner

Guide users through platform-side voice cloning, then generate personalized TTS with the resulting cloned `voice_id`.

## What This Skill Does

- Explain the official SenseAudio voice-cloning workflow
- Validate whether a sample is likely suitable for cloning
- Help users manage cloned voice slots and `voice_id` values
- Generate TTS with a cloned voice through the official TTS API
- Apply optional pronunciation dictionary control for cloned voices

## Credential and Dependency Rules

- Read the API key from `SENSEAUDIO_API_KEY`.
- Send auth only as `Authorization: Bearer <API_KEY>`.
- Do not place API keys in query parameters, logs, or saved examples.
- If Python helpers are used, this skill expects `python3`, `requests`, and `pydub`.
- `pydub` is only needed for optional local audio validation.

## Official Voice-Cloning Constraints

Use the official SenseAudio platform voice-cloning rules summarized below:

- Cloning itself is platform-side only; there is no direct public API to create a cloned voice.
- Users must first clone on the platform, then retrieve the resulting `voice_id` for API use.
- Sample requirements for platform cloning:
  - duration: `3-30` seconds
  - size: `<=50MB`
  - format: `MP3`, `WAV`, or `AAC`
  - recording environment: quiet and echo-free
- Cloning consumes a voice slot on the user's plan.
- Deleting unused cloned voices frees slots.

## Official TTS Constraints for Cloned Voices

Use the official TTS API on `/v1/t2a_v2` after the user already has a cloned `voice_id`:

- Standard TTS model: `SenseAudio-TTS-1.0`
- `voice_setting.voice_id` is required and may be a cloned voice ID
- Optional audio formats: `mp3`, `wav`, `pcm`, `flac`
- Optional sample rates: `8000`, `16000`, `22050`, `24000`, `32000`, `44100`
- Optional MP3 bitrates: `32000`, `64000`, `128000`, `256000`
- Optional channels: `1` or `2`
- Optional pronunciation `dictionary` is only for cloned voices and requires `model=SenseAudio-TTS-1.5`

## Recommended Workflow

1. Confirm cloning status:
- If the user does not yet have a cloned voice, direct them to the platform cloning flow first.
- If they already have a cloned voice, ask for the `voice_id`.

2. Validate the source sample when helpful:
- Check duration, file type, and basic audio quality locally.
- Warn when the sample is noisy, reverberant, or outside the documented size/duration limits.

3. Generate TTS with the cloned voice:
- Use `SenseAudio-TTS-1.0` for normal synthesis.
- Use `SenseAudio-TTS-1.5` only when a pronunciation `dictionary` is needed.

4. Keep output safe and reproducible:
- Decode returned hex audio before writing files.
- Keep filenames deterministic and avoid logging secrets.

## Platform Guidance Helper

```python
def guide_voice_cloning():
    return """
To clone a voice on the SenseAudio platform:

1. Open https://senseaudio.cn/platform/voice-clone
2. Prepare a clean speech sample:
   - Duration: 3-30 seconds
   - Format: MP3 / WAV / AAC
   - Size: 50MB or less
   - Environment: quiet, low echo, clear speech
3. Upload or record the sample on the platform
4. Wait for the platform to finish training
5. Copy the resulting voice_id from the voice list
6. Use that voice_id in later TTS API calls
"""
```

## Minimal TTS Helper

```python
import binascii
import os

import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


def generate_with_cloned_voice(text, voice_id, speed=1.0, vol=1.0, pitch=0):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "SenseAudio-TTS-1.0",
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": "mp3",
                "sample_rate": 32000,
                "bitrate": 128000,
                "channel": 2,
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return binascii.unhexlify(data["data"]["audio"]), data.get("trace_id")
```

## Pronunciation Dictionary Pattern

Use this only for cloned voices that need explicit polyphone correction.

```python
def generate_with_dictionary(text, voice_id, dictionary):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "SenseAudio-TTS-1.5",
            "text": text,
            "voice_setting": {"voice_id": voice_id},
            "dictionary": dictionary,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
```

Dictionary items follow the official shape:

- `original`: source text span
- `replacement`: pronunciation override such as `[hao4]干净`

## Optional Local Validation

```python
from pydub import AudioSegment


def validate_cloning_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    issues = []

    if not 3000 <= len(audio) <= 30000:
        issues.append("duration_out_of_range")
    if audio.frame_rate < 16000:
        issues.append("sample_rate_low")
    if audio.channels > 2:
        issues.append("too_many_channels")
    if not audio_file.lower().endswith((".mp3", ".wav", ".aac")):
        issues.append("unsupported_extension")

    return {
        "valid": not issues,
        "issues": issues,
        "duration_ms": len(audio),
        "sample_rate": audio.frame_rate,
        "channels": audio.channels,
    }
```

## Output Options

- MP3 or WAV audio synthesized with a cloned voice
- Markdown instructions for platform cloning and slot management
- JSON metadata containing `voice_id` labels and local descriptions
- Optional validation report for source samples

## Safety Notes

- Do not claim that voice cloning can be initiated through the public API.
- Do not mix `API_KEY` and `SENSEAUDIO_API_KEY`; use `SENSEAUDIO_API_KEY` consistently.
- Use `SenseAudio-TTS-1.0` by default; reserve `SenseAudio-TTS-1.5` for cloned-voice dictionary use.
- Treat `voice_id` values as user-specific operational identifiers.
