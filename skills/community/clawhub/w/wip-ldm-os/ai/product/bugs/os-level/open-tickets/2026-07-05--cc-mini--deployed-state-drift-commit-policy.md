---
title: "Deployed-state drift in tracked homes (~/.claude, ~/.openclaw): no policy for who commits what the tools wrote"
status: open
priority: P2
owner: unassigned
reviewer: OS-Level CC Partner
repo: wip-ldm-os-private (fix spans dot-claude / dot-openclaw / dot-ldm repos + guard + installer)
created: 2026-07-05
---

## What happened

2026-07-05 audit: `~/.claude` sat 3 commits behind origin and could not pull because the live tree carried drift no one owns committing: 7 deleted transient `plans/` files, 6 modified `rules/` + settings files (written by `ldm install` deploying new rule content), and 12 untracked files. The same pattern recurs in every tracked home. Historical precedent exists (commit `77d7f71` "Commit installer-deployed hooks added by ldm install") but it is ad hoc: there is no rule for WHEN machine-written drift gets committed, BY WHOM, and the branch-guard blocks agents from doing it on main, so the drift accumulates until pulls wedge.

This is the third face of one problem, with the other two already ticketed:
- remediation of live state (bugs/guard/2026-07-04 no-blessed-recipe ticket)
- artifact churn in ~/.ldm (dotldm-repo-tracking-strategy sibling ticket)
This ticket owns the POLICY for legitimate tool-written changes to tracked config.

## Fix

1. Classify tracked-home paths into: transient (plans/, session state: gitignore them), deployed (rules/, skills/, hook wiring in settings.json: installer-owned), personal (model, permissions grants: user-owned).
2. Gitignore the transient class in each home repo so it stops blocking pulls.
3. Installer-owned drift gets a sanctioned commit path: `ldm install` finishes by offering (or a `ldm doctor --commit-deployed` performs) a "chore(deploy): record installer-deployed state" commit on main of the home repo, with the diff shown. Guard whitelists exactly that command's flow, mirroring the doctor-owned repair shape from the guard ticket.
4. Personal-class drift stays uncommitted until the user chooses; it must never block pulls (achieved by 1 + 2 leaving only small, mergeable files).
5. Document in system-config-files.md: the three classes and who commits each.

## Acceptance

- `git pull` in ~/.claude works on a machine with normal drift, without stashes or hand-holding.
- After `ldm install`, deployed rule/skill changes are either committed via the sanctioned path or listed as one actionable line, not silent dirt.
- Guard block message for home-repo pulls points at the sanctioned path instead of a dead end.

## Related

- `ai/product/bugs/guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md` (repair shape; this ticket is the recording shape)
- `2026-07-05--cc-mini--dotldm-repo-tracking-strategy.md` (sibling: same contract question for ~/.ldm)
- dot-claude repo commit 77d7f71 (the precedent to formalize)
