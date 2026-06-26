---
name: workspace-org
description: "Standardized workspace directory layout for multi-agent OpenClaw deployments. All agent-generated files go under files/ to keep root clean. Defines where agents store files, exchange deliverables, and cleanup policies. Trigger on workspace setup, file placement decisions, workspace cleanup, multi-agent convention setup, workspace compliance check."
---

# Workspace Org

Standardized directory conventions for OpenClaw multi-agent workspaces.

## Layout

```
workspace/                          ← or any agent workspace dir
├── AGENTS.md, SOUL.md ...         ← core config (never moved)
├── skills/                        ← ClawHub skills
├── memory/                        ← long-term memory
├── files/                         ← all agent-generated content
│   ├── tmp/       disposable temp files
│   ├── notes/     working docs worth keeping
│   ├── inbox/     deliverables from other agents
│   ├── outbox/    files for owner/other agents
│   ├── archive/   inactive projects
│   └── experts/   (workspace root only) expert engagements
```

## Rules

- **Core config** files stay at workspace root. Never moved.
- **All generated files** go into `files/{subdir}/`. No exceptions.
- **Cross-agent handoff**: sender writes to `files/outbox/`, receiver picks from `files/inbox/`.

### Cleanup policy
| Subdir | Cleanup rule |
|--------|-------------|
| `files/tmp/` | Eligible for auto-cleanup at any time |
| `files/notes/` | Keep; never auto-clean |
| `files/archive/` | Manual review before removal |
| `files/experts/` | Remove after expert engagement ends |
| `files/inbox/` | Clear after processing deliverable |

## Enforcement for future work

### When creating files
All generated files go into `files/` subdirectories:
- **Temp/one-off** scripts, patches, downloads → `files/tmp/`
- **Keep-worthy** docs, analysis, snapshots → `files/notes/`
- **Cross-agent handoff** → `files/inbox/` or `files/outbox/`
- **Old projects** → `files/archive/`

### Periodic compliance check
```bash
# Check if current workspace has layout violations
python3 {{SKILL_DIR}}/scripts/sweep.py

# JSON output for automation
python3 {{SKILL_DIR}}/scripts/sweep.py --json
```

### Fix existing violations
```bash
python3 {{SKILL_DIR}}/scripts/apply.py --execute
```

HEARTBEAT.md can include a periodic sweep to catch drift.

## Scripts

### `scripts/apply.py`
Creates `files/` and sub-directories, migrates existing files into correct locations.
Auto-detects workspace root vs agent workspace. Dry-run by default.
Agent directories (containing AGENTS.md) are never moved.

### `scripts/sweep.py`
Audits workspace for layout violations. Returns exit code 0 (clean), 1 (warnings), or 2 (violations).

## References
- [layout.md](references/layout.md) — Full specification with agent-type variations
