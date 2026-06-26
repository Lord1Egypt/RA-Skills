---
name: system-controller
description: >
  Control Windows desktop software, hardware, and IoT devices.
  This skill should be used when the user wants to open/close/resize windows,
  start/stop/monitor processes, adjust volume/brightness, manage power settings,
  control network adapters, communicate with Arduino or serial devices,
  or interact with smart home platforms like Home Assistant.
  Also covers mouse/keyboard automation, screenshots, OCR, and visual recognition.
  Trigger phrases include "open app", "close window", "set volume", "adjust brightness",
  "lock screen", "shutdown", "list processes", "send serial command", "control light",
  "connect Arduino", "enable WiFi", "USB devices", "click here", "screenshot",
  "OCR", "find image on screen", "type text", "mouse click", "drag", "scroll",
  or any request involving controlling software, hardware, or external devices.
---

# System Controller

Unified control interface for Windows desktop software, system hardware, serial devices, and IoT platforms.

## Architecture

```
User Request → Natural Language Understanding → Script Execution → System Action
```

Six control modules, each with a dedicated Python script:

| Module | Script | Scope |
|--------|--------|-------|
| Window Manager | `scripts/window_manager.py` | Desktop window control |
| Process Manager | `scripts/process_manager.py` | System process management |
| Hardware Controller | `scripts/hardware_controller.py` | System hardware settings |
| Serial Communication | `scripts/serial_comm.py` | Arduino / serial devices |
| IoT Controller | `scripts/iot_controller.py` | Smart home / HTTP APIs |
| GUI Controller | `scripts/gui_controller.py` | Mouse, keyboard, screenshot, OCR |

All scripts are standalone CLI tools. No inter-script dependencies.

## Execution Model

### Prerequisites

- **OS**: Windows 10/11
- **PowerShell**: 5.1+ (built-in)
- **Python**: Managed runtime (auto-provided by WorkBuddy)
- **Optional**: `pyserial` (auto-installed by serial_comm.py), `requests` (auto-installed by iot_controller.py), `pyautogui` (auto-installed by gui_controller.py), `pillow` (auto-installed by gui_controller.py), `pytesseract` (optional, for OCR), `nircmd` (for precise volume control), `tesseract-ocr` (system-level, for Chinese OCR: `choco install tesseract`)

### Python Path

Use the managed Python runtime for all script executions:
```
C:\Users\wave\.workbuddy\binaries\python\versions\3.13.12\python.exe
```

For GUI controller (which needs pyautogui/pillow), use the venv Python:
```
C:\Users\wave\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

If the venv does not exist, create it and install packages:
```
C:\Users\wave\.workbuddy\binaries\python\versions\3.13.12\python.exe -m venv C:\Users\wave\.workbuddy\binaries\python\envs\default
C:\Users\wave\.workbuddy\binaries\python\envs\default\Scripts\pip install pyautogui pillow pyserial requests
```

### Script Path

All scripts are located at:
```
~/.workbuddy/skills/system-controller/scripts/
```

### Execution Pattern

Always use `execute_command` to run scripts. Never try to run them inline.

Pattern:
```
{python_path} {script_path} {action} {flags}
```

### Safety Rules

1. **NEVER execute destructive actions without explicit user confirmation** (shutdown, restart, kill processes, close windows, disable network adapters).
2. **Always list/query first** before taking action. Example: run `list` before `close`, `list --name` before `kill`.
3. **Warn the user** before power operations (shutdown, restart, sleep, hibernate) and require explicit confirmation.
4. **Never disable critical network adapters** (the one used for active internet connection) without warning.
5. **For serial communication**, always `list` ports first to confirm the correct port name.

## Module Details

### 1. Window Manager (`window_manager.py`)

Control desktop application windows via Windows UI Automation and Win32 API.

**Capabilities**: list, activate, close, minimize, maximize, resize, send-keys

**Decision flow**:
1. User says "open/close/focus X" → `list` to find the window → confirm with user → execute action
2. User says "resize/move X" → `list` to find PID → `resize` with coordinates
3. User says "type/send X to Y" → `activate` target window → `send-keys`

**Common examples**:
- "打开记事本" → `process_manager.py start "notepad.exe"`
- "关闭Chrome" → `window_manager.py list` → find Chrome → `window_manager.py close --title "Chrome"`
- "把微信调到前台" → `window_manager.py activate --title "微信"`
- "全屏当前窗口" → `window_manager.py maximize --title "..."`

### 2. Process Manager (`process_manager.py`)

List, start, stop, and monitor system processes.

**Capabilities**: list, kill, start, info, system

**Decision flow**:
1. User says "查看进程" → `list` or `list --name`
2. User says "结束X进程" → `list --name X` → confirm → `kill --name X`
3. User says "启动X" → `start "X"`
4. User says "系统状态" → `system`

**Common examples**:
- "有哪些程序在运行" → `process_manager.py system`
- "关掉所有记事本" → `process_manager.py kill --name notepad`
- "启动VS Code" → `process_manager.py start "code"`

### 3. Hardware Controller (`hardware_controller.py`)

Control system hardware settings via PowerShell and WMI.

**Capabilities**:
- Volume: get, set, mute
- Screen: brightness (get/set), display info
- Power: lock, sleep, hibernate, shutdown, restart, cancel
- Network: list adapters, enable/disable, WiFi scan, network info
- USB: list devices

**Decision flow**:
1. User says "音量/声音" → volume commands
2. User says "亮度/屏幕" → screen/brightness commands
3. User says "关机/锁屏/睡眠" → power commands (**always confirm**)
4. User says "网络/WiFi" → network commands
5. User says "USB" → usb list

**Common examples**:
- "把音量调到50" → `hardware_controller.py volume set --level 50`
- "静音" → `hardware_controller.py volume mute`
- "屏幕调暗一点" → `hardware_controller.py screen brightness --level 30`
- "锁屏" → `hardware_controller.py power lock`
- "扫描WiFi" → `hardware_controller.py network wifi`

### 4. Serial Communication (`serial_comm.py`)

Communicate with Arduino, ESP32, and other serial devices via pyserial.

**Capabilities**: list ports, detect baud rate, send, receive, chat, monitor

**Decision flow**:
1. User says "串口/Arduino/COM" → `list` ports first
2. User says "发送到Arduino" → `send --port COMx --data "..."`
3. User says "读取传感器" → `chat --port COMx --data "READ"`

**Auto-install**: Automatically installs `pyserial` on first use.

**Common examples**:
- "有哪些串口" → `serial_comm.py list`
- "给Arduino发指令开灯" → `serial_comm.py send --port COM3 --data "LED_ON"`
- "读取温度传感器" → `serial_comm.py chat --port COM3 --data "GET_TEMP"`
- "监听串口数据" → `serial_comm.py monitor --port COM3 --duration 30`

### 5. IoT Controller (`iot_controller.py`)

Control smart home devices via Home Assistant REST API, Mijia, or generic HTTP endpoints.

**Capabilities**:
- Home Assistant: list entities, get state, turn on/off/toggle, call any service
- Generic HTTP: GET, POST, PUT to any REST endpoint
- Mijia: device discovery guidance

**Decision flow**:
1. User mentions "智能家居/Home Assistant/灯光/温度" → IoT commands
2. User says "控制设备/开关灯" → requires URL and token from user
3. User says "调用API" → generic HTTP commands

**Auto-install**: Automatically installs `requests` on first use.

**Common examples**:
- "列出所有智能设备" → `iot_controller.py homeassistant --url ... --token ... list`
- "打开客厅灯" → `iot_controller.py homeassistant --url ... --token ... on --entity-id light.living_room`
- "关掉卧室空调" → `iot_controller.py homeassistant --url ... --token ... off --entity-id climate.bedroom`
- "调用这个API" → `iot_controller.py http --url ... get --path ...`

### 6. GUI Controller (`gui_controller.py`)

Full GUI automation: mouse control, keyboard input, screenshots, OCR, and visual recognition.

**Capabilities**:
- Mouse: move, click (left/right/double), drag, scroll, get position
- Keyboard: type text, press hotkeys, key down/up (hold/release)
- Screenshot: full screen, region, active window, list saved screenshots
- OCR: extract text from screen regions (requires pytesseract or Windows OCR fallback)
- Visual: find image template on screen, click by image, find by color, get pixel color

**Auto-install**: Automatically installs `pyautogui` and `pillow` on first use.

**Decision flow**:
1. User says "click/鼠标点击" → determine position (by coordinates, image template, or color), then click
2. User says "type/输入文字" → `keyboard type --text "..."`
3. User says "screenshot/截图" → `screenshot full` or `screenshot active-window`
4. User says "read screen/OCR/识别文字" → `visual ocr` on the relevant region
5. User says "find/查找图标" → `visual find --template "icon.png"`
6. User says "scroll/滚动" → `mouse scroll`
7. User says "drag/拖拽" → `mouse drag --start-x ... --start-y ... --end-x ... --end-y ...`

**Common examples**:
- "截图" → `gui_controller.py screenshot full`
- "截取当前窗口" → `gui_controller.py screenshot active-window`
- "鼠标移到(500,300)" → `gui_controller.py mouse move --x 500 --y 300`
- "点击(500,300)" → `gui_controller.py mouse click --x 500 --y 300`
- "右键点击" → `gui_controller.py mouse right-click --x 500 --y 300`
- "双击" → `gui_controller.py mouse double-click --x 500 --y 300`
- "拖拽文件从(100,200)到(500,400)" → `gui_controller.py mouse drag --start-x 100 --start-y 200 --end-x 500 --end-y 400`
- "向下滚动" → `gui_controller.py mouse scroll --direction down --clicks 10`
- "输入Hello World" → `gui_controller.py keyboard type --text "Hello World"`
- "按Ctrl+C" → `gui_controller.py keyboard press --keys "ctrl+c"`
- "按Alt+Tab" → `gui_controller.py keyboard press --keys "alt+tab"`
- "识别屏幕上的文字" → `gui_controller.py visual ocr`
- "识别(100,100,800,600)区域的文字" → `gui_controller.py visual ocr --x 100 --y 100 --width 800 --height 600`
- "在屏幕上找这个图标" → `gui_controller.py visual find --template "button.png"`
- "找到并点击这个图片" → `gui_controller.py visual click-image --template "submit.png"`
- "获取(200,200)位置的颜色" → `gui_controller.py visual pixel --x 200 --y 200`
- "获取鼠标位置" → `gui_controller.py mouse position`
- "获取屏幕分辨率" → `gui_controller.py screenshot size`

**Safety Rules**:
- Mouse and keyboard operations affect whatever is on screen — **always screenshot first** if unsure.
- The **failsafe** is enabled: moving mouse to any screen corner will abort all pyautogui operations.
- OCR and image recognition are best-effort — accuracy depends on screen resolution, language, and image quality.
- For OCR, install Tesseract for best results: `choco install tesseract` then `pip install pytesseract`.

## Handling Unknown Devices

When the user requests control of a device or software not directly covered:

1. **Check if it can be started as a process**: Use `process_manager.py start "app_name"`
2. **Check if it has windows**: Use `window_manager.py list` to find it
3. **Take a screenshot**: Use `gui_controller.py screenshot full` to see what's on screen
4. **Use OCR to read text**: Use `gui_controller.py visual ocr` to extract text from screen
5. **Click by image matching**: Save a template, then `gui_controller.py visual click-image --template icon.png`
6. **Use mouse/keyboard**: `gui_controller.py mouse click --x 100 --y 200` for direct control
7. **Check if it has an API**: Use `iot_controller.py http` to interact
8. **Check if it's USB-connected**: Use `hardware_controller.py usb list` then `serial_comm.py list`
9. **Suggest alternatives**: If none of the above work, explain the limitation and suggest MCP Server or custom script

## Quick Reference

For detailed command syntax, read `references/command_reference.md`.
