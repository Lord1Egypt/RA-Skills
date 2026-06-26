# winguictl

Windows desktop automation CLI tool built on pywinauto and pywin32.

## Features

- **Window Management** — List, focus, minimize, maximize, restore, close, move, and resize desktop windows
- **Structure Snapshots** — Capture HWND tree, UIA tree, or OCR text regions of any window
- **Element Finding** — Locate UI elements by text, UIA properties, OCR, or image matching
- **Interaction Actions** — Click, drag, type text, press keys, and trigger hotkeys
- **Control Operations** — Directly manipulate Win32 controls (checkbox, combobox, etc.) and UIA elements (scroll, expand/collapse, slider, etc.)
- **Screenshot Capture** — Capture full window or rectangular region screenshots

## Installation

### Prerequisites

- Python 3.10 or higher
- Windows operating system

### Install Dependencies

```powershell
pip install -r requirements.txt
```

## Quick Start

```powershell
# List all visible windows
python scripts\winguictl.py window list

# Focus a window
python scripts\winguictl.py window --window-id <id> focus

# Take a UIA snapshot of a window
python scripts\winguictl.py snapshot --window-id <id> uia

# Click a UIA element
python scripts\winguictl.py uia-control --window-id <id> --element-id <elem_id> click

# Type text into a window
python scripts\winguictl.py action --window-id <id> type --text "Hello World"

# Take a screenshot
python scripts\winguictl.py screenshot --window-id <id> --output shot.png
```

## Documentation

- [SKILL.md](SKILL.md) — Complete skill documentation with workflow and security guidelines
- [AGENTS.md](AGENTS.md) — Architecture and development best practices
- [references/](references/) — Detailed command reference documentation

## License

MIT
