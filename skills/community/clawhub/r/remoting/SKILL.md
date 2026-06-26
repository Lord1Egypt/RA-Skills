---
name: remoting
description: "Mirror your Claude Code terminal in a browser for remote viewing and real-time interaction. Creates a public web terminal via localhost.run tunnel."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🖥️"
    homepage: https://github.com/topcheer/claude-remoting
    os:
      - macos
      - linux
---

# /remoting - Mirror Claude Code in a Browser

Expose the current Claude Code session as a public web terminal. Anyone with the URL can view and interact with the terminal from their browser.

## When to Use

The user says something like:
- "Share my terminal"
- "Mirror my Claude session"
- "Let someone watch my screen"
- "Remote access to this terminal"
- "Open in browser"

## Quick Start

Install and launch:

```bash
# If not already installed
npm install -g @remotego/remotego

# Start mirroring Claude Code
remotego claude
```

Or run without installing:

```bash
npx @remotego/remotego claude
```

### With Options

```bash
# Custom port
remotego claude --port 9000

# Custom tunnel domain (localhost.run)
remotego claude --domain myterm.localhost.run

# Custom working directory
remotego claude --cwd ~/my-project
```

## What the User Sees

1. Terminal output shows:
   - Local URL: `http://localhost:7681?session=<uuid>`
   - Public URL: `https://xxxxx.lhr.life?session=<uuid>`
2. Browser opens automatically with the public URL
3. Terminal output from Claude Code appears in the browser in real-time
4. Browser users can type and interact with the session

## Security

- Random session UUID per start — only URL holders can connect
- 5-second auth timeout for new connections
- All output is cached so new viewers see full history

## Stopping

Press `Ctrl+C` in the terminal, or the user can type `/exit`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `node` not found | Install from https://nodejs.org/ |
| Tunnel fails | Falls back to localhost URL; check SSH port 22 |
| Port in use | Use `--port` to pick another |
