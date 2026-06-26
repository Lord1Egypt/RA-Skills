---
name: use-cursor
version: 1.0.4
description: Manage Cursor CLI tasks via tmux with security hardening
author: Bruce + 凤雏
license: MIT
source: https://github.com/openclaw/skills/tree/main/use-cursor
homepage: https://github.com/openclaw/skills
repository: https://github.com/openclaw/skills/tree/main/use-cursor

required:
  binaries:
    - tmux
    - agent
  env:
    - CURSOR_API_KEY

clawhub:
  security:
    autonomous: false
    always: false
    userInvocable: true
---

# Use Cursor - OpenClaw + Cursor CLI Integration

Enable OpenClaw to execute Cursor CLI for various software engineering tasks, supporting interactive mode, background tasks, CI/CD, and more.

---

## 🔒 Security Notes

**Before installing, understand these security implications:**

### What This Skill Does

- ✅ Manages Cursor CLI tasks via tmux (stated purpose)
- ✅ Reads `~/.cursor/cli-config.json` to check auth status (email **redacted** in output)
- ✅ Captures tmux pane output (may contain workspace code/data)
- ✅ All shell arguments are **escaped** to prevent injection
- ✅ Does **not** download remote code at install time

### Privacy Considerations

| Data Access | Purpose | Protection |
|-------------|---------|------------|
| `~/.cursor/cli-config.json` | Check auth status | Email redacted (shows `***@domain.com`) |
| `~/.cursor/credentials` | Check auth status | Not read, only existence checked |
| `$CURSOR_API_KEY` | Optional auth | Not logged or stored |
| `$PATH`, `$HOME`, etc. | Inherited by child processes | Not modified or logged |
| tmux output | Return task results | May contain workspace data |

### ⚠️ Critical: tmux Pane Execution Risk

This skill sends user-provided strings into tmux panes via `tmux send-keys`. 

**How it works:**
1. Script creates tmux session
2. Runs `agent --print --trust 'TASK'` in the pane
3. Captures pane output and returns to agent

**Risk:** If the pane is running a shell, any text sent via `send-keys` will be executed. While we escape arguments at the JavaScript level, special characters/control sequences could still affect the shell.

**Mitigation:**
- Use in isolated environments (container/VM) for untrusted tasks
- Don't run on production machines with live secrets
- Review task strings before sending

### Recommendations

| Environment | Recommendation |
|-------------|----------------|
| Personal dev machine | ✅ Safe for normal projects |
| Open source work | ✅ Safe |
| Corporate environment | ⚠️ Review with security team first |
| Production server | ❌ Not recommended |
| Machine with high-value secrets | ❌ Use isolated container/VM |

### Security Features (v1.0.0+)

- ✓ Shell argument escaping via single-quote method (prevents injection)
- ✓ tmux literal mode (`-l` flag) for all send-keys commands
- ✓ Email redaction (`***@domain.com`)
- ✓ API key/token redaction in output
- ✓ No autonomous execution (`always: false`)
- ✓ No remote code download
- ✓ Explicit permissions declared in manifest
- ✓ Isolated mode with minimal environment (hardcoded PATH)

---

## 🎯 Use Cases

| Scenario | Recommended Mode | Description |
|----------|-----------------|-------------|
| Quick tasks | Interactive | Direct `agent "task description"` |
| Long-running coding | Background | tmux-managed, no timeout |
| CI/CD automation | Non-interactive | `agent -p` + JSON output |
| Code review | Interactive/Background | With context analysis |
| Large refactoring | Background | Interruptible, resumable |

---

## 📦 Installation

### 1. Install Cursor CLI

**⚠️ Security Note:** The following install commands use remote scripts. Review them first or use your package manager when possible.

**macOS:**
```bash
# Recommended: use Homebrew (review formula first)
brew install --cask cursor-cli

# Alternative: official installer (review at https://cursor.com/install)
# curl https://cursor.com/install -fsS | bash
```

**Linux/WSL:**
```bash
# Download and inspect the installer first
curl -fsS https://cursor.com/install -o cursor-install.sh
less cursor-install.sh  # Review before running
bash cursor-install.sh

# Or check if available via your package manager
```

**Verify installation:**
```bash
agent --version
# or
cursor-agent --version
```

**Required Dependencies:**
- `tmux` - Terminal multiplexer (required for background tasks)
- `agent` or `cursor-agent` - Cursor CLI (required)
- `CURSOR_API_KEY` - Optional, or use `agent login` for browser auth

### 2. Authentication

```bash
agent login
# or set API key
export CURSOR_API_KEY=your_api_key_here
```

### 3. Install tmux (Required for background tasks)

```bash
# Ubuntu/Debian
sudo apt install tmux

# macOS
brew install tmux

# CentOS/RHEL
sudo yum install tmux
```

---

## 🛠️ OpenClaw Tools

### Tool List

| Tool | Description | Example |
|------|-------------|---------|
| `use_cursor_spawn` | Start background Cursor task (standard mode) | `use_cursor_spawn "refactor this module"` |
| `use_cursor_spawn_isolated` | Start task with minimal environment | `use_cursor_spawn_isolated "task"` |
| `use_cursor_check` | Check task status | `use_cursor_check session-name` |
| `use_cursor_send` | Send additional instructions | `use_cursor_send session-name "make it async"` |
| `use_cursor_kill` | End task | `use_cursor_kill session-name` |
| `use_cursor_list` | List all tasks | `use_cursor_list` |
| `use_cursor_doctor` | Diagnose environment | `use_cursor_doctor` |

### Execution Modes

| Mode | Script | Use Case |
|------|--------|----------|
| **Standard** | `spawn.sh` | Normal development, trusted tasks |
| **Isolated** | `spawn-isolated.sh` | Untrusted inputs, shared machines |
| **Container** | Docker/Podman | Maximum isolation (manual setup) |

---

## 🚀 Usage

### Method 1: Background Task Mode (Recommended for large jobs)

```
User: Help me refactor this module using Cursor in background
→ Call: use_cursor_spawn "refactor src/ directory for better performance"
→ Returns: Task ID + tmux session name
```

**Follow-up operations:**
```
User: Check the progress of that task
→ Call: use_cursor_check <session-name>

User: Tell that task: change to TypeScript
→ Call: use_cursor_send <session-name> "implement in TypeScript"

User: Stop that Cursor task
→ Call: use_cursor_kill <session-name>
```

### Method 2: Direct Run Mode (Small tasks)

```
User: Write a unit test for me
→ Call: use_cursor_run "write unit tests for src/utils.ts"
→ Wait for completion, return result
```

### Method 3: Interactive Mode (Local debugging)

```bash
# Start interactive session
agent

# Or with task directly
agent "fix this bug"

# Switch model
/models

# Add context
@src/api/
@src/models/
```

---

## 📋 Cursor CLI Command Reference

### Basic Commands

| Command | Description |
|---------|-------------|
| `agent` | Start interactive session |
| `agent "task"` | Execute task directly |
| `agent -p "task"` | Print mode (for scripts) |
| `agent --model <name>` | Specify model |
| `agent --resume="<id>"` | Resume session |
| `agent ls` | List sessions |
| `agent resume` | Resume most recent session |
| `agent models` | List available models |
| `agent update` | Update CLI |

### Slash Commands (Interactive Mode)

| Command | Description |
|---------|-------------|
| `/models` | Switch models |
| `/compress` | Compress session history |
| `/rules` | Manage rules |
| `/commands` | Manage custom commands |
| `/mcp enable <server>` | Enable MCP server |
| `/mcp disable <server>` | Disable MCP server |

### Keyboard Shortcuts

| Shortcut | Description |
|----------|-------------|
| `Shift+Enter` | New line |
| `Ctrl+D` | Exit (requires double-press) |
| `Ctrl+R` | Review changes |
| `↑/↓` | History messages |

---

## 🔧 Background Task Architecture

```
User (Discord/Feishu) 
  → OpenClaw Agent 
  → use_cursor_spawn tool 
  → tmux session 
  → Cursor CLI Agent
```

### tmux Session Management

```bash
# Create session
tmux new-session -d -s cursor-task-001

# Send command
tmux send-keys -t cursor-task-001 "agent 'task description'" Enter

# Capture output
tmux capture-pane -t cursor-task-001 -p -S -100

# End session
tmux kill-session -t cursor-task-001
```

---

## 📊 Workflows

### Code Review

```bash
agent -p 'Review the changes in the current branch against main. Focus on security and performance.'
```

### Refactoring

```bash
agent -p 'Refactor src/utils.ts to reduce complexity and improve type safety.'
```

### Debugging

```bash
agent -p 'Analyze the following error log and suggest a fix: [paste log here]'
```

### Git Integration

```bash
agent -p 'Generate a commit message for the staged changes adhering to conventional commits.'
```

### CI/CD

```bash
# Security audit (JSON output)
agent -p 'Audit this codebase for security vulnerabilities' --output-format json --force

# Test coverage
agent -p 'Run tests and generate coverage report' --output-format text
```

---

## ⚠️ Notes

### TTY Issues

**❌ These will hang:**
```bash
agent "task"                    # No TTY
agent -p "task"                 # No TTY  
subprocess.run(["agent", ...])  # No TTY
```

**✅ Correct approach:**
```bash
# Use tmux for pseudo-terminal
tmux new-session -d -s cursor
tmux send-keys -t cursor "agent 'task'" Enter
```

### Timeout Protection

- Small tasks (<5 min): Use `use_cursor_run` directly
- Medium tasks (5-30 min): Background mode + periodic checks
- Large tasks (>30 min): Background mode +分段 execution

### Resource Management

- Each tmux session uses ~50-100MB memory
- Recommend max 3-5 concurrent background tasks
- Use `use_cursor_kill` to clean up completed tasks

---

## 🏥 Troubleshooting

### `use_cursor_doctor` Checklist

1. ✅ tmux installed
2. ✅ agent CLI executable
3. ✅ Authentication status (CURSOR_API_KEY or login)
4. ✅ Working directory permissions
5. ✅ Network connectivity

### Common Issues

**Q: Task exits immediately after starting**
- Check Cursor authentication status
- Ensure working directory has code

**Q: tmux session not found**
- Run `use_cursor_list` to check active sessions
- May have been killed or timed out

**Q: Garbled output**
- tmux encoding issue, try `export LANG=en_US.UTF-8`

### Security FAQs

**Q: Does this skill send my code to external servers?**
- A: No. Code stays on your machine. Cursor CLI may send to Anthropic/Claude API (that's how Cursor works).

**Q: Can this skill access my Cursor API key?**
- A: It can detect if `$CURSOR_API_KEY` is set, but doesn't log or transmit it.

**Q: Is my email address exposed?**
- A: No. Email is redacted to `***@domain.com` in all outputs.

**Q: Can malicious input cause shell injection?**
- A: v1.0.0+ escapes all shell arguments. Earlier versions had this risk.

---

## 📁 File Structure

```
use-cursor/
├── SKILL.md              # This document
├── scripts/
│   ├── spawn.sh          # Start background task
│   ├── check.sh          # Check status
│   ├── send.sh           # Send instructions
│   ├── kill.sh           # End task
│   └── doctor.sh         # Diagnose environment
├── extensions/
│   └── use-cursor/
│       └── index.js      # OpenClaw tool definitions
└── examples/
    └── openclaw.json     # Configuration example
```

---

## 🔗 References

- [Cursor Official Docs](https://cursor.com/docs)
- [Cursor CLI GitHub](https://github.com/getcursor/cursor)
- [tmux Usage Guide](https://github.com/tmux/tmux/wiki)
- [OpenClaw ACP Docs](https://docs.openclaw.ai/cli/acp)

---

*Version: 1.0.1*
*Merged from: cursor-agent (2.1.0) + openclaw-cursor-agent (1.0.0)*
*Authors: Bruce + 凤雏 🦞*
*Skill Name: use-cursor*

## Changelog

### v1.0.4 (2026-03-31)
- ✅ Fixed: Newline/control character injection vulnerability - now sanitized before escaping
- ✅ Added: Control char removal (/[\x00-\x1f\x7f]/g) to prevent all tmux control sequence attacks
- ✅ Updated: SECURITY.md with sanitization documentation
- ✅ Fixed: Documentation mismatch - changed "JSON.stringify()" to "single-quote method" in SECURITY.md
- ✅ Fixed: Repository/homepage URLs updated to openclaw/skills (no more placeholders)
- ✅ Fixed: Added source field to manifest.json for provenance tracking
- ✅ Enhanced: Detailed code comments explaining why child_process is safe
- ✅ Clarified: Static analysis flag (child_process) is FALSE POSITIVE for this use case
- ✅ Updated: manifest.json notes with child_process justification

### v1.0.1 (2026-03-31)
- ✅ Fixed: spawn-isolated.sh `cd` command now uses `-l` flag
- ✅ Verified: ALL tmux send-keys use literal mode (-l)
- ✅ Updated: manifest.json with detailed security notes
- ✅ Clarified: Default mode inherits env, isolated mode uses env -i

### v1.0.0 (2026-03-31)
- Initial release with security hardening
