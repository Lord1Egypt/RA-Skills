---
name: static-server
description: Start a local HTTP server to preview static HTML pages. Use when testing static pages, previewing HTML files, or when browser tools cannot access file:// URLs. Provides localhost URL for browser testing.
---

# Static Server

Start a Python HTTP server to preview static HTML files in a browser.

## When to Use

- Testing static HTML pages
- Previewing web pages before deployment
- When browser tools block `file://` protocol
- Need a localhost URL for browser automation

## Quick Start

Use the bundled script to start a server:

```bash
python scripts/serve.py <path> [--port PORT]
```

**Arguments:**
- `<path>`: File path (serves parent directory) or directory path
- `--port`: Optional port number (default: 8000)

**Examples:**

```bash
# Serve a specific HTML file
python scripts/serve.py /path/to/index.html

# Serve a directory
python scripts/serve.py /path/to/project

# Use custom port
python scripts/serve.py /path/to/index.html --port 9000
```

## Output

The script prints:
- Access URL: `http://localhost:PORT/filename.html`
- Directory being served
- Instructions to stop (Ctrl+C)

## Usage in Testing

When testing static pages with browser tools:

1. Start server with `exec` (background mode)
2. Use the localhost URL with browser tools
3. Complete testing
4. Kill the server process

**Example workflow:**

```javascript
// 1. Start server in background
exec({
  command: "python scripts/serve.py /path/to/index.html --port 8888",
  background: true
})

// 2. Open in browser
browser({
  action: "open",
  targetUrl: "http://localhost:8888/index.html"
})

// 3. Test and screenshot
browser({ action: "screenshot", fullPage: true })

// 4. Clean up
process({ action: "kill", sessionId: "..." })
browser({ action: "close" })
```

## Alternative: One-liner

For quick testing without the script:

```bash
python -m http.server 8000 --directory /path/to/dir
```

Note: This serves the directory root, not a specific file.
