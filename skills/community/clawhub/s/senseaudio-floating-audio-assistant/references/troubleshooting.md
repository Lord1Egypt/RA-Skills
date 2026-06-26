# Troubleshooting

If the overlay does not start:

- Run `bash "{baseDir}/scripts/check-senseaudio-floating-audio-assistant-setup.sh"`.
- Confirm `swiftc`, `python3`, and a SenseAudio key are available.
- Confirm `SwitchAudioSource` is available if using system-audio capture.

If there is no subtitle output:

- Confirm macOS output is a Multi-Output Device containing BlackHole 2ch.
- Play real system audio after starting ASR.
- If local fast captions appear but SenseAudio does not, check realtime quota and API key validity.

If computer audio changes after use:

- Run `bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"`.
- The stop script restores the previous output device and volume from workspace state.

If AudioClaw organization waits forever:

- Realtime ASR/TTS/music may still work.
- Organization depends on the configured `audioclaw agent` text model returning a real result.

If the device chain is not configured:

- Open Audio MIDI Setup with `bash "{baseDir}/scripts/open_audio_midi_setup.sh"`.
- Create a Multi-Output Device.
- Select both the real output device and `BlackHole 2ch`.
- Re-run the check script before starting ASR again.
