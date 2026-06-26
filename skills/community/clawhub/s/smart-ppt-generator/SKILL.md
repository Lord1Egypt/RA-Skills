---
name: smart-ppt-generator
description: "One-click AI-powered PPT generator. Smart style detection, auto design layout, preview confirmation, exports to PPTX. No API key needed!"
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["node", "bash", "puppeteer", "pptxgenjs"]
      env: []
      skills: ["frontend-design", "canvas-design"]
---

# Smart PPT Generator 📊

AI-powered PowerPoint generator - create professional presentations with one command!

## Features

- ✅ **No API needed** - runs locally, no paid services
- Smart style detection (Tech/Business/Education/Marketing/Creative+)
- Auto design layout using professional design skills
- Preview confirmation - see before you download
- Dynamic color schemes - 10 styles × 5 color palettes
- High-end mode - Canvas design for artistic results
- Online color search - auto-refresh after 5+ feedback
- One-click download via file hosting

## Dependencies

### Required Tools

| Tool | Install | Purpose |
|------|---------|---------|
| Node.js | pre-installed | Runtime |
| puppeteer | `npm install puppeteer` | Screenshot capture |
| pptxgenjs | `npm install pptxgenjs` | PPTX generation |

### Required Skills

| Skill | Purpose |
|-------|---------|
| frontend-design | Normal mode layout |
| canvas-design | High-end mode design |

### Required Services

| Service | Purpose | Deploy |
|---------|---------|--------|
| FileBrowser | File hosting | Docker :8080 |

## Setup

```bash
# Install Node dependencies
cd /tmp && npm install puppeteer pptxgenjs

# Deploy FileBrowser
docker run -d --name filebrowser \
  -v /path/to/share:/srv \
  -p 127.0.0.1:8080:80 \
  filebrowser/filebrowser:latest

# Configure Nginx reverse proxy + HTTPS
```

## Usage

### Command Line

```bash
bash scripts/generate-ppt.sh --topic "AI Technology" --pages 5

# Parameters
# --topic: Presentation topic (required)
# --pages: Number of slides (default: 5)
# --style: Style (tech/corporate/comic/marketing/etc)
# --reset: Force refresh color scheme
```

### In AI Chat

```
User: "Make me a PPT about AI"

AI:
1. Analyze → tech style, normal mode
2. Call frontend-design for layout
3. Generate preview → send 3 images
4. User says "looks good"
5. Generate PPTX → upload → download link
```

## Workflow

```
1. Receive request → detect style
2. Determine mode:
   - Normal → frontend-design skill
   - High-end → canvas-design skill
3. Generate preview → 3 images to user
4. Wait for confirmation
5. Generate full PPTX
6. Upload to FileBrowser
7. Return download link
```

## Color System

- 10 preset styles, 5 color palettes each
- Online search triggers after 5+ modifications
- Use `--reset` to force refresh

## Output

- Preview: 3 PNG images (sent separately)
- Final: PPTX file
- Download: https://your-domain.com/public/xxx.pptx

## Troubleshooting

**puppeteer not found?**
```bash
ls /tmp/node_modules/puppeteer
# Reinstall: npm install puppeteer
```

**Can't download?**
```bash
docker ps | grep filebrowser
# Check public directory permissions
```

**Don't like the colors?**
```bash
# Use --reset flag or modify 5+ times
```
