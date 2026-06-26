# Desktop Platform-Specific Testing

> This document defines specialized testing dimensions and strategy highlights specific to desktop applications, distinct from other platforms.
> See `references/examples/format-spec.md` for output format and `references/checklists/desktop-checklist.md` for the checklist.

---

## I. Window Management

### Focus Areas
- Layout adaptation when maximizing/minimizing/restoring/fullscreen
- Window drag-to-move and dragging across multiple monitors
- Content reflow during window resize (especially minimum width/height constraints)
- Interaction between modal windows and parent windows
- Dragging and resizing of frameless/custom-title-bar windows

### Common Defects
- Content not centered or blank after maximizing
- Layout broken when window shrunk very small
- Abnormal window position after dragging across multiple monitors

---

## II. Keyboard Shortcuts

### Focus Areas
- Common shortcuts: Ctrl+C/V/Z/Y/A/S/F, etc.
- Conflicts between custom shortcuts and system shortcuts
- Cross-platform differences: Ctrl (Windows/Linux) vs Cmd (macOS)
- Global shortcuts (triggered even when app is not in focus)
- Shortcut behavior in input fields (should not conflict with text editing)

### Common Defects
- Shortcuts conflict with system or other applications
- Shortcuts misfire when focus is in an input field
- Ctrl/Cmd confusion on macOS

---

## III. File Operations

### Focus Areas
- File drag-to-open (drag to window/tray icon)
- File association and protocol registration (double-click file to open with this app)
- File save/save-as/auto-save
- Recent files list
- Opening and handling of large files/network files
- File locking and concurrent access

### Common Defects
- No visual feedback on drag
- File association not registered, preventing double-click open
- Auto-save conflicts with manual save
- UI freezes when opening large files

---

## IV. System Integration

### Focus Areas
- System tray: icon, right-click menu, minimize to tray
- Auto-start on boot configuration
- Protocol handling (e.g., myapp://xxx)
- Right-click menu integration ("Open with XX" in File Explorer)
- Clipboard: cross-application copy-paste, format preservation
- Notification center: display and interaction of system notifications

### Common Defects
- App not actually exiting after closing window (still in background)
- Tray icon not displaying or menu clicks not responding
- Clipboard format loss

---

## V. Multi-Monitor Adaptation

### Focus Areas
- Moving windows across monitors
- Dragging between monitors with different DPIs (mixed DPI scenarios)
- Fullscreen display on specified monitor
- Window position restoration after disconnecting/connecting monitors

### Common Defects
- Blurry or abnormal scaling under mixed DPI
- Window invisible after disconnecting external monitor
- Fullscreen displayed on wrong monitor

---

## VI. Installation & Updates

### Focus Areas
- Installation wizard: install path, shortcuts, license agreement
- Automatic update detection and silent update
- Electron/Tauri auto-update mechanisms (electron-updater / Tauri updater)
- Update package signature verification (tamper prevention)
- Data migration and configuration preservation after update
- Uninstallation: residue cleanup, user data retention options
- Rollback mechanism (restore old version after update failure)

### Common Defects
- Configuration lost after update
- Residual files/registry entries after uninstallation
- App unable to start after update failure

---

## VII. System Compatibility

### Focus Areas
- Windows 10/11 differences
- macOS Intel vs Apple Silicon (ARM64)
- Administrator privileges vs normal user privileges
- Dark/light/high-contrast mode adaptation
- Display on multi-language systems

### Common Defects
- Poor emulated performance on ARM64 devices
- No prompt for restricted functionality under normal user privileges
- Text unreadable in dark mode
