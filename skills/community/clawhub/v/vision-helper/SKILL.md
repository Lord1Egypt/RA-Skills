---
name: vision-helper
description: Analyze images using local or cloud vision models via Ollama. Use when you need to identify screenshots, analyze UI elements, read image content, or perform OCR. Triggers on: "analyze image", "screenshot", "what's in this image", "OCR", "识图", "看图", "截图识别".
---

# 📸 Vision Helper — Image Analysis

Analyze images using vision models via Ollama, with extended timeout support for cloud-based models.

## Why Not Use the Built-in `image` Tool?

The built-in `image` tool has limited timeout settings that cause failures with cloud vision models (which often need 40–120 seconds). This skill calls the Ollama API directly with a 180-second timeout, supporting both local and cloud models reliably.

It also bypasses the built-in tool's file path restrictions, allowing analysis of images from any readable directory.

## Usage

### Basic

```bash
# Analyze an image (default: English description)
python3 <skill-dir>/scripts/analyze_image.py <image_path>

# With a custom prompt
python3 <skill-dir>/scripts/analyze_image.py <image_path> "Is this a chess game? Describe the board state"

# With a specific model
python3 <skill-dir>/scripts/analyze_image.py <image_path> "Describe content" kimi-k2.5:cloud
```

> `<skill-dir>` resolves to your OpenClaw skill installation directory, typically `~/.openclaw/workspace/skills/vision-helper/`.

### In Conversation

When you need to analyze an image, use the `exec` tool:

```
exec: python3 <skill-dir>/scripts/analyze_image.py /path/to/image.png "What do you see?"
```

**Important:** Set exec timeout to 120–180 seconds, as cloud vision models are slow.

### Screenshot + Analysis Workflow

#### Option A: Browser screenshot → analyze

```
1. browser(action="screenshot") → get screenshot path (MEDIA: xxx)
2. exec("<skill-dir>/scripts/analyze_image.py <screenshot_path> 'Describe this UI'")
3. Act on the analysis result
```

#### Option B: Desktop screenshot → analyze

**macOS:**
```
1. exec("screencapture -x /tmp/screen.png")
2. exec("<skill-dir>/scripts/analyze_image.py /tmp/screen.png 'Describe the desktop'")
```

**Linux:**
```
1. exec("gnome-screenshot -f /tmp/screen.png")
   — or —
   exec("import /tmp/screen.png")  # ImageMagick
   — or —
   exec("scrot /tmp/screen.png")
2. exec("<skill-dir>/scripts/analyze_image.py /tmp/screen.png 'Describe the desktop'")
```

#### Option C: Game/App UI → analyze → act

```
1. Screenshot the current screen
2. Use vision-helper to identify UI elements, buttons, text
3. Execute clicks/input based on the analysis
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VISION_MODEL` | `gemma4:31b` | Default vision model |
| `VISION_TIMEOUT` | `180` | Request timeout in seconds |
| `OLLAMA_API_URL` | `http://localhost:11434/api/chat` | Ollama API endpoint |

## Supported Models

| Model | Vision | Speed | Recommendation |
|-------|--------|-------|----------------|
| `gemma4:31b` | ✅ | Local, fast | ⭐ **Primary** (privacy, no API needed) |
| `kimi-k2.6:cloud` | ✅ | 40–120s | 🔬 Advanced (high quality, cloud) |
| `kimi-k2.5:cloud` | ✅ | 40–90s | Alternative cloud option |
| `qwen3.5:cloud` | ✅ | 30–60s | Fast cloud recognition |
| `qwen3.5:397b-cloud` | ✅ | 40–90s | High quality cloud |
| `gemma4:31b` | ✅ | Local, fast | Privacy-first (runs offline) |

Note: Cloud models require the model to be available in your Ollama instance. Use `VISION_MODEL` env var to switch.

## FAQ

### Q: Can I use the built-in `image` tool instead?
A: It works for local models but will time out on cloud vision models. Always prefer this skill's script for reliable results.

### Q: What image formats are supported?
A: PNG, JPG, JPEG, GIF, WebP, BMP, TIFF, SVG. Maximum file size: 20 MB.

### Q: Where should I save screenshots?
A: Any readable directory works — `/tmp/`, your workspace, etc. This script has no path restrictions.

### Q: How do I use a Chinese prompt?
A: Pass it as the second argument: `python3 <skill-dir>/scripts/analyze_image.py /tmp/img.png "请描述这张图片的内容"`

## Automation Ideas

- **Game automation**: Screenshot → analyze game state → decide next action
- **Browser verification**: Screenshot → verify page loaded correctly
- **Desktop monitoring**: Periodic screenshots → detect changes
- **UI testing**: Screenshot → verify rendered output
- **OCR**: Extract text content from images