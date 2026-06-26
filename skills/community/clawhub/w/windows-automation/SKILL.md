# Windows Automation Skill

> Automate Windows desktop interactions using PyAutoGUI

## Overview

This skill provides comprehensive Windows desktop automation capabilities. Use it when you need to:
- Simulate mouse clicks and keyboard input
- Automate GUI interactions in non-web applications
- Capture screenshots
- Manage clipboard content
- Launch applications
- Run system commands

## Setup

The required packages are already installed:
- `pyautogui` - Core automation engine
- `pywin32` - Windows API access
- `pyperclip` - Clipboard operations

If needed, install manually:
```bash
pip install pyautogui pywin32 pyperclip
```

---

## Tools

### 🖱️ Mouse Control

#### `windows_click`
Click at specified screen coordinates.

```python
windows_click(x=100, y=200, button="left", clicks=1)
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `x` | float | required | X coordinate |
| `y` | float | required | Y coordinate |
| `button` | str | "left" | "left", "right", "middle" |
| `clicks` | int | 1 | Number of clicks |

---

#### `windows_double_click`
Double click at position.

```python
windows_double_click(x=500, y=300)
```

---

#### `windows_right_click`
Right click at position.

```python
windows_right_click(x=100, y=200)
```

---

#### `windows_move`
Move mouse to position.

```python
windows_move(x=800, y=600, duration=0.5)
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `x` | float | required | X coordinate |
| `y` | float | required | Y coordinate |
| `duration` | float | 0.2 | Movement duration in seconds |

---

### ⌨️ Keyboard Control

#### `windows_type`
Type text using keyboard.

```python
windows_type(text="Hello World!", interval=0.05)
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | str | required | Text to type |
| `interval` | float | 0.05 | Delay between keystrokes |

---

#### `windows_press`
Press a single key.

```python
windows_press(key="enter")
```

**Supported keys:**
- Function keys: `f1` - `f24`
- Special keys: `enter`, `esc`, `tab`, `space`, `backspace`, `delete`
- Arrow keys: `up`, `down`, `left`, `right`
- Modifiers: `ctrl`, `alt`, `shift`, `win`

---

#### `windows_hotkey`
Press keyboard shortcut combination.

```python
windows_hotkey("ctrl", "c")   # Copy
windows_hotkey("ctrl", "v")   # Paste
windows_hotkey("alt", "f4")   # Close window
windows_hotkey("win", "r")    # Open Run dialog
```

---

### 📸 Screen Operations

#### `windows_screenshot`
Take a screenshot.

```python
windows_screenshot(filename="screenshot.png")
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `filename` | str | "screenshot.png" | Filename to save |

---

### ℹ️ Information

#### `windows_cursor_position`
Get current cursor position.

```python
windows_cursor_position()
# Returns: {"x": 500, "y": 300}
```

---

#### `windows_screen_size`
Get screen resolution.

```python
windows_screen_size()
# Returns: {"width": 1920, "height": 1080}
```

---

#### `windows_system_info`
Get basic system information.

```python
windows_system_info()
# Returns: {
#   "platform": "Windows",
#   "version": "10.0.22631",
#   "screen_size": {"width": 1920, "height": 1080},
#   "cursor_position": {"x": 500, "y": 300}
# }
```

---

### 🪟 Applications

#### `windows_launch_app`
Launch a Windows application.

```python
windows_launch_app(name="notepad")
windows_launch_app(name="calc")
windows_launch_app(name="excel")
windows_launch_app(name="C:\\Program Files\\App\\app.exe")
```

---

### 💻 System

#### `windows_command`
Run a PowerShell or cmd command.

```python
windows_command(command="ipconfig")
windows_command(command="Get-Process | Select-Object -First 5")
windows_command(command="dir C:\\")
```

---

### 📋 Clipboard

#### `windows_clipboard_read`
Read clipboard content.

```python
windows_clipboard_read()
# Returns: "clipboard content"
```

---

#### `windows_clipboard_write`
Write text to clipboard.

```python
windows_clipboard_write(text="Hello from OpenClaw!")
```

---

## Usage Examples

### Example 1: Open Notepad and Type Text

```
User: Open notepad and type hello
→ windows_launch_app with name="notepad"
→ windows_type with text="Hello World!"
```

### Example 2: Fill a Form

```
User: Click on the name field and enter John
→ windows_click x=300 y=200
→ windows_type text="John"
→ windows_press key="tab"
→ windows_type text="john@example.com"
```

### Example 3: Screenshot and Save

```
User: Take a screenshot
→ windows_screenshot filename="screen_20260101.png"
```

### Example 4: Copy File Path

```
User: Copy C:\Documents\file.txt to clipboard
→ windows_clipboard_write text="C:\\Documents\\file.txt"
```

### Example 5: Get System Info

```
User: What's my screen resolution?
→ windows_screen_size
```

---

## Safety Notes

- ⚠️ The mouse failsafe is disabled for smoother operation
- 📍 Screen coordinates start at (0, 0) in top-left corner
- 🖥️ Multi-monitor setups may have different coordinate systems
- 🔒 Some applications may block simulated input (games, secure apps)

---

## Dependencies

| Package | Purpose |
|---------|---------|
| pyautogui | Core automation |
| pywin32 | Windows API |
| pyperclip | Clipboard |

---

**Built for OpenClaw** 🦞
