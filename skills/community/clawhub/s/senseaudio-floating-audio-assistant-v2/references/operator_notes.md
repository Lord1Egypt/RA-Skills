# Operator Notes

This skill opens and manages the AudioClaw SenseAudio floating audio assistant on macOS. It captures system output audio through BlackHole, displays fast local ASR plus SenseAudio ASR/translation, and keeps recent projects for AudioClaw agent organization.

The upload package bundles the runtime source files under `runtime/realtime_interpreter/`, including the native Swift overlay UI, the Python runner, SenseAudio helpers, and the optional web overlay UI. It intentionally excludes local virtual environments, compiled binaries, downloaded model archives, and machine-specific state.

## Requirements

- macOS desktop with Xcode Command Line Tools (`swiftc`).
- `python3`, `bash`, and `SwitchAudioSource` from `switchaudio-osx`.
- `BlackHole 2ch`.
- A Multi-Output Device named `Multi-Output Device` or `多输出设备`, containing both the real speaker/headphones and `BlackHole 2ch`.
- AudioClaw runtime with `audioclaw agent` available for organizing recent-project transcripts.
- SenseAudio API key supplied by the AudioClaw runtime environment.

## Configure

Install system audio dependencies, create the Multi-Output Device, and provide the SenseAudio credential through AudioClaw's normal runtime configuration. This upload package intentionally does not include credential files, key values, or environment-variable samples.

Open Audio MIDI Setup when the device route needs to be created or repaired:

```bash
bash "{baseDir}/scripts/open_audio_midi_setup.sh"
```

## Use

```bash
bash "{baseDir}/scripts/start-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/status-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"
```

Run diagnostics without consuming SenseAudio quota:

```bash
bash "{baseDir}/scripts/doctor-senseaudio-floating-audio-assistant.sh"
python3 "{baseDir}/scripts/senseaudio_api_smoke.py"
```

Use `--live-tts` only when a small real SenseAudio TTS call is acceptable.
