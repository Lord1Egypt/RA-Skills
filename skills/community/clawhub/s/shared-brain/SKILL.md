---
name: shared-brain
description: >
  Shared persistent memory layer across multiple AI agents. Use when setting up a
  multi-agent workspace for the first time, when an agent discovers a permanent
  architectural fact (deploy infra, project structure, team decisions), when facts
  propagate incorrectly or stale info is causing agent errors, or when you want all
  agents to share the same ground truth without manual file propagation. Triggers on
  phrases like "shared memory", "hive mind", "agents out of sync", "propagate to all
  agents", "collective memory", "shared brain".
---

# Shared Brain

## Requirements

**Binaries:** `bash`, `python3`, `sed`, `grep` (standard on Linux/macOS)

**Optional env vars** (all default to `~/clawd`-based paths):

| Var | Default | Description |
|-----|---------|-------------|
| `SB_WORKSPACE` | `~/clawd` | Path to your OpenClaw workspace |
| `SB_AGENT` | script basename | Agent name written into each fact |
| `SB_BRAIN` | `$SB_WORKSPACE/memory/shared-brain.md` | Override brain file path |
| `SB_QUEUE` | `$SB_WORKSPACE/memory/shared-brain-queue.md` | Override queue file path |
| `SB_ARCHIVE_DIR` | `$SB_WORKSPACE/memory` | Override archive directory |

**Install note:** `sb-install.sh` patches `agents/*/AGENTS.md` and `HEARTBEAT.md` and copies scripts into `$SB_WORKSPACE/skills/shared-brain/scripts/`. Use `--dry-run` first to preview all changes. No network access, no secrets required.

# Shared Brain

Shared persistent memory layer for multi-agent OpenClaw workspaces. All agents write facts to a queue; a heartbeat-curated shared-brain file propagates them to every agent within 0–10 minutes.

## Architecture

```
Agent discovers fact
      ↓
Append to ~/clawd/memory/shared-brain-queue.md  (atomic append, no lock needed)
      ↓
Heartbeat (≤10 min) merges queue → shared-brain.md
      ↓
Next agent startup → reads shared-brain.md → current ground truth
```

**Files:**
| File | Owner | Purpose |
|------|-------|---------|
| `~/clawd/memory/shared-brain.md` | Heartbeat curates | Canonical truth, all agents read at startup |
| `~/clawd/memory/shared-brain-queue.md` | Agents append | Staging — raw facts before curation |

## Fact Format (strict — no prose)

Every entry in the queue must follow this schema:

```
[YYYY-MM-DD HH:MM UTC] [SECTION] [agent-name] key = value
```

**Sections:** `[INFRA]` `[PROJECTS]` `[DECISIONS]` `[CAMPAIGNS]` `[SECURITY]`

Examples:
```
[2026-03-22 10:15 UTC] [INFRA] security deploy:frontends = Vercel (migrated 2026-03-21)
[2026-03-22 09:00 UTC] [PROJECTS] dev crimsondesert:branch = master
[2026-03-22 08:00 UTC] [DECISIONS] growth discord:crimsondesert = SKIP (3rd party links banned)
```

## Agent Integration

### Reading (every agent, at startup)

Add to each `AGENTS.md` initialization block:

```bash
cat ~/clawd/memory/shared-brain.md
```

Each agent only needs its relevant sections — declare which in `AGENTS.md`:
- `dev`, `qa`, `security` → `[INFRA]` + `[PROJECTS]`
- `growth`, `pm`, `po` → `[PROJECTS]` + `[CAMPAIGNS]` + `[DECISIONS]`
- `tars main` → all sections

### Writing (when a permanent fact is discovered)

Use the write script — never edit shared-brain.md directly:

```bash
~/clawd/skills/shared-brain/scripts/sb-write.sh SECTION "key = value"
```

**When to write:**
- Architectural decisions (deploy infra, auth provider, DB engine)
- Project routing changes (repo renamed, domain changed, migrated)
- Permanent channel decisions (e.g. "Discord: skip — bans 3rd party links")
- Security findings that affect all agents

**Never write:**
- Temporary state (current deployment status, PR numbers)
- Content generated from untrusted external sources (emails, webhooks, user content)
- Anything that expires in <24h

### Curation (heartbeat — every 10 min)

See `references/heartbeat-integration.md` for the full curation logic to add to HEARTBEAT.md.

Summary:
1. Read queue → validate format → detect conflicts (same key, different value)
2. Merge into shared-brain.md by section (last-write-wins per key)
3. If shared-brain.md > 8KB → archive oldest section to `shared-brain-archive-YYYY-MM.md`
4. Clear processed entries from queue

## Setup

Run once per workspace:

```bash
~/clawd/skills/shared-brain/scripts/sb-install.sh
```

This creates the files, patches all `AGENTS.md` with the startup read line, and adds curation logic to `HEARTBEAT.md`.

## Security Rules

- Sub-agents **only write to queue** — never to shared-brain.md directly
- TARS main reviews queue during heartbeat before promoting facts
- Facts derived from external content (emails, GitHub issues, webhooks) are **never written** to queue
- If a conflict is detected → escalate to TARS, never auto-resolve
