# use-cursor

> OpenClaw skill for managing Cursor CLI tasks via tmux with security hardening

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What It Does

This skill enables OpenClaw to execute Cursor CLI for software engineering tasks:

- 🚀 **Background tasks** - Long-running coding jobs in tmux (no timeout)
- 📊 **Status monitoring** - Check task progress anytime
- 💬 **Interactive control** - Send follow-up instructions
- 🔒 **Security hardened** - Shell escaping, output redaction, privacy protection
- 🛡️ **Isolation modes** - Standard, isolated (minimal env), or container

## Quick Start

### Prerequisites

```bash
# Install tmux
sudo apt install tmux  # Ubuntu/Debian
brew install tmux      # macOS

# Install Cursor CLI
curl https://cursor.com/install -fsS | bash

# Authenticate
agent login
```

### Installation

```bash
# Via ClawHub
clawhub install <author>/use-cursor

# Or manual
git clone <repo> ~/.openclaw/workspace/skills/use-cursor
```

### Usage

```bash
# Start a task (standard mode)
use_cursor_spawn "Refactor src/ for better performance"

# Start a task (isolated mode - recommended for sensitive projects)
use_cursor_spawn_isolated "Task description"

# Check status
use_cursor_check cursor-123456

# Send follow-up
use_cursor_send cursor-123456 "Also add type annotations"

# List tasks
use_cursor_list

# Kill task
use_cursor_kill cursor-123456

# Environment check
use_cursor_doctor
```

## Security

**Read before installing:** [SECURITY.md](SECURITY.md)

### Key Points

- ✅ Shell arguments escaped (single-quote method, prevents injection)
- ✅ tmux literal mode (`-l` flag, prevents metacharacter expansion)
- ✅ Email addresses redacted in output
- ✅ API keys/tokens redacted in output
- ✅ Isolated mode available (minimal environment, hardcoded PATH)
- ⚠️ Reads `~/.cursor/cli-config.json` (auth check only)
- ⚠️ Captures tmux output (may contain workspace data)

### Execution Modes

| Mode | Environment | Use Case |
|------|-------------|----------|
| **Standard** | Full env | Normal development |
| **Isolated** | Minimal env | Sensitive projects, untrusted inputs |
| **Container** | Docker/Podman | Maximum isolation |

### Safe For

- ✅ Personal dev machines
- ✅ Standard coding projects
- ✅ Open source work

### Review First For

- ⚠️ Corporate environments
- ⚠️ Projects with secrets
- ⚠️ Shared servers

### Not Recommended For

- ❌ Production servers with live credentials
- ❌ Machines with high-value secrets (use isolated mode instead)

## Tools

| Tool | Description |
|------|-------------|
| `use_cursor_spawn` | Start background task (standard mode) |
| `use_cursor_spawn_isolated` | Start task with minimal environment |
| `use_cursor_check` | Check task status |
| `use_cursor_send` | Send additional instructions |
| `use_cursor_kill` | End task |
| `use_cursor_list` | List all tasks |
| `use_cursor_doctor` | Diagnose environment |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "use-cursor": {
        "enabled": true
      }
    }
  }
}
```

## Development

```bash
# Run diagnostics
npm run doctor

# Test
npm run test
```

## License

MIT

## Authors

- Bruce
- 凤雏 (Feng Chu)

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-31
