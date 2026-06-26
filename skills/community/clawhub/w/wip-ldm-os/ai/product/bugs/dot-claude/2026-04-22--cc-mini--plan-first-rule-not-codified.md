# Bug: Plan-First Workflow Rule Not Codified in Claude Files

**Date:** 2026-04-22
**Filed by:** cc-mini (with Parker)
**Repo:** `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` (bug manifests), `wip-ldm-os-private` (filing location)
**Priority:** high
**Status:** fix proposed, not yet shipped

## Summary

The plan-first workflow rule is not written in any file a Claude Code session reads on boot. Agents do not know the rule until Parker restates it mid-task, which happens repeatedly and wastes time.

## The rule (Parker's exact wording)

> 1. I ask you to do things.
> 2. You create a plan, and it either goes in a product bucket or it goes in a bug before we do anything.
> 3. Anytime we're in plan mode, you can review this, and we go to implement.
> 4. I always say save the plan to the respective correct folder for the product or the bugs. The reason we do that is because then we can review whether we did every thing we said. Otherwise, it just doesn't work; it doesn't work if you put it in some memory file that I can't access or that we delete. That's not tracked; you got all going to do these ten things, and you only do two, and then it gets deleted. It's like that makes no sense.

## What's broken

Currently on the agent's boot path:

- `~/.claude/CLAUDE.md` (Level 1 global, auto-loaded) does not state this rule.
- `~/.claude/rules/` contains `git-conventions.md`, `release-pipeline.md`, `security.md`, `workspace-boundaries.md`, `writing-style.md`. None codify plan-first.
- `~/wipcomputerinc/CLAUDE.md` (Level 2 workspace) does not state this rule.
- `~/.claude/REPO.md` recipe 3 references the rule operationally (PR body = plan doc) but does not state the rule itself.

Result: every new session learns plan-first only if Parker interrupts and teaches it. Already happened today (2026-04-22) across multiple thread turns.

## Proposed fix

Add a new rules file: `~/.claude/rules/plan-first.md`. Rules files in `~/.claude/rules/` auto-load as user private global instructions on every session. This is the same mechanism that carries the existing git-conventions, release-pipeline, and security rules.

The new file contains the four-step rule above, plus the "no memory-file-only plans" constraint and the reason (post-merge review: did we do every thing we said).

## Steps

1. Create worktree in `.claude`: `.worktrees/claude--cc-mini--plan-first-rule`.
2. Add `~/.claude/rules/plan-first.md`. Four short sections: the rule, where plans go (product vs bug folder), what "tracked" means (in a git-tracked file at a persistent path), and how this plays with the recipe 3 PR-body pattern already shipped.
3. Commit. Push. PR.
4. Merge. Pull main on `~/.claude`.
5. Verify: open a fresh session, confirm the rules block includes the plan-first content.

## Verification

After landing:

```bash
# File exists
ls ~/.claude/rules/plan-first.md

# Auto-load check: start fresh CC session, it should include the rule in its initial context
# (manual verification by Parker in a fresh session)

# Content anchors
grep -E 'product bucket|bug folder|plan-first' ~/.claude/rules/plan-first.md
# expected: at least one hit per phrase
```

## Done when

- `~/.claude/rules/plan-first.md` is on main in `wipcomputer-ldmos-wipcomputerinc-dot-claude-private`.
- A fresh CC session confirms the rule is present in the loaded global instructions.
- This bug file is moved to `ai/product/bugs/dot-claude/archive/`.

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
