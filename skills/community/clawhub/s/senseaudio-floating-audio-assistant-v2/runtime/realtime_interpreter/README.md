# Realtime Interpreter Prototype

## What This Prototype Does

This is a macOS real-time subtitle worker prototype built around SenseAudio WebSocket ASR, with an optional local `sherpa-onnx` fast-caption layer.

Current capabilities:

- stream live microphone PCM using a native Swift helper
- capture loopback PCM from `BlackHole 2ch`
- stream WAV or PCM test files into SenseAudio real-time ASR
- generate low-latency local partial captions with `sherpa-onnx`
- emit original-language subtitle segments
- keep translated stream optional and disabled by default in the system-audio profile
- automatically fall back to original-only subtitles if the translated stream cannot start
- persist recognized segments into a log file
- tune realtime VAD thresholds for mic vs system-audio input

## Important Current Limitation

With the current API key used in this workspace, a second concurrent real-time session can be rejected by the service with:

- `[400025] 并发配额不足，请升级套餐或等待配额刷新`

Because of that, the system-audio profile in this workspace now defaults to original-only subtitles unless the quota is increased.

## Files

- `runner.py`: main prototype runner
- `scripts/sherpa_onnx_stream_probe.py`: local file-based streaming probe for `sherpa-onnx`
- `scripts/sherpa_onnx_live_probe.py`: local live system-audio probe for `sherpa-onnx`
- `mic_pcm_stream.swift`: native PCM capture helper for microphone or BlackHole
- `config.example.json`: system-audio runtime config template
- `config.mic.example.json`: microphone runtime config template
- `requirements.txt`: Python dependencies
- `start_mic_bilingual_subtitles.sh`: local bootstrap script
- `start_system_bilingual_subtitles.sh`: system-audio bootstrap script
- `subtitle_overlay.swift`: native macOS floating subtitle window
- `start_system_subtitle_overlay.sh`: one-click launcher for the floating subtitle window
- `start_system_bilingual_overlay.sh`: bilingual launcher for the floating subtitle window
- `enter_subtitle_mode.sh`: switch macOS audio into subtitle capture mode
- `exit_subtitle_mode.sh`: restore the previous macOS audio output and volume
- `stop_system_subtitle_overlay.sh`: stop the overlay and restore the previous macOS audio output
- `validate_system_audio_loopback.sh`: end-to-end BlackHole routing self-test

## Quick Start

From the workspace root:

```bash
bash workspace/tools/realtime_interpreter/start_mic_bilingual_subtitles.sh
```

This will:

- create a local virtual environment on first run
- install `websockets`
- compile the Swift microphone helper when needed
- start the live microphone subtitle worker

## System Audio Mode

To capture app, browser, or video playback audio on macOS:

1. Install `BlackHole 2ch`
2. In Audio MIDI Setup, create a `Multi-Output Device`
3. Add your headphones or speakers and `BlackHole 2ch`
4. Set that Multi-Output Device as the macOS output device
5. Run the loopback validator:

```bash
bash workspace/tools/realtime_interpreter/validate_system_audio_loopback.sh
```

6. Start the realtime worker:

```bash
bash workspace/tools/realtime_interpreter/start_system_bilingual_subtitles.sh
```

If the validation script reports silence, macOS output is not yet routed through `BlackHole 2ch`.

## Floating Subtitle Window

Launch the native macOS overlay:

```bash
bash workspace/tools/realtime_interpreter/start_system_subtitle_overlay.sh
```

When this starts, it will automatically:

- remember the current macOS output and system output devices
- remember the current output volume when available
- switch both output routes to the existing `多输出设备` or `Multi-Output Device`
- launch the floating subtitle window

Stop the overlay and restore the previous audio state:

```bash
bash workspace/tools/realtime_interpreter/stop_system_subtitle_overlay.sh
```

Launch the bilingual overlay variant:

```bash
bash workspace/tools/realtime_interpreter/start_system_bilingual_overlay.sh
```

What it does:

- opens a borderless always-on-top subtitle window
- auto-starts the system-audio ASR worker
- automatically switches macOS into subtitle capture mode on launch
- restores the previous audio route and output volume on exit
- shows original subtitles immediately
- uses local fast captions in the first line when available
- uses SenseAudio final text as the second-line final pass in original-only mode
- runs in single-stream original-subtitle mode by default
- keeps the second line reserved for future translation or status text
- ignores stale older-segment updates to reduce flicker
- remembers the last window position

## Test With A WAV File

The runner accepts an existing `16kHz mono 16-bit PCM WAV` input:

```bash
bash workspace/tools/realtime_interpreter/start_mic_bilingual_subtitles.sh \
  --input-wav-file /absolute/path/to/test.wav \
  --debug
```

Disable translated stream:

```bash
bash workspace/tools/realtime_interpreter/start_mic_bilingual_subtitles.sh \
  --input-wav-file /absolute/path/to/test.wav \
  --no-translation \
  --debug
```

## Environment

The runner reads:

- `AUDIOCLAW_ASR_API_KEY`
- `SENSEAUDIO_API_KEY`

by default from:

- `workspace/.env`

## Current Recommended Use

For this workspace and key, the most reliable mode right now is:

- mic, file input, or BlackHole system-audio input
- original subtitle stream enabled
- translated stream disabled by default

That gives us a stable base to keep building toward the menu bar system-audio version.
