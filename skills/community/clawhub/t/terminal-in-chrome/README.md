# Web Terminal Extension

A Chrome extension that injects a fully functional, resizable local terminal into any website you visit.

## Architecture
1. **Server (`/server`)**: A lightweight Node.js backend running locally (`ws://localhost:8989`) that spawns the actual terminal process (`bash` or `zsh`) using `node-pty`.
2. **Extension (`/extension`)**: A Chrome extension that injects `xterm.js` into websites and connects back to the local server via WebSockets.

## Setup

### 1. Start the Local Server
```bash
cd server
npm install
npm start
```
The server will run on port `8989`.

### 2. Install the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right corner).
3. Click **Load unpacked**.
4. Select the `extension` folder from this project (`web-terminal-extension/extension`).

## Usage
- Go to any website.
- Press **`Ctrl + \``** or **`Cmd + J`** to toggle the terminal.
- Drag the top border to resize it.
- The terminal history and height persist across page reloads!
