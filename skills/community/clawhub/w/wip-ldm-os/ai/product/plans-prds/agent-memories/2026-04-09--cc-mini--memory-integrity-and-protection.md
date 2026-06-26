# Plan: Agent Memory Integrity and Protection

**Date:** 2026-04-09
**Author:** cc-mini (with Parker)
**Status:** plan
**Related repos:** wip-ldm-os-private (installer), wip-private-mode-private (wipe), wip-file-guard-private (guard), wip-root-key-private (elevation)

## The Problem

Agent memories (daily logs, journals, sessions, transcripts) are the agent's identity and history. They currently exist on disk with no integrity tracking, no protection from deletion, and no audit trail. A prompt injection, a buggy hook, or an agent error could delete or rewrite memories with no record.

At the same time, the branch guard blocks commits on main in `~/.ldm/`, treating it like a code repo. But memory writes happen on every turn (cc-hook writes daily logs). The guard blocks legitimate memory operations.

## The Principle

Memory files are append-only. Git is the audit trail. Private-mode wipe is the only authorized deletion path, gated by root-key (1Password now, Face ID future).

## Memory File Types

```
~/.ldm/agents/{id}/memory/
  daily/YYYY-MM-DD.md       Breadcrumbs after each turn (written by cc-hook)
  journals/*.md              Session narratives (written by agent)
  sessions/*.md              Full session exports
  transcripts/*.md           Raw conversation transcripts
```

Additional memory locations:
- `~/.ldm/memory/crystal.db` ... Memory Crystal database (binary, NOT in git)
- `~/.ldm/memory/context-embeddings.sqlite` ... conversation embeddings (binary, NOT in git)
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md` ... Lesa's daily logs
- `~/.openclaw/workspace/MEMORY.md` ... Lesa's main memory

## What Goes in Git

**In git (tracked for integrity):**
- All agent identity files (SOUL.md, IDENTITY.md, CONTEXT.md, REFERENCE.md)
- All agent config files (config.json)
- All agent memory markdown files (daily/, journals/, sessions/, transcripts/)
- System config (~/.ldm/config.json)
- OS documentation (~/.ldm/library/documentation/)
- Deployed hooks (~/.ldm/hooks/)
- Shared rules, boot, prompts (~/.ldm/shared/ or ~/.ldm/library/)

**NOT in git (binary, sensitive, or reproducible):**
- `memory/*.db`, `memory/*.sqlite` (binary databases, can't diff)
- `secrets/` (SA tokens, API keys)
- `extensions/` (deployed by installer, reproducible)
- `backups/` (large, redundant)
- `tmp/`, `logs/`, `state/` (operational)
- `node_modules/`, `.DS_Store`

## Protection Rules

| Operation | Allowed? | Enforcement |
|---|---|---|
| Create new memory file | Yes | Normal hook/agent operation |
| Append to existing memory | Yes | Edit with additions only |
| Read any memory | Yes | Always |
| Delete a memory file | **Blocked** | Requires root-key elevation |
| Overwrite a memory file | **Blocked** | File guard blocks Write on memory paths |
| Remove lines from a memory | **Blocked** | File guard blocks Edit with net removal > 2 lines |
| `rm` or `git rm` on memory | **Blocked** | Branch guard blocks destructive commands on memory paths |
| Wipe all memories | **Blocked** | Private-mode wipe requires root-key |

## Three Layers of Protection

### Layer 1: File Guard (wip-file-guard)

Already protects memory files from Write (overwrite) and Edit with large removals. Matches patterns: `memory/`, `journal/`, `daily.*log/`.

**Needs:** Add explicit protection for `rm` and `git rm` on memory paths. Currently the file guard only covers Edit and Write tools, not Bash commands that delete files.

### Layer 2: Root-Key Elevation (wip-root-key)

Currently 1Password-backed. Any operation that deletes or significantly modifies memory requires a root-key token. The agent requests elevation, the human approves, the token is one-time use.

**Needs:** Wire root-key into private-mode wipe. Currently wipe runs without any gate. Should call root-key before executing.

**Future:** Replace 1Password with Face ID via the Kaleidoscope iOS app. Push notification to phone, biometric approval, cryptographic token returned. The agent cannot forge a Face ID signature.

### Layer 3: Git Audit Trail

Every memory file change is tracked in git. Diffs show exactly what changed. Commits show when and by whom.

**Needs:**
1. `.gitignore` in `~/.ldm/` that excludes binary DBs, secrets, extensions, but includes all memory markdown
2. Auto-commit hook that commits memory changes periodically (after each session or on a schedule)
3. System repos (`~/.ldm/`, `~/.openclaw/`, `~/.claude/`) need different guard rules than code repos. Main commits are normal here.

## System Repos vs Code Repos

| Type | Branch rule | Commit rule | Examples |
|---|---|---|---|
| Code repo | Worktree -> branch -> PR -> merge | Never commit on main | wip-ldm-os-private, memory-crystal-private |
| System repo | Direct commits on main | Auto-commit by hooks | ~/.ldm/, ~/.openclaw/, ~/.claude/ |

The branch guard needs to distinguish these. System repos are identified by path (under `~/`, not under `~/wipcomputerinc/repos/`). Or by a marker file (`.ldm-system-repo` or similar).

## Private-Mode Integration

`wip-private-mode-private` has three functions:

1. **Toggle memory on/off:** Controls whether hooks capture new memories. Does not touch existing memories. No elevation needed.

2. **Wipe scan:** Finds all memory locations across all storage (crystal.db, workspace, agents/, embeddings). Read-only. No elevation needed.

3. **Wipe execute:** Deletes memories from all locations. **MUST require root-key elevation.** Without root-key token, wipe execute refuses to run.

When wipe executes with root-key approval:
- Git records exactly what was deleted (the diff shows removed files)
- The wipe is auditable forever
- Parker approved it with biometric proof
- No prompt injection can trigger it

## Auto-Commit Hook

A new hook (PostToolUse:Stop or a cron) that:
1. Checks if `~/.ldm/` has uncommitted memory changes
2. Stages only memory files (not config changes, which go through PRs)
3. Commits with message: `memory: auto-commit YYYY-MM-DD HH:MM (cc-mini)`
4. Pushes to origin

This keeps the audit trail continuous. Every session's memory changes are committed and pushed. If the machine dies, the memory is on GitHub.

## Implementation Order

1. **`.gitignore` for `~/.ldm/`** ... exclude binaries, secrets, extensions. Include everything else.
2. **Initial commit** ... commit all existing memory files. This is the baseline.
3. **Guard exception for system repos** ... branch guard allows main commits on `~/.ldm/`, `~/.openclaw/`, `~/.claude/`.
4. **Auto-commit hook** ... commits memory changes after each session.
5. **Root-key gate on private-mode wipe** ... wipe execute requires elevation.
6. **Branch guard: block rm on memory paths** ... no deletion via Bash.
7. **Face ID elevation** (future) ... replace 1Password with Kaleidoscope app.

## Cross-references

- `repos/ldm-os/utilities/wip-private-mode-private/` ... wipe function source
- `repos/ldm-os/utilities/wip-root-key-private/` ... elevation source
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-file-guard/` ... file guard source
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/` ... branch guard source
- `repos/ldm-os/components/memory-crystal-private/` ... crystal database
- `~/.ldm/agents/cc-mini/memory/` ... CC's memory files
- `~/.ldm/agents/oc-lesa-mini/memory/` ... Lesa's memory files
- `ai/product/plans-prds/current/wip-code/_temp-backups/` ... backup of files before destructive changes
