# System Audio Setup For BlackHole

## Important Note

BlackHole usually requires a macOS reboot before the new device appears in the audio device list.

## After Installation

Run:

```bash
bash check_system_audio_setup.sh
```

If `BlackHole 2ch` appears, do this in `Audio MIDI Setup`:

1. Create a `Multi-Output Device`
2. Add:
   - your headphones or preferred output
   - `BlackHole 2ch`
3. Set that Multi-Output Device as the macOS system output

This makes macOS do two things at once:

- play sound through your headphones
- mirror the same sound into BlackHole so the interpreter can capture it

## Interpreter Config

For system-audio mode, the current config template is:

`config.example.json`

Key capture settings:

```json
{
  "capture": {
    "source": "system",
    "input_device_name": "BlackHole 2ch"
  }
}
```

## Current Status

Right now the prototype has:

- working real-time ASR over SenseAudio WebSocket
- native macOS microphone PCM streaming
- file-input test path
- graceful fallback when translated parallel stream exceeds concurrency quota

What remains for true system-audio mode is:

- successful BlackHole installation
- reboot
- device detection
- input-device selection in the capture worker
