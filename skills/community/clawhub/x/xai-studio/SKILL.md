---
name: xai-studio
description: "xAI Studio — generate and edit images and videos via the xAI API. Image: text-to-image, batch generation, multi-image editing, concurrent style transfers, multi-turn chaining. Video: text-to-video, image-to-video, video editing, concurrent video edits. All from a single expandable CLI."
license: MIT-0
repository: https://github.com/H0llyW00dzZ/xai-studio-skills
metadata:
  openclaw:
    homepage: "https://github.com/H0llyW00dzZ/xai-studio-skills"
    emoji: "📽️"
    requires:
      bins:
        - python3
      env:
        - XAI_API_KEY
    primaryEnv: XAI_API_KEY
    useVenv: true
    files:
      - scripts/run.py
    install:
      - id: pip3
        kind: apt
        package: python3-pip
        label: "Install pip3"
      - id: xai-sdk
        kind: pip3
        package: xai-sdk
        label: "Install official xAI SDK"
---

# xAI Studio

Generate and edit images and videos using xAI's models via the xAI SDK.

## Setup (Venv + SDK)

Create an isolated virtual environment and install the SDK:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install xai-sdk
deactivate
```

## Generate Images

```bash
venv/bin/python3 scripts/run.py generate --prompt "A futuristic cityscape at dawn"
```

Generate multiple images in one request:

```bash
venv/bin/python3 scripts/run.py generate --prompt "Abstract art" --count 4
```

## Edit Images

Edit an existing image with a text prompt:

```bash
venv/bin/python3 scripts/run.py edit --prompt "Make it a watercolor painting" --image photo.png
```

Combine up to 3 source images:

```bash
venv/bin/python3 scripts/run.py edit --prompt "Add the cat to the landscape" --image cat.png --image landscape.png
```

## Concurrent Style Transfers

Apply multiple styles to the same image in parallel:

```bash
venv/bin/python3 scripts/run.py concurrent --image photo.png --prompt "oil painting" --prompt "pencil sketch" --prompt "pop art"
```

## Multi-Turn Editing

Chain edits sequentially — each output feeds into the next:

```bash
venv/bin/python3 scripts/run.py multi-turn --image photo.png --prompt "Add dramatic clouds" --prompt "Make it a sunset"
```

## Common Flags

- `--model`: Model name (default: `grok-imagine-image`)
- `--aspect-ratio`: e.g. `16:9`, `4:3`, `auto` (default: `1:1`)
- `--resolution`: `1k` or `2k` (default: API default)
- `--format`: `base64` (default) or `url`
- `--out-dir`: Output directory (default: `media/xai-output`)

## Output

Images are saved to `<out-dir>/<YYYY-MM-DD>/<prefix>_<NNN>_<HHMMSS>.<ext>`, organized by UTC date. The prefix reflects the subcommand: `generate`, `edit`, `style` (concurrent), or `step` (multi-turn). The file extension is detected automatically from image magic bytes (PNG, JPEG, WebP, GIF).

---

## Video: Generate

```bash
# Text-to-video
venv/bin/python3 scripts/run.py video-generate --prompt "A rocket launching from Mars" --duration 10 --resolution 720p

# Image-to-video
venv/bin/python3 scripts/run.py video-generate --prompt "Animate this scene" --image photo.png --duration 5
```

## Video: Edit

```bash
venv/bin/python3 scripts/run.py video-edit --prompt "Add a silver necklace" --video https://example.com/clip.mp4
```

## Video: Concurrent Edits

```bash
venv/bin/python3 scripts/run.py video-concurrent --video https://example.com/clip.mp4 --prompt "Add a hat" --prompt "Change outfit to red"
```

## Video Flags

- `--model`: Model name (default: `grok-imagine-video`)
- `--duration`: Length in seconds, 1–15 (default: `5`) — generate only
- `--aspect-ratio`: e.g. `16:9` (default: API default)
- `--resolution`: `480p` or `720p` (default: API default)
- `--timeout`: Max polling wait in seconds (default: SDK default)
- `--poll-interval`: Seconds between status checks (default: SDK default)

Videos are saved as `.mp4` to `<out-dir>/<YYYY-MM-DD>/<prefix>_<NNN>_<HHMMSS>.mp4`. The prefix reflects the subcommand: `video` (generate), `video_edit`, or `video_style` (concurrent).
