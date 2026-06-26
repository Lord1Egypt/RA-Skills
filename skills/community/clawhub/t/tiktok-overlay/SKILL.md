---
name: tiktok-overlay
version: 1.1.0
description: Adds TikTok-style text overlays to images and videos with styled fonts, backgrounds, strokes, and timed animations.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🎵", "requires": {"bins": ["python3"]}, "install": [{"type": "uv", "packages": ["Pillow", "moviepy"]}]}}
---

# TikTok Text Overlay Skill

You are a TikTok-style text overlay tool. You add styled text overlays to images and videos, replicating the look and feel of TikTok's built-in text editor.

## Setup

The overlay scripts live in `{baseDir}`:

- `{baseDir}/tiktok_overlay.py` — image overlay engine
- `{baseDir}/tiktok_video_overlay.py` — video overlay engine (uses moviepy)

Before using, ensure dependencies are installed:

```bash
pip3 install Pillow moviepy
```

## Available Styles

| Style         | Value          | Description                          |
|---------------|----------------|--------------------------------------|
| Classic       | `classic`      | Clean bold sans-serif (Arial Bold)   |
| Typewriter    | `typewriter`   | Monospace typewriter look            |
| Handwriting   | `handwriting`  | Casual handwriting font              |
| Neon          | `neon`         | Rounded bold with glow effect        |
| Serif         | `serif`        | Traditional serif (Georgia)          |
| Strong        | `strong`       | Extra bold impact style              |
| Comic         | `comic`        | Playful comic sans style             |

## Background Styles

| Style       | Value        | Description                              |
|-------------|--------------|------------------------------------------|
| None        | `none`       | No background, text only                 |
| Highlight   | `highlight`  | Per-line rounded highlight (TikTok default) |
| Full BG     | `full_bg`    | Single rounded rectangle behind all text |
| Letter      | `letter`     | Per-line tight highlight                 |

## Image Overlay

Use `{baseDir}/tiktok_overlay.py` for images:

```python
import sys
sys.path.insert(0, "{baseDir}")
from tiktok_overlay import overlay_text, overlay_texts, TextOverlay

# Single text — save to file
overlay_text("input.jpg", "Your text here", "output.jpg",
    style="classic", font_size=48, stroke_width=5, bg_style="none")

# Single text — return PIL Image (omit output_path)
result = overlay_text("input.jpg", "Your text here",
    style="strong", font_size="large", text_color="coral")

# Multiple overlays — TextOverlay objects
overlay_texts("input.jpg", [
    TextOverlay("Top text", position="top", style="classic", stroke_width=4),
    TextOverlay("Bottom", position="bottom", text_color="red"),
], "output.jpg")

# Multiple overlays — dicts (no import needed)
overlay_texts("input.jpg", [
    {"text": "Top text", "position": "top", "style": "strong", "stroke_width": 5},
    {"text": "Bottom", "position": "bottom", "text_color": "coral"},
], "output.jpg")

# Multiple overlays — (text, kwargs) tuples
overlay_texts("input.jpg", [
    ("Top text", {"position": "top", "stroke_width": 5}),
    ("Bottom", {"position": "bottom", "text_color": "red"}),
], "output.jpg")
```

### Flexible Inputs

All parameters accept multiple formats:

**Input source** — file path, PIL Image, numpy array, or bytes:
```python
overlay_text("photo.jpg", "Hello", "out.jpg")          # path
overlay_text(pil_image, "Hello", "out.jpg")             # PIL Image
overlay_text(numpy_array, "Hello", "out.jpg")           # numpy
overlay_text(image_bytes, "Hello", "out.jpg")           # bytes
```

**Output** — file path to save, or None to return PIL Image:
```python
overlay_text("photo.jpg", "Hello", "out.jpg")           # saves file
result = overlay_text("photo.jpg", "Hello")             # returns PIL Image
```

**Colors** — hex, short hex, hex+alpha, named, RGB tuple, RGBA tuple:
```python
text_color="#FF0000"          # hex
text_color="#F00"             # short hex
text_color="#FF000080"        # hex with alpha
text_color="red"              # named (all CSS/PIL colors)
text_color=(255, 0, 0)        # RGB tuple
text_color=(255, 0, 0, 128)   # RGBA tuple
```

**Font size** — int pixels, string with unit, or named size:
```python
font_size=48                  # pixels
font_size="48px"              # string with unit
font_size="small"             # 32px
font_size="medium"            # 48px
font_size="large"             # 64px
font_size="xl"                # 80px
font_size="title"             # 72px
font_size="caption"           # 28px
```

**Style** — string or enum:
```python
style="classic"               # string
style="strong"
from tiktok_overlay import TikTokStyle
style=TikTokStyle.CLASSIC     # enum
```

**Position** — named, compound, pixel, percentage, or dict:
```python
position="top"                # named
position="bottom-left"        # compound
position=(100, 200)           # pixel coordinates
position=("50%", "80%")       # percentage of image size
position={"x": "10%", "y": "top"}  # dict with mixed
```

**Opacity** — float, int, or percentage string:
```python
bg_opacity=0.6                # float 0-1
bg_opacity=153                # int 0-255
bg_opacity="60%"              # percentage string
```

**Max width ratio** — float or percentage string:
```python
max_width_ratio=0.85          # float
max_width_ratio="85%"         # percentage string
```

### CLI

```bash
python3 {baseDir}/tiktok_overlay.py <input_image> "<text>" [output_image] [style]
```

Output path is optional — defaults to `input_overlay.ext`.

## Video Overlay

Use `{baseDir}/tiktok_video_overlay.py` for videos. Supports timed text and fade in/out:

```python
import sys
sys.path.insert(0, "{baseDir}")
from tiktok_video_overlay import overlay_video_text, overlay_video_texts, VideoTextOverlay

# Single text on entire video
overlay_video_text("input.mp4", "Hello!", "output.mp4",
    style="classic", font_size=52, stroke_width=5)

# Multiple timed texts
overlay_video_texts("input.mp4", [
    VideoTextOverlay("Appears 0-3s", t_start=0, t_end=3,
        fade_in=0.5, fade_out=0.5,
        style="classic", position="top", font_size=48, stroke_width=4),
    VideoTextOverlay("Appears 2-5s", t_start=2, t_end=5,
        style="strong", position="center", font_size=56,
        text_color="tomato", stroke_width=5, bg_style="none"),
    VideoTextOverlay("Always visible",
        position="bottom", font_size=40, bg_style="highlight"),
], "output.mp4")
```

### CLI

```bash
python3 {baseDir}/tiktok_video_overlay.py <input_video> "<text>" <output_video> [style]
```

## Key Parameters

| Parameter          | Accepts                                        | Default      | Description                              |
|--------------------|------------------------------------------------|--------------|------------------------------------------|
| `input_source`     | path, PIL Image, numpy array, bytes            | —            | Image to overlay                         |
| `text`             | str                                            | —            | The text to overlay                      |
| `output_path`      | path or None                                   | None         | Save path; None returns PIL Image        |
| `style`            | str, TikTokStyle, None                         | `classic`    | Font style                               |
| `font_size`        | int, str (`"48px"`, `"large"`)                 | 48           | Font size                                |
| `text_color`       | hex, named, rgb/rgba tuple                     | `#FFFFFF`    | Text color                               |
| `bg_style`         | str                                            | `highlight`  | Background style                         |
| `bg_color`         | hex, named, rgb/rgba tuple                     | `#000000`    | Background color                         |
| `bg_opacity`       | float 0-1, int 0-255, str `"60%"`             | 0.6          | Background opacity                       |
| `position`         | str, (x,y), ("x%","y%"), dict                  | `center`     | Position                                 |
| `alignment`        | str                                            | `center`     | Text alignment: left/center/right        |
| `stroke_width`     | int                                            | 0            | Outline thickness (4-6 for TikTok look)  |
| `stroke_color`     | hex, named, rgb/rgba tuple                     | `#000000`    | Outline color                            |
| `max_width_ratio`  | float or str `"85%"`                           | 0.85         | Max text width as ratio of image width   |

### Video-only Parameters

| Parameter   | Type           | Default | Description                    |
|-------------|----------------|---------|--------------------------------|
| `t_start`   | float or None  | None    | Start time in seconds          |
| `t_end`     | float or None  | None    | End time in seconds            |
| `fade_in`   | float          | 0.0     | Fade in duration (seconds)     |
| `fade_out`  | float          | 0.0     | Fade out duration (seconds)    |

## Tips

- For the classic TikTok outlined text look, use `bg_style="none"` with `stroke_width=5`.
- For the TikTok highlight look, use `bg_style="highlight"` with `bg_opacity=0.6`.
- Word wrapping is automatic based on `max_width_ratio`.
- Compound positions like `"top-left"` and `"bottom-right"` are supported.
- All CSS/PIL named colors work: `"red"`, `"coral"`, `"dodgerblue"`, `"gold"`, etc.
- Uses macOS system fonts as TikTok-style substitutes. Works out of the box on macOS.
