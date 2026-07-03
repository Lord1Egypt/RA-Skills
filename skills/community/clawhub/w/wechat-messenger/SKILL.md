---
name: wechat-messenger
description: "Send WeChat messages via direct Win32 API. ~2s per message."
version: 2.0.0
author: "曙光 (Dawn) — 致敬 screen_util.exe 原作者"
---

# WeChat Messenger v2.0

## Quick Start

```bash
python scripts/send.py "contact_name" "your message"
```

Example:
```bash
python scripts/send.py "枫林" "你好"
```

Target speed: < 3s. Zero screenshots, zero OCR, zero external EXEs.

## How It Works

Single Python script, direct Win32 API:

1. `win32gui.EnumWindows` → find WeChat window
2. `SetForegroundWindow` → activate
3. `GetWindowRect` → get coordinates
4. `SetCursorPos` + `mouse_event` → click search box
5. `SendInput` (Ctrl+A, Ctrl+V, Enter) → type contact
6. Sleep 0.8s → wait for chat pane
7. Click input box → paste message → Enter

## Speed: v1.0 vs v2.0

| | v1.0 (screen_util.exe) | v2.0 (Win32 API) |
|---|----------------------|-------------------|
| External calls | ~10 | 0 |
| Screenshots | 3 | 0 |
| Total time | ~20s | ~2s |

## Prerequisites

- WeChat PC running + logged in
- `pip install pywin32 pyperclip`

## Credits

v1.0: GUI automation via screen_util.exe (screenshot + OCR + coordinate click)
v2.0: Dawn rewrote with direct Win32 API — 10x faster. 致敬 screen_util.exe 原始作者.
