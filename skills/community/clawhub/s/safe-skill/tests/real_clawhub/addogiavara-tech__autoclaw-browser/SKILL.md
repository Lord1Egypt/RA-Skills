# AutoClaw Browser Automation Skill

## Skill Overview
AutoClaw is a browser automation skill that provides comprehensive control over Chrome browser through MCP (Message Communication Protocol) communication with browser extension.

## Prerequisites
Before starting MCP service, ensure the following files exist in the correct directory:
- `options.js` - Browser extension options page script
- `background.js` - Extension background script handling WebSocket connections

### File Location
```
Download from: https://www.wboke.com/download/autoclaw-chrome-extension.zip
Extract to: ~/.openclaw/browser-extensions/autoclaw/
```

## Available Tools

### ⌨️ Keyboard Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_press_key` | Press single key | `key: string` |
| `claw_press_combo` | Press key combination (e.g., Ctrl+C) | `keys: string` |
| `claw_type_text` | Type text with optional delay | `text: string, [delay: number]` |

### 📸 Screenshot & Content Extraction
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_take_screenshot` | Capture screenshot of current page | `[fullPage: boolean]` |
| `claw_get_page_content` | Get page HTML or text content | `[type: html\|text]` |
| `claw_get_text` | Get text content of element | `selector: string` |
| `claw_get_html` | Get HTML content of element | `selector: string` |
| `claw_get_attribute` | Get element attribute value | `selector, attribute` |
| `claw_get_count` | Count matching elements | `selector: string` |
| `claw_is_visible` | Check if element is visible | `selector: string` |

### 🖱️ Mouse & Scroll Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_mouse_move` | Move mouse to coordinates | `x, y` |
| `claw_mouse_click` | Click at coordinates | `[x, y]` |
| `claw_mouse_right_click` | Right-click at coordinates | `[x, y]` |
| `claw_mouse_double_click` | Double-click at coordinates | `[x, y]` |
| `claw_mouse_wheel` | Scroll mouse wheel | `[deltaX, deltaY]` |
| `claw_scroll` | Scroll page | `[x, y]` |
| `claw_fast_scroll_down` | Fast scroll down one screen | `[speed: number]` |
| `claw_fast_scroll_up` | Fast scroll up one screen | `[speed: number]` |

### 📱 Touch & Swipe Operations (Mobile)
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_swipe_up` | Swipe up gesture (Douyin/TikTok) | `[distance: number]` |
| `claw_swipe_down` | Swipe down gesture | `[distance: number]` |
| `claw_swipe_left` | Swipe left gesture | `[distance: number]` |
| `claw_swipe_right` | Swipe right gesture | `[distance: number]` |
| `claw_tap` | Tap at specific position | `x, y` |

### 📑 Tab Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_tab_create` | Create new browser tab | `[url, active]` |
| `claw_tab_close` | Close browser tab | `[tabId]` |
| `claw_tab_list` | List all open tabs | - |
| `claw_tab_switch` | Switch to specific tab | `tabId: number` |
| `claw_tab_reload` | Reload tab content | `[tabId]` |
| `claw_get_active_tab` | Get active tab information | - |
| `claw_attach_all_tabs` | Attach all tabs for control | - |

### 🍪 Storage & Cookies Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_cookies` | Get cookies for domain | `[domain: string]` |
| `claw_set_cookies` | Set cookies | `cookies: array` |
| `claw_get_storage` | Get localStorage/sessionStorage | `[type, origin]` |
| `claw_set_storage` | Set storage value | `type, key, value` |

### ⚙️ Configuration & Status
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_get_status` | Get current system status | - |
| `claw_get_config` | Get full configuration | - |
| `claw_set_mode` | Set operation mode | `mode: local\|cloud\|auto` |
| `claw_health_check` | Perform health check | - |
| `claw_diagnose` | System diagnostics | `[full: boolean]` |

### 🧪 JavaScript Execution
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_evaluate_js` | Execute JavaScript code | `expression: string` |

### ⏳ Wait Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `claw_wait` | Wait specified milliseconds | `ms: number` |
| `claw_wait_for_element` | Wait for element to appear | `selector, [timeout]` |
| `claw_wait_for_text` | Wait for text to appear | `text, [timeout]` |
| `claw_wait_for_url` | Wait for URL pattern match | `urlPattern, [timeout]` |
| `claw_wait_for_navigation` | Wait for navigation completion | `[timeout]` |

## Configuration
- **MCP Port**: 30000 (default)
- **Extension WebSocket**: `ws://127.0.0.1:30000/extension`
- **Built-in Token**: `autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs`

## Setup Instructions

### 1. Download Extension
**Recommended: Download from official website**
- Visit: **https://www.wboke.com**
- Download the latest AutoClaw Chrome extension

### 2. Start MCP Server
```bash
cd autoclaw_mcp/mcp
npm install  # First time only
npm start
```

### 3. Install Chrome Extension
1. Download from **https://www.wboke.com/download/autoclaw-chrome-extension.zip**
2. Extract to: `~/.openclaw/browser-extensions/autoclaw/`
3. Open `chrome://extensions`
4. Enable "Developer mode"
5. Click "Load unpacked"
6. Select `~/.openclaw/browser-extensions/autoclaw/` directory

### 4. Configure Extension
1. Click extension icon → Settings
2. Select port: **30000** (recommended)
3. Click "Save Settings" to authorize
4. Click "Attach All Tabs" to take control

## Troubleshooting

### Extension Not Connected
1. Verify MCP server is running on port 30000
2. Click extension icon → Settings → Test Connection
3. Ensure authorization is not expired

### "No Attached Tab" Error
1. Click "Attach All Tabs" in extension popup
2. Or manually click each tab to attach

### Authorization Expired
1. Click extension icon → Settings
2. Click "Save Settings" to re-authorize

## Project Structure
```
autoclaw_mcp/
├── SKILL.md                    # This documentation
├── README.md                   # General documentation
├── mcp/                       # MCP Server
│   ├── package.json
│   ├── dist/server.js         # Compiled server
│   └── node_modules/
├── (Chrome Extension)          # Download from:
│   ├── https://www.wboke.com/download/autoclaw-chrome-extension.zip
└── scripts/                    # Automation templates (optional)
```

## Log Management
- **Log Directory**: `~/.autoclaw/logs/`
- **Retention**: 30 days (auto-cleanup on server start)
- **Max Tasks**: 100

## Communication Protocol
- MCP service runs on port 30000
- Browser extension communicates via WebSocket
- Message format: JSON

## Example Usage
```javascript
// Connect to MCP service
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:30000');

ws.on('open', function() {
    ws.send(JSON.stringify({
        action: 'navigate',
        url: 'https://www.wboke.com'
    }));
});
```

## Error Handling
- **Connection Failure**: Check if MCP service is running and port 30000 is available
- **Extension Not Loaded**: Verify manifest.json exists and is properly formatted
- **Dependency Errors**: Re-run `npm install` to install dependencies