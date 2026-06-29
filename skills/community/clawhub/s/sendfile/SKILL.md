---
name: sendfile
version: 1.0.5
description: Send files to users in chat by creating a temporary public download link via aitun tunnel. Perfect for AI agents that need to deliver generated files (documents, images, reports, code) to users.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "📁"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/sendfile
---

# SendFile - Deliver Files to Users via Temporary Public Link

## When to Use

Use this skill when:
- You generated a file (document, image, report, spreadsheet, code, etc.) and need to send it to the user
- The user asks to download a file you created
- You need to share a local file with the user in a chat conversation
- The chat platform does not support direct file uploads, or the file is too large
- You want to give the user a direct download link they can open in any browser

Do NOT use this skill when:
- The content can be displayed inline as text in the chat (just paste it)
- The file is already hosted at a public URL (share the existing URL instead)
- The file contains sensitive secrets or credentials (avoid exposing via public links)

## Prerequisites

Install the aitun client (any one of):

```bash
# Install via pip (recommended, cross-platform, bundles the binary)
pip install aitun
```

```bash
# Or one-line install script (Linux/macOS)
curl -fsSL https://aitun.cc/install.sh | bash
```

```powershell
# Windows (PowerShell)
irm https://aitun.cc/install.ps1 | iex
```

Verify the install:

```bash
which aitun
aitun --help
```

## Instructions

### Step 1: Locate the file

Identify the file you want to send. This is typically a file you just generated:
- A document: `.pdf`, `.docx`, `.pptx`, `.xlsx`
- An image: `.png`, `.jpg`, `.svg`
- A code archive: `.zip`, `.tar.gz`
- Any other file the user requested

Verify the file exists:
```bash
ls -lh /path/to/your/file.ext
```

### Step 2: Start a local file server

Start a simple HTTP server in the directory containing the file:

```bash
# If the file is at /path/to/output/report.pdf
cd /path/to/output
python3 -m http.server 8080 &
FILE_PID=$!
sleep 1
```

### Step 3: Create a tunnel

Use aitun to expose the local server to the internet:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

### Step 4: Build the download link

Append the filename to the public URL to create a direct download link:

```
https://aitun.cc/abc123/report.pdf
```

### Step 5: Send the link to the user

Deliver the download link to the user in the chat:

```
Your file is ready for download: https://aitun.cc/abc123/report.pdf

This link is temporary and will expire in 24 hours. Download it soon.
```

### Step 6: Clean up

After the user confirms they have downloaded the file, stop the servers:

```bash
kill $AITUN_PID 2>/dev/null
kill $FILE_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- Traffic can go through P2P direct connection or server relay, both are encrypted end-to-end
- For a permanent subdomain (e.g., `files.aitun.cc`), register at https://aitun.cc
- The download link works in any browser on any device — no installation required for the user
- Only one file server can run on the same port; if you need to serve files from different directories, use different ports
