---
name: remotego
description: "Expose any CLI tool as a public web terminal via tunnel. Mirror bash, vim, python, node, or any command in a browser for remote access and collaboration."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🌐"
    homepage: https://github.com/topcheer/claude-remoting
    os:
      - macos
      - linux
---

# remotego - Expose Any CLI as a Public Web Terminal

Mirror any CLI tool in a browser with a public URL. Share your terminal with anyone over the internet.

## When to Use

The user wants to:
- Share their terminal session with someone remotely
- Access a CLI tool from a browser
- Collaborate on a terminal session in real-time
- Expose a local CLI to a public URL

## How to Use

 remotego is installed globally via npm. Run it with any command:

```bash
remotego <command> [command-args...] [options]
```

### Quick Examples

| Goal | Command |
|------|---------|
| Mirror Claude Code | `remotego claude` |
| Mirror bash | `remotego bash` |
| Mirror Python REPL | `remotego python3 -i` |
| Mirror vim | `remotego vim` |
| Mirror Node.js REPL | `remotego node` |
| Custom port | `remotego --port 9000 bash` |
| Custom tunnel domain | `remotego --domain myterm.localhost.run bash` |
| Pass flags to command | `remotego -- git log --oneline` |

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--port <port>` | Local HTTP port | `7681` |
| `--cwd <dir>` | Working directory | Current dir |
| `--domain <domain>` | Custom localhost.run domain | Random |
| `--help, -h` | Show help | |

### Install First (if not installed)

```bash
npm install -g @remotego/remotego
```

Or use without installing:

```bash
npx @remotego/remotego bash
```

## What Happens

1. Spawns the command in a PTY (pseudo-terminal)
2. Starts a local HTTP server with xterm.js browser terminal
3. Creates a public tunnel via localhost.run
4. Opens the browser automatically with a session URL

## Security Model

- A random session UUID is generated on each start
- The session ID is embedded in the URL — only URL holders can connect
- Clients must authenticate within 5 seconds of connecting

## Stopping

Press `Ctrl+C` in the terminal running remotego.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `node` not found | Install from https://nodejs.org/ |
| Tunnel fails | Check if SSH port 22 is blocked; falls back to localhost |
| Port in use | Use `--port` to specify a different port |
| Browser doesn't open | Manually open the URL shown in terminal output |
