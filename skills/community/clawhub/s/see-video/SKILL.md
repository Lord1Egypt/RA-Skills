---
name: see-video
description: "Use when the user sends a video file or asks about video content. Extracts frames and injects them as an image grid directly into the LLM context — no proxy model, no description handoff. uniform mode (default): evenly spaced sampling. highlight mode: scene-change biased sampling. ⚠️ Requires a vision-capable (multimodal) model."
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": { "bins": ["ffmpeg", "node"] },
      "install": [
        {
          "id": "brew",
          "kind": "brew",
          "formula": "ffmpeg",
          "bins": ["ffmpeg"],
          "label": "Install ffmpeg (brew)",
        },
        {
          "id": "apt",
          "kind": "apt",
          "package": "ffmpeg",
          "bins": ["ffmpeg"],
          "label": "Install ffmpeg (apt)",
        },
      ],
    },
  }
---

# see-video

Extract frames from a video and inject them as a grid image + XML timestamps into LLM context.

## Setup (first time only)

```bash
cd <skill directory>
npm install
```

## Usage

```bash
node {baseDir}/scripts/inject.mjs <video_path> [--mode uniform|highlight] [--start N] [--end N]
```

On success, outputs JSON to stdout:

```json
{
  "gridPath": "/tmp/video_llm-frames.jpg",
  "description": "<video_frames>...</video_frames>",
  "duration": 1326,
  "frameCount": 28,
  "layout": { "cols": 4, "rows": 7, "cellW": 384, "cellH": 216 },
  "videoWidth": 854,
  "videoHeight": 480,
  "inputSizeMb": 42.3
}
```

If the video exceeds 10 minutes and uniform mode was used without `--start/--end`, a `hint` field is included:

```json
{
  "hint": "Video is 30 minutes long. This is a uniform overview. For better scene coverage re-run with --mode highlight, or use --start/--end to zoom into a specific section."
}
```

**Recommended workflow for long videos:**
1. First run with `--mode highlight` — shows key scene changes across the whole video
2. If the user wants detail on a specific section, re-run with `--start N --end N`

On error, writes `ERROR: <message>` + `Hint: <diagnosis>` to stderr and exits 1.

## Injection procedure

**Step 1 — Run the script (bash tool):**

```bash
node {baseDir}/scripts/inject.mjs "/path/to/video.mp4"
```

**Step 2 — Parse JSON:**
Extract `gridPath` and `description`.

**Step 3 — Inject image (read tool):**

```
read <gridPath>
```

The `read` tool injects the jpg as a native multimodal image block into context.
After viewing the grid, use the `description` XML timestamps to reference frames:

> "Look at the grid image above. Use the timestamps in the description XML to analyze the video. The number in the top-left of each cell is the frame index."

**On error:**
- Translate the `Hint:` message into natural language for the user. Do not paste raw error output.
- If `read <gridPath>` fails — `/tmp/` files are ephemeral. Re-run the script and read immediately.

## Options

| Option | Default | Description |
|---|---|---|
| `--mode uniform` | ✅ | Evenly spaced frames |
| `--mode highlight` | | Scene-change biased sampling |
| `--start N` | `0` | Segment start (seconds) |
| `--end N` | end of video | Segment end (seconds) |

## Diagnostics

| Error | Cause | Action |
|---|---|---|
| `Input file not found` | File missing or dropped by channel media size limit | Ask the user to share the file path directly as text |
| `corrupt, incomplete, or unsupported format` | Damaged file, interrupted transfer, or unsupported codec | Try a different file, or use `--start`/`--end` to skip problematic sections |
| `moov atom not found` | Incomplete mp4 (streaming not finished) | Retry with a complete file |
| `ffmpeg not found` | ffmpeg not installed | Check ffmpeg installation |

## Notes

- Frame count and cell size are determined automatically from video duration and aspect ratio
- Grid is ~1500×1500px, cell long side 384–512px
- Timestamps are in the `description` XML only, not overlaid on the image
- Portrait and landscape videos both supported
- **Telegram users:** if a video file is not attached to the message, check `channels.telegram.mediaMaxMb` in the OpenClaw config — the file may have been dropped at the channel level before reaching the agent
