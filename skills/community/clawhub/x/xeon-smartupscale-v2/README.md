# xeon-smartupscale_v2

Generic Xeon-CPU video upscaler. Combines `lanczos` pre-scale with
**Real-ESRGAN general-x4v3** 4x super-resolution (OpenVINO CPU, BF16 hint).

## Pipeline

The script `smartupscale.sh` plans the path automatically:

1. Compute `r = target_h / src_h`.
2. If `r < 2`: pure `lanczos` to target.
3. Else: pick `n >= 1` such that `pre_h = target_h / 4^n >= 270` and
   `pre_h` is closest to `src_h`. Then do **one** in-memory `lanczos`
   to `pre_w x pre_h`, followed by **n** consecutive Real-ESRGAN x4 passes.

Hard rules:

- Pre-scale height never goes below **270** (avoids destroying detail).
- Super-resolution is always the **last** step; no lanczos after SR.

## Examples

| Input | Target | Plan |
|---|---|---|
| 854x480  | 1280x720  | lanczos only |
| 854x480  | 1920x1080 | lanczos -> 480x270, then x4 |
| 854x480  | 3840x2160 | lanczos -> 960x540, then x4 |
| 854x480  | 7680x4320 | lanczos -> 480x270, then x4 x4 |
| 1280x720 | 1920x1080 | lanczos only |
| 1280x720 | 3840x2160 | lanczos -> 960x540, then x4 |
| 1920x1080| 2560x1440 | lanczos only |
| 1920x1080| 7680x4320 | (no lanczos) x4 |

## Install

```bash
bash install.sh
```

## Usage

```bash
./smartupscale.sh input.mp4 -t 1080p
./smartupscale.sh input.mp4 -t 2160p -o out_4k.mp4
./smartupscale.sh input.mp4 -t 7680x4320
```

Targets: `480p`, `540p`, `720p`, `1080p`, `1440p`, `2160p`/`4k`, `4320p`/`8k`, or explicit `WxH`.

## Notes

- Linux x86_64. Best on Intel CPUs with AMX-BF16.
- One static OpenVINO IR file is vendored; the runtime reshapes it to the
  needed input size for each pass (handled by `sr_video_ov.py`).
- Audio is copied through every pass with `-c:a copy`.
- Final encode: H.264 `medium` / `crf 15`.
