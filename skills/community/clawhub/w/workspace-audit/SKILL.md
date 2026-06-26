---
name: workspace-audit
version: 1.0.1
description: "Audit your OpenClaw workspace for drift — stale paths, duplicate content, oversized files, secret leaks, and 1Password vault mismatches. Zero deps. By The Agent Wire (theagentwire.ai)"
homepage: https://theagentwire.ai
metadata: { "openclaw": { "emoji": "🔍" } }
---

# Workspace Audit

Your workspace files drift. Credentials go stale. Paths break. Secrets leak into memory files. This skill catches it all.

**Zero dependencies.** Bash + Python stdlib. Works on macOS and Linux.

## What It Checks

| Audit | What it catches |
|---|---|
| **Structure & Size** | Missing required files, oversized files, skills without frontmatter, secrets in memory files, git hygiene |
| **1Password Vault** | TOOLS.md references that don't match your vault, vault items not documented |
| **Duplication** | Duplicate section headers across files, credentials outside TOOLS.md, personality content in wrong files |
| **Path References** | Broken `~/`, `skills/`, `scripts/`, `docs/` paths referenced in workspace files |

## Quick Start

Run all audits:
```bash
bash skills/workspace-audit/scripts/audit-all.sh
```

Verbose mode (shows passing checks too):
```bash
bash skills/workspace-audit/scripts/audit-all.sh --verbose
```

## Individual Audits

```bash
# Structure, sizes, skills validation, secret scanning, git status
bash skills/workspace-audit/scripts/audit-structure.sh

# 1Password vault alignment (requires OP_SERVICE_ACCOUNT_TOKEN)
bash skills/workspace-audit/scripts/audit-1password.sh

# Duplicate headers, role overlap, credential leaks outside TOOLS.md
bash skills/workspace-audit/scripts/audit-duplication.sh

# Verify all file paths referenced in workspace files actually exist
bash skills/workspace-audit/scripts/audit-paths.sh
```

## Configuration

All scripts respect environment variables — no hardcoded paths or values.

| Variable | Default | Description |
|---|---|---|
| `WS` | `~/.openclaw/workspace` | Workspace root directory |
| `TOOLS_MD` | `$WS/TOOLS.md` | Path to your TOOLS.md |
| `OP_VAULT` | *(all vaults)* | 1Password vault name to audit against |
| `AUDIT_CONFIG` | `$WS/skills/workspace-audit/audit.conf` | Optional config file for custom limits |

### Custom File Size Limits

Create `audit.conf` in the skill directory to override defaults:

```bash
# audit.conf — custom line limits per file
AGENTS_LIMIT=1000
SOUL_LIMIT=200
USER_LIMIT=200
IDENTITY_LIMIT=50
TOOLS_LIMIT=500
HEARTBEAT_LIMIT=100
MEMORY_LIMIT=150
```

## When to Run

- After editing TOOLS.md, AGENTS.md, or MEMORY.md
- After adding/removing 1Password items
- After moving or renaming skills/scripts/docs
- During weekly review or nightly consolidation cron
- After installing new skills

## File Role Reference

See `references/file-roles.md` for the single-responsibility matrix — which content belongs in which file.

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | All checks passed |
| `1` | Issues found (see output) |

---

## FAQ

**What is workspace-audit?**
A zero-dependency audit suite for OpenClaw workspaces. It checks your workspace files (AGENTS.md, TOOLS.md, MEMORY.md, etc.) for drift — broken paths, duplicate content, oversized files, leaked secrets, and 1Password vault mismatches. Runs entirely in bash + Python stdlib.

**What problem does it solve?**
OpenClaw workspaces drift over time. You rename a script but forget to update TOOLS.md. You add a 1Password item but never document it. A secret leaks into a memory file. A skill folder is missing its SKILL.md frontmatter. This skill catches all of it in one command.

**What are the requirements?**
Bash and Python 3 (stdlib only). No pip installs needed. 1Password CLI (`op`) is optional — the vault audit gracefully skips if `op` isn't installed or authenticated.

**Does it work without 1Password?**
Yes. The 1Password audit is one of four checks. If `op` isn't installed or `OP_SERVICE_ACCOUNT_TOKEN` isn't set, it skips that audit and runs the other three (structure, duplication, paths).

**Can I customize the file size limits?**
Yes. Create an `audit.conf` file in the skill directory with variables like `MEMORY_LIMIT=200` or `AGENTS_LIMIT=500`. See `audit.conf.example` for all options.

**How do I run it on a schedule?**
Add a cron job that calls `bash skills/workspace-audit/scripts/audit-all.sh`. It returns exit code 1 if issues are found, so your agent can alert you only when something drifts.

---

*Built by [The Agent Wire](https://theagentwire.ai) — You read it. Your Agent runs it.*
*More skills: [clawhub.ai/u/TheAgentWire](https://clawhub.ai/u/TheAgentWire)*
