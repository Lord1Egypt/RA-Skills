# Quickstart

Use this skill when the user wants the SenseAudio floating audio assistant, system-audio ASR, bilingual captions, copied-text TTS, recent projects, or music workshop.

Primary commands:

```bash
bash "{baseDir}/scripts/start-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/status-senseaudio-floating-audio-assistant.sh"
bash "{baseDir}/scripts/doctor-senseaudio-floating-audio-assistant.sh"
```

Required setup:

- Provide a SenseAudio API key through the AudioClaw runtime environment before launching.
- Install `BlackHole 2ch`, then create a Multi-Output Device that includes the physical output device and `BlackHole 2ch`.
- Name the route `Multi-Output Device` or `多输出设备`; the launcher searches those names before starting capture.
- Make sure `SwitchAudioSource`, `swiftc`, `python3`, and `bash` are available.
- Keep `audioclaw agent` configured for recent-project organization; do not fake organization output if the agent is unavailable.

Expected runtime flow:

1. The start script resolves the workspace relative to the skill directory.
2. It launches the existing realtime interpreter toolchain.
3. The toolchain switches macOS output to a Multi-Output Device containing BlackHole 2ch.
4. The native overlay captures system audio, streams ASR to SenseAudio, and writes project runs under workspace state.
5. The stop script restores the previous macOS audio route and volume.
