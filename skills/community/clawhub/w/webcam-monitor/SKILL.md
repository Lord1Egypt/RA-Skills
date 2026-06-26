---
name: webcam-monitor
description: Webcam motion detection and monitoring system for WSL2 with USB/IP passthrough. Use when setting up motion detection on a USB webcam, monitoring camera snapshots, auto-analyzing images with AI, or managing webcam-based security/activity monitoring. Supports Insta360 Link and other UVC cameras via usbipd on Windows.
---

# Webcam Monitor

Complete webcam motion detection and monitoring system for WSL2 environments.

## Overview

This skill provides:
- Motion detection with automatic snapshot capture
- Real-time folder monitoring with auto-analysis queue
- Web-based live preview (port 8081)
- Auto-cleanup of old snapshots (1 hour default)
- Person identification via AI image analysis

## Prerequisites

**Windows Side (PowerShell as Admin):**
```powershell
winget install usbipd
usbipd list
usbipd bind --busid=1-4
usbipd attach --wsl --busid=1-4
```

**WSL2 Side:**
```bash
ls /dev/video*  # Should show /dev/video0
```

**Note:** If `/dev/video*` does not appear, you may need to **restart WSL2**:
```powershell
# In Windows PowerShell:
wsl --shutdown
# Then re-attach the camera:
usbipd attach --wsl --busid=1-4
```

## Quick Start

### 1. Start Motion Detection
```bash
python3 scripts/motion_detector_headless.py
```
- Runs in background (no GUI)
- Saves snapshots to `~/.openclaw/workspace/camera/snapshots/`
- Logs to `~/.openclaw/workspace/camera/motion.log`

### 2. Start Folder Monitor with Auto-Cleanup
```bash
python3 scripts/watcher_with_cleanup.py
```
- Monitors for new snapshots every 2 seconds
- Auto-deletes snapshots older than 1 hour (every 5 minutes)
- Queues new images for analysis
- Logs to `~/.openclaw/workspace/camera/watcher.log`

### 3. Start Web Preview (Optional)
```bash
python3 scripts/web_preview.py
```
- Opens web server on port 8081
- View at http://localhost:8081
- **Note:** Stop motion detection first — camera can only be used by one program

## Configuration

Edit `scripts/motion_detector_headless.py`:
- `MOTION_THRESHOLD` — Sensitivity (lower = more sensitive, default: 25)
- `MIN_CONTOUR_AREA` — Minimum motion area (default: 500)
- `SNAPSHOT_COOLDOWN` — Seconds between snapshots (default: 5)
- `MAX_AGE_HOURS` — Auto-cleanup threshold (default: 1)

## Scripts

| Script | Purpose |
|--------|---------|
| `motion_detector_headless.py` | Background motion detection daemon |
| `watcher_with_cleanup.py` | Folder monitor + auto-cleanup + analysis queue |
| `web_preview.py` | Web-based live preview (port 8081) |
| `snapshot.sh` | Quick manual snapshot |
| `cleanup.py` | Manual cleanup of old snapshots |

## File Locations

- **Snapshots:** `~/.openclaw/workspace/camera/snapshots/`
- **Logs:** `~/.openclaw/workspace/camera/motion.log`
- **Watcher Log:** `~/.openclaw/workspace/camera/watcher.log`
- **Analysis Queue:** `~/.openclaw/workspace/camera/analysis_queue/`

## Troubleshooting

### "Could not open camera"
```bash
# Check USB passthrough
ls /dev/video*
```

**If no video devices appear, restart WSL2:**
```powershell
# In Windows PowerShell:
wsl --shutdown
# Then re-attach the camera:
usbipd attach --wsl --busid=1-4
```

**Then verify in WSL2:**
```bash
ls /dev/video*  # Should now show /dev/video0
```

### Permission denied
```bash
sudo chmod 666 /dev/video0
```

### Camera in use
Only one program can use the camera at a time:
```bash
# Stop motion detection
pkill -f motion_detector

# Stop web preview
pkill -f web_preview

# Stop watcher
pkill -f watcher
```

## Person Identification

The watcher can queue snapshots for AI analysis. To identify people:

1. Update `MEMORY.md` with person details:
```markdown
### Webcam Identification
- **Person:** [Name]
- **Appearance:** [Description - include hair, jewelry, clothing, wigs if applicable]
- **Setting:** [Location details]
```

**Example:**
```markdown
### Webcam Identification
- **Person:** Jade
- **Appearance:** Middle-aged, light-colored/graying hair (short, receding), often wears star-shaped pendant necklace, sometimes in bathrobe/robe when at desk, sometimes wears shoulder-length hair wig
- **Setting:** Home office with black mesh chair, cat tree, bookshelves
```

2. Analyze queued images using the image tool with qwen model

## Auto-Cleanup

By default, snapshots older than 1 hour are automatically deleted every 5 minutes.

To change:
- Edit `CLEANUP_INTERVAL` in `watcher_with_cleanup.py` (seconds)
- Edit `MAX_AGE_HOURS` in `watcher_with_cleanup.py` (hours)

## Integration with OpenClaw

The watcher creates queue files in `analysis_queue/` that can trigger automatic image analysis by the main agent. Check for new queue files and analyze with:

```python
# Example: Check queue and analyze
queue_dir = Path.home() / ".openclaw/workspace/camera/analysis_queue"
for queue_file in queue_dir.glob("analyze_*.txt"):
    image_path = queue_file.read_text().strip()
    # Analyze image with image tool
```