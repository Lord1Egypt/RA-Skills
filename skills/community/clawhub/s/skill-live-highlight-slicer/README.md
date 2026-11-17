# byted-sol-live-highlight-slicer

OpenClaw skill for extracting highlight clips from a local livestream recording.

## What It Does

- Supports `.webm`, `.mp4`, and `.mov` recordings.
- Detects candidate highlights with audio energy, scene changes, hybrid overlap, audio/scene union, or ASR keyword density.
- Exports independent `.mp4` clips.
- Writes `segments.json` with timing and analysis metadata.
- Optionally creates `merged_highlights.mp4`.

## Requirements

- Python 3.9 or newer.
- `ffmpeg` and `ffprobe` available on `PATH`.
- Python packages:

```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

```bash
python3 scripts/highlight_slicer.py \
  --input "/absolute/path/live-recording.mp4" \
  --method hybrid \
  --output-dir "./highlights" \
  --merge true
```

## Arguments

| Argument | Required | Default | Description |
| --- | --- | --- | --- |
| `--input` | Yes | None | Absolute path to the source recording. |
| `--method` | No | `hybrid` | `audio`, `scene`, `hybrid`, `combined`, or `asr`. |
| `--threshold` | No | `1.5` | Audio energy threshold multiplier. |
| `--scene-threshold` | No | `0.1` | Scene-change threshold. |
| `--min-clip-duration` | No | `5` | Minimum clip duration in seconds. |
| `--padding` | No | `2` | Seconds added before and after detected segments. |
| `--output-dir` | No | `./highlights` | Output directory. |
| `--merge` | No | `true` | Whether to create a merged highlight video. |
| `--asr-file` | For `asr` | None | Existing ASR transcript JSON or JSONL file. |
| `--asr-window` | No | `8` | ASR scoring window size in seconds. |
| `--top-n` | No | `8` | Maximum ASR windows to keep. |

## Safety Notes

This skill processes local media and writes derived files to the requested output directory. It does not upload files or contact external services.

