---
name: workspace-hygiene
version: 0.1.0
description: >
  Audit and maintain workspace file structure, memory quality, and project documentation.
  Use when: cleaning up the workspace, running a file audit, checking memory health,
  ensuring project READMEs exist, or during weekly Monday heartbeat.
  Triggers: "clean up workspace", "run hygiene", "audit files", "workspace health",
  "check file structure", or scheduled Monday heartbeat.
metadata:
  openclaw:
    emoji: "🧹"
    requires:
      bins: ["python3"]
    os: ["linux", "darwin"]
---

# Workspace Hygiene

Maintains clean, RAG-friendly workspaces across all agents. Runs on demand or weekly.

## Quick Start

```bash
python3 skills/workspace-hygiene/scripts/hygiene.py --workspace ~/.openclaw/workspace
```

Or for a specific agent:
```bash
python3 skills/workspace-hygiene/scripts/hygiene.py --workspace ~/.openclaw/workspace-claire
```

## What It Does

### 1. Structure Audit
Reads `STRUCTURE.md` from the workspace root. Scans for:
- Files at root that aren't agent config (AGENTS.md, SOUL.md, etc.)
- Folders that don't match the canonical layout
- Files in wrong locations (e.g. Claire scripts in Maggie's workspace)

### 2. Memory Health
Scans `memory/` for:
- Files using timestamp format (YYYY-MM-DD-HHMM.md) instead of date or topic
- Daily logs older than 30 days that haven't been distilled into MEMORY.md
- Gaps in daily logging (missing dates during active periods)
- MEMORY.md line count — flag if over 150

### 3. Project README Audit
Checks every folder in `projects/` for a `README.md`. Missing READMEs degrade RAG retrieval — `memory_search` can't find project context without them.

### 4. Memory Format Check
Validates that recent memory entries (last 7 days) use the tagged format:

```markdown
[DECISION] What was decided and why
[FACT] A durable fact worth retaining
[PROJECT] Project name — status update
[RULE] A rule or preference established
[EVENT] Something that happened
```

Untagged entries are flagged for manual review, not auto-tagged.

### 5. Health Report
Writes a report to `projects/system/hygiene-YYYY-MM-DD.md` with:
- Structure violations (with suggested fixes)
- Memory health score
- Missing project READMEs
- Untagged memory entries
- Recommended actions (prioritized)

## Auto-Fix vs Flag

| Issue | Action |
|-------|--------|
| Timestamp-format memory files | Auto-consolidate into date file |
| Missing project README | Flag — agent should write it with project context |
| Files in wrong location | Flag with suggested move command |
| MEMORY.md over 150 lines | Flag for manual trimming |
| Root-level junk files | Flag with suggested archive command |
| Untagged memory entries | Flag — don't auto-tag (context needed) |

## Deployment

Install to each agent workspace's `skills/` folder, or install to `~/.openclaw/skills/` for global access.

Add to `HEARTBEAT.md`:
```markdown
## Weekly Hygiene (Monday)
- Run `python3 skills/workspace-hygiene/scripts/hygiene.py --workspace <path>`
- Review the report at projects/system/hygiene-YYYY-MM-DD.md
- Fix flagged issues or escalate to Steve
```

## Reference Docs

| File | Purpose |
|------|---------|
| `memory-format.md` | Canonical memory entry format and tagging rules |
| `rag-index.md` | How to write project READMEs for optimal RAG retrieval |
| `audit.md` | Detailed audit rules and canonical structure |
