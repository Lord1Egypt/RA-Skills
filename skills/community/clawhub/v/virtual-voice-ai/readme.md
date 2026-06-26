# voice-pipeline

A Node.js skill that intercepts your real microphone, runs it through an AI brain (Speech-to-Text → LLM → Text-to-Speech), and routes the processed voice output to a virtual audio cable — so any meeting app (Google Meet, Zoom, Teams) hears the AI voice instead.

## What it does

```
Real Mic → ffmpeg (resample) → Deepgram STT → LLM → Sentence Chunker → TTS → PCM Decode → VB-Cable → Meeting App
```

## Requirements

- Node.js 18+
- ffmpeg installed and in PATH
- VB-Audio Cable (Windows) or BlackHole 2ch (macOS)
- API keys: Deepgram, an LLM provider (Groq/OpenAI/etc), a TTS provider (ElevenLabs/Cartesia)

## Usage

> "Set up the voice pipeline skill in my project"
> "Run step 3 of the voice pipeline"
> "My Deepgram transcripts aren't appearing, debug the pipeline"
> "Wire the kill switch into my app"

## Install

Add to your project's `.env`:

```env
DEEPGRAM_API_KEY=
LLM_PROVIDER=groq
LLM_API_KEY=
LLM_MODEL=llama3-8b-8192
TTS_PROVIDER=elevenlabs
TTS_API_KEY=
VIRTUAL_CABLE_NAME=CABLE Input
```

## Skill files

| File | Purpose |
|---|---|
| `scripts/01_list_devices.js` | Find your VB-Cable device name |
| `scripts/02_capture_resample.js` | Mic capture + 16kHz resample |
| `scripts/03_deepgram_ws.js` | STT WebSocket |
| `scripts/04_llm_stream.js` | LLM token stream |
| `scripts/05_sentence_chunker.js` | Buffer tokens to sentence boundaries |
| `scripts/06_tts_ws.js` | TTS WebSocket |
| `scripts/07_pcm_write.js` | Decode + write to VB-Cable |