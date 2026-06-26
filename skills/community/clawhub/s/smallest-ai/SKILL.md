---
name: smallest-ai
description: >
  Ultra-fast text-to-speech and speech-to-text via Smallest AI's Lightning v3.1 and Pulse models.
  Use when the user wants to generate speech, convert text to voice, read text aloud,
  create voice notes, transcribe audio to text, or clone a voice.
  Sub-100ms latency TTS. 64ms TTFT STT. Supports 30+ languages including Hindi and Spanish.
  Voices include sophia, robert, advika, vivaan, camilla, and 80+ more.
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["curl"]
      env: ["SMALLEST_API_KEY"]
    primaryEnv: "SMALLEST_API_KEY"
---

# Smallest AI — Ultra-Fast Voice Suite

Text-to-speech (sub-100ms) via Lightning v3.1 and speech-to-text (64ms TTFT) via Pulse.

## Setup

1. Get API key from https://waves.smallest.ai → click "API Key" in left panel
2. Set `SMALLEST_API_KEY` in your environment:
```bash
export SMALLEST_API_KEY="your_key_here"
```

## Defaults

- Default female voice: `sophia` (American English)
- Default male voice: `robert` (American English)
- Default language: `en`
- Default speed: `1.0`
- Default sample rate: `24000`

## Voice Selection Rules

Follow these rules to select the voice:

1. If user explicitly names a voice (e.g. "use advika"), use that voice.
2. If user asks for a **male** voice, use the configured `defaultVoiceMale`.
3. If user asks for a **female** voice, use the configured `defaultVoiceFemale`.
4. If no gender preference, use `defaultVoiceFemale` (sophia by default).
5. For **Hindi** content: use `advika` (female) or `vivaan` (male).
6. For **Spanish** content: use `camilla` (female) or `carlos` (male).
7. For **Tamil** content: use `anitha` (female) or `raju` (male).

Always pass the configured `defaultLanguage`, `defaultSpeed`, and `defaultSampleRate` as `--lang`, `--speed`, and `--rate` flags unless the user overrides them.

## Text-to-Speech

Generate speech audio from text using Lightning v3.1 model.

### Shell (preferred — zero dependencies)

```bash
{baseDir}/scripts/tts.sh "Text to speak" --voice sophia --rate 24000 --speed 1.0 --lang en
```

### Python (requires `pip install smallestai` or just `requests`)

```bash
python3 {baseDir}/scripts/tts.py "Text to speak" --voice sophia --speed 1.0 --lang en --out speech.wav
```

### Voices

| Voice     | Gender | Accent          | Best For                    |
|-----------|--------|-----------------|-----------------------------|
| sophia    | Female | American        | General use (default)       |
| robert    | Male   | American        | Professional, reports (default) |
| advika    | Female | Indian          | Hindi content, code-switch  |
| vivaan    | Male   | Indian          | Bilingual English/Hindi     |
| camilla   | Female | Mexican/Latin   | Spanish content             |
| zara      | Female | American        | Conversational              |
| melody    | Female | American        | Storytelling, greetings     |
| arjun     | Male   | Indian          | English/Hindi bilingual     |
| stella    | Female | American        | Expressive, warm            |

80+ more voices available. List all with: `{baseDir}/scripts/voices.sh`

### Options

- `--voice <id>`: Voice identifier (default: sophia)
- `--rate <hz>`: Sample rate — 8000 | 16000 | 24000 | 44100 (default: 24000)
- `--speed <n>`: Playback speed 0.5–2.0 (default: 1.0)
- `--lang <code>`: Language code (default: en). See `{baseDir}/references/languages.md`
- `--out <path>`: Output file (default: auto-named `media/tts_<timestamp>.wav`)

### Output

Scripts print `MEDIA: <filepath>` on success. OpenClaw sends this as an audio attachment.

### Multilingual

Supports 30+ languages. Pass `--lang` with ISO code:

```bash
{baseDir}/scripts/tts.sh "नमस्ते, कैसे हैं आप?" --voice advika --lang hi
{baseDir}/scripts/tts.sh "Bonjour le monde" --voice sophia --lang fr
{baseDir}/scripts/tts.sh "Hola, buenos días" --voice camilla --lang es
```

Code-switching (mixing languages) works automatically — no flag needed:

```bash
{baseDir}/scripts/tts.sh "Hey, मुझे meeting remind कर दो" --voice advika --lang hi
```

## Speech-to-Text

Transcribe audio files using Pulse model. Supports WAV, MP3, OGG, FLAC.

### Shell

```bash
{baseDir}/scripts/stt.sh /path/to/audio.wav
{baseDir}/scripts/stt.sh /path/to/audio.wav --diarize --timestamps --emotions
```

### Python

```bash
python3 {baseDir}/scripts/stt.py /path/to/audio.wav --diarize --timestamps --lang en
```

### Options

- `--lang <code>`: Language (default: en)
- `--diarize`: Identify different speakers
- `--timestamps`: Word-level timing
- `--emotions`: Detect emotional tone

### Output

Returns JSON with `transcription` field. With `--diarize`, includes speaker labels per word.

## When to Use

Trigger this skill when the user:

- Asks to "say", "speak", "read aloud", or "generate speech/audio"
- Wants a "voice message", "voice note", or "audio file"
- Asks to "transcribe", "convert speech/audio to text"
- Mentions "Smallest AI", "Lightning TTS", or "Pulse STT"
- Needs fast or low-latency speech generation
- Wants Hindi, Spanish, multilingual, or code-switched voice output
- Asks to compare TTS providers or benchmark latency

## Error Handling

- Missing API key → tell user to set `SMALLEST_API_KEY`
- HTTP 401 → invalid or expired API key
- HTTP 429 → rate limited, wait and retry
- HTTP 400 → check text length (max ~5000 chars per request). Split long text into chunks.
- Empty audio → verify voice_id is valid

## Limits

- Max text per request: ~5000 characters
- For longer text: split into sentences, synthesize each, concatenate with sox or ffmpeg
- Free tier: 30 minutes/month of TTS
- Basic ($5/mo): 3 hours of TTS + 1 voice clone
