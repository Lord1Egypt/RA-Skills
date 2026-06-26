# VoiceTrust Runtime

Self-contained runtime for the `Skill-VoiceTrust` bundle.

## Included
- runtime source under `src/`
- runtime config under `configs/`
- owner profile storage under `data/owners/`
- local model asset directory under `assets/models/` (populated on demand by `../scripts/ensure_models.py`)

## Runtime note
VoiceTrust no longer depends on `torchcodec` for its core audio-loading path.
The runtime now uses a more resilient loader:
- prefer `soundfile` for direct decode
- fall back to local `ffmpeg` for formats that need conversion
- normalize to mono 16 kHz before inference

This reduces breakage from `torchaudio` backend changes after environment rebuilds.

## First-time setup
Before setup, prepare **3 to 5** audio samples from the intended owner.
All samples should be from the same person and should use clean, natural speech.

From this `runtime/` directory:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
uv run --python .venv/bin/python ../scripts/ensure_models.py
uv run --python .venv/bin/python ../scripts/demo.py --list-speakers
```

## System dependency
For the ffmpeg fallback path, ensure a local `ffmpeg` binary is available.
VoiceTrust resolves ffmpeg via `FFMPEG_BIN`, then `PATH`, then `/opt/homebrew/bin/ffmpeg` as a macOS fallback.
On macOS/Homebrew this is typically:

```bash
brew install ffmpeg
```

## Enroll owner samples
```bash
uv run --python .venv/bin/python ../scripts/demo.py \
  --audio /path/to/owner_sample_01.wav \
  --speaker owner \
  --enroll-sample \
  --json
```

## Normal verification
```bash
uv run --python .venv/bin/python ../scripts/demo.py \
  --audio /path/to/incoming_audio.ogg \
  --speaker owner \
  --json
```
