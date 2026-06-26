# Security Documentation

## Security Model

This skill manages Cursor CLI tasks via tmux. It requires trust because it:

1. **Executes shell commands** - Uses tmux and Cursor CLI
2. **Reads local config** - Checks `~/.cursor/cli-config.json` for auth status
3. **Captures output** - Returns tmux pane content to the agent

## Security Improvements in v1.0.0

### Fixed Issues

| Issue | Status | Fix |
|-------|--------|-----|
| Shell injection via unescaped args | ✅ Fixed | All args escaped with single-quote method (`'arg'` → `'arg'\''s'`) |
| Email exposure in output | ✅ Fixed | Redacted to `***@domain.com` |
| API key exposure | ✅ Fixed | Redacted from output |
| Undocumented env access | ✅ Fixed | Added `required.env` to package.json |
| Autonomous execution | ✅ Safe | `always: false` (user-invocable only) |

### Remaining Considerations

| Risk | Severity | Mitigation |
|------|----------|------------|
| tmux output may contain sensitive code | Medium | Review output before sharing; run in isolated env for sensitive projects |
| Config file access | Low | Only reads auth status, redacts PII |
| Shell command execution | Medium | All inputs escaped; review scripts if concerned |

## Safe Usage Guidelines

### ✅ Safe Environments

- Personal development machines
- Standard coding projects
- Open source work
- Learning/experimentation

### ⚠️ Review First

- Corporate environments with IP concerns
- Projects with API keys/secrets in code
- Shared development servers

### ❌ Not Recommended

- Production servers with live credentials
- Machines with high-value secrets
- Air-gapped systems without review

## Isolation Modes

### Standard Mode (Default)

```bash
use_cursor_spawn "task description"
```

- Uses full environment (inherits all env vars)
- Suitable for normal development
- May expose env vars to Cursor CLI

### Isolated Mode (Recommended for Sensitive Projects)

```bash
# Use spawn-isolated.sh directly
bash scripts/spawn-isolated.sh my-session "task description"
```

- Clears most environment variables
- Only keeps: `PATH`, `HOME`, `USER`, `CURSOR_API_KEY`
- Reduces risk of secret exposure
- Recommended for:
  - Untrusted task inputs
  - Shared machines
  - Corporate environments

### Container Mode (Maximum Security)

Run inside Docker/Podman:

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -v ~/.cursor:/root/.cursor:ro \
  your-image \
  use_cursor_spawn "task"
```

- Complete filesystem isolation
- Network can be disabled (`--network none`)
- Best for high-security requirements

## Technical Details

### Shell Escaping (Node.js)

```javascript
// All shell arguments are escaped using single-quote method:
function escapeShellArg(arg) {
    let str = String(arg);
    
    // SECURITY: Remove newlines and control characters to prevent tmux injection
    // Even with -l flag, newlines in tmux send-keys act as Enter keypress
    str = str.replace(/[\r\n\t]/g, ' ');      // Replace newlines/tabs with spaces
    str = str.replace(/[\x00-\x1f\x7f]/g, ''); // Remove control chars
    
    // Escape single quotes: ' → '\''
    const escaped = str.replace(/'/g, "'\\''");
    return `'${escaped}'`;
}

// Example:
// Input:  task'; rm -rf /
// Output: 'task'\''; rm -rf /'
// Shell receives: literal string, no injection possible

// Input with newline (BLOCKED):
// Input:  "task\nrm -rf /"
// After sanitize: "task rm -rf /"
// Output: 'task rm -rf /'  (newline removed, no injection)
```

### tmux Literal Mode

**ALL** tmux send-keys invocations now use `-l` flag:

```bash
# spawn.sh - cd command
tmux send-keys -t "$SESSION_NAME" -l -- "cd $WORKDIR" Enter

# spawn.sh - agent invocation
tmux send-keys -t "$SESSION_NAME" -l -- "$AGENT_CMD --model auto --print --trust $TASK" Enter

# send.sh - user commands
tmux send-keys -t "$SESSION_NAME" -l -- "$COMMAND" Enter
```

**What `-l` does:**
- Sends keys literally to tmux
- Prevents tmux from interpreting `$`, `` ` ``, `\`, `|`, `;`, etc.
- Even if pane runs a shell, metacharacters are NOT expanded
- This is the tmux-recommended way to send untrusted text

### Argument Flow (No Double-Quoting)

```
User Input:  "task'; rm /"
    ↓
JS escapeShellArg():  'task'\''; rm /'
    ↓
bash script.sh 'task'\''; rm /'
    ↓
script receives: $TASK = task'; rm /  (literal string)
    ↓
tmux send-keys -l -- "agent --trust $TASK"
    ↓
tmux sends literal: agent --trust task'; rm /
    ↓
Cursor receives: literal string "task'; rm /" (no injection)
```

**Key fix in v1.0.0:**
- Removed extra quoting in JS layer (`'${params.task}'` → `params.task`)
- Scripts use `-l` flag, so no shell expansion occurs
- Clean, single-pass escaping

### Environment Isolation

**Standard mode:**
```bash
# Inherits full environment (convenient but less secure)
agent --print --trust "task"
```

**Isolated mode:**
```bash
# Clears all env vars, sets only safe ones
env -i \
  PATH=/usr/local/bin:/usr/bin:/bin \
  HOME=$HOME \
  USER=$USER \
  CURSOR_API_KEY=${CURSOR_API_KEY:-} \
  agent --print --trust "task"
```

**PATH is hardcoded** to prevent malicious PATH injection.

### Output Redaction

```javascript
// Redacts from output:
// - Email addresses → [EMAIL_REDACTED]
// - API keys (sk-...) → [KEY_REDACTED]
// - Token patterns → token=[REDACTED]
```

### File Access

| File | Access Type | Data Extracted |
|------|-------------|----------------|
| `~/.cursor/cli-config.json` | Read (grep) | Email domain only |
| `~/.cursor/credentials` | Existence check | None |
| `$CURSOR_API_KEY` | Env var check | None |

## Audit Checklist

Before installing on sensitive systems:

- [ ] Review `scripts/*.sh` for shell commands
- [ ] Review `extensions/use-cursor/index.js` for data handling
- [ ] Test in isolated environment first
- [ ] Configure OpenClaw to require user approval for tool calls
- [ ] Ensure tmux and Cursor CLI are from trusted sources

## Incident Response

If you suspect misuse:

1. **Kill all tmux sessions**: `tmux kill-server`
2. **Review logs**: Check OpenClaw logs for tool invocations
3. **Rotate credentials**: If you ran on a system with secrets
4. **Report**: File an issue on the skill repository

## Version History

| Version | Date | Security Changes |
|---------|------|------------------|
| 1.0.4 | 2026-03-31 | Control character sanitization (newline injection fix) |
| 1.0.3 | 2026-03-31 | Fixed documentation mismatch (JSON.stringify → single-quote) |
| 1.0.2 | 2026-03-31 | Enhanced code comments, child_process justification |
| 1.0.1 | 2026-03-31 | Fixed spawn-isolated.sh missing -l flag |
| 1.0.0 | 2026-03-31 | Shell escaping, output redaction, security docs, tmux -l mode |
| 0.1.0 | 2026-03-30 | Initial release |

## Contact

Report security issues to: [your contact info]

---

*Last updated: 2026-03-31*
*Version: 1.0.0*
