# WeChat Voice Notes

## Purpose

This skill handles WeChat voice attachments, especially raw SILK voice files without extensions.

## Known-good local approach

- Detect SILK via file header `#!SILK_V3`
- Decode with Python package `silk-python`
- Wrap decoded PCM into WAV
- Transcribe with Python `faster-whisper`

## Why not openai-whisper CLI here

A direct `python3 -m pip install --user openai-whisper` attempt in this environment started pulling a very large PyTorch/CUDA dependency chain, so `faster-whisper` is the preferred local path.

## Current dependency assumptions

- Python 3 available
- ffmpeg available
- `silk-python` installed via pip user install
- `faster-whisper` installed via pip user install

## Maintenance

If SILK decode fails, verify that `silk-python` is installed and that the input really is `#!SILK_V3` WeChat audio.
If local transcription quality is poor, try changing the model from `base` to `small`, or add a preprocessing step before transcription.
