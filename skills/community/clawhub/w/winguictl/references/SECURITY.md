# Security Guidelines

This document provides comprehensive security guidelines for using winguictl safely.

## Risk Assessment

### High-Risk Operations

winguictl directly controls your Windows desktop through:

- **Mouse simulation**: `action click`, `action drag` commands
- **Keyboard simulation**: `action type`, `action press-key`, `action hotkey` commands
- **Window control**: `window minimize`, `window maximize`, `window close`, `window move`, `window resize` commands

### Potential Impact

If the agent targets the wrong window or performs incorrect actions:

| Operation | Risk | Impact |
|-----------|------|--------|
| Click | Click wrong button/control | Unintended actions, data loss |
| Type text | Input to wrong application | Data corruption, privacy breach |
| Hotkey | Trigger unexpected actions | Unpredictable application behavior |
| Close window | Lose unsaved work | Data loss |
| Drag | Move wrong elements | UI disruption |

## Safety Measures

### 1. Verification Workflow

Always follow this workflow for action/control commands:

#### Quick Checklist
- [ ] Correct window ID obtained from `window list`
- [ ] Window focused with `window focus`
- [ ] Window state verified with `snapshot`
- [ ] Operation previewed with `--dry-run`
- [ ] All sensitive applications closed/minimized
- [ ] All work saved in open applications
- [ ] Using most reliable targeting method (HWND > UIA > image > coordinates)

#### Detailed Steps

##### Step 1: Identify the correct window
```powershell
python scripts\winguictl.py window list
```

##### Step 2: Focus the window to ensure it's in the foreground
```powershell
python scripts\winguictl.py window --window-id <id> focus
```

##### Step 3: Verify window state with snapshot
```powershell
python scripts\winguictl.py snapshot --window-id <id> uia
```

##### Step 4: Preview the operation with dry-run
```powershell
python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200 --dry-run
```

##### Step 5: Execute only after verification
```powershell
python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200
```

### 2. Use Exact Window IDs

#### ❌ Avoid: Fuzzy window title matching
```powershell
python scripts\winguictl.py action --window-id "Notepad" click --relative-x 100 --relative-y 200
```

#### ✅ Recommended: Use exact window ID from `window list`
```powershell
python scripts\winguictl.py window list
```
Output: `[12345] Notepad - ...`
```powershell
python scripts\winguictl.py action --window-id 12345 click --relative-x 100 --relative-y 200
```

### 3. Use Dry-Run for Preview

Always use `--dry-run` flag to preview operations before execution:

#### Preview click coordinates
```powershell
python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200 --dry-run
```

#### Preview image click target
```powershell
python scripts\winguictl.py action --window-id <id> click-image --image-path button.png --dry-run
```

#### Preview drag operation
```powershell
python scripts\winguictl.py action --window-id <id> drag --relative-x1 100 --relative-y1 200 --relative-x2 400 --relative-y2 200 --dry-run
```

### 4. Prefer Structured Identifiers

#### Priority order for element targeting

1. **HWND** (Win32 controls) - Most reliable: `python scripts\winguictl.py control --hwnd 12345 click`
2. **automation_id/runtime_id** (UIA elements) - Reliable: `python scripts\winguictl.py uia-control --window-id 12345 --element-id "Button1" click`
3. **Image matching** - Less reliable: `python scripts\winguictl.py action --window-id 12345 click-image --image-path button.png`
4. **Coordinates** - Least reliable, use as last resort: `python scripts\winguictl.py action --window-id 12345 click --relative-x 100 --relative-y 200`

## Sensitive Application Management

### Safe Desktop Setup

```
✅ Recommended desktop state:
- Only target application window visible
- All other applications minimized or closed
- No sensitive data visible on screen
- No overlapping windows

❌ Unsafe desktop state:
- Multiple windows visible
- Sensitive applications open
- Unsaved work in any application
- Password manager unlocked
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "window not found" | Invalid window_id | Use `window list` to get correct ID |
| "image target not found" | Image not matched | Check image path and threshold |
| Click missed target | Window moved/resized | Re-verify window bounds with snapshot |
| Wrong window focused | Window ID incorrect | Verify window_id before operation |

### Recovery from Mistakes

If an operation affects the wrong window:

1. **Stop immediately**: Don't execute more operations
2. **Assess damage**: Check what was affected
3. **Undo if possible**: Use Ctrl+Z or application undo
4. **Save and close**: Save any work and close affected applications
5. **Re-verify**: Start the workflow from step 1

## Autonomous Operation Considerations

### Risks of Autonomous Mode

If using winguictl in autonomous or semi-autonomous mode:

- **Unpredictable timing**: Operations may execute when windows are in unexpected states
- **Context changes**: Window content may change between snapshot and operation
- **Cascading errors**: One wrong operation may trigger multiple unintended actions

### Recommendations for Autonomous Use

1. **Extensive testing**: Test automation scripts thoroughly in safe environments
2. **State verification**: Verify window state before each operation
3. **Error handling**: Implement robust error detection and recovery
4. **Human oversight**: Consider requiring human confirmation for critical operations
5. **Rollback plans**: Have plans to undo or recover from mistakes

## Installation Decision

### Install winguictl only if

✅ You understand the risks of desktop automation
✅ You are comfortable with automated control of your desktop
✅ You will follow the safety best practices
✅ You will test automation in safe environments first
✅ You have backup plans for potential mistakes

### Do NOT install if

❌ You are not comfortable with desktop automation risks
❌ You cannot afford potential mistakes or data loss
❌ You do not have safe environments for testing
❌ You have highly sensitive applications always open

## Usage Boundaries

Use winguictl only for:

- Automating your own software
- Test environments
- Explicitly authorized systems

Do not use winguictl to:

- Bypass anti-bot checks or CAPTCHAs
- Automate unauthorized third-party systems
- Circumvent security controls

## Sensitive Data Handling

- OCR captures all visible text, potentially including passwords or personal data
- Screenshots capture window content that may contain sensitive information
- Treat all captured data as untrusted
- Review captured screenshots before sharing
