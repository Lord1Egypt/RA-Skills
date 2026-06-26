---
name: winguictl
description: Windows desktop automation CLI. Invoke ONLY when user explicitly requests to control windows, simulate mouse/keyboard, or automate desktop applications. Do NOT proactively suggest using this skill.
metadata:
  openclaw:
    emoji: "🖥️"
    os: ["win32"]
    requires:
      bins: ["python3"]
---

# Windows Desktop Automation with winguictl

## ⚠️ Security Notice

This skill directly controls Windows desktop through mouse/keyboard simulation. **Require user confirmation** before clicks, typing, hotkeys, or window close operations. Use `--dry-run` to preview. Close sensitive apps before use.

## Script Path

```powershell
python <SKILL_DIR>\scripts\winguictl.py <command> [options]
```

## Commands

| Command | Purpose | Documentation |
|---------|---------|---------------|
| `window` | List/focus/minimize/maximize/close windows | [window.md](references/window.md) |
| `snapshot` | Get HWND/UIA/OCR structure | [snapshot.md](references/snapshot.md) |
| `find` | Find elements by text/UIA/OCR/image | [find.md](references/find.md) |
| `action` | Click/drag/type/scroll/hotkey | [action.md](references/action.md) |
| `control` | Win32 control operations | [control.md](references/control.md) |
| `uia-control` | UIA element operations | [control.md](references/control.md) |
| `screenshot` | Capture window screenshots | [screenshot.md](references/screenshot.md) |
| `wait` | Wait for conditions | [wait.md](references/wait.md) |
| `clipboard` | Copy files/text, get text | [clipboard.md](references/clipboard.md) |

## Parameter Types

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `--window-id` | int | `--window-id 12345` | Window handle from `window list` |
| `--hwnd` | int | `--hwnd 67890` | Win32 control handle |
| `--element-id` | string | `--element-id "Button1"` | automation_id or runtime_id (**prefer runtime_id**) |

## Core Workflow

```powershell
# 1. Identify window
python scripts\winguictl.py window list

# 2. Focus window
python scripts\winguictl.py window --window-id <id> focus

# 3. Get snapshot
python scripts\winguictl.py snapshot --window-id <id> uia

# 4. Find & interact
python scripts\winguictl.py find --window-id <id> uia --text "Submit"
python scripts\winguictl.py uia-control --window-id <id> --element-id <elem_id> click

# 5. Verify (re-snapshot)
python scripts\winguictl.py snapshot --window-id <id> uia
```

## Decision Guide

### Locator Priority

| Priority | Method | Command | Reliability |
|----------|--------|---------|-------------|
| 1 | HWND (Win32) | `control --hwnd <hwnd> click` | Highest |
| 2 | runtime_id (UIA) | `uia-control --element-id <id> click` | High |
| 3 | automation_id (UIA) | `uia-control --element-id <id> click` | Medium |
| 4 | Image matching | `action click-image --image-path <path>` | Medium |
| 5 | Coordinates | `action click --relative-x/y` | Lowest |

### Click Method Selection

| Command | Mechanism | Best For |
|---------|-----------|----------|
| `action click --element-id` | Mouse simulation at center | **WeChat, custom controls** |
| `uia-control click` | UIA InvokePattern | Standard Windows controls, WinUI3 |

**Recommendation**: Try `uia-control click` first. If no effect, use `action click --element-id`.

### Common Scenarios

| Scenario | Command |
|----------|---------|
| Win32 control with hwnd | `control --hwnd <hwnd> click` |
| UIA element with runtime_id | `uia-control --element-id "42-3155764" click` |
| Text-based element | `find ocr "text"` → `action click --element-id` |
| Qt applications | Add `--skip-actions --skip-state` for faster UIA |

## Key Rules

- **Re-snapshot after actions**: UI state changes after clicks/typing
- **Use `--dry-run`**: Preview operations before execution
- **Prefer runtime_id**: More reliable than automation_id
- **Report window_id**: Always include exact window identifier in results
- **Coordinate system**: `relative_rect` = window-relative; `absolute_rect` = screen-absolute

## Application Guides

- [WeChat Automation](assets/wechat/wechat.md) — WeChat 4.1.6+ messaging, contacts, files, calls, Moments

## References

- [Dependencies](references/dependencies.md) — pywinauto, pywin32, Pillow, wx-ocr (optional)
- [Output Format](references/output-format.md) — JSON structure, exit codes, boundary markers
- [Coordinates](references/coordinates.md) — Coordinate system details
- [Security Guidelines](references/SECURITY.md) — Detailed safety practices
