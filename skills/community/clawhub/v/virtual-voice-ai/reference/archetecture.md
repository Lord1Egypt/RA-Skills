# Pipeline Architecture

## Signal Flow

```
[Real Mic]
    │  (44.1kHz stereo, raw)
    ▼
[ffmpeg process]          ← spawned as child_process, stdout = PCM stream
    │  (16kHz mono PCM)
    ▼
[Deepgram WebSocket]      ← wss://api.deepgram.com/v1/listen
    │  (text transcript)
    ▼
[LLM stream]              ← Groq / OpenAI / local (streaming mode)
    │  (token stream)
    ▼
[Sentence chunker]        ← custom buffer, flushes on . ? ! or 30 words
    │  (full sentence strings)
    ▼
[TTS WebSocket]           ← ElevenLabs / Cartesia streaming endpoint
    │  (MP3 audio chunks)
    ▼
[PCM decoder]             ← ffmpeg spawned per chunk, stdin=MP3, stdout=PCM
    │  (raw PCM)
    ▼
[VB-Cable write]          ← ffmpeg -f s16le piped to virtual audio device
    │
    ▼
[Google Meet / Zoom]      ← reads from VB-Cable output as microphone
```

## Layer Color Code

- **Audio infra** (teal): ffmpeg processes, VB-Cable write
- **AI services** (purple): Deepgram, LLM, TTS
- **Custom logic** (amber): Sentence chunker — the one piece you write from scratch

## Audio Format Contract

Every layer boundary has a strict format:

| Boundary | Format | Why |
|---|---|---|
| Mic → ffmpeg | OS default (44.1kHz stereo) | Whatever the OS provides |
| ffmpeg → Deepgram | 16kHz, 16-bit, mono, PCM | Deepgram requirement |
| LLM → chunker | UTF-8 text tokens | Standard streaming format |
| Chunker → TTS | UTF-8 string (15–30 words) | TTS minimum viable input |
| TTS → decoder | MP3 binary stream | ElevenLabs/Cartesia default |
| Decoder → VB-Cable | 44.1kHz, 16-bit, stereo, PCM | VB-Cable default input format |

## WebSocket Reconnection Strategy

Both Deepgram and TTS sockets must implement:
1. `close` event → wait 1s → reconnect
2. `error` event → log + reconnect
3. Max 5 reconnect attempts before emitting `pipeline:error` to host app

## Kill Switch Contract

The skill exports a `stop()` function. When called:
1. Destroy the TTS audio buffer immediately (silence starts now)
2. Abort the active LLM fetch request
3. Close Deepgram socket gracefully
4. Kill ffmpeg child processes

Host app wires `stop()` to whatever trigger it uses (hotkey, IPC message, API call).