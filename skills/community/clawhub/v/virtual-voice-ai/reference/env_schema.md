# Environment Variables

Add all of these to your project's `.env` file before running any script.

## Required

```env
# --- Speech-to-Text ---
DEEPGRAM_API_KEY=your_deepgram_key_here
# Get from: https://console.deepgram.com

# --- LLM ---
LLM_PROVIDER=groq
# Options: groq | openai | anthropic | ollama
LLM_API_KEY=your_llm_key_here
LLM_MODEL=llama3-8b-8192
# Groq models: llama3-8b-8192 (fastest), mixtral-8x7b-32768
# OpenAI models: gpt-4o-mini, gpt-4o
# Ollama: set LLM_API_KEY=none, set LLM_MODEL to your local model name

# --- Text-to-Speech ---
TTS_PROVIDER=elevenlabs
# Options: elevenlabs | cartesia
TTS_API_KEY=your_tts_key_here
TTS_VOICE_ID=your_voice_id_here
# ElevenLabs: get voice ID from voice library
# Cartesia: get voice ID from dashboard

# --- Audio Device ---
VIRTUAL_CABLE_NAME=CABLE Input
# Exact string from running: node scripts/01_list_devices.js
# Windows VB-Cable: usually "CABLE Input (VB-Audio Virtual Cable)"
# macOS BlackHole: usually "BlackHole 2ch"
```

## Optional

```env
# Sentence chunker tuning
CHUNK_MAX_WORDS=25
# Default: 25. Lower = faster but more robotic TTS. Higher = more natural but more latency.

CHUNK_FLUSH_TIMEOUT_MS=800
# Default: 800. Flush partial sentence after this many ms of silence from LLM.

# Deepgram tuning
DEEPGRAM_ENDPOINTING_MS=300
# Default: 300. How long Deepgram waits after speech stops before finalizing transcript.

# Debug
PIPELINE_DEBUG=false
# Set to true to log every stage boundary to console.
```

## .env validation

The skill checks for missing required vars on startup and throws a clear error:

```
[voice-pipeline] Missing required env vars: TTS_API_KEY, VIRTUAL_CABLE_NAME
Add them to your .env and restart.
```