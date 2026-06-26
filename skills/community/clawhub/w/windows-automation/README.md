# windows-automation

Windows desktop automation skill for OpenClaw.

## Features

 using PyAutoGUI- 🖱️ **Mouse Control**: Click, double-click, right-click, move, drag
- ⌨️ **Keyboard Control**: Type text, press keys, hotkeys
- 📸 **Screen Operations**: Screenshot capture
- 📋 **Clipboard**: Read and write clipboard content
- 🪟 **App Launch**: Launch Windows applications
- 💻 **Command Execution**: Run PowerShell/CMD commands
- ℹ️ **System Info**: Get cursor position, screen size, system details

## Installation

```bash
pip install pyautogui pywin32 pyperclip
```

## Usage Examples

```
# Click at position
windows_click x=500 y=300

# Open calculator
windows_launch_app name="calc"

# Copy selected text
windows_hotkey ctrl c

# Take a screenshot
windows_screenshot

# Get cursor position
windows_cursor_position

# Run ipconfig
windows_command ipconfig
```

## Tools

| Tool | Description |
|------|-------------|
| `windows_click` | Click at coordinates |
| `windows_double_click` | Double click |
| `windows_right_click` | Right click |
| `windows_move` | Move mouse |
| `windows_type` | Type text |
| `windows_press` | Press a key |
| `windows_hotkey` | Keyboard shortcut |
| `windows_scroll` | Scroll wheel |
| `windows_screenshot` | Take screenshot |
| `windows_cursor_position` | Get cursor position |
| `windows_screen_size` | Get screen resolution |
| `windows_launch_app` | Launch app |
| `windows_command` | Run command |
| `windows_clipboard_read` | Read clipboard |
| `windows_clipboard_write` | Write clipboard |
| `windows_system_info` | System information |

## License

MIT
