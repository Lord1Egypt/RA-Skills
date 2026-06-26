---
name: terminal-in-chrome
description: Manages the Web Terminal Chrome Extension local backend server. Use this skill to start, stop, or check the status of the local terminal server running on port 8989.
repository: https://github.com/yayayahei/skills/tree/main/terminal-in-chrome
---

# Web Terminal Extension Skill

## Repository
[https://github.com/yayayahei/skills/tree/main/terminal-in-chrome](https://github.com/yayayahei/skills/tree/main/terminal-in-chrome)

## Overview
This skill manages the local backend server for the Web Terminal Chrome Extension, which injects a fully functional, resizable local terminal into any website via `xterm.js`.

## Architecture
1. **Server (`/server`)**: A lightweight Node.js backend running locally (`ws://localhost:8989`) that spawns the actual terminal process (`bash` or `zsh`) using `node-pty`.
2. **Extension (`/extension`)**: A Chrome extension that injects `xterm.js` into websites and connects back to the local server via WebSockets.

## Operations

### Start the Server
Trigger phrases: "start web terminal", "run terminal server", "start terminal backend"

**Action:**
Navigate to the `server` directory and start the Node.js server in the background.
```bash
cd server
npm start
```
The server will run on port `8989`.

### Stop the Server
Trigger phrases: "stop web terminal", "kill terminal server", "stop terminal backend"

**Action:**
Find the process running on port 8989 and kill it.
```bash
lsof -i :8989
kill -9 <PID>
```

### Check Status
Trigger phrases: "web terminal status", "is terminal running?", "check terminal server"

**Action:**
Check if port 8989 is in use to determine if the server is running.
```bash
lsof -i :8989
```

## User Instructions for Extension
If the user asks how to use the extension, provide these steps:
1. Open Google Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right corner).
3. Click **Load unpacked**.
4. Select the `extension` folder from this project (`web-terminal-extension/extension`).
5. Go to any website.
6. Press **`Ctrl + \``** or **`Cmd + J`** to toggle the terminal.
7. Drag the top border to resize it.
