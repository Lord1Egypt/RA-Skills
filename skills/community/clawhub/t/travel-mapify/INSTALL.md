# Installation Guide for flyai-travelmapify

This skill is designed to be portable and work on any system with the required dependencies.

## Prerequisites

1. **Python 3.7+** - Required for all scripts
2. **OpenClaw** - The skill should be placed in your OpenClaw workspace
3. **FlyAI CLI** - Must be installed and accessible in your PATH or via npm
4. **amap-maps skill** - Required OpenClaw skill for Amap LBS services
5. **Amap API** - Built-in default API key included (no user key required)
6. **AI Vision Capability** - For image input processing, your OpenClaw agent should have access to an image-capable model for POI extraction

## Installation Steps

### Option 1: Using OpenClaw Workspace (Recommended)

If you're using OpenClaw, simply place this entire `flyai-travelmapify` directory in your workspace skills folder:

```
~/.openclaw/workspace/skills/flyai-travelmapify/
```

The skill will automatically detect your workspace path and configure itself.

### Option 2: Standalone Usage

You can run the skill from anywhere by executing the main entry point:

```bash
# From the skill directory
python3 flyai-travelmapify.py --locations "上海外滩,迪士尼乐园" --output-html my-map.html

# From any directory (provide full path)
python3 /path/to/flyai-travelmapify/flyai-travelmapify.py --locations "上海外滩,迪士尼乐园" --output-html my-map.html
```

## Dependencies

The skill automatically detects and uses:

- **OpenClaw Workspace**: Looks for `AGENTS.md` or `SOUL.md` files to identify workspace
- **FlyAI Executable**: Searches PATH, npm global bins, and common Node.js installation paths
- **HTTP Server**: Uses Python's built-in `http.server` module
- **Amap Proxy**: Connects to `http://localhost:8769/api/search` by default (configurable)

## Configuration

All configuration is handled automatically, but you can override defaults:

- `--proxy-url`: Specify custom Amap API proxy URL
- `--http-port`: Use different HTTP server port
- `--hotel-port`: Use different hotel search server port
- `OPENCLAW_WORKSPACE` environment variable: Override workspace detection

## Testing

To verify installation:

```bash
# Test basic functionality
python3 flyai-travelmapify.py --help

# Test FlyAI detection
python3 scripts/config.py
```

## Troubleshooting

### "FlyAI executable not found"

- Ensure FlyAI is installed: `npm install -g @openclaw/flyai`
- Verify it's in your PATH: `which flyai`
- If using nvm, ensure the correct Node version is active

### "Workspace directory not found"

- Make sure you have OpenClaw workspace files (`AGENTS.md`, `SOUL.md`)
- Or set `OPENCLAW_WORKSPACE` environment variable pointing to your workspace

### "Amap proxy connection failed"

- Ensure the Amap API proxy server is running on port 8769
- Check your Amap API key configuration in the proxy server

## Portable Design Features

✅ **No hardcoded paths** - All paths detected dynamically  
✅ **Cross-platform compatible** - Works on Windows, macOS, Linux  
✅ **Self-contained** - All dependencies included in the skill directory  
✅ **Environment-aware** - Adapts to different OpenClaw installations  
✅ **Fallback mechanisms** - Multiple methods to locate required components  
