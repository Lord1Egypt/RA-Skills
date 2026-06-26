# autoclaw_wboke

Empower OpenClaw with enhanced web page control and bookmark management capabilities.

## Features

| Feature | Description |
|---------|-------------|
| Bookmark Management | Complete CRUD operations, support for folder operations |
| CDP Deep Control | Execute JavaScript, element operations, screenshots |
| Automation Scripts | Reusable script templates |
| One-time Authorization | Take control of all tabs without repeated authorization |

## Two Modes

### Enhanced Mode (Recommended) - Port 30000
- MCP enhanced features
- Complete bookmark management
- One-time authorization to take control of all tabs

### Simple Mode - Port 18792
- Direct connection to Gateway
- Basic web page operations

## Quick Start

### 1. Download Extension

**Recommended: Download from official website**
- Visit: **https://www.wboke.com**
- Download the latest AutoClaw Chrome extension
- Or load from local: `autoclaw-plugin/` directory

### 2. Start MCP Server

1. Open Chrome extension management page `chrome://extensions`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked"
4. Select `autoclaw_wboke/autoclaw-plugin`

### 2. Start MCP Server

```bash
cd autoclaw/mcp
npm start
```

### 3. Configure Extension

1. Click extension icon → Settings
2. Select port **30000** (recommended)
3. Click "Take control of all tabs" to complete authorization

## Usage

### Through OpenClaw

1. Copy `autoclaw_wboke` to `~/.openclaw/workspace/skills/`
2. Speak directly in OpenClaw, such as:
   - "Help me bookmark this page"
   - "Open Baidu and take a screenshot"
   - "Search bookmarks for Python"

### Through Command Line

```bash
# Open web page
curl -X POST http://127.0.0.1:30000/mcp -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "claw_navigate",
    "arguments": {"url": "https://www.baidu.com"}
  }
}'

# Take screenshot
curl -X POST http://127.0.0.1:30000/mcp -d '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "claw_take_screenshot"
  }
}'

# Create bookmark
curl -X POST http://127.0.0.1:30000/mcp -d '{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "claw_create_bookmark",
    "arguments": {"title": "Baidu", "url": "https://www.baidu.com"}
  }
}'
```

## File Structure

```
autoclaw_wboke/
├── SKILL.md              # Skill definition
├── scripts/             # Automation script templates
│   ├── 抖音点赞.json    # Douyin like script
│   ├── 批量截图.json    # Batch screenshot script
│   └── 自动搜索.json    # Auto search script
├── autoclaw-plugin/     # Chrome extension
│   ├── background.js
│   ├── popup.html
│   └── options.html
└── README.md
```

## Available Tools

### Bookmark Management
- `claw_get_bookmarks` - Get all bookmarks
- `claw_create_bookmark` - Create new bookmark
- `claw_delete_bookmark` - Delete bookmark
- `claw_create_folder` - Create new folder
- `claw_move_bookmark` - Move bookmark
- `claw_search_bookmarks` - Search bookmarks

### Page Operations
- `claw_navigate` - Navigate to URL
- `claw_click_element` - Click page element
- `claw_fill_input` - Fill input field
- `claw_evaluate_js` - Execute JavaScript
- `claw_take_screenshot` - Take screenshot
- `claw_scroll` - Scroll page

## FAQ

### Q: MCP server cannot start
A: Ensure dependencies are installed: `cd autoclaw/mcp && npm install`

### Q: Extension cannot connect
A: 1. Check if MCP service is running on port 30000
   2. Check if Token is correct
   3. Click "Take control of all tabs" to complete authorization

### Q: How to use script templates?
A: In OpenClaw, simply say "Use Douyin like script" and AI will automatically read and execute it.

## Technical Support

- MCP service port: 30000
- Token: autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs

---
Made with ❤️ for OpenClaw