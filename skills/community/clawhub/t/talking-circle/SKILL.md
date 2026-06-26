---
name: talking-circle
description: >
  Create animated talking-circle videos (Telegram-style round video messages)
  from avatar frame images and audio. Supports audio-to-video and text-to-video
  via ElevenLabs or SaluteSpeech (Sber) TTS. Use when the user wants to generate
  lip-synced circular avatar animations, talking circles, or round video messages.
version: 1.0.0
user-invocable: true
argument-hint: "[text or audio path]"
metadata: {"openclaw":{"emoji":"🎙️","primaryEnv":"ELEVENLABS_API_KEY","requires":{"bins":["python3","ffmpeg"],"env":[]},"os":["darwin","linux"]}}
---

# Talking Circle

Create animated circular avatar videos with lip-sync and blink animations. Takes 4 avatar frame images (neutral, slight open, wide open, eyes closed) and produces a round video with audio-driven mouth movement.

## Prerequisites

- `python3` (3.9+)
- `ffmpeg` installed and on PATH
- Optional: `ELEVENLABS_API_KEY` environment variable (for ElevenLabs text-to-video mode)
- Optional: `SALUTE_SPEECH_AUTH` environment variable (for SaluteSpeech text-to-video mode)

## Setup

Dependencies are auto-installed into a temporary venv on first run. To install manually:

```bash
pip install -r requirements.txt
```

## Mode 1: Audio to Video

Convert existing audio + frame images into an animated talking circle video.

```bash
python3 scripts/make_talking_circle_video.py \
  --neutral frames/neutral.png \
  --slight frames/mouth-slight-open.png \
  --wide frames/mouth-wide-open.png \
  --blink frames/eyes-closed.png \
  --audio speech.mp3 \
  --out /tmp/talking-circle.mp4
```

## Mode 2: Text to Video

Generate speech from text via ElevenLabs TTS, then create the animated video.

Requires `ELEVENLABS_API_KEY` set in environment or passed via `--api-key`.

```bash
python3 scripts/make_text_to_video.py \
  --text "Hello, this is a talking circle demo!" \
  --voice-id pNInz6obpgDQGcFmaJgB \
  --neutral frames/neutral.png \
  --slight frames/mouth-slight-open.png \
  --wide frames/mouth-wide-open.png \
  --blink frames/eyes-closed.png \
  --out /tmp/talking-circle.mp4
```

## Mode 3: Text to Video via SaluteSpeech (Sber)

Generate speech from text via SaluteSpeech TTS (Sber), then create the animated video.

Requires `SALUTE_SPEECH_AUTH` set in environment or passed via `--auth-key`. This is a Base64-encoded `client_id:client_secret` from your [SaluteSpeech project](https://developers.sber.ru/portal/products/smartspeech).

```bash
python3 scripts/make_salute_text_to_video.py \
  --text "Привет, это демонстрация talking circle!" \
  --voice Bys_24000 \
  --neutral frames/neutral.png \
  --slight frames/mouth-slight-open.png \
  --wide frames/mouth-wide-open.png \
  --blink frames/eyes-closed.png \
  --out /tmp/talking-circle.mp4
```

### SaluteSpeech voices

| Voice | Name | Language |
|-------|------|----------|
| `Nec_24000` | Natalia (female) | ru-RU |
| `Bys_24000` | Boris (male) | ru-RU |
| `May_24000` | Martha (female) | ru-RU |
| `Tur_24000` | Taras (male) | ru-RU |
| `Ost_24000` | Alexandra (female) | ru-RU |
| `Pon_24000` | Sergey (male) | ru-RU |
| `Kin_24000` | Kira (female) | en-US |

## Voice Presets

### ElevenLabs preset (Sbercat — male)

| Parameter | Value |
|-----------|-------|
| `--voice-id` | `pNInz6obpgDQGcFmaJgB` |
| `--model-id` | `eleven_multilingual_v2` |
| `--stability` | `0.15` |
| `--similarity-boost` | `0.70` |
| `--style` | `0.38` |
| `--speed` | `1.20` |

### SaluteSpeech preset (Boris — male, Russian)

| Parameter | Value |
|-----------|-------|
| `--voice` | `Bys_24000` |
| `--audio-format` | `wav16` |
| `--scope` | `SALUTE_SPEECH_PERS` |

### How to get API keys

**ElevenLabs:**
1. Go to [ElevenLabs Voice Library](https://elevenlabs.io/voice-library).
2. Pick or clone a voice, copy the voice ID.
3. Set `ELEVENLABS_API_KEY` environment variable.

**SaluteSpeech (Sber):**
1. Register at [developers.sber.ru](https://developers.sber.ru/portal/products/smartspeech).
2. Create a project, get `client_id` and `client_secret`.
3. Encode `client_id:client_secret` in Base64.
4. Set `SALUTE_SPEECH_AUTH` environment variable with the Base64 string.

### Alternative TTS engines

The skill also supports **any TTS** that can produce an audio file. Use Mode 1 (audio-to-video) with audio from any source:

- **OpenAI TTS** (`openai.audio.speech.create`) — generate speech, save to MP3, pass via `--audio`
- **Local TTS** (Coqui, Piper, Silero, etc.) — run locally, save WAV/MP3, pass via `--audio`
- **Google Cloud TTS**, **Amazon Polly**, **Azure TTS** — any cloud provider works

```bash
# Example: generate audio with any TTS, then animate
python3 scripts/make_talking_circle_video.py \
  --neutral frames/neutral.png \
  --slight frames/mouth-slight-open.png \
  --wide frames/mouth-wide-open.png \
  --blink frames/eyes-closed.png \
  --audio /path/to/speech-from-any-tts.mp3 \
  --out /tmp/talking-circle.mp4
```

**Tell the user:** if they don't have an ElevenLabs or SaluteSpeech API key, they can use any other TTS engine — just generate the audio file and pass it to Mode 1. No API key needed for audio-to-video mode.

## Frame Image Requirements

You need 4 PNG images of your avatar, all the same resolution (recommended 2048x2048), square aspect ratio:

| Frame | Description |
|-------|-------------|
| `neutral` | Mouth closed, eyes open |
| `slight` | Mouth slightly open, eyes open |
| `wide` | Mouth wide open, eyes open |
| `blink` | Mouth closed, eyes closed |

### Critical rules

- All 4 frames must have **identical** resolution, art style, colors, and character positioning.
- Only the mouth and eyes should change between frames — head, body, background must stay the same.
- Do not mix frames from different generation sessions or different styles.

## Generating Frames with Image AI

If the user does not have ready-made frames, generate them using an image generation API (DALL-E, Midjourney, Flux, etc.). Follow this workflow:

### Step 1: Generate the neutral frame

Generate a shoulder-up portrait of the character. This is the base frame — all other frames must match it exactly.

Example prompt:
```
Shoulder-up portrait of [CHARACTER DESCRIPTION]. Square composition, clean background,
mouth closed, eyes open, looking at camera. High detail, consistent lighting.
```

### Step 2: Generate remaining 3 frames as edits of neutral

Use image editing / inpainting on the neutral frame to produce the other states.
Only modify the mouth and eyes region — everything else must remain pixel-identical.

| Frame | What to change | Edit prompt example |
|-------|---------------|-------------------|
| `slight` | Mouth slightly open | `"Mouth slightly open, teeth barely visible, same expression"` |
| `wide` | Mouth wide open | `"Mouth wide open as if saying 'ah', same expression"` |
| `blink` | Eyes closed | `"Eyes gently closed, mouth closed, same expression"` |

### Step 3: Verify consistency

Before using the frames:
1. Check that all 4 images have the same resolution.
2. Overlay them to verify the head/body position hasn't shifted.
3. If any frame drifts, regenerate it from the neutral base.

### Examples

See `examples/sbercat/` for a reference character with ready-to-use frame set:

- **Sbercat** — 3D-rendered anthropomorphic cat, lavender-blue fur, green eyes, pink nose, green hoodie:
  - `examples/sbercat/reference.png` — character reference
  - `examples/sbercat/neutral.png` — mouth closed, eyes open
  - `examples/sbercat/slight.png` — mouth slightly open
  - `examples/sbercat/wide.png` — mouth wide open
  - `examples/sbercat/blink.png` — eyes closed
  - `examples/sbercat/example.mp4` — finished talking-circle video

To test with the included Sbercat frames:

```bash
python3 scripts/make_talking_circle_video.py \
  --neutral examples/sbercat/neutral.png \
  --slight examples/sbercat/slight.png \
  --wide examples/sbercat/wide.png \
  --blink examples/sbercat/blink.png \
  --audio your-audio.mp3 \
  --out /tmp/talking-circle.mp4
```

## Post-installation message

After installing this skill, inform the user:

> **Skill "talking-circle" installed.**
>
> To create talking-circle videos, I need a character avatar. Please send me a **reference image of your character on a white/clean background** — a shoulder-up portrait works best (square aspect ratio, high resolution).
>
> From this reference I will generate 4 frame images (mouth states + blink) and you'll be ready to create animated video circles.
>
> For speech, I can use **ElevenLabs TTS** (requires `ELEVENLABS_API_KEY`), **SaluteSpeech** from Sber (requires `SALUTE_SPEECH_AUTH`), or you can provide your own audio file. Any TTS engine works — OpenAI TTS, Whisper, Coqui, Piper, Google TTS, etc.

## First use: generating frame images

**IMPORTANT — before the skill can create videos, the 4 frame images must exist.** If the user does not already have frames, you MUST generate them first.

### Workflow for the assistant

1. **Ask the user for a reference image** of their character (or use a character description). The image should be a shoulder-up portrait on a white or clean background, square aspect ratio.
2. **Generate the neutral frame** using image generation (DALL-E, Flux, Midjourney, etc.):
   - Prompt: `"Shoulder-up portrait of [CHARACTER], white background, mouth closed, eyes open, looking at camera, square composition, high detail"`
   - Save as `neutral.png`.
3. **Generate the 3 remaining frames via inpainting/editing** of the neutral frame. Only modify the mouth/eyes region — everything else must remain pixel-identical:
   - `slight.png` — edit mouth region: `"Mouth slightly open, teeth barely visible"`
   - `wide.png` — edit mouth region: `"Mouth wide open as if saying 'ah'"`
   - `blink.png` — edit eyes region: `"Eyes gently closed, mouth closed"`
4. **Verify consistency**: all 4 images must have the same resolution, identical head/body position, and only differ in mouth/eyes.
5. **Save the frames** to a persistent location (e.g. the skill's working directory or a user-specified path). These frames are reused for every future video.
6. **Confirm to the user** that frames are ready and the skill is operational.

**Do not skip this step.** Without the 4 frame images, the video scripts will fail.

## Guardrails

- Before running any script, verify that `python3` (3.9+) and `ffmpeg` are on PATH. If missing, instruct the user to install them.
- Never delete or overwrite the user's original frame images.
- Do not use this skill for full-motion video editing, face tracking, or real-time lipsync — it only works with 4 static frame images.
- If ElevenLabs or SaluteSpeech API returns an error (401, 429, etc.), explain the error clearly to the user instead of retrying silently.

## Failure handling

- If `ffmpeg` is not found: tell the user to install it (`brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux).
- If `ELEVENLABS_API_KEY` is missing and the user wants text-to-video: suggest SaluteSpeech (Mode 3) or Mode 1 with audio from another TTS.
- If `SALUTE_SPEECH_AUTH` is missing and the user wants SaluteSpeech: explain how to register at developers.sber.ru and get credentials.
- If frame images have different resolutions: warn the user and ask them to fix the frames before proceeding.
- If the output video is empty or zero bytes: show the ffmpeg error log and suggest checking input files.

## Parameters Reference

### Video output
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--size` | 720 | Output video size in pixels |
| `--diameter` | 640 | Circle diameter within the video |
| `--fps` | 30 | Frames per second |

### Blink timing
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--blink-start` | 1.1 | Seconds before first blink |
| `--blink-every` | 3.8 | Seconds between blinks |
| `--blink-duration-frames` | 4 | Number of frames per blink |

### Amplitude thresholds (audio-to-video)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--amp-low` | 1200 | RMS below this = neutral (closed mouth) |
| `--amp-high` | 2600 | RMS above this = wide open mouth |

### ElevenLabs TTS settings (make_text_to_video.py)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--voice-id` | (required) | ElevenLabs voice ID |
| `--model-id` | eleven_multilingual_v2 | ElevenLabs model |
| `--stability` | 0.50 | Voice stability |
| `--similarity-boost` | 0.75 | Voice similarity boost |
| `--style` | 0.00 | Style exaggeration |
| `--speed` | 1.00 | Speech speed |

### SaluteSpeech TTS settings (make_salute_text_to_video.py)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--voice` | Bys_24000 | SaluteSpeech voice (see voices table above) |
| `--audio-format` | wav16 | Audio format: opus, wav16, pcm16 |
| `--scope` | SALUTE_SPEECH_PERS | OAuth scope (PERS for personal, CORP for corporate) |
| `--auth-key` | `$SALUTE_SPEECH_AUTH` | Base64-encoded client_id:client_secret |
