---
name: voice-huayan
description: Local Chinese TTS playback on Windows using Piper zh_CN-huayan-medium with automatic fallback to System.Speech. Use when user asks to read replies aloud locally (direct speaker playback) and wants huayan voice style.
---

# Voice Huayan

Run local Chinese speech playback with huayan voice.

## Run

```powershell
{baseDir}/bin/voice-huayan.ps1 "要播报的文本"
```

## Behavior

- Prefer Piper `zh_CN-huayan-medium`
- Auto fallback to `Microsoft Huihui Desktop` if Piper/model/runtime is unavailable
- Output `PLAYBACK_OK (...)` when playback succeeds
