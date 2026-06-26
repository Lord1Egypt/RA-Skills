# Manim Animation Technical Guide

## Table of Contents

1. [Manim Community Overview](#manim-community-overview)
2. [Scene Code Structure](#scene-code-structure)
3. [Voiceover Integration (manim-voiceover)](#voiceover-integration-manim-voiceover)
4. [Subtitle System](#subtitle-system)
5. [Common Animation Patterns](#common-animation-patterns)
6. [Advanced Tips](#advanced-tips)
7. [Troubleshooting Guide](#troubleshooting-guide)

---

## Manim Community Overview

Manim Community (manim) is a community-maintained mathematical animation engine, derived from the original manimgl created by Grant Sanderson of 3Blue1Brown.

**Core Philosophy**: Describe mathematical animations with Python code — everything is programmable, version-controllable, and automatable.

### Version Selection

| Version | Package | Features |
|---------|---------|----------|
| **Manim Community** | `manim` | Community-maintained, well-documented, rich plugin ecosystem |
| manimgl | `manimgl` | 3B1B's personal version, OpenGL rendering, real-time preview |

**This skill uses Manim Community (`pip install manim`).**

**Default typography:** use **`Roboto`** for all `Text()` (see `references/default_typography.py` and `DESIGN_THEME.md`) unless the user requests another font.

---

## Scene Code Structure

### Basic Scene (Animation Only)

```python
from manim import *

class BasicScene(Scene):
    def construct(self):
        # Create objects
        circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
        label = Text("Circle", font="Roboto", font_size=24)
        label.next_to(circle, DOWN)

        # Animate
        self.play(Create(circle))
        self.play(Write(label))
        self.wait(1)

        # Transform
        square = Square(side_length=3, color=GREEN, fill_opacity=0.5)
        self.play(Transform(circle, square))
        self.wait(1)
```

### Voiceover Scene (Animation + Voice + Subtitles)

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class NarrationScene(VoiceoverScene):
    def _make_subtitle(self, text_str):
        """Create subtitle with dark background at bottom."""
        sub = Text(text_str, font_size=22, color=WHITE, weight=BOLD)
        # Prevent subtitle from overflowing left/right edges
        max_width = config.frame_width - 1.0  # 0.5 margin each side
        if sub.width > max_width:
            sub.scale_to_fit_width(max_width)
        sub.to_edge(DOWN, buff=0.4)
        bg = BackgroundRectangle(sub, color=BLACK, fill_opacity=0.6, buff=0.15)
        return VGroup(bg, sub)

    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        # Scene 1: Title
        title = Text("Title", font_size=48, color=BLUE)
        sub_text = "Welcome to the demo video."
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            # FadeIn(sub) in the FIRST play() to sync subtitle with voice
            self.play(Write(title), FadeIn(sub), run_time=tracker.duration)
        self.play(FadeOut(sub))
        self.wait(0.3)

        # Scene 2: Content
        self.play(FadeOut(title))
        circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
        sub_text = "Let's create a circle."
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            self.play(Create(circle), FadeIn(sub), run_time=tracker.duration)
        self.play(FadeOut(sub))
        self.wait(0.3)
```

---

## Voiceover Integration (manim-voiceover)

### TTS Engine Comparison

| Engine | Installation | Cost | Network | Quality | Chinese |
|--------|-------------|------|---------|---------|---------|
| **gTTS** | `pip install "manim-voiceover[gtts]"` | Free | Required | Medium | ✅ |
| **pyttsx3** | `pip install "manim-voiceover[pyttsx3]"` | Free | Not required | Lower | ✅ |
| **Azure** | `pip install "manim-voiceover[azure]"` | Paid | Required | High | ✅ |
| **OpenAI** | `pip install "manim-voiceover[openai]"` | Paid | Required | High | ✅ |
| **ElevenLabs** | `pip install "manim-voiceover[elevenlabs]"` | Paid | Required | Very High | ✅ |

### Core Pattern

```python
# 1. Initialize TTS engine
self.set_speech_service(GTTSService(lang="en"))

# 2. voiceover context manager
with self.voiceover(text="Speech text") as tracker:
    # tracker.duration — TTS speech duration (seconds)
    # tracker.time_until_bookmark("mark1") — Time to bookmark
    self.play(SomeAnimation(), run_time=tracker.duration)

# 3. Use bookmarks for precise alignment
with self.voiceover(
    text='Part one, <bookmark mark="A"/>Part two.'
) as tracker:
    self.play(animation1, run_time=tracker.time_until_bookmark("A"))
    self.play(animation2, run_time=tracker.duration - tracker.time_until_bookmark("A"))
```

### Audio Cache

manim-voiceover caches generated TTS audio in the `media/voiceovers/` directory:
- Identical text will not be regenerated
- Modified text triggers automatic regeneration
- Clear cache: `rm -rf media/voiceovers/`

### SRT Subtitle Auto-Generation

manim-voiceover automatically generates `.srt` subtitle files in the same directory as the video, in standard format compatible with any media player.

---

## Subtitle System

### Option 1: In-Scene Subtitles (Manim Text Objects)

Render subtitle text directly within the Manim scene as part of the animation.

**Pros**: No additional tools needed; subtitles are part of the animation
**Cons**: Cannot be toggled on/off by the media player

```python
def _make_subtitle(self, text_str):
    sub = Text(text_str, font_size=22, color=WHITE, weight=BOLD)
    # Prevent subtitle from overflowing left/right edges
    max_width = config.frame_width - 1.0  # 0.5 margin each side
    if sub.width > max_width:
        sub.scale_to_fit_width(max_width)
    sub.to_edge(DOWN, buff=0.4)
    bg = BackgroundRectangle(sub, color=BLACK, fill_opacity=0.6, buff=0.15)
    return VGroup(bg, sub)

# Usage — FadeIn(sub) must be in the FIRST self.play() to sync with voice
with self.voiceover(text=sub_text) as tracker:
    sub = self._make_subtitle(sub_text)
    self.play(FadeIn(sub), SomeAnimation(), run_time=tracker.duration)
self.play(FadeOut(sub))
```

**⚠️ Subtitle Overflow Protection**: `_make_subtitle()` uses `scale_to_fit_width` to ensure long text does not exceed left/right frame boundaries. `font_size=22` is better than the default 28 for long sentences.

**⚠️ Subtitle Sync**: `FadeIn(sub)` must be placed in the **first** `self.play()` call within the voiceover block; otherwise, the subtitle will lag behind the voice.

### Option 2: SRT External Subtitles (ffmpeg Burn-in)

Use the SRT files auto-generated by manim-voiceover and burn them into the video with ffmpeg.

**Pros**: Flexible subtitle styling; SRT files can be edited independently
**Cons**: Requires ffmpeg + libass (install ffmpeg-full)

```bash
ffmpeg -y -i video.mp4 \
    -vf "subtitles=subtitle.srt:force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,BackColour=&H80000000,BorderStyle=4,MarginV=30'" \
    -c:a copy \
    output_subtitled.mp4
```

### ⚠️ Avoid Double Subtitles

**Do not** use both in-scene subtitles (`_make_subtitle`) and SRT burn-in simultaneously, otherwise two overlapping subtitle layers will appear.

**Correct Approach**: Choose one
- **Option A (Recommended)**: Render subtitles in code with `_make_subtitle()`, do not burn SRT. Subtitles sync with animation, no extra processing needed.
- **Option B**: Do not render subtitles in code, burn SRT with ffmpeg. Subtitle styling can be flexibly controlled via `force_style`.

---

## Common Animation Patterns

### Title + Subtitle

```python
title = Text("Main Title", font_size=48, color=BLUE)
subtitle = Text("Subtitle", font_size=28, color=GRAY)
subtitle.next_to(title, DOWN, buff=0.5)

self.play(Write(title))
self.play(FadeIn(subtitle))
self.wait(1)
self.play(title.animate.to_edge(UP), FadeOut(subtitle))
```

### Formula Derivation

```python
eq1 = MathTex(r"x^2 + y^2 = r^2")
eq2 = MathTex(r"y = \pm\sqrt{r^2 - x^2}")
eq2.next_to(eq1, DOWN, buff=0.5)

self.play(Write(eq1))
self.wait(0.5)
self.play(TransformMatchingShapes(eq1.copy(), eq2))
```

### Shape Transformation

```python
circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
square = Square(side_length=3, color=GREEN, fill_opacity=0.5)

self.play(Create(circle))
self.wait(0.5)
self.play(Transform(circle, square))
```

### Coordinate System + Function Graph

```python
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 2, 1],
    axis_config={"include_numbers": True}
)
graph = axes.plot(lambda x: np.sin(x), color=YELLOW)
label = axes.get_graph_label(graph, r"\sin(x)")

self.play(Create(axes))
self.play(Create(graph), Write(label))
```

### Grouping + Layout

```python
items = VGroup(
    Square(color=RED),
    Circle(color=GREEN),
    Triangle(color=BLUE),
)
items.arrange(RIGHT, buff=0.8)
items.scale(0.8)

self.play(LaggedStart(*[Create(item) for item in items], lag_ratio=0.3))
```

### Scene Transition

```python
# Fade out all objects, start new scene
self.play(*[FadeOut(mob) for mob in self.mobjects])
self.wait(0.3)
```

---

## Advanced Tips

### Multi-Scene Concatenation

A single file can contain multiple Scene classes. Render them in order, then concatenate with ffmpeg:

```bash
# Render all scenes
manim render -qh scenes.py Scene1
manim render -qh scenes.py Scene2
manim render -qh scenes.py Scene3

# Concat
echo "file 'Scene1.mp4'" > list.txt
echo "file 'Scene2.mp4'" >> list.txt
echo "file 'Scene3.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
```

### Custom Fonts

```python
Text("Custom font text", font="PingFang SC", font_size=36)
```

### Color Themes

```python
# Manim built-in color constants
RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, GOLD, WHITE, GRAY
# Hex colors
Text("Text", color="#FF6B6B")
```

### LaTeX + Manim Integration

```python
# Inline formula
formula = MathTex(r"E = mc^2", font_size=72, color=YELLOW)
# Multi-line aligned formula
aligned = MathTex(
    r"f(x) &= x^2 + 2x + 1 \\",
    r"&= (x+1)^2"
)
```

---

## Troubleshooting Guide

### 1. `ModuleNotFoundError: No module named 'pkg_resources'`

**Cause**: setuptools changes in Python 3.12+

**Solution**:
```bash
pip install "setuptools>=69.0,<72.0"
```

### 2. `UnknownCodecError: libx264`

**Cause**: Manim hardcodes the `libx264` encoder, but the current ffmpeg was compiled without libx264 support (common in conda environments where ffmpeg defaults to `--disable-gpl`).

**Solution**:
```bash
# Option A: macOS Homebrew — Install ffmpeg-full (recommended, includes libx264 + libass)
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg-full
brew link --force ffmpeg-full

# Option B: Conda environment — Install x264 package
conda install x264 -c conda-forge

# Verify
ffmpeg -codecs 2>&1 | grep libx264
# Output should include: encoders: libx264 libx264rgb
```

### 3. `ffmpeg: No such filter: 'subtitles'`

**Cause**: ffmpeg was compiled without libass

**Solution** (macOS):
```bash
# ffmpeg-full already includes libass; no extra steps if already installed
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg-full
brew link --force ffmpeg-full

# Verify
ffmpeg -filters 2>&1 | grep subtitles
```

### 4. gTTS Error: `gTTSError: Connection error`

**Cause**: Network cannot access Google TTS service

**Solution**:
```python
# Option 1: Use a proxy — set CORP_HTTP_PROXY / CORP_HTTPS_PROXY in your environment
# (never hardcode proxy URLs or credentials in scene code you commit).
import os
for dst, src in (("HTTP_PROXY", "CORP_HTTP_PROXY"), ("HTTPS_PROXY", "CORP_HTTPS_PROXY")):
    if os.environ.get(src):
        os.environ[dst] = os.environ[src]

# Option 2: Switch to offline TTS
from manim_voiceover.services.pyttsx3 import Pyttsx3Service
self.set_speech_service(Pyttsx3Service())
```

### 5. Chinese Characters Display as Blocks

**Cause**: System lacks Chinese fonts

**Solution**:
```bash
# Linux
sudo apt install fonts-noto-cjk

# macOS (built-in PingFang SC, usually OK)

# Specify font
Text("Text", font="Noto Sans CJK SC")
```

### 6. `WARNING: Some options were not used: shortest, metadata`

**Cause**: Manim passes unused options when calling FFmpeg

**Solution**: Can be safely ignored; does not affect the output video.

### 7. Slow Rendering Speed

**Suggestions**:
- Use `-ql` (480p15) for quick preview during development
- Use `-qh` (1080p60) or `-qp` (4K) for final output
- Voiceover audio is cached; second render will be much faster

### 8. Video Has No Sound

**Checklist**:
- Confirm using `VoiceoverScene` instead of `Scene`
- Confirm `self.set_speech_service()` is called
- Confirm there are animations inside the voiceover block (empty blocks produce no audio)
- Check if `.mp3` files exist in `media/voiceovers/` directory
