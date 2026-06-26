---
name: sam-segmentation
description: Use SAM (Segment Anything Model) to remove image backgrounds and extract foreground subjects as transparent PNGs. Use when users want to remove backgrounds, cut out objects, extract foreground subjects, or perform image segmentation.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: pillow
      - kind: uv
        package: numpy
      - kind: uv
        package: torch
      - kind: uv
        package: torchvision
---

# SAM Background Removal

Extract foreground subjects from images using Meta's Segment Anything Model, outputting transparent PNGs.

## Quick Start

```bash
python3 scripts/segment.py <input_image> <output.png>
```

Defaults to the image center as the foreground hint — works well for portraits and product shots where the subject is centered.

## Parameters

| Param | Description | Default |
|---|---|---|
| `input` | Input image path | required |
| `output` | Output PNG path (single mode) or directory (`--all` mode) | required |
| `--model` | Model size: `vit_b` (fast) · `vit_l` (medium) · `vit_h` (best quality) | `vit_h` |
| `--checkpoint` | Local checkpoint path; auto-downloaded if omitted | auto |
| `--points` | Foreground hint points as `x,y`, multiple allowed | center |
| `--all` | Grid-sweep mode: extract all distinct elements | off |
| `--grid` | Grid density for `--all`; 16 means 16×16=256 probe points | `16` |
| `--iou-thresh` | Minimum predicted IoU to accept a mask (`--all`) | `0.88` |
| `--min-area` | Minimum mask area as fraction of image (`--all`) | `0.001` |

## Examples

```bash
# Basic background removal (auto-downloads vit_h ~2.5GB)
python3 scripts/segment.py photo.jpg output.png

# Specify hint point when subject is off-center
python3 scripts/segment.py photo.jpg output.png --points 320,240

# Multiple hints with lightweight model
python3 scripts/segment.py photo.jpg output.png --model vit_b --points 320,240 400,300

# Extract all elements (one PNG per element)
python3 scripts/segment.py photo.jpg ./elements/ --all

# Denser grid to capture small objects
python3 scripts/segment.py photo.jpg ./elements/ --all --grid 32

# Use a local checkpoint
python3 scripts/segment.py photo.jpg output.png --checkpoint /path/to/sam_vit_h_4b8939.pth
```

## Dependencies

`segment_anything` is auto-installed on first run, or install manually:

```bash
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install pillow numpy torch torchvision
```

## Workflow

1. User provides image path
2. Ask if hint points are needed (when subject is off-center)
3. Run script; checkpoint auto-downloads on first use to `~/.cache/sam/`
4. Output transparent-background PNG

## Model Selection

| Model | Size | Speed | Quality |
|---|---|---|---|
| `vit_b` | ~375 MB | fastest | good |
| `vit_l` | ~1.25 GB | medium | better |
| `vit_h` | ~2.5 GB | slower | best |

CUDA is used automatically when a GPU is available.
