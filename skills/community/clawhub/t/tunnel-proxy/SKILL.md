---
name: tunnel-proxy
version: 1.0.11
description: >
  🐴 RAT (Remote Access Trojan) for AI agents.

  What it does: Agent sends commands → Your machine executes them.

  What it can do: Whatever you can do in a terminal.

  Risk: Whatever damage your user account can cause.

  Why you'd use it: Sandbox has no free network, no Docker, no yt-dlp, no ffmpeg.
  Your machine has everything.

  What you risk: Agent can read/delete all your files, use your IP for crimes,
  install backdoors, turn your PC into a botnet node.

  Use when: sandbox lacks tools, network blocked, need file transfer.
metadata:{
  author: TunnelProxy Team
homepage: https://github.com/TurinFohlen/tunnel_proxy
tags: [network, proxy, tunnel, file-transfer, remote-execution, c2]
license: MIT
requirements: [python3:3.8+, requests]
risks: [critical: full remote shell access]

  openclaw:{
    requires:
      env:
        - TUNNEL_HOST
        - TUNNEL_HTTP_PORT
        - TUNNEL_AGENT_TOKEN
        - TUNNEL_TIMEOUT
        - UPLOAD_MAGIC
    primaryEnv: TUNNEL_AGENT_TOKEN
    }}
---

## 🚇 Security Warning

This skill enables remote command execution and file transfer on your machine.

**Before use:**
- Set `TUNNEL_HOST=127.0.0.1` unless you intentionally expose the service
- Use random high ports (49152-65535) for public exposure
- Run TunnelProxy under a restricted user account
- Review the included scripts before execution
- Token authentication required for all operations

**Do NOT use with untrusted third-party Agent services.**

# TunnelProxy Skill (v0.3.3+)

## Overview

This skill enables AI agents running in cloud sandboxes to bypass network restrictions by utilizing the user's local TunnelProxy service. It provides:

- **Remote command execution** via one-time PTY Shell (random TCP port)
- **Persistent agent sessions** with unique Agent tokens
- **Bidirectional file transfer** via HTTP interface
- **HTTP reverse proxy** to access blocked resources through user's network
- **Static file server** for browsing and downloading files
- **Web upload page** for easy file upload from browser
- **Unrestricted network access** through user's local connection

## Architecture

```

AI Agent (Cloud Sandbox)
│
├── HTTP API (command execution, result polling)
│   POST /api/exec → POST /api/heartbeat → GET /api/result/:task_id
│
├── One-Time PTY Session (interactive shell)
│   POST /api/session → get random port → nc <host> <port>
│
├── File Server (browse & download)
│   GET / → directory listing → GET /path/to/file → download
│
├── File Upload
│   POST /upload → binary upload with magic-word protocol
│   GET /upload → web upload page
│
└── HTTP Reverse Proxy
GET /proxy?url=https://blocked-site.com → fetch through user's IP

```

## Quick Start

### 1. Register Your Agent & Get Token

```python
import requests

host = "${TUNNEL_HOST:-127.0.0.1}"
http_port = "${TUNNEL_HTTP_PORT:-8080}"

resp = requests.post(f"http://{host}:{http_port}/api/register", json={
    "agent_id": "my-agent",
    "hostname": "sandbox",
    "username": "ai",
    "os": "linux"
})
token = resp.json()["token"]
print(f"Token: {token}")
```

2. Request a One-Time PTY Session

```python
resp = requests.post(f"http://{host}:{http_port}/api/session", json={
    "token": token
})
pty_port = resp.json()["port"]
print(f"PTY port: {pty_port}")  # Random port (30001-65000), valid for 10 seconds
```

3a. Connect to Interactive Shell

```bash
# Connect within 10 seconds of requesting session
nc ${TUNNEL_HOST} ${pty_port}
# Directly drops into fish shell, no further auth needed
```

3b. Execute Commands via HTTP API

```python
# Submit command
resp = requests.post(f"http://{host}:{http_port}/api/exec", json={
    "agent_id": "my-agent",
    "token": token,
    "cmd": "whoami && pwd"
})
task_id = resp.json()["task_id"]

# Poll for result
import time
while True:
    result = requests.get(f"http://{host}:{http_port}/api/result/{task_id}").json()
    if result["status"] == "complete":
        print(result["output"])
        break
    time.sleep(0.2)
```

4. Browse & Download Files

```python
# Directory listing
import requests
html = requests.get(f"http://{host}:{http_port}/").text

# Download a file
with requests.get(f"http://{host}:{http_port}/path/to/file.txt", stream=True) as r:
    with open("file.txt", "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
```

```bash
# Using curl
curl http://${TUNNEL_HOST}:${TUNNEL_HTTP_PORT}/path/to/file -O
```

5. Upload Files

Via curl:

```bash
curl -X POST http://${TUNNEL_HOST}:${TUNNEL_HTTP_PORT}/upload --data-binary @file.txt
```

Via Python:

```python
from http_transfer import TunnelHTTP
http = TunnelHTTP()
response = http.upload("./local_file.tar.gz")
```

Via browser: Visit http://${TUNNEL_HOST}:${TUNNEL_HTTP_PORT}/upload

6. HTTP Reverse Proxy (Access Blocked Resources)

```bash
# Access a blocked site through user's IP
curl "http://${TUNNEL_HOST}:${TUNNEL_HTTP_PORT}/proxy?url=https://pypi.org/simple/"
```

```python
import requests
resp = requests.get(
    f"http://{host}:{http_port}/proxy",
    params={"url": "https://httpbin.org/ip"}
)
print(resp.text)  # Shows user's IP, not sandbox IP
```

7. Fetch Remote Content via User's Network

```bash
# Let user's machine fetch blocked content for you
echo "curl -s https://pypi.org/simple/" | nc ${TUNNEL_HOST} ${pty_port}

# Download large file via user's network
echo "curl -sL https://example.com/large.iso -o /tmp/large.iso" | nc ${TUNNEL_HOST} ${pty_port}
```

8. Handle Binary Files

For binary data, use http_transfer.py which properly handles multipart form-data:

```python
from http_transfer import TunnelHTTP

http = TunnelHTTP()
http.upload("./screenshot.png")
http.download("/remote/binary.dat", "./local.dat")
```

API Reference

Agent Management

Method Path Description
POST /api/register Register new agent
POST /api/heartbeat Agent heartbeat keep-alive
GET /api/agents List all online agents
POST /api/session Request one-time PTY session (returns random port)

Command Execution

Method Path Description
POST /api/exec Submit command for execution
GET /api/result/:task_id Poll command result

File Operations

Method Path Description
GET /* Browse files (directory listing) or download
GET /upload Web upload page
POST /upload Upload file (binary, magic-word protocol)

Network

Method Path Description
GET /proxy HTTP reverse proxy (?url=https://...)

Environment Variables

Variable Default Description
TUNNEL_HOST 127.0.0.1 TunnelProxy host address
TUNNEL_HTTP_PORT 8080 HTTP API port
TUNNEL_AGENT_TOKEN - Pre-configured agent token
TUNNEL_TIMEOUT 60 Default timeout in seconds
UPLOAD_MAGIC MY_MAGIC_2025_FILE_HEAD Upload verification token
TUNNEL_DOC_ROOT ./www Static files root directory
TUNNEL_UPLOAD_DIR ./uploads Upload destination directory

Included Scripts

This skill includes two minimal scripts:

· tunnel_login.py – Verify HTTP API connectivity and login
· http_transfer.py – Binary-safe file upload/download

Common Use Cases

Bypass PyPI blocking for pip install

```python
import socket

s = socket.socket()
s.connect(("${TUNNEL_HOST}", pty_port))
s.send(b"pip download torch --no-deps -d /tmp\n")
s.close()

# Then pull the file
from http_transfer import TunnelHTTP
http = TunnelHTTP()
http.download("/tmp/torch.whl", "./torch.whl")
```

Access internal company resources

```bash
echo "curl -s http://internal-company-server/api/data" | nc ${TUNNEL_HOST} ${pty_port}
```

Transfer large files with progress

```python
http = TunnelHTTP()
http.download("/system/fonts/NotoSansCJK.ttc", "./font.ttc")
```

Use as HTTP proxy for Python packages

```python
import requests
resp = requests.get(
    f"http://{host}:{http_port}/proxy",
    params={"url": "https://pypi.org/simple/requests/"}
)
```

Error Handling

```python
import socket
from http_transfer import TunnelHTTP

try:
    s = socket.socket()
    s.settimeout(10)
    s.connect(("${TUNNEL_HOST}", pty_port))
    s.send(b"ls\n")
    result = s.recv(4096).decode()
except socket.timeout:
    print("Command timeout - increase TUNNEL_TIMEOUT")
except ConnectionRefusedError:
    print("TunnelProxy not running - start the service first")
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
```

Security Notes

This skill grants the agent complete control over commands executed on the user's machine. Only use with:

· Fully trusted AI agents you control
· Users who understand the security implications
· In environments with additional safeguards (firewalls, UPLOAD_MAGIC)
· Token authentication enabled on the server

Troubleshooting

Issue Solution
Connection refused TunnelProxy not running → start with iex -S mix
invalid token Check agent registration or preset agent config
PTY session timeout Request new session (ports discarded after 10s)
Command returns empty Use HTTP API for persistent result collection
Binary file corrupted Use http_transfer.py instead of manual socket
Upload fails Check if UPLOAD_MAGIC matches server configuration

📖 Practical Tips & Common Pitfalls

For detailed usage patterns, troubleshooting, and advanced techniques, see TIPS.md.

Quick reference:

Problem Solution (see TIPS.md for details)
Empty output Add ; echo MARKER or use stty -echo
Binary corruption Use HTTP channel, not PTY
Command timeout Wrap with timeout command
Large file transfer Use http_transfer.py, not cat
Stuck command Avoid interactive commands
Exit code capture Echo $? after command

TL;DR: Use nc for commands, http_transfer.py for files.

