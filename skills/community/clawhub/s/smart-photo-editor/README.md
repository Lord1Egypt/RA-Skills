# Smart Photo Editor - Quick Start Guide

AI-powered photo editing and restoration skill for OpenClaw.

## Quick Start

### ⭐ Recommended: Unified CLI (`edit.py`)
```bash
./scripts/edit.py --task remove-object --image photo.jpg \
  --prompt "Remove the power cable" --output out.jpg
```

### Remove Object from Photo
```
"Use smart-photo-editor to remove the power cable from this mountain photo"
```
→ Automatically uses Seedream AI for complex scenes

### Restore Old Photo
```
"Use smart-photo-editor to restore this old photo"
```
→ Removes scratches, enhances clarity, restores colors

### Remove Background
```
"Use smart-photo-editor to remove the background from this portrait"
```
→ Uses rembg (if installed) or falls back to ImageMagick

### Remove Diagonal/Angled Lines (OpenCV)
```bash
./scripts/inpaint.py input.jpg output.jpg --type line --x1 100 --y1 200 --x2 500 --y2 400 --thickness 3
```

### Remove Watermark/Logo Region (OpenCV)
```bash
./scripts/inpaint.py input.jpg output.jpg --type rect --x 50 --y 50 --w 400 --h 80 --feather 5
```

### Remove Multiple Spots/Lines (Batch Mode)
```bash
# Multiple spots in one command
./scripts/inpaint.py input.jpg output.jpg --type spots --spots "100,150,8;200,300,10;50,400,6"

# Multiple lines in one command
./scripts/inpaint.py input.jpg output.jpg --type lines --lines "0,100,800,100,3;100,200,500,400,5"

# Batch processing from JSON config
./scripts/inpaint.py input.jpg output.jpg --type batch --batch tasks.json
```

### Resize for API Compatibility
```bash
./scripts/inpaint.py input.jpg output.jpg --type resize --max-dim 2048
```

### Portrait Retouching
```bash
# All enhancements at once
./scripts/portrait.py input.jpg output.jpg --all

# Subtle skin smoothing + eye brightening
./scripts/portrait.py input.jpg output.jpg --smooth 2 --enhance-eyes

# Face brightness + contrast adjustment
./scripts/portrait.py input.jpg output.jpg --brightness 10 --contrast 15
```

### EXIF Utilities
```bash
./scripts/exif_utils.py read photo.jpg        # Read EXIF tags
./scripts/exif_utils.py strip photo.jpg -o out.jpg  # Remove EXIF
./scripts/exif_utils.py copy src.jpg dst.jpg  # Copy EXIF to another image
```

### Smart Auto-Crop
```bash
./scripts/smart_crop.py input.jpg output.jpg               # Auto-detect salient region
./scripts/smart_crop.py input.jpg output.jpg --aspect 16/9 # Crop to aspect ratio
./scripts/smart_crop.py input.jpg output.jpg --debug      # Generate debug overlay
```

### Additional OpenCV Operations (denoise / sharpen / adjust)
```bash
./scripts/inpaint.py input.jpg output.jpg --type denoise --strength 15
./scripts/inpaint.py input.jpg output.jpg --type sharpen --strength 1.5
./scripts/inpaint.py input.jpg output.jpg --type adjust --brightness 15 --contrast 10 --gamma 0.9
```

## Features

| Feature | Best Tool | Quality |
|---------|-----------|---------|
| Object removal | Seedream AI | Excellent |
| Old photo restoration | Seedream AI | Excellent |
| Background removal | rembg AI | Excellent |
| Solid background removal | ImageMagick | Good (fast) |
| Wire/line removal | OpenCV | Good (fast) |
| Sensor dust removal | OpenCV | Good (fast) |
| Batch multi-region | OpenCV | Good (fast) |
| Portrait retouching | OpenCV | Good |
| Skin smoothing | OpenCV bilateral | Good |
| Smart auto-crop | OpenCV saliency | Good |
| Denoise / sharpen / adjust | OpenCV | Good |
| Resize/crop/compress | ImageMagick | Excellent |
| Color adjustment | ImageMagick | Excellent |
| EXIF preservation | piexif/exif | — |

## Skill File Structure

```
~/.openclaw/skills/smart-photo-editor/
├── SKILL.md              # Full documentation
├── README.md             # This file
├── scripts/
│   ├── edit.py           # ⭐ Unified CLI (all operations)
│   ├── inpaint.py        # OpenCV wire/spot/line/rect/denoise/sharpen/adjust
│   ├── portrait.py       # Portrait retouching (skin, eyes, teeth)
│   ├── smart_crop.py     # Smart auto-crop based on saliency detection
│   ├── exif_utils.py     # EXIF read/strip/copy utility
│   └── remove_bg.sh      # Background removal wrapper
└── examples/             # Before/after comparison examples (add your own)
```

## Tips

1. **Large images** are automatically handled - no more "image too large" errors
2. **Chinese prompts work** - the skill automatically translates to optimized English
3. **Automatic fallback** - if Seedream fails, OpenCV will be tried for simple cases
4. **EXIF preserved** - all editing scripts preserve camera metadata automatically
5. **Face auto-detection** - portrait retouching automatically finds faces for targeted edits
6. **Smart crop** - automatically finds the most interesting region in any image

## Install Optional rembg

For better AI background removal:
```bash
source ~/.openclaw/venv-clawd/bin/activate
pip install rembg
```
