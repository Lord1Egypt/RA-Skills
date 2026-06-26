---
name: ring-doorbell
description: Control and monitor Ring doorbells and cameras. List devices, capture snapshots, view events. Use when user asks about their Ring cameras, doorbell activity, or wants to see live snapshots.
license: MIT
metadata:
  openclaw:
    requires:
      bins: [python3, ffmpeg]
      pips: [ring-doorbell]
---

# Ring Doorbell & Camera Control

Monitor and control Ring devices from your AI assistant.

## Features

- 📷 Capture snapshots from any Ring camera or doorbell
- 📋 List all devices with battery status
- 📹 View recent doorbell events and motion history
- 🔋 Monitor battery levels

## Setup

### 1. Install Dependencies

```bash
pip3 install ring-doorbell
```

Note: `ffmpeg` is required for video frame extraction on some doorbell models.

### 2. Authenticate

First time setup requires authentication with 2FA:

```bash
python3 <skill_dir>/ring_tool.py auth
```

Token will be saved to `~/.openclaw/ring_token.json` and auto-refresh.

## Usage

### List All Devices

```bash
python3 <skill_dir>/ring_tool.py list
```

Returns JSON with device name, type, battery level, and online status.

### Capture Snapshot

```bash
python3 <skill_dir>/ring_tool.py snapshot "前门门铃"
```

Device name supports partial/fuzzy match. Returns path to saved image.

### View Recent Events

```bash
python3 <skill_dir>/ring_tool.py events --limit 10
python3 <skill_dir>/ring_tool.py events --device "车库门铃"
```

## When to Use This Skill

- "看一下前门的摄像头"
- "拍一张后院的照片"
- "门铃最近有没有人按？"
- "所有设备电量多少？"
- "车库门摄像头状态"

## Notes

- Token auto-refreshes; re-run auth if it expires
- Snapshots require device to be online
- Some doorbell models may not support live snapshot (uses video frame instead)
- Images saved to `~/.openclaw/media/ring/`

## Credits

Built with [ring-doorbell](https://github.com/tchellomello/python-ring-doorbell) Python library.
