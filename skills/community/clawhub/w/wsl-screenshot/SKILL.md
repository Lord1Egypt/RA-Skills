---
name: wsl-screenshot
description: "Capture screenshots from WSL by calling Windows PowerShell. Use when user wants to take a screenshot from WSL environment, or needs screenshot functionality in WSL. Works on WSL2 by invoking Windows PowerShell to capture the primary screen."
---

# WSL Screenshot

Capture screenshots from WSL using Windows PowerShell.

## Usage

### Take a Screenshot

```bash
# Run the screenshot script
~/.openclaw/workspace/skills/wsl-screenshot/scripts/screenshot.sh

# Output: C:\Users\97027\Pictures\wsl_screenshot_YYYYMMDD_HHMMSS.png
```

### Send Screenshot to User

After taking a screenshot, send it via message:

```bash
# Get the latest screenshot path
LATEST=$(ls -t /mnt/c/Users/97027/Pictures/wsl_screenshot_*.png | head -1)

# Send via message tool
message action=send media="$LATEST" caption="📸 Screenshot"
```

Or use direct path:
```bash
message action=send media="/mnt/c/Users/97027/Pictures/wsl_screenshot_YYYYMMDD_HHMMSS.png"
```

## Requirements

- WSL2 with Windows 10/11
- PowerShell available at `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`

## Resources

- `scripts/screenshot.sh` - Screenshot script