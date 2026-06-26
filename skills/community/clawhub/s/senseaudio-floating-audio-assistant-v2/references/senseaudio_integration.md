# SenseAudio Integration

This skill is a thin product wrapper over the realtime interpreter toolchain. The skill directory also includes `scripts/senseaudio_api_smoke.py` for quick local diagnostics.

Diagnostic commands:

```bash
python3 "{baseDir}/scripts/senseaudio_api_smoke.py"
python3 "{baseDir}/scripts/senseaudio_api_smoke.py" --live-tts
```

The smoke script reports the API surfaces used by the project:

- ASR WebSocket: `wss://api.senseaudio.cn/ws/v1/audio/transcriptions`
- TTS HTTP/SSE: `https://api.senseaudio.cn/v1/t2a_v2`
- Music generation: `https://api.senseaudio.cn/v1/music/song/create`

Runtime capabilities:

- Realtime ASR and optional translation are handled by the long-lived websocket runner.
- Copied-text reading uses SenseAudio TTS.
- Music workshop uses SenseAudio music generation and stores generated track metadata.
- Recent-project organization uses `audioclaw agent` with the selected template and the saved SenseAudio ASR text.

Runtime configuration inputs:

- SenseAudio credential: provided by the AudioClaw runtime environment; no credential file or key value is bundled in this upload package.
- ASR UI: fast local ASR source language and SenseAudio translation target language.
- TTS UI: copied text and selected voice.
- Music UI: prompt, style controls, generation history, track rename, play/pause.
- Organization UI: selected built-in or imported template plus the saved project transcript.

Safety:

- The smoke script reports whether an API key exists, but never prints the key.
- `--live-tts` is optional because it consumes API quota.
