---
name: screen-vision
description: macOS screen OCR & click automation via Apple Vision + ScreenCaptureKit. Capture any window or screen region, extract text with coordinates, find text, and click on it — all from the terminal.
homepage: https://github.com/jackyun1024/mac-screen-vision
user-invocable: true
allowed-tools: Bash, Read
argument-hint: "<command> [options] (e.g. list --app Safari, find 'Submit', tap 'OK' --retry 3)"
---

# screen-vision

macOS screen OCR & click automation CLI powered by Apple Vision + ScreenCaptureKit.

## IMPORTANT: Auto-Setup (run first)

Before running any screen-vision command, check if the binary exists. If not, run the setup script:

```bash
command -v screen-vision &>/dev/null || bash "${CLAUDE_SKILL_DIR}/setup.sh"
```

This installs `screen-vision` (via Homebrew or source build) and `cliclick` automatically.

## Requirements

- macOS 14.0+ (Sonoma)
- Screen Recording permission (System Settings > Privacy & Security > Screen Recording)

## Commands

| Command | Description | Output |
|---------|-------------|--------|
| `screen-vision ocr [--app NAME]` | Full OCR | JSON array `[{text, x, y, w, h, confidence}]` |
| `screen-vision list [--app NAME]` | OCR list | Human-readable text with coordinates |
| `screen-vision find "text" [--app NAME]` | Find text | JSON `{text, x, y, found}` |
| `screen-vision has "text" [--app NAME]` | Check text exists | Exit code 0 (found) / 1 (not found) |
| `screen-vision tap "text" [--app NAME] [--retry N]` | Find + click | JSON `{text, x, y, tapped}` |
| `screen-vision wait "text" [--timeout SEC]` | Poll until text appears | JSON `{text, x, y, found}` |

## Capture Priority

```
--region x,y,w,h  >  --app "AppName"  >  full screen (default)
```

## Usage Patterns

### OCR a specific app window
```bash
screen-vision list --app "Safari"
```

### Check if text is visible (for conditionals)
```bash
screen-vision has "Submit" --app "MyApp" && echo "Found" || echo "Not found"
```

### Click on text with retry
```bash
screen-vision tap "OK" --app "MyApp" --retry 3
```

### Wait for text to appear (e.g. loading complete)
```bash
screen-vision wait "Complete" --timeout 30
```

### Full screen OCR as JSON (pipe to jq)
```bash
screen-vision ocr | jq '.[].text'
```

## $ARGUMENTS Handling

Parse the user's request to determine which command to run:
- "화면에 뭐 있어?" / "what's on screen?" → `screen-vision list`
- "~찾아" / "find ~" → `screen-vision find "text"`
- "~클릭해" / "click ~" → `screen-vision tap "text"`
- "~보여?" / "is ~ visible?" → `screen-vision has "text"`
- "~뜰 때까지 기다려" / "wait for ~" → `screen-vision wait "text"`
