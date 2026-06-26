# xeon-smartupscale

Smart hybrid video upscaler for Intel Xeon CPUs: **lanczos pre-scale + ETDS 2x AI super-resolution**.

ETDS only supports a strict 2x scale factor. This skill bridges the gap so you can target *any* resolution (1080p, 1440p, 4K…) regardless of input size, by:

1. ffmpeg `lanczos` → `(target_w/2, target_h/2)`
2. ETDS x2 (OpenVINO CPU, AMX-BF16) → `(target_w, target_h)`

## Install
```bash
bash install.sh
```

## Usage
```bash
./smartupscale.sh input.mp4 -t 1080p
./smartupscale.sh input.mp4 -t 4k -o out_4k.mp4
./smartupscale.sh input.mp4 -t 1920x1080
```
Targets: `480p`, `540p`, `720p`, `1080p`, `1440p`, `2160p`, `4k`, or explicit `WxH`.

## Notes
- Linux x86_64 only.
- Best on Intel CPUs with AMX-BF16 (Sapphire Rapids / Granite Rapids).
- Output: H.264 CRF 18, original audio merged.
- Model `ETDS_M7C48_x2` is vendored (~380KB).
