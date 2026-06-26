---
name: raw-video-processing
description: Post-process raw screen recordings by removing silent segments and applying speed adjustments. Uses FFmpeg-based Python scripts to optimize video pacing automatically.
---

# Skill: Raw Video Processing

Post-process raw screen recordings to improve pacing — remove silent segments, then speed up the result.

> **Prerequisite**: FFmpeg and uv must be installed.

---

## When to Use

The user has recorded a screencast and wants to clean it up before publishing. Typical issues in raw recordings:
- Long pauses / dead air while thinking or waiting for loading
- Keyboard typing sounds and other low-level background noise that should be treated as silence
- Overall pacing feels slow and could benefit from a slight speed boost

---

## Default Workflow

When the user provides a raw video file, **run both scripts in sequence** by default:

### Step 1: Remove Silent Segments

```bash
uv run --python 3.12 /path/to/skills/raw-video-processing/scripts/remove_silence.py <input.mp4> -t="-20dB" -d 0.5
```

This detects and cuts out silent portions (including keyboard sounds), producing `<input>_nosilence.mp4`.

**Always pass these parameters** (tuned for screen recordings with keyboard noise):
- `-t="-20dB"` — aggressive threshold that filters out keyboard typing and background noise (use `=` syntax to avoid argparse treating negative values as flags)
- `-d 0.5` — remove short silences too (0.5s minimum)
- `-p 0.2` — seconds of breathing room kept around speech boundaries (default, usually no need to pass)

The script prints a detailed summary: number of silent segments found, total silence removed, and all kept segments with timestamps. Review this output to confirm the result looks reasonable.

### Step 2: Speed Up the Video

```bash
uv run --python 3.12 /path/to/skills/raw-video-processing/scripts/speed_video.py <input>_nosilence.mp4
```

This applies a speed multiplier to the silence-removed video, producing `<input>_nosilence_1.2x.mp4`.

**Default parameters**:
- `--speed 1.2` — 1.2x playback speed (a subtle boost that doesn't feel rushed)

---

## Script Options

### remove_silence.py

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `<input>_nosilence.mp4` | Custom output path |
| `-t`, `--threshold` | `-30dB` | Silence threshold in dB (higher = more aggressive). **Always use `-20dB` for screencasts** — pass as `-t="-20dB"` to avoid argparse issues with negative values |
| `-d`, `--duration` | `0.8` | Minimum silence duration in seconds to remove. **Use `0.5` for screencasts** |
| `-p`, `--padding` | `0.2` | Padding kept around non-silent segments |
| `--dry-run` | off | Only print detected segments, don't export |

### speed_video.py

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `<input>_<speed>x.mp4` | Custom output path |
| `-s`, `--speed` | `1.2` | Playback speed multiplier |

---

## Custom Scenarios

- **Only remove silence** — run just Step 1.
- **Only speed up** — run just Step 2 directly on the input file.
- **Conservative cleanup** — use `-t="-30dB" -d 0.8` if the default is cutting too much speech.
- **Extra aggressive cleanup** — use `-t="-15dB" -d 0.3` and `--speed 1.5` for maximum compression.
- **Preview before committing** — use `--dry-run` on remove_silence.py to see what would be cut without creating a file.
- **Custom output name** — use `-o` on either script to control the output path.

---

## Important Notes

- Always run remove_silence **before** speed_video. Silence detection works on the original audio; speeding up first would alter the audio characteristics and make silence detection less accurate.
- For long videos (>30 min), the silence removal step may take a few minutes as it processes each segment individually.
- Both scripts preserve video quality — remove_silence uses stream copy (no re-encoding), while speed_video re-encodes with FFmpeg defaults.
