# Desktop Test Points

> This file defines the test dimensions and strategy points that distinguish desktop applications from other platforms.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/desktop-checklist.md`.

---

## 1. Window Management

### Key focus points
- Layout adaptation when maximizing / minimizing / restoring / going full screen
- Dragging windows, including between multiple monitors
- Content reflow when resizing windows (especially minimum width / height limits)
- Interaction between modal windows and their parent window
- Dragging and resizing windows without a title bar / with a custom-drawn title bar

### Common defects
- Content not centered or blank areas after maximizing
- Layout broken when the window is made very small
- Abnormal window position after dragging across monitors

---

## 2. Keyboard Shortcuts

### Key focus points
- Common shortcuts: Ctrl+C/V/Z/Y/A/S/F, etc.
- Conflicts between custom shortcuts and system shortcuts
- Cross-platform differences: Ctrl (Windows/Linux) vs Cmd (macOS)
- Global shortcuts (triggered even when the app is not in focus)
- Shortcut behavior in input boxes (must not conflict with text editing)

### Common defects
- Shortcuts conflict with the system or other apps
- Shortcuts triggered by mistake while focus is in an input box
- Ctrl / Cmd confused on macOS

---

## 3. File Operations

### Key focus points
- Opening files by drag and drop (onto the window / tray icon)
- File associations and protocol registration (double-clicking a file opens it in this app)
- Save / Save As / autosave
- Recent files list
- Opening and handling large files / network files
- File locking and concurrent access

### Common defects
- No visual feedback while dragging
- File association not registered, so double-clicking does not open the file
- Conflicts between autosave and manual save
- UI freezes when opening large files

---

## 4. System Integration

### Key focus points
- System tray: icon, context menu, minimize to tray
- Launch at startup setting
- Protocol handling (e.g., myapp://xxx)
- Context menu integration ("Open with XX" in File Explorer)
- Clipboard: copy and paste across apps, format retention
- Notification center: display and interaction of system notifications

### Common defects
- The app does not actually exit after closing the window (still running in the background)
- Tray icon not shown or menu clicks unresponsive
- Clipboard formatting lost

---

## 5. Multi-Monitor Adaptation

### Key focus points
- Moving windows across monitors
- Dragging between monitors with different DPI (mixed-DPI scenarios)
- Full-screen mode on a specified monitor
- Window position restored after disconnecting / connecting a monitor

### Common defects
- Blurry UI or abnormal scaling with mixed DPI
- Window invisible after disconnecting an external monitor
- Full screen shown on the wrong monitor

---

## 6. Installation and Updates

### Key focus points
- Installation wizard: install path, shortcuts, license agreement
- Automatic update detection and silent updates
- Electron / Tauri auto-update mechanisms (electron-updater / Tauri updater)
- Update package signature verification (tamper protection)
- Data migration and configuration retention after updates
- Uninstallation: cleanup of leftovers, option to keep user data
- Rollback mechanism (restore the old version after an update fails)

### Common defects
- Configuration lost after updating
- Leftover files / registry entries after uninstalling
- The app cannot start after a failed update

---

## 7. System Compatibility

### Key focus points
- Differences between Windows 10 and 11
- macOS Intel vs Apple Silicon (ARM64)
- Administrator vs standard user permissions
- Dark / light / high-contrast mode adaptation
- Display on systems in different languages

### Common defects
- Poor performance under translation on ARM64 devices
- Features restricted under standard user permissions without any prompt
- Text unreadable in dark mode
