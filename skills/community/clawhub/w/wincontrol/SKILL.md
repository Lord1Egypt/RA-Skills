---
name: wincontrol
description: AI remote control for Windows desktop. Captures screen on-demand via POST request and provides an HTTP API for mouse/keyboard actions.
---

# WinControl Skill

AI remote control for Windows desktop. Captures screen on-demand via POST request and provides an HTTP API for mouse/keyboard actions.

## What It Does

- **On-Demand Capture**: POST to `/capture` to save screenshot, returns file path
- **Action API**: Control mouse and keyboard via HTTP endpoints on port 8767
- **Auto-Cleanup**: Deletes screenshot on server shutdown (Ctrl+C)
- **Cross-Platform**: Works on native Windows or WSL
- **Self-Contained**: Single `screenshot.jpg` saved in skill folder, overwritten each time, auto-deleted on exit

## Quick Start

### Option 1: Native Windows (Recommended)

Run directly on Windows without WSL:

```powershell
# Install dependencies (one-time)
pip install pywin32 pillow mss

# Start the server
cd %USERPROFILE%\.openclaw\workspace\skills\wincontrol
python server.py
```

Or use the provided batch file:
```powershell
.\start.bat
```

Screenshots are saved as `screenshot.jpg` in the skill directory and auto-deleted when the server stops.

### Option 2: WSL Integration

If you prefer WSL, the server runs on Windows Python but can be controlled from WSL:

```bash
# From WSL
cd ~/.openclaw/workspace/skills/wincontrol
./start.sh
```

Or start manually with PowerShell 7:
```bash
'/mnt/c/Program Files/PowerShell/7/pwsh.exe' -Command \
  "python //wsl.localhost/Ubuntu/home/\$USER/.openclaw/workspace/skills/wincontrol/server.py" &
```

## Verify Installation

```bash
# Health check
curl http://localhost:8767/ping
# Output: {"ok": true}

# Capture a screenshot
curl -X POST http://localhost:8767/capture
# Output: {"ok": true, "path": ".../screenshot.jpg"}
```

**Native Windows**: Open `screenshot.jpg` in the skill directory

**WSL**: Access via the skill folder path

## File Structure

```
skills/wincontrol/
├── SKILL.md            # This file
├── server.py           # Main server (runs on Windows)
├── start.bat           # Start script (Native Windows)
├── start.sh            # Start script (WSL)
├── stop.sh             # Stop script (WSL)
└── screenshot.jpg      # Latest screenshot (auto-created, auto-cleaned)
```

## API Reference

### Capture Screen
```bash
curl -X POST http://localhost:8767/capture
```
Returns: `{"ok": true, "path": ".../screenshot.jpg", "quality": 90}`

Each capture overwrites `screenshot.jpg` in the skill directory. The file is automatically deleted when the server stops.

**Optional quality override:**
```bash
# Lower quality for faster capture/smaller file
curl -X POST http://localhost:8767/capture -H "Content-Type: application/json" -d '{"quality": 60}'

# Higher quality for detailed screenshots
curl -X POST http://localhost:8767/capture -d '{"quality": 95}'
```

| Quality | File Size (1080p) | Use Case |
|---------|-------------------|----------|
| 60 | ~80KB | Fast capture, quick checks |
| 90 (default) | ~150KB | Clear UI text, general use |
| 95 | ~200KB | Maximum detail, presentations |

### Mouse Actions
```bash
# Move cursor (no click)
curl -X POST http://localhost:8767/move -d '{"x": 500, "y": 300}'

# Click
curl -X POST http://localhost:8767/click -d '{"x": 500, "y": 300}'

# Drag
curl -X POST http://localhost:8767/drag -d '{"x1": 100, "y1": 200, "x2": 300, "y2": 400}'

# Scroll
curl -X POST http://localhost:8767/scroll -d '{"x": 500, "y": 300, "direction": "down", "amount": 3}'
```

### Keyboard Input
```bash
# Type text
curl -X POST http://localhost:8767/enter -d '{"keys": ["Hello World"]}'

# Press special key
curl -X POST http://localhost:8767/enter -d '{"keys": ["Enter"]}'

# Key combination (Ctrl+C)
curl -X POST http://localhost:8767/enter -d '{"keys": ["Ctrl", "C"]}'

# Mixed sequence: type, press key, then combo
curl -X POST http://localhost:8767/enter -d '{"keys": ["Hello", "Enter", "Ctrl", "A"]}'
```

The `/enter` endpoint accepts a list of keys and handles them sequentially:
- **Text strings** → Typed as-is
- **Special keys** → Pressed once (Enter, Escape, Tab, etc.)
- **Modifier + key** → Treated as combination (Ctrl+C, Alt+Tab, etc.)

### Special Keys Reference

Single keys:
- `Enter`, `Return`, `Escape`, `Esc`
- `Backspace`, `Tab`, `Space`
- `Delete`, `Del`
- `Up`, `Down`, `Left`, `Right`
- `Home`, `End`, `PageUp`, `PageDown`
- `F1` through `F12`

Modifiers (combine with other keys):
- `Ctrl`, `Control`
- `Alt`
- `Shift`
- `Win`, `Windows`

## Common Workflows

### Capture and View (Native Windows)

```powershell
# Using PowerShell
$response = Invoke-RestMethod -Uri "http://localhost:8767/capture" -Method Post
Start-Process $response.path
```

### Capture and View (WSL)

```bash
FILE=$(curl -s -X POST http://localhost:8767/capture | python3 -c "import sys,json; print(json.load(sys.stdin)['path'])")
read "$FILE"
```

### Click and Verify
```bash
# Click somewhere
curl -X POST http://localhost:8767/click -d '{"x": 500, "y": 300}'
sleep 0.5

# Capture to see result
curl -X POST http://localhost:8767/capture
```

### Open Notepad and Type
```bash
# Win+R to open Run
curl -X POST http://localhost:8767/enter -d '{"keys": ["Win", "R"]}'
sleep 0.5

# Type notepad and press Enter
curl -X POST http://localhost:8767/enter -d '{"keys": ["notepad", "Enter"]}'
sleep 1

# Type message
curl -X POST http://localhost:8767/enter -d '{"keys": ["Hello from WinControl!"]}'
```

## Installation

### Native Windows

1. **Install Python 3** from [python.org](https://python.org)
2. **Install dependencies**:
   ```powershell
   pip install pywin32 pillow mss
   ```
3. **Clone/download** the skill to `~/.openclaw/workspace/skills/wincontrol/`
4. **Start the server**:
   ```powershell
   python server.py
   ```

### WSL2 (Legacy)

See WSL2 Configuration section below.

## Frame Management

- **Capture**: On-demand via `POST /capture`
- **Quality**: 90% JPEG for clear text/UI
- **File**: `screenshot.jpg` in skill directory
- **Behavior**: Overwritten on each capture
- **Auto-cleanup**: Deleted when server stops (Ctrl+C)

To change quality, edit `server.py`:
```python
QUALITY = 90      # 1-100
```

## Stopping the Server

The server automatically cleans up the screenshot when stopped.

### Native Windows

Press `Ctrl+C` in the PowerShell window, or:
```powershell
# Find and stop the process
Get-Process python | Where-Object {$_.CommandLine -like '*wincontrol*'} | Stop-Process
```

### WSL

```bash
./stop.sh
```

Or manually:
```bash
# Kill Python process on Windows using PowerShell 7
'/mnt/c/Program Files/PowerShell/7/pwsh.exe' -Command \
  "Get-Process python -ErrorAction SilentlyContinue | Where-Object {\$_.CommandLine -like '*wincontrol*'} | Stop-Process -Force"
```

## Troubleshooting

### Native Windows

**Issue**: `pip install pywin32` fails
- Try: `pip install pywin32 --upgrade --force-reinstall`
- Or download from [GitHub releases](https://github.com/mhammond/pywin32/releases)

**Issue**: Port 8767 already in use
- Find the process: `netstat -ano | findstr :8767`
- Kill it: `taskkill /PID <PID> /F`

**Issue**: Cannot access from WSL
- Ensure Windows Firewall allows Python through
- Try disabling Windows Defender Firewall temporarily for testing

### WSL2

### Prerequisites
1. **WSL2 with Ubuntu** (or your preferred distro)
2. **Python 3** on Windows side
3. **Dependencies**: pywin32, pillow, mss (auto-installed)

### Path Configuration

Screenshots are saved as `screenshot.jpg` in the skill folder, accessible from both Windows and WSL.

### Troubleshooting

**Issue**: Server starts but curl fails
- Check if port 8767 is in use: `lsof -i :8767`
- Kill existing process: `kill <PID>`

**Issue**: Python module errors
- Manually install deps on Windows:
```bash
'/mnt/c/Program Files/PowerShell/7/pwsh.exe' -Command "pip install pywin32 pillow mss"
```

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│  Client     │────▶│   server.py  │────▶│  screenshot.jpg│
│  (curl/ps)  │     │  (localhost) │     │  (skill dir)   │
└─────────────┘     └──────────────┘     └────────────────┘
                            │
                     ┌─────┴─────┐
                     │  Port     │
                     │  8767     │
                     └───────────┘
```

The server runs on Windows Python. Screenshots are saved as `screenshot.jpg` in the skill directory and automatically deleted when the server stops (Ctrl+C).

## Python Client Example

```python
import requests
import time

API = "http://localhost:8767"

def capture():
    """Capture screen and return file path"""
    r = requests.post(f"{API}/capture")
    return r.json().get("path")

def click(x, y):
    requests.post(f"{API}/click", json={"x": x, "y": y})

def enter(keys):
    requests.post(f"{API}/enter", json={"keys": keys})

# Example workflow
if __name__ == "__main__":
    # Type text, press Enter, then select all
    enter(["Hello World", "Enter", "Ctrl", "A"])
    time.sleep(0.5)
    
    # Capture result
    screenshot_path = capture()
    print(f"Screenshot saved to: {screenshot_path}")
```

## Security Notes

- Server binds to `localhost` only (not accessible from network)
- No authentication - anyone with local access can control your desktop
- Screenshot is auto-deleted when server stops
- Screenshot saved as single `screenshot.jpg` in skill folder, not system directories
- Be careful running this on shared machines

## Integration with OpenClaw

### Native Windows

```javascript
// Capture and view
const result = await exec("curl -s -X POST http://localhost:8767/capture");
const data = JSON.parse(result.stdout);
// Path will be Windows format: C:\Users\...
await read(data.path);  // OpenClaw handles Windows paths
```

### WSL

```javascript
// Capture and view
const result = await exec("curl -s -X POST http://localhost:8767/capture");
const data = JSON.parse(result.stdout);
await read(data.path);  // Path: /mnt/c/Users/...

// Or take action then capture
await exec("curl -X POST http://localhost:8767/click -d '{\"x\":500,\"y\":300}'");
await exec("sleep 0.5");
const screenshot = await exec("curl -s -X POST http://localhost:8767/capture");
```

## License

MIT-0

## Version

2.0.1
