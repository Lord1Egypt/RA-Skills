---
name: xeon-smartupscale_v2
description: Generic Xeon-CPU video upscaler. Plans lanczos pre-scale + N Real-ESRGAN general-x4v3 x4 passes to reach any target resolution, with super-resolution always the last step and a 270-line pre-scale floor.
metadata:
  openclaw:
    requires:
      bins: [bash, python3, curl, tar, unzip]
---

## Goal

Upscale a video to any target resolution with two hard rules:

1. The lanczos pre-scale height is never below **270**.
2. Real-ESRGAN super-resolution is always the **last** step.

## Planning rule

Given source `(src_w, src_h)` and target `(t_w, t_h)`:

- `r = t_h / src_h`
- If `r < 2`: pure lanczos to target.
- Else: pick `n >= 1` so `pre_h = t_h / 4^n >= 270`, choose `pre_h`
  closest to `src_h`. Then do one lanczos to `pre_w x pre_h`, followed
  by `n` consecutive x4 passes.

## Usage

```bash
bash <skill_dir>/install.sh
bash <skill_dir>/smartupscale.sh <input.mp4> -t 1080p
bash <skill_dir>/smartupscale.sh <input.mp4> -t 2160p
bash <skill_dir>/smartupscale.sh <input.mp4> -t 1920x1080 -o <out.mp4>
```

Targets: `480p`, `540p`, `720p`, `1080p`, `1440p`, `2160p`/`4k`, `4320p`/`8k`, or explicit `WxH`.

## Output

- H.264 `medium` / `crf 15`, audio copied from source through every pass.
- Final size may differ by a few pixels from the requested target when
  `t_h / 4^n` is not an integer; `smartupscale.sh` reports the actual size.
