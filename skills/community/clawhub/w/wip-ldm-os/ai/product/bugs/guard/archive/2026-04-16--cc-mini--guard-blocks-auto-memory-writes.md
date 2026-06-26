# Bug: branch-guard blocks Writes to the Claude Code auto-memory directory

**Date:** 2026-04-16
**Filed by:** cc-mini (with Parker)
**Repo:** `wip-ai-devops-toolbox-private` (guard source), `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` (where the block manifests), `wip-ldm-os-private` (filing location)
**Priority:** medium
**Status:** fix proposed, not yet shipped
**Related:** `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` (guard master plan), `ai/product/bugs/guard/2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md` (same class of over-broad block)

## Context

The Claude Code harness persists auto-memory files at `~/.claude/projects/<project>/memory/` (index at `MEMORY.md`, individual entries at sibling `.md` files). These files are **gitignored** (`.gitignore` line 5 of the `.claude` repo lists `projects/`). They are harness infrastructure, not repo artifacts. The CC system prompt explicitly instructs the agent to write to them directly with the Write tool:

> "You have a persistent, file-based memory system at `/Users/lesa/.claude/projects/<project>/memory/`. This directory already exists ... write to it directly with the Write tool."

## The block

When CC is in `~/.claude/` on main and tries to Write a memory file, the branch-guard blocks with:

```
BLOCKED: Cannot Write while on main branch.
The process: worktree -> branch -> commit -> push -> PR -> merge -> wip-release -> deploy-public.
```

The block is correct in spirit (Writes on main of a tracked repo should go through the worktree + PR flow) but over-broad in practice: the memory path is gitignored and is not part of the git tree. The guard does not know that.

## Why it matters

- Auto-memory is the mechanism the harness uses to preserve learnings across sessions.
- When the guard blocks it, insights from the current session do not persist.
- The obvious workaround (make a worktree to Write a gitignored file) is absurd: the gitignored file will not exist in the worktree, and writing it there does not put it in the auto-memory directory the harness actually reads.
- Without a fix, the agent either loses memory or has to ask the user to explicitly authorize a bypass every time.

## Root cause

In `tools/wip-branch-guard/guard.mjs` the logic at lines 582-608 defines a `SHARED_STATE_PATTERNS` whitelist of paths that are always allowed to be written on main (harness-writable paths: `.claude/plans/`, `.claude/rules/`, `.ldm/logs/`, workspace shared-state files, etc). The auto-memory path `.claude/projects/<project>/memory/` is not in that whitelist. The block at line 611 catches it.

## Proposed fix (surgical)

Add one pattern to `SHARED_STATE_PATTERNS`:

```javascript
/\.claude\/projects\/.*\/memory\//,   // Claude Code auto-memory (gitignored, harness-managed)
```

This follows the same pattern as the existing entries for `.claude/plans/` and `.claude/rules/`. One line. No behavior change elsewhere.

## Why the surgical fix, not a broader one

A more principled fix is: "call `git check-ignore` before blocking, and allow anything gitignored." That is correct in general but has larger surface area. Any gitignored path in any repo would then be writable on main. This could mask legitimate guard catches (e.g. a misconfigured `.gitignore` entry that accidentally allowlists source files). The whitelist approach scopes exactly to the known-harness-writable case. Broader gitignore-aware logic can land as a separate fix if wanted.

## Scope

In scope:
- Add one pattern to `SHARED_STATE_PATTERNS` in `tools/wip-branch-guard/guard.mjs`
- Bump the sub-tool version and package version per the guard master plan's release practice
- Add a test case in `tools/wip-branch-guard/test.sh` asserting that Writes under `.claude/projects/<proj>/memory/` on main are allowed
- Hotfix deploy to `~/.ldm/extensions/wip-branch-guard/` (pre-approved per `#315` lenient list for deployed extensions)

Out of scope (possible follow-ups):
- General `git check-ignore` fallback for Write tool calls
- Auditing other gitignored but harness-writable paths for inclusion

## Verification

After the hotfix is deployed:

```bash
# Write a test memory file while on main of the .claude repo
# From inside CC, Write a file at /Users/lesa/.claude/projects/-Users-lesa-wipcomputerinc/memory/_test.md
# Expected: allowed, no guard block

# Guard version reports new number
node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version

# Test suite passes
cd ~/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard
bash test.sh
```

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)

## Resolution

Status: Closed on 2026-04-24.

The auto-memory write allowlist is now part of deployed guard regression coverage and remains narrow to the known harness-managed memory paths. This was verified during the guard test sweep for `wip-branch-guard 1.9.88`.

Verification:

- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
- Deployed guard smoke: `wip-branch-guard doctor` passes with source and deployed version `1.9.88`.
