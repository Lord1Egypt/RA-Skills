---
name: screengrab
description: |
  Quick macOS display snapshot. Captures what's currently on screen without opening a browser. Saves to /tmp or a custom path. Supports multiple displays and periodic watch mode.

  USE WHEN: Agent needs to see what's on the Mac's screen right now — for debugging visual state, checking what app is open, verifying output, or remote awareness without a full browser session. Also use to list connected displays or capture a specific one.

  DON'T USE WHEN: User wants to screenshot a specific URL or web page (use browser snapshot instead). Not for headless/offscreen rendering.
---

# screengrab

Thin wrapper around macOS `screencapture`. No dependencies beyond Python 3.

## Requirements

- macOS only (`/usr/sbin/screencapture`)
- Script: `scripts/screengrab.py`

## Commands

```bash
# Capture all displays → /tmp/screengrab-TIMESTAMP.png
python3 scripts/screengrab.py snap

# Custom output path
python3 scripts/screengrab.py snap --out ~/Desktop/snap.png

# Specific display (0=main, 1=second)
python3 scripts/screengrab.py snap --display 0

# Open in Preview immediately
python3 scripts/screengrab.py snap --open

# Quiet mode — just prints the file path (useful for piping to image tool)
python3 scripts/screengrab.py snap --quiet

# List connected displays
python3 scripts/screengrab.py list

# Periodic capture (every 30s)
python3 scripts/screengrab.py watch
python3 scripts/screengrab.py watch --interval 10 --out-dir ~/Desktop/snaps
python3 scripts/screengrab.py watch --count 5   # stop after N captures
```

## Typical Agent Workflow

```bash
# Grab screen and analyze with image tool
path=$(python3 scripts/screengrab.py snap --quiet)
# Then pass $path to image analysis
```
