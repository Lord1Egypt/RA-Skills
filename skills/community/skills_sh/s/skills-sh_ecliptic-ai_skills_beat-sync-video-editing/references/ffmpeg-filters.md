# FFmpeg Filter Reference for Beat-Sync Editing

## filter_complex Overview

FFmpeg's `-filter_complex` flag allows building complex filter graphs that process multiple streams. In beat-sync editing, the filter graph trims video segments, concatenates them in order, and trims the audio track.

## Video Filters

### trim

Extract a time segment from a video stream:

```
[0:v]trim=start=10.000:duration=5.000,setpts=PTS-STARTPTS[v0]
```

- `start` — Start time in seconds (3 decimal places)
- `duration` — Length of segment in seconds
- `setpts=PTS-STARTPTS` — **Required.** Resets presentation timestamps so the segment starts at 0. Without this, there will be frozen frames at the beginning.

### concat

Join multiple video segments sequentially:

```
[v0][v1][v2]concat=n=3:v=1:a=0[outv]
```

- `n=3` — Number of input segments
- `v=1` — One video output stream
- `a=0` — No audio output (audio handled separately)
- Input labels must match the output labels from trim filters
- **Order matters** — segments play in the order listed

### Common Video Issues

**Black frames between clips**: Usually caused by missing `setpts=PTS-STARTPTS` after trim.

**Resolution mismatch**: If source video changes resolution (e.g., mixed content), add `scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2` before concat.

**Frame rate issues**: For consistent output, add `fps=30` after trim if source has variable frame rate.

## Audio Filters

### atrim

Extract a time segment from an audio stream:

```
[1:a]atrim=start=13.000:duration=30.000,asetpts=PTS-STARTPTS[outa]
```

- `start` — Start position in audio file (seconds)
- `duration` — Length to extract
- `asetpts=PTS-STARTPTS` — Reset audio timestamps

### Audio Fade (optional)

Add fade in/out to avoid abrupt starts/ends:

```
[1:a]atrim=start=13.000:duration=30.000,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.5,afade=t=out:st=29.5:d=0.5[outa]
```

## Complete Filter Pattern

### Single clip

```
[0:v]trim=start=10.000:duration=30.000,setpts=PTS-STARTPTS[outv];
[1:a]atrim=start=0.000:duration=30.000,asetpts=PTS-STARTPTS[outa]
```

### Multiple clips (typical)

```
[0:v]trim=start=8.000:duration=2.000,setpts=PTS-STARTPTS[v0];
[0:v]trim=start=45.000:duration=1.500,setpts=PTS-STARTPTS[v1];
[0:v]trim=start=22.000:duration=3.000,setpts=PTS-STARTPTS[v2];
[v0][v1][v2]concat=n=3:v=1:a=0[outv];
[1:a]atrim=start=13.000:duration=6.500,asetpts=PTS-STARTPTS[outa]
```

### Rapid cuts (12+ clips)

Same pattern scales to any number of clips. The build-filter.ts script handles labeling (`[v0]`, `[v1]`, ..., `[v11]`) automatically.

## FFmpeg Command Template

```bash
ffmpeg -y \
  -i "<video_path>" \
  -i "<audio_path>" \
  -filter_complex "<fullFilter>" \
  -map "[outv]" \
  -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac \
  -shortest \
  "<output_path>"
```

### Flag Reference

| Flag | Purpose |
|------|---------|
| `-y` | Overwrite output without asking |
| `-i` | Input file (first = video, second = audio) |
| `-filter_complex` | The filter graph string |
| `-map "[outv]"` | Use the labeled video output |
| `-map "[outa]"` | Use the labeled audio output |
| `-c:v libx264` | H.264 video codec |
| `-preset fast` | Encoding speed (ultrafast/fast/medium/slow) |
| `-crf 23` | Quality (0=lossless, 23=default, 51=worst) |
| `-c:a aac` | AAC audio codec |
| `-shortest` | End when shortest stream ends |

### Quality Presets

| Use Case | Preset | CRF | Notes |
|----------|--------|-----|-------|
| Preview/draft | ultrafast | 28 | Fast render, larger file |
| Standard | fast | 23 | Good balance |
| High quality | medium | 18 | Slower, better quality |
| Archive | slow | 15 | Best quality, slow render |

## Escaping in Shell

The filter string contains characters that need careful handling in shell commands:

- Semicolons (`;`) — Separate filter chains. Must be inside quotes.
- Square brackets (`[]`) — Label streams. Safe inside quotes.
- Equals (`=`) — Set parameters. Safe inside quotes.

Always wrap the entire filter_complex value in double quotes when passing to FFmpeg via shell.
