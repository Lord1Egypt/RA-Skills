---
name: supertonic-tts
description: On-device multilingual text-to-speech using Supertonic (Supertone). Use when the user needs local/offline TTS, voice generation, speech synthesis, or converting text to audio without cloud APIs. Triggers on mentions of supertonic, TTS, text-to-speech, voice synthesis, local speech, offline TTS, edge TTS, or multilingual voice generation. Base synthesis runs entirely on-device via ONNX — no API key, no cloud calls during generation. Note: voice cloning requires a one-time upload to a third-party service.
---

# Supertonic TTS Skill

Local, multilingual text-to-speech powered by Supertone's Supertonic ONNX model.

## Core Features

- **Offline synthesis** — Base TTS runs on-device via ONNX with no API key and no cloud calls during generation.
- **Tiny footprint** — 66M–99M parameters. Runs on Pi, browser, e-reader, phone.
- **Stupid fast** — Up to 167× real-time on consumer hardware. 4s of audio in ~25ms.
- **Studio output** — 44.1kHz 16-bit mono WAV, no upsampler needed.
- **31 languages** — Full multilingual support with `lang="na"` auto-detect fallback.
- **Voice cloning** — Clone any voice via online Voice Builder (requires uploading a reference clip to a third-party service), then deploy the exported voice style offline permanently.
- **Expression tags** — Only `<laugh>` is user-verified to produce audible expression. `<breath>` and `<sigh>` are weak/unconfirmed. All others fail silently.

## Prerequisites

Requires the Python SDK and model assets. Install once:

```bash
pip install supertonic
```

First run auto-downloads ~400MB of ONNX models from Hugging Face into `~/.cache/supertonic3/`.

## Quick Use

### Python SDK

```python
from supertonic import TTS

tts = TTS(auto_download=True)
style = tts.get_voice_style(voice_name="M1")

wav, duration = tts.synthesize(
    text="Your text here",
    lang="en",           # language code or "na" for auto-detect
    voice_style=style,
    total_steps=8,       # quality: 5 (low) to 12 (high)
    speed=1.0,           # 0.7 (slow) to 2.0 (fast)
)

tts.save_audio(wav, "output.wav")
```

### CLI (via supertonic package)

```bash
# Basic synthesis
supertonic tts "Hello world" -o output.wav

# Pick voice and quality
supertonic tts "Use a different voice." -o output.wav --voice F1 --steps 10

# Custom cloned voice
supertonic tts "Hello in my voice." -o output.wav --custom-style-path voices/my_voice.json

# Multilingual
supertonic tts "こんにちは" -o japanese.wav --lang ja
supertonic tts "Bonjour" -o french.wav --lang fr
```

### Skill Scripts

```bash
cd ~/.openclaw/workspace/skills/supertonic-tts/scripts
source ~/.openclaw/workspace/.browser-use-venv/bin/activate

# Quick synthesis
python3 synthesize.py "Hello world" --voice M1 --output ~/hello.wav

# With expression tags (only <laugh> is confirmed to work)
python3 synthesize.py "You did it <laugh> I am so proud." --voice M5 --output laugh.wav

# Custom voice
python3 synthesize.py "Hello" --custom-style my_voice.json --output cloned.wav

# Japanese
python3 synthesize.py "こんにちは" --voice F3 --lang ja

# List voices
python3 list_voices.py
```

## Voices

10 built-in voices: F1–F5 (female), M1–M5 (male).

**Voice cloning**: Record a short clip → upload to [Voice Builder](https://supertonic.supertone.ai/voice_builder) (online service, see privacy note in `references/voices.md`) → export JSON → load with `get_voice_style_from_path()`.

See `references/voices.md` for voice descriptions and Voice Builder workflow.

## Expression Tags

> **⚠️ Mostly non-functional in practice**
>
> Supertonic accepts inline self-closing tags, but **only `<laugh>` has been user-verified** to produce a clearly audible expression (laughter burst). `<breath>` and `<sigh>` may insert minor pauses but are not confirmed as audible breathing/sighing sounds.
>
> **Do not rely on tags for expression.** Tested tags that failed to produce audible effect include: `<sarcastic>`, `<excited>`, `<whisper>`, `<shout>`, `<happy>`, `<sad>`, `<angry>`, `<chuckle>`, `<giggle>`, `<snort>`, `<gasp>`, `<grunt>`, `<cough>`, `<scream>`, `<sing>`, `<cry>`, `<yawn>`, `<hmm>`, `<aha>`.

**Correct syntax** (self-closing, inline):
```python
text = "You did it <laugh> I am so proud."
```

**Reliable alternative** for emotion: explicit language + `speed` modulation:

| Emotion | Technique |
|---------|-----------|
| Happy | Upbeat words + `speed=1.1` |
| Sad | Subdued words + `speed=0.85` |
| Excited | Exclamations + `speed=1.15` |
| Urgent | Short imperatives + `speed=1.2` |

See `references/expression-tags.md` for full testing results.

## Parameters

| Param | Range | Default | What It Does |
|-------|-------|---------|-------------|
| `total_steps` | 5–12 | 8 | Quality vs speed tradeoff |
| `speed` | 0.7–2.0 | 1.0 | Speech rate multiplier |
| `max_chunk_length` | any | 300 | Break long text into chunks (120 for Korean) |
| `silence_duration` | any | 0.3 | Pause between chunks (seconds) |
| `lang` | ISO 639-1 or `"na"` | `"en"` | `"na"` = language-agnostic auto-detect |
| `verbose` | True/False | `False` | Show detailed progress |

## Languages

31 languages + `na` (language-agnostic auto-detect). See `references/languages.md` for all codes.

## Output

- Format: 44.1kHz 16-bit mono WAV
- Returns: `(wav_array, duration_array)`
- `wav.shape` = `(1, num_samples)`
- `duration[0]` = length in seconds

## Multi-Runtime Deployment

Supertonic runs across: Python, Node.js, Browser (WebGPU), Java, C++, C#, Go, Swift, iOS, Rust, Flutter.

## Scripts

- `scripts/synthesize.py` — CLI for quick text-to-speech (supports custom voices)
- `scripts/list_voices.py` — Available voices and metadata

## References

- `references/voices.md` — Voice descriptions, selection guide, Voice Builder workflow
- `references/expression-tags.md` — All tags, examples, caveats
- `references/languages.md` — Supported language codes
- `references/deployment.md` — Multi-runtime deployment options
