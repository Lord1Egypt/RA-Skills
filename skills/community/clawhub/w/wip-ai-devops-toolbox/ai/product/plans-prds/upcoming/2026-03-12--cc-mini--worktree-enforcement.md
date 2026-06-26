# Plan: Enforce Git Worktrees as Default for All Agent Sessions

**Date:** 2026-03-12
**Author:** cc-mini
**Issue:** wipcomputer/wip-ai-devops-toolbox#86
**Priority:** 1 (foundational safety ... blocks an entire class of multi-agent bugs)

## Context

Agents working in the same repo corrupt each other's state. Three incidents in 48 hours: mixed commits from parallel subagents, Lesa writing to CC's branch before pulling, a private directory created in the wrong clone. All caused by agents sharing a working tree.

Current mitigations (branch prefixes, "don't touch each other's folders", "never push to main") depend on memory. Memory dies on compaction. Worktrees make the safe behavior structural.

**Principle:** Repos-per-agent is identity. Worktrees are the fail-safe.

## Architecture

```
~/.ldm/agents/cc-mini/repos/memory-crystal-private/     <- main working tree (read-only in practice)
  .claude/worktrees/
    fix-search/                                          <- worktree 1 (own branch, own files)
    fix-install/                                         <- worktree 2 (isolated)
    release-notes/                                       <- worktree 3 (isolated)
```

No session ever works in the main working tree. Every session starts in a worktree. Main is the clean reference copy. Worktrees are disposable workspaces.

## Rollout Plan

### Phase 1: Subagent isolation (immediate, no tooling changes)

**What:** Use `isolation: "worktree"` on every Agent tool call that writes code.

**Where:** Every CC session, starting now. No repo changes needed. This is a behavior change in how CC launches subagents.

**Effect:** Fixes the parallel agent problem (tonight's #71/#74/#75 incident). Each subagent gets its own worktree, its own branch, its own files. No mixed commits.

**Risk:** Low. Worktree branches need to be merged manually. Subagents can't see each other's changes (which is the point).

**Validation:** Launch 3 parallel subagents editing the same file. Verify each produces a clean, independent branch.

### Phase 2: .gitignore + Dev Guide (1 hour, one PR)

**What:** Add `.claude/worktrees/` to `.gitignore` on every repo. Update the Dev Guide.

**Repos affected:** All repos under `ldm-os/` (30+ repos).

**Implementation:**

1. Script to add `.claude/worktrees/` to every repo's `.gitignore`:

```bash
for repo in ~/Documents/.../repos/ldm-os/*/*/; do
  if [ -d "$repo/.git" ]; then
    grep -q 'claude/worktrees' "$repo/.gitignore" 2>/dev/null || \
      echo '.claude/worktrees/' >> "$repo/.gitignore"
  fi
done
```

2. Dev Guide updates:
   - New section: "Worktree Workflow"
   - Every session starts in a worktree
   - "Never push to main" is now structurally enforced
   - Commit and push before session ends (worktree cleanup deletes uncommitted work)
   - Branch naming in worktrees follows prefix convention (cc-mini/, lesa-mini/)

3. PR per repo, or batch via a script that commits + pushes + PRs.

**Risk:** Low. `.gitignore` additions are non-breaking.

### Phase 3: wip-install worktree setup (2-3 hours, one PR on devops toolbox)

**What:** When `wip-install` deploys a repo, it automatically:
1. Adds `.claude/worktrees/` to `.gitignore` (if not present)
2. Verifies git worktree support (git 2.15+, always true on modern macOS)
3. Logs a note in the install output about worktree isolation

**Where:** `tools/wip-universal-installer/install.js`

**Risk:** Low. Additive only.

### Phase 4: Boot hook enforcement (2-3 hours, PR on wip-ldm-os-private)

**What:** The SessionStart boot hook detects if the session is running in the main working tree (not a worktree) and warns:

```
! You are working directly in the main working tree.
  Consider using: claude --worktree <name>
  Or say "work in a worktree" to isolate your changes.
```

For now this is a warning, not a block. Some operations (releases, deploys) legitimately run from the main tree.

**Where:** `src/boot/boot-hook.mjs` in wip-ldm-os-private

**Detection:** `git rev-parse --is-inside-work-tree` returns true for both, but `git rev-parse --show-toplevel` vs `git worktree list` can distinguish the main tree from a worktree.

**Risk:** Low. Warning only.

### Phase 5: wip-release worktree guard (1 hour, one PR on devops toolbox)

**What:** wip-release detects if it's running inside a worktree and blocks:

```
✗ wip-release must run from the main working tree, not a worktree.
  Current: .claude/worktrees/fix-search/
  Run from: /path/to/repo/
```

Releases should happen on main after PRs are merged. Running wip-release from a worktree would create a tag on the wrong branch.

**Where:** `tools/wip-release/core.mjs`, new gate at the top of `release()`.

**Risk:** Low. Blocking gate with clear error message.

### Phase 6: Lesa integration (after phases 1-5)

**What:** Lesa keeps her own repo clones. That's identity. But when she spawns parallel work (skills, sub-tasks, `claude-code` skill invocations), those should use worktrees.

**Decision (from Parker, 2026-03-12):** Every agent keeps their own repos. Worktrees are for parallel work within an agent, not for sharing repos between agents.

**Implementation:**
1. Add `.claude/worktrees/` to `.gitignore` on Lesa's repos (same as Phase 2)
2. If OpenClaw supports spawning Claude Code via the `claude-code` skill, those invocations should use `--worktree`
3. If OpenClaw adds native sub-agent support, those should use worktree isolation

**Risk:** Low. Same pattern as CC, just in Lesa's workspace.

## What NOT to change

- **Repos-per-agent stays.** Each agent has their own clone list, their own folder structure. That's identity. Worktrees are for parallel work within an agent, not for sharing repos between agents.
- **Branch prefixes stay.** `cc-mini/`, `lesa-mini/`, `cc-air/`. Worktree branches still use these prefixes.
- **Workspace separation stays.** Lesa's `~/.openclaw/workspace/` and CC's `~/.ldm/agents/cc-mini/` are identity, not git. Worktrees don't touch this.

## Rollout timeline

| Phase | Effort | Dependency | When |
|-------|--------|------------|------|
| 1. Subagent isolation | 0 (behavior change) | None | Now |
| 2. .gitignore + Dev Guide | 1 hour | None | Next session |
| 3. wip-install setup | 2-3 hours | Phase 2 | Next session |
| 4. Boot hook warning | 2-3 hours | Phase 2 | After boot hook PR merges |
| 5. wip-release guard | 1 hour | Phase 2 | Next session |
| 6. Lesa integration | TBD | Discussion | After phases 1-5 |

Phases 1-3 can ship in one session. Phase 4 depends on the boot hook work happening in wip-ldm-os-private. Phase 5 is a quick add to the devops toolbox. Phase 6 needs Parker's input.

## Success criteria

1. No more mixed commits from parallel subagents
2. No more "agent wrote to wrong branch" incidents
3. `wip-release` refuses to run from a worktree
4. Boot hook warns when session is in main working tree
5. Every repo has `.claude/worktrees/` in `.gitignore`
