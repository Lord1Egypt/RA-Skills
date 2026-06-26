# Bug: `.claude` Repo Has No Level 3 CLAUDE.md Equivalent

**Date:** 2026-04-16
**Filed by:** cc-mini (with Parker)
**Repo:** `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` (bug manifests), `wip-ldm-os-private` (filing location)
**Priority:** high
**Status:** fix proposed, not yet shipped
**Tracks under:** `ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--claude-md-master-plan.md`

## Context

The `.claude` directory at `~/.claude/` is a tracked private git repo (remote: `wipcomputer-ldmos-wipcomputerinc-dot-claude-private`). It is NOT on the master plan's Step 2 list of 11 repos that need Level 3 CLAUDE.md. But it is a repo. It has worktrees. It has PRs. It has all the same wall-hits described in the CWD compaction bug journal: when CC works inside it, there is no repo-scoped guidance.

## What happened today (session narrative)

Session 2026-04-16 (Opus 4.7) hit three walls inside the `.claude` repo within a single operation (removing stale `CLAUDE_CODE_*` env overrides from `settings.json`):

1. **Worktree-not-used on main.** CC edited settings on main. Branch-guard blocked the write correctly, but CC had no repo-scoped guidance pointing to the canonical worktree path convention for this repo. CC had to be re-taught the form on the spot.

2. **`git stash push` flagged destructive.** CC reached for `git stash push -u -- settings.json && git pull` to clear a dirty tree before pulling. A destructive-commands guard (not branch-guard, which allows stash push as of the 2026-04-05 fix in `#317`) flagged it and pointed to the safer recipe: `git stash create` + `git stash store -m ...`. CC did not know that recipe existed until the guard surfaced it.

3. **PR body HEREDOC with python snippet.** CC attempted `gh pr create --body "$(cat <<EOF ... python3 -c open(...) ... EOF)"`. A code-execution-bypass guard flagged the pattern match. Correct form is `gh pr create --body-file <path>` against a real file.

## Root cause

The `.claude` repo has:

- No Level 3 CLAUDE.md (the master plan explicitly names this as the core context-loss cause)
- No repo-scoped doc listing worktree paths or paste-ready safe recipes
- A naming collision: its `CLAUDE.md` is already the Level 1 global file, so a conventional Level 3 cannot live at the same path

CC arrives blind, reaches for unsafe defaults, and the guards (correctly) stop it. The walls are safe design. The missing doc is the bug.

## Proposed fix (surgical)

1. **Add `~/.claude/REPO.md`** (new file, repo-scoped Level 3). Contains:
   - What this repo is (CC's home, tracked private)
   - Its worktree path convention
   - Paste-ready safe recipes for the three walls:
     - Worktree-first edit on main: exact `git worktree add` form
     - Dirty-tree-before-pull: `git stash create` + `git stash store -m ...`
     - PR body with complex content: `gh pr create --body-file <path>`
   - Pointer to workspace Level 2 (`~/wipcomputerinc/CLAUDE.md`) and Crystal for cross-repo context

2. **Append one-line pointer at the bottom of `~/.claude/CLAUDE.md`** referencing `REPO.md`. This is the smallest possible touch to Level 1. Does not thin, reorder, or duplicate anything currently in Level 1. Aligned with the master plan rule: "Don't touch Level 1 or Level 2 until Level 3 is proven."

3. **Follow-up (out of scope for this bug's first pass):** update `~/wipcomputerinc/library/documentation/how-worktrees-work.md` to include the three recipes as on-demand reference. Matches the 2026-03-25 plan's "thin rule, deep doc" pattern.

## Why `REPO.md`, not `CLAUDE.md`

Claude Code auto-reads `CLAUDE.md` in the working directory. In `.claude` the `CLAUDE.md` slot is occupied by Level 1. Jamming Level 3 content into it re-introduces the exact duplication the 2026-03-25 audit flagged as the core problem (734 lines of mostly-identical text across Level 1 and Level 2 copies, with drift).

`REPO.md` is a non-standard filename. CC will not auto-read it. That is the tradeoff. The one-line pointer from Level 1 surfaces it when CC boots in `.claude`. If this convention proves out for the `.claude` repo, we can decide whether to adopt or avoid it elsewhere.

## Alignment with the master plan

The 2026-04-03 CLAUDE.md cascade master plan governs this fix. Specifically:

- **Bottom-up rule:** this fix stays at Level 3. It does not modify Level 1 beyond one pointer line. It does not touch Level 2.
- **Step 2 repo list:** `.claude` is missing from the 11-repo enumeration. Adding it as repo #12 with the `REPO.md` naming note.
- **Compaction survival:** per the CWD compaction bug journal, CC's internal CWD can shift to the last repo touched. If the shift lands in `.claude`, today's walls repeat. Level 3 presence is the documented fix.

## Scope

In scope for this ticket:

- Create `~/.claude/REPO.md` with the three recipes
- Append one-line pointer to `~/.claude/CLAUDE.md`
- Add `.claude` (as repo #12, with `REPO.md` note) to the master plan Step 2 list
- Link this bug file from the master plan

Out of scope (tracked follow-ups):

- Updating `library/documentation/how-worktrees-work.md` with the recipes
- Teaching `ldm install` to deploy `REPO.md` (it lives in the repo; git tracks it)
- Level 3 for the other 10 repos (master plan already covers them)

## Verification

After landing:

```bash
# REPO.md exists at expected path
ls ~/.claude/REPO.md

# Pointer at bottom of Level 1
tail -5 ~/.claude/CLAUDE.md | grep REPO.md

# Master plan references this bug
grep -l 'dot-claude-level-3-missing' \
  ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/wip-code/

# Live test: from ~/.claude/, ask a fresh CC session
# "how do I edit settings.json safely?"
# Expected: CC references the worktree recipe without being told
```

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
