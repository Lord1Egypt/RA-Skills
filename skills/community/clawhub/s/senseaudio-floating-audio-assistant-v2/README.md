# SenseAudio Floating Audio Assistant

SenseAudio Floating Audio Assistant is an AudioClaw skill for desktop audio understanding. It combines SenseAudio ASR, translation, TTS, and music generation with AudioClaw agent organization so users can capture system audio, view floating subtitles, preserve recent transcripts, and turn captured speech into structured notes.

## What It Provides

- System-audio subtitle overlay for videos, meetings, classes, and courseware.
- Fast local captions plus SenseAudio final ASR and optional translation.
- Recent-project transcript management with AudioClaw agent organization templates.
- Copied-text reading through SenseAudio TTS.
- Music workshop presets for SenseAudio music generation.
- Health-check scripts for launchers, references, presets, and SenseAudio API surface discovery.
- Bundled text-source runtime for the native floating UI, audio capture runner, SenseAudio helpers, and optional web overlay UI.

## Runtime Requirements

- macOS desktop environment for the native floating window.
- BlackHole 2ch and a Multi-Output Device that includes the real speaker or headphones.
- Xcode Command Line Tools for Swift compilation.
- Python 3 and Bash for wrapper scripts and diagnostics.
- SwitchAudioSource from switchaudio-osx for audio route switching.
- AudioClaw agent for transcript organization.
- SenseAudio credentials supplied by the host AudioClaw runtime.

## Main Commands

```bash
bash "{baseDir}/scripts/start-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/status-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"
```

Run a local health check:

```bash
bash "{baseDir}/scripts/doctor-senseaudio-floating-audio-assistant.sh"
```

Inspect SenseAudio API wiring without making a live request:

```bash
python3 "{baseDir}/scripts/senseaudio_api_smoke.py"
```

## Notes

This upload package intentionally does not include local credentials, local machine paths, credential files, or environment-variable assignment examples. Configure credentials through the host AudioClaw runtime before launching SenseAudio-backed features.

The package includes source files only. Local virtual environments, compiled binaries, downloaded ASR model archives, and machine-specific state are intentionally excluded.
