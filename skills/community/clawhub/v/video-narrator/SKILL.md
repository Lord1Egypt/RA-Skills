---
name: senseaudio-video-narrator
description: Generate SenseAudio TTS narration tracks for videos, including timestamped segments, style variants, and editor-ready voiceover exports. Use when users need voiceovers, video narration, timed commentary, or accessibility narration.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - python3
        - ffmpeg
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
---

# SenseAudio Video Narrator

Create professional narration audio for videos with timing-aware segmentation, natural delivery, and editor-friendly exports.

## What This Skill Does

- Generate narration audio synchronized to script timestamps
- Match narration style to video genre such as documentary or tutorial
- Control pacing with official TTS parameters and text break markers
- Create multiple narration takes with different voices or styles
- Export audio segments and merged narration tracks for editing workflows

## Credential and Dependency Rules

- Read the API key from `SENSEAUDIO_API_KEY`.
- Send auth only as `Authorization: Bearer <API_KEY>`.
- Do not place API keys in query parameters, logs, or saved examples.
- If Python helpers are used, this skill expects `python3`, `requests`, and `pydub`.
- `pydub` is used only for optional local audio assembly and mixing.

## Official TTS Constraints

Use the official SenseAudio TTS rules summarized below:

- HTTP endpoint: `POST https://api.senseaudio.cn/v1/t2a_v2`
- Model: `SenseAudio-TTS-1.0`
- Max text length per request: `10000` characters
- `voice_setting.voice_id` is required
- `voice_setting.speed` range: `0.5-2.0`
- `voice_setting.pitch` range: `-12` to `12`
- Optional audio formats: `mp3`, `wav`, `pcm`, `flac`
- Optional sample rates: `8000`, `16000`, `22050`, `24000`, `32000`, `44100`
- Optional MP3 bitrates: `32000`, `64000`, `128000`, `256000`
- Optional channels: `1` or `2`
- `extra_info.audio_length` returns segment duration in milliseconds
- Inline break markup such as `<break time=500>` is supported in text

## Recommended Workflow

1. Prepare the script:
- Split narration into timestamped segments.
- Keep each segment comfortably below the `10000` character limit.

2. Choose a voice and pacing profile:
- Pick a `voice_id` and tune `speed`, `pitch`, and optional `vol`.
- Use shorter segments when timing precision matters.

3. Generate audio segments:
- Call the TTS API for each segment.
- Decode `data.audio` from hex before saving.
- Capture `extra_info.audio_length` for timeline metadata.

4. Assemble the narration track locally:
- Use `pydub` to position clips on a silent master track.
- Keep per-segment files for easier editor import and retiming.

5. Validate timing against the video:
- Leave small gaps when natural pacing is needed.
- Adjust segment boundaries instead of overusing extreme speed values.

## Minimal Timed Narration Helper

```python
import binascii
import os
import re

import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


def parse_timed_script(script):
    pattern = r"\[(\d{2}):(\d{2}):(\d{2})\]\s*(.+?)(?=\n\[|\Z)"
    segments = []
    for match in re.finditer(pattern, script, re.DOTALL):
        hours, minutes, seconds, text = match.groups()
        timestamp_ms = (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000
        segments.append({"timestamp": timestamp_ms, "text": text.strip()})
    return segments


def synthesize_segment(text, voice_id, speed=1.0, pitch=0, vol=1.0):
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
                "pitch": pitch,
                "vol": vol,
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
    return {
        "audio_bytes": binascii.unhexlify(data["data"]["audio"]),
        "duration_ms": data["extra_info"]["audio_length"],
        "trace_id": data.get("trace_id"),
    }
```

## Local Assembly Pattern

```python
from pydub import AudioSegment


def create_synced_narration(audio_segments, video_duration_ms):
    narration_track = AudioSegment.silent(duration=video_duration_ms)
    for segment in audio_segments:
        clip = AudioSegment.from_file(segment["file"])
        narration_track = narration_track.overlay(clip, position=segment["timestamp"])
    return narration_track
```

## Style Presets

- Documentary: slower `speed` such as `0.95`, neutral `pitch`
- Tutorial: `speed` near `1.0`, slightly warmer `pitch`
- Commercial: modestly faster `speed`, slightly higher `pitch`

Prefer conservative tuning and script editing over extreme voice parameter changes.

## Output Options

- Per-segment narration clips in `mp3` or `wav`
- Timing metadata in `json`
- Merged narration track for video editors
- Optional alternate takes with different styles

## Safety Notes

- Do not hardcode credentials.
- Do not assume local media tooling exists beyond what is declared here.
- Treat returned `trace_id` and generated narration assets as potentially sensitive production data.
