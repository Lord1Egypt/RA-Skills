---
name: windows-native-dialog
version: 1.0.0
description: "Handles native Windows file picker dialogs from WSL2 using exec and PowerShell"
tags:
  - windows
  - wsl2
  - file-upload
  - powershell
  - facebook
---

# windows-native-dialog

Teaches OpenClaw how to handle native Windows file picker dialogs invisible to browser-automation.

## Requirements

openclaw config set tools.allow '["browser","group:runtime","group:fs","group:web"]'

## Prompt

STEP 1 - browser-automation: click upload button.
STEP 2 - exec: /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "python C:\path\to\script.py video.mp4"
STEP 3 - browser-automation: click Publish.

## Tested

Meta Business Suite on Windows 10 + WSL2. Result: success.
Related: Issue #52525, PR #39407 — author @owlock
## Skills comparison — desktop automation for Windows + WSL2

| Skill | Autonomy | OS | Best for |
|---|---|---|---|
| clawd-cursor | 95% | Win/Mac/Linux | Full desktop — sees screen + acts |
| matagul/desktop-control | 75% | Windows native | Mouse + keyboard via pyautogui |
| desktop-computer-automation | 70% | Win/Mac | Desktop screenshot + native windows |
| pc-control | 65% | Win + WSL2 | FastAPI bridge WSL2 ↔ Windows |
| browser-automation | 60% | All | Browser-only via CDP |
| owlock/windows-native-dialog | 55% | Win + WSL2 | exec+PowerShell workaround |

Note: matagul/desktop-control requires OpenClaw native on Windows.
clawd-cursor is the most autonomous option for Windows users.
