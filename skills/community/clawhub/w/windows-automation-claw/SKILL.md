---
name: windows-automation
description: This skill should be used when the user needs to automate Windows desktop operations through PowerShell and Python scripts. Trigger phrases include: "打开应用" (open app), "截图" (screenshot), "移动鼠标" (move mouse), "点击" (click), "键盘输入" (keyboard input), "自动操作" (automate), "RPA" (robotic process automation), "模拟鼠标" (simulate mouse), "模拟键盘" (simulate keyboard), "控制应用" (control app), "窗口操作" (window operation). Use this skill for any Windows automation tasks involving application control, screen capture, mouse/keyboard simulation, or desktop interaction.
---

# Windows Automation Skill

## Overview

This skill enables Windows desktop automation through integrated PowerShell and Python scripts. It provides capabilities for launching applications, capturing screenshots, and simulating mouse/keyboard interactions. This skill is ideal for RPA (Robotic Process Automation) scenarios, automated testing, repetitive task automation, and controlling Windows applications programmatically.

## Trigger Phrases and Execution Logic

### Primary Trigger Phrases

**Application Control:**
- "打开 [应用名称]" (open [app name])
- "启动 [应用]" (launch [app])
- "关闭 [应用]" (close [app])
- "打开网站 [URL]" (open website [URL])

**Screenshot:**
- "截图" (screenshot)
- "截屏" (capture screen)
- "保存屏幕截图" (save screenshot)
- "截取窗口 [窗口标题]" (capture window [window title])

**Mouse Operations:**
- "移动鼠标到 (x, y)" (move mouse to)
- "点击" (click)
- "右键点击" (right click)
- "双击" (double click)
- "拖拽从 (x1, y1) 到 (x2, y2)" (drag from to)
- "滚动 [上/下]" (scroll [up/down])

**Keyboard Operations:**
- "输入文本 [文本]" (type text)
- "按下 [按键]" (press key)
- "组合键 [按键1] [按键2]" (combo key)
- "快捷键 [按键组合]" (hotkey)

## Core Capabilities

### 1. Application Launching (`app_launcher.py`)

Execute application control operations through the `app_launcher.py` script.

**Start an application:**
```bash
python scripts/app_launcher.py start "C:\Program Files\Notepad++\notepad++.exe"
```

**Open URL:**
```bash
python scripts/app_launcher.py url "https://www.google.com"
```

**List running processes:**
```bash
python scripts/app_launcher.py list
```

**Kill an application:**
```bash
python scripts/app_launcher.py kill "notepad"
```

**When to use:**
- User wants to open a specific application
- User wants to launch a website
- User needs to manage running processes
- User wants to close/terminate applications

### 2. Screen Capture (`screenshot.py`)

Execute screenshot operations through the `screenshot.py` script.

**Capture full screen:**
```bash
python scripts/screenshot.py screen "C:\Users\YourName\Desktop\screenshot.png" 0
```

**Capture specific window:**
```bash
python scripts/screenshot.py window "Notepad" "C:\Users\YourName\Desktop\notepad.png"
```

**List all visible windows:**
```bash
python scripts/screenshot.py list
```

**When to use:**
- User wants to capture the entire screen
- User wants to screenshot a specific application window
- User needs to list all visible windows
- User wants to document UI states

### 3. Mouse Control (`mouse_control.py`)

Execute mouse operations through the `mouse_control.py` script.

**Move mouse to position:**
```bash
python scripts/mouse_control.py move 500 300
```

**Click at position:**
```bash
python scripts/mouse_control.py click left 500 300 1
```

**Drag and drop:**
```bash
python scripts/mouse_control.py drag 100 100 500 500 1.0
```

**Scroll:**
```bash
python scripts/mouse_control.py scroll down 5
```

**Get current mouse position:**
```bash
python scripts/mouse_control.py position
```

**When to use:**
- User wants to automate UI interactions
- User needs to navigate application interfaces
- User wants to perform drag-and-drop operations
- User needs to position mouse for other operations

### 4. Keyboard Control (`keyboard_control.py`)

Execute keyboard operations through the `keyboard_control.py` script.

**Type text:**
```bash
python scripts/keyboard_control.py type "Hello, World!"
```

**Press single key:**
```bash
python scripts/keyboard_control.py key enter
```

**Press combination keys:**
```bash
python scripts/keyboard_control.py combo ctrl c
```

**Press hotkey:**
```bash
python scripts/keyboard_control.py hotkey ctrl shift esc
```

**When to use:**
- User wants to automate text input
- User needs to simulate keyboard shortcuts
- User wants to fill forms automatically
- User needs to navigate applications via keyboard

## Workflow Examples

### Example 1: Automated Form Filling

**User Request:** "帮我打开Chrome,打开一个表单页面,填写姓名和邮箱"

**Execution Logic:**
1. Launch Chrome browser using `app_launcher.py start chrome`
2. Navigate to form URL using `app_launcher.py url <form_url>`
3. Wait for page to load
4. Use `mouse_control.py move` to position cursor in name field
5. Use `keyboard_control.py type` to enter name
6. Use `mouse_control.py move` to position cursor in email field
7. Use `keyboard_control.py type` to enter email

### Example 2: Application Testing

**User Request:** "测试记事本应用,输入一些文字,截图保存"

**Execution Logic:**
1. Launch Notepad using `app_launcher.py start notepad`
2. Wait for application to be ready
3. Use `keyboard_control.py type` to input test text
4. Capture window screenshot using `screenshot.py window "Notepad"`
5. Report results and screenshot path to user

### Example 3: Data Entry Automation

**User Request:** "自动打开Excel,输入一批数据到表格"

**Execution Logic:**
1. Launch Excel using `app_launcher.py start excel`
2. Open specific file using `keyboard_control.py combo ctrl o`
3. Use `keyboard_control.py type` to enter file path
4. Use `keyboard_control.py key enter` to confirm
5. Navigate to cells using `mouse_control.py move` or arrow keys
6. Enter data using `keyboard_control.py type`
7. Save using `keyboard_control.py combo ctrl s`

## Integration Guidelines

### Script Execution

1. **Always check script output:** Each script returns JSON with `success`, `message`, and optional data fields
2. **Handle errors gracefully:** Check `success` field before proceeding with dependent operations
3. **Use appropriate delays:** Add delays between operations to allow UI to respond
4. **Coordinate with window states:** Ensure windows are in the expected state before interacting

### Error Handling

- If `app_launcher.py` fails to start an app, check if the path is correct
- If `screenshot.py` fails, verify window title or check permissions
- If `mouse_control.py` operations don't work, check screen resolution coordinates
- If `keyboard_control.py` input is incorrect, verify key names are supported

### Coordinate System

- Mouse coordinates are absolute screen coordinates
- (0, 0) is the top-left corner of the primary monitor
- Use `mouse_control.py position` to find current coordinates
- For multi-monitor setups, specify monitor index in screenshot operations

### Key Naming Conventions

**Letter keys:** a, b, c, ..., z
**Number keys:** 0, 1, 2, ..., 9
**Special keys:** space, enter, tab, backspace, escape, delete, insert, home, end, pageup, pagedown
**Arrow keys:** up, down, left, right
**Function keys:** f1, f2, ..., f12
**Modifier keys:** ctrl, alt, shift, win

## Resources

### scripts/

This skill includes four executable Python scripts for Windows automation:

- **`app_launcher.py`** - Application launching and process management
- **`screenshot.py`** - Screen and window capture functionality
- **`mouse_control.py`** - Mouse movement, clicking, and scrolling
- **`keyboard_control.py`** - Keyboard input simulation and key combinations

**Note:** Scripts are executed without loading into context window for efficiency. Read them only when patching or debugging is needed.

### references/

Delete this directory if not needed. Currently contains placeholder references.

### assets/

Delete this directory if not needed. Currently contains placeholder assets.
