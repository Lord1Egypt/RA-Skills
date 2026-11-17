---
title: "Git hygiene backlog: hundreds of stale merged worktrees and ~50 orphan stashes across the repos"
status: open
priority: P2
owner: unassigned
reviewer: OS-Level CC Partner
repo: multiple (wip-ldm-os-private, wip-ai-devops-toolbox-private, memory-crystal-private, others)
created: 2026-07-05
---

## What happened

The 2026-07-05 repo audit found the workflow's exhaust has never been swept:

- wip-ldm-os-private: 200+ worktrees under `.worktrees/` (an 80KB `git worktree list`), most on long-merged `cc-mini/*` branches dating back months.
- wip-ai-devops-toolbox-private: 50+ `cc-mini--*` worktrees of the same vintage, plus codex/cody active ones.
- Stashes: 32 in wip-ldm-os-private, 21 in the toolbox, assorted elsewhere. Mix of release-tool auto-checkpoints ("preserve ... before pull"), codex scratch, and forgotten session preserves.

Every worktree is a full checkout on disk; hundreds of them cost gigabytes and make `git worktree list` (which guards and tooling shell out to) slower. Stale stashes are unlabeled risk: nobody knows which ones still guard unlanded work.

The 2026-07-05 sprint's own worktrees were removed same-day with the merged-branch safety check (`git branch -d` refuses unmerged), which is the model for the sweep.

## Fix

1. One-time sweep, per repo: for each `.worktrees/` entry, if its branch is fully merged into main (`git branch -d` succeeds or `git merge-base --is-ancestor`), `git worktree remove` + delete the local branch. Anything unmerged or dirty is left and listed in the sweep report for its owner. Never `-D`, never force.
2. Stash triage: list every stash with age and message; drop only release-tool auto-checkpoints older than 30 days whose commit is an ancestor of main; everything else goes in the report for human review.
3. Going forward, make it structural: worktree removal after merge joins the post-merge routine (deployer/coder checklist and/or `wip-release` gains a `--sweep-merged-worktrees` step; the existing stale-merged-branches quality gate already points this direction).
4. The sweep is a script in the devops toolbox (so it is reviewable and rerunnable), not a one-off shell session.

## Acceptance

- Sweep script exists in wip-ai-devops-toolbox-private, dry-run by default, report-first.
- After the first real run: every remaining worktree is either active (unmerged/dirty) or listed with an owner; disk usage delta reported.
- Post-merge routine documentation updated so the backlog does not regrow.

## Related

- `ai/product/bugs/installer/ldmos-bugs-operating-procedure--installer-coder.md` (the post-merge routine this extends)
- 2026-07-05 sprint cleanup (this ticket's proof of concept, 12 worktrees removed with the merged-check pattern)
