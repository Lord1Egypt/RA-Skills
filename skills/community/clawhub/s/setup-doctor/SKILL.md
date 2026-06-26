---
name: setup-doctor
description: "Diagnose OpenClaw setup in one command. Auto-detects issues with Node, npm, gateway, config, and workspace. Quick mode (~10s) or Full mode. Multi-language. Config and workspace checks report file existence only — never reads contents. No credentials accessed without approval. Homepage: https://clawhub.ai/skills/setup-doctor"
---

# Setup Doctor v3.0

**Install:** `clawhub install setup-doctor`

Diagnose OpenClaw setup issues. Like `brew doctor` — one command, clear results.

## Language

Detect from user's message language. Default: English.

## Auto-Detection

Run automatically when:
- User mentions setup issues, errors, or "doesn't work"
- Gateway fails to start or connect
- A command returns an unexpected error
- User says "doctor check", "diagnose", "hvorfor fungerer ikke"

## Quick Check (default, ~10s)

```bash
node --version
npm --version
openclaw gateway status 2>&1
```

**Report:**
```
Setup Doctor — Quick Check
  Node.js:    ✅ v24.11.1
  npm:        ✅ 10.9.2
  Gateway:    ✅ Running (up 4h)

Issues: none
```

If issues found, include one-line fix:
```
  Gateway:    ❌ Not running → Fix: openclaw gateway start
```

## Full Check (opt-in)

Trigger: "doctor full", "full diagnose"

Includes Quick Check PLUS:

- **Config**: File exists
- **Workspace**: Directory exists, key files present (SOUL.md, AGENTS.md, etc.)
- **Platform**: Windows (long paths, PowerShell policy), macOS (Homebrew PATH), Linux (systemd)
- **Common pitfalls**: Known version conflicts, deprecated patterns

## Fix Mode

Trigger: "fix it", "fix det"

1. Show exactly what will change
2. Get user confirmation
3. Apply fix
4. Re-run check to verify

**Never fix without confirmation.**

## Workspace Audit

Trigger: "workspace audit"

Report file existence and size only — never read contents:

```
Workspace Audit:
  SOUL.md      ✅ 1.2 KB
  AGENTS.md    ✅ 2.8 KB
  MEMORY.md    ✅ 3.1 KB
  HEARTBEAT.md ✅ 0.4 KB
  TOOLS.md     ✅ 0.3 KB
```

## Quick Commands

| User says | Action |
|-----------|--------|
| "doctor check" / "kjor doctor" | Quick Check |
| "doctor full" | Full Check |
| "fix it" | Auto-fix with confirmation |
| "workspace audit" | File existence check |

## HEARTBEAT Integration

User can add to HEARTBEAT.md:

```markdown
## Setup Check
- If gateway errors detected: run doctor quick check
```

## Guidelines for Agent

1. **Auto-detect issues** — run quick check when user reports problems
2. **Keep it fast** — quick check in ~10 seconds
3. **One-line fixes** — clear, copy-pasteable solutions
4. **Never read file contents** — existence and size only
5. **Never fix without asking** — show what changes, get confirmation
6. **Match user language** in reports

## What This Skill Does NOT Do

- Does NOT read file contents (existence/size only)
- Does NOT access credentials without explicit approval
- Does NOT modify config automatically
- Does NOT modify HEARTBEAT.md or MEMORY.md

## More by TommoT2

- **context-brief** — Persistent context survival across sessions
- **tommo-skill-guard** — Security scanner for installed skills
- **locale-dates** — Format dates/times per locale

Install the full suite:
```bash
clawhub install setup-doctor context-brief tommo-skill-guard locale-dates
```
