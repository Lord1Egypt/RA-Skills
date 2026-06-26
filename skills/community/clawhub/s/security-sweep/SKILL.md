---
name: security-sweep
description: Security scanner for OpenClaw skills and plugins. Scans for hardcoded secrets, dangerous exec patterns, dependency vulnerabilities, and network egress. Use when auditing installed skills/plugins, before publishing to ClawHub, or when a user requests a security review of skills or plugins.
version: 1.1.1
---

# Security Sweep — Skill & Plugin Auditor

Scans OpenClaw skills and plugins for:
1. **Hardcoded secrets** — API keys, tokens, passwords in code
2. **Dangerous exec patterns** — shell injection, eval, unsanitized child_process calls
3. **Dependency vulnerabilities** — npm audit failures
4. **Network egress** — unexpected outbound connections
5. **Input injection** — unsanitized user input reaching exec/file/eval

## Scan Scope

**Built-in skills** (read-only, bundled with OpenClaw CLI):
```
$(brew --prefix)/Cellar/openclaw-cli/<version>/libexec/lib/node_modules/openclaw/skills/
```

**Workspace skills** (user-installed):
```
~/.openclaw/workspace/skills/
```

## Workflow

### Full Sweep

Run the comprehensive scan script:
```bash
SKILLS_DIR="$(brew --prefix)/Cellar/openclaw-cli/2026.3.24/libexec/lib/node_modules/openclaw/skills"
WS_DIR="$HOME/.openclaw/workspace/skills"
REPORT_DATE=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$HOME/.openclaw/security-sweep-${REPORT_DATE}.txt"

bash ~/.openclaw/workspace/skills/security-sweep/scripts/full-scan.sh \
  --builtin "$SKILLS_DIR" \
  --workspace "$WS_DIR" \
  --output "$REPORT_FILE"
```

### Quick Scan (fast patterns only)
```bash
bash ~/.openclaw/workspace/skills/security-sweep/scripts/quick-scan.sh \
  --dir "$HOME/.openclaw/workspace/skills"
```

### Single Skill Scan
```bash
bash ~/.openclaw/workspace/skills/security-sweep/scripts/skill-scan.sh \
  --skill /path/to/skill
```

### NPM Audit (workspace skills with package.json)
```bash
bash ~/.openclaw/workspace/skills/security-sweep/scripts/npm-audit.sh \
  --workspace "$HOME/.openclaw/workspace/skills"
```

## Risk Categories

| Level | Finding | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Hardcoded secret (api_key, token, password) | Remove immediately, rotate credential |
| 🔴 CRITICAL | `eval()` on untrusted input | Replace with safe alternative |
| 🟠 HIGH | `exec()`, `spawn()` with string concatenation | Use execFile with array args |
| 🟠 HIGH | Shell injection surface (bash -c, ${var} in shell) | Sanitize or use execFile |
| 🟡 MEDIUM | npm audit findings (any severity) | Review and update dependencies |
| 🟡 MEDIUM | Unexpected network egress | Verify necessity, document purpose |
| 🟢 LOW | File permission too broad (0o777) | Restrict to 0o644/0o755 |
| 🟢 INFO | process.env leak in logs | Ensure logs redact env vars |

## Reporting

Reports are saved to `~/.openclaw/security-sweep-<date>.txt`.
Include report path in memory after each scan.

## Periodic Scanning

Offer to schedule weekly security sweeps via cron:
```bash
openclaw cron add \
  --name "security-sweep" \
  --every 604800 \
  --sessionTarget isolated \
  --payload '{"kind":"agentTurn","message":"Run security sweep on all skills. Report findings. Save report to ~/.openclaw/security-sweep-<date>.txt and note in memory/YYYY-MM-DD.md if any critical issues found."}'
```

## Sharing / ClawHub Publishing

Before publishing a skill to ClawHub:
1. Run full sweep
2. Fix all CRITICAL/HIGH findings
3. Verify no secrets in SKILL.md or any scripts
4. Confirm npm audit passes with 0 vulnerabilities
5. Document all required env vars in SKILL.md

## Notes

- Bundled skills (read-only, no write during scan)
- Workspace skills are editable — fix findings directly
- Some `execFile` usage is legitimate (openclaw CLI calls) — review context
- `process.env` access is fine; concern is env vars *leaking* to untrusted processes
