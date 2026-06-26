---
name: yyds-auto
description: Control Android devices via MCP — tap, swipe, OCR, screenshot, UI automation, shell, file management, and AI agent orchestration for Android RPA.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - YYDS_DEVICE_HOST
        - YYDS_DEVICE_PORT
      bins:
        - node
      anyBins:
        - adb
    primaryEnv: YYDS_DEVICE_HOST
    emoji: "\U0001F4F1"
    homepage: https://yydsauto.com
    os:
      - windows
      - macos
      - linux
    install:
      - kind: node
        package: yyds-auto-mcp
        bins: [yyds-auto-mcp]
---

# Yyds.Auto — Android RPA Skill for AI Agents

> Let LLMs directly control Android devices through the MCP protocol.

Yyds.Auto is a production-grade Android RPA (Robotic Process Automation) platform that exposes **60 MCP tools** covering the full spectrum of Android device automation — from pixel-level touch injection and OCR to UI hierarchy inspection, file management, and on-device AI agent orchestration.

## What Can It Do?

| Category | Tools | Capabilities |
|----------|-------|-------------|
| 📱 Device Info | 4 | Device model, screen size, IMEI, foreground app, network status |
| 👆 Touch & Input | 8 | Tap, swipe, long press, drag, text input, clipboard, key press |
| 📸 Screenshot | 2 | Screenshot as base64 image (LLM can see it directly), save to device |
| 🌲 UI Automation | 5 | UI hierarchy dump, find elements by attributes, element relations, wait & scroll |
| 🔍 OCR & Image | 8 | Screen OCR, tap-on-text, template matching, pixel color, image comparison |
| 💻 Shell | 1 | Execute shell commands with ROOT/SHELL privileges |
| 📦 App Management | 8 | Launch/stop apps, list installed, install/uninstall APK, open URL, toast |
| 📁 File Operations | 7 | List, read, write, delete, rename files and directories on device |
| 🐍 Script Projects | 5 | List/start/stop Python projects, execute Python code snippets |
| 📚 Pip Management | 4 | List, install, uninstall, inspect Python packages |
| 🤖 AI Agent | 8 | Configure and run an on-device AI agent with natural language instructions |

## Architecture

```
AI Agent (Claude / GPT / Gemini / Cursor / Windsurf / ...)
  ↓ MCP Protocol (stdio, JSON-RPC)
yyds-auto-mcp (Node.js, this skill)
  ↓ HTTP REST (JSON, port 61140)
yyds.py engine (Android, aiohttp server)
  ↓ IPC
yyds.auto engine (Android, kernel-level UI automation)
```

The MCP server communicates with the on-device engine via HTTP REST. When connected via USB, ADB port forwarding is set up automatically. Remote devices over WiFi/LAN are also supported.

## Prerequisites

1. **Android device** with [Yyds.Auto](https://yydsauto.com) installed and the engine running
2. **Connection**: USB (auto ADB forward) or WiFi (same LAN)
3. **Node.js** >= 18

## Quick Start

### Install the MCP Server

```bash
npm install -g yyds-auto-mcp
```

### Connect to a USB Device (auto-detected)

```bash
# Default: 127.0.0.1:61140, ADB forward set up automatically
yyds-auto-mcp
```

### Connect to a Remote Device

```bash
YYDS_DEVICE_HOST=192.168.1.100 YYDS_DEVICE_PORT=61140 yyds-auto-mcp
```

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yyds-auto": {
      "command": "npx",
      "args": ["-y", "yyds-auto-mcp"],
      "env": {
        "YYDS_DEVICE_HOST": "127.0.0.1",
        "YYDS_DEVICE_PORT": "61140"
      }
    }
  }
}
```

### Cursor / Windsurf / VS Code Configuration

Add the same MCP server configuration in your editor's MCP settings.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `YYDS_DEVICE_HOST` | `127.0.0.1` | Device IP address |
| `YYDS_DEVICE_PORT` | `61140` | Engine port number |
| `YYDS_DEVICE_SERIAL` | *(first device)* | Specify ADB device serial |
| `YYDS_ADB_PATH` | *(auto-detect)* | Custom ADB binary path |

## Tool Reference

### Device Information

- **`device_info`** — Comprehensive device info: engine version, screen size, IMEI, foreground app
- **`get_foreground_app`** — Current foreground app & Activity
- **`get_screen_size`** — Device screen resolution
- **`is_network_online`** — Check network connectivity

### Touch & Input

- **`tap`** *(x, y, count?, interval?)* — Tap at coordinates (supports multi-tap)
- **`swipe`** *(x1, y1, x2, y2, duration?)* — Swipe gesture
- **`long_press`** *(x, y, duration?)* — Long press at coordinates
- **`drag`** *(x1, y1, x2, y2, duration?)* — Drag from point A to B
- **`input_text`** *(text)* — Input text into the focused field
- **`set_clipboard`** / **`get_clipboard`** — Clipboard operations
- **`press_key`** *(key)* — Press a key (home, back, enter, etc.)

### Screenshot

- **`take_screenshot`** *(quality?)* — Returns base64 JPEG image (LLM directly interprets it)
- **`save_screenshot`** *(path?)* — Save screenshot to device storage

### UI Automation

- **`dump_ui_hierarchy`** — Full UI tree (auto-trimmed when >15KB to save tokens)
- **`find_ui_elements`** *(text?, resourceId?, className?, clickable?, ...)* — Find elements by attributes
- **`get_element_relation`** *(hashcode, type?)* — Get parent/children/sibling of an element
- **`wait_for_element`** *(text?, resourceId?, timeout?)* — Wait until an element appears
- **`scroll_to_find`** *(text?, direction?, maxScrolls?)* — Scroll until an element is found

### OCR & Image

- **`screen_ocr`** *(x?, y?, w?, h?)* — Recognize text on screen (region supported)
- **`tap_text`** *(text, index?)* — OCR + tap on the matching text
- **`image_ocr`** *(path)* — Recognize text from an image file
- **`find_image_on_screen`** *(templates, threshold?)* — Template matching
- **`get_pixel_color`** *(x, y)* — Get pixel color at coordinates
- **`compare_images`** *(image1, image2)* — Image similarity comparison
- **`wait_for_screen_change`** *(timeout?, threshold?)* — Wait for the screen to change

### Shell

- **`run_shell`** *(command)* — Execute shell commands with elevated privileges

### App Management

- **`launch_app`** / **`stop_app`** *(packageName)* — Start/stop apps
- **`list_installed_apps`** — List all non-system installed apps
- **`is_app_running`** *(packageName)* — Check if an app is running
- **`open_url`** *(url)* — Open URL in browser
- **`show_toast`** *(message)* — Display a toast notification
- **`install_apk`** / **`uninstall_app`** — Install/uninstall apps

### File Operations

- **`list_files`** / **`read_file`** / **`write_file`** — Browse, read, write files
- **`file_exists`** / **`delete_file`** / **`rename_file`** / **`create_directory`**

### Script Projects

- **`list_projects`** / **`project_status`** — View Python projects
- **`start_project`** / **`stop_project`** — Control project execution
- **`run_python_code`** *(code)* — Execute Python code snippets on the device

### Pip Management

- **`pip_list`** / **`pip_install`** / **`pip_uninstall`** / **`pip_show`**

### AI Agent

- **`agent_run`** *(instruction)* — Run an on-device AI agent with natural language
- **`agent_stop`** / **`agent_status`** — Control and monitor the agent
- **`agent_get_config`** / **`agent_set_config`** — Configure AI provider & model
- **`agent_get_providers`** / **`agent_get_models`** — List available providers & models
- **`agent_test_connection`** — Verify AI model connectivity

## Key Features

### 🔄 Auto-Reconnect
USB connection drops are handled gracefully — when the device disconnects, the MCP server automatically re-establishes ADB port forwarding and retries the request.

### 🚀 Auto-Bootstrap
On first connection via USB, the server automatically sets up ADB forwarding and starts the engine on the device if it's not already running.

### 🧠 Smart UI Dump
UI hierarchy dumps over 15KB are automatically trimmed to keep only actionable elements (those with text, resource-id, content-desc, or clickable/scrollable attributes), reducing LLM token usage.

### 🎯 Kernel-Level Touch
Touch events are injected at the Linux kernel level, making them work in any app including games, locked-down apps, and areas that block accessibility-based input.

## Example Prompts

Once connected, try these prompts with your AI agent:

- *"Take a screenshot and describe what's on the screen"*
- *"Open WeChat and send 'Hello' to the first chat"*
- *"Find all buttons on the screen and list their labels"*
- *"OCR the screen and find any phone numbers"*
- *"Swipe up 3 times to scroll through the feed"*
- *"Install the APK at /sdcard/Download/app.apk"*
- *"Run this Python code on the device: `print('Hello from Android!')`"*

## Links

- 🌐 **Website**: [yydsauto.com](https://yydsauto.com)
- 📦 **npm**: [yyds-auto-mcp](https://www.npmjs.com/package/yyds-auto-mcp)
- 🐙 **GitHub**: [yyds-auto-mcp](https://github.com/ChenAnZong/yyds-auto-mcp)
