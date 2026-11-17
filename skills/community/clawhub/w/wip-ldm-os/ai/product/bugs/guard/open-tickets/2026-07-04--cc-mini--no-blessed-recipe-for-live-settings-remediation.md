---
title: "Guard: no blessed recipe for live-state remediation of ~/.claude/settings.json"
status: open
priority: P2
owner: unassigned
reviewer: Guard CC Partner
repo: wip-ldm-os-private
created: 2026-07-04
---

## What happened

Twice on 2026-07-04, an agent needed to repair machine-mutated state in `~/.claude/settings.json` and had no sanctioned path to do it:

1. **Morning:** 10 duplicate SessionStart boot-hook entries (see `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md`). The session deduped the live file manually with a `.bak-2026-07-04` backup.
2. **Afternoon (CORRECTED 2026-07-04 after CC review of PR #1086):** an agent misread the saved model value `"model": "opus[1m]"` as paste corruption and attempted a live repair. The bracketed suffix is in fact the legitimate 1M-context model-ID form (`claude-fable-5[1m]`, `claude-opus-4-8[1m]`); real paste corruption carries an ESC control character (0x1B), which this value did not. The branch-guard blocked the Edit on the main working tree... and in doing so protected a valid setting from a wrong "fix." The case still illustrates both sides of this ticket: agents need a sanctioned live-remediation path for the cases that ARE real (case 1 above), and any such path must be doctor-grade validated, not hand-judged, precisely because hand judgment got this one wrong. (`claude config set` also no longer exists in current Claude Code; it spawns a prompt instead.)

## Why the worktree recipe does not cover this

`~/.claude/settings.json` is a hybrid file. It is git-tracked in the dot-claude repo, but it is also **live state mutated directly by tools**: the Claude Code TUI (`/model`, permission grants), `ldm install` (hook registration), and plugins all write to it outside any branch. At any moment the live file carries uncommitted drift that exists nowhere else.

The blessed recipe (worktree from `origin/main`, edit, PR, merge, pull) cannot reach that drift:

- A worktree checkout of `origin/main` does not contain the corrupted or duplicated lines, so there is nothing to fix on the branch.
- After a merge, `git pull` on the main working tree meets the uncommitted drift and either conflicts or stalls behind the dirty-tree wall.

So for this file class, the guard's redirect points at a recipe that structurally cannot perform the repair. The result in practice is either delegation to Parker's keyboard (violates agent-completes-the-work) or ad-hoc manual edits with `.bak` files (works, but is exactly the unaudited path guards exist to prevent).

## Proposed fix

Add a blessed live-state remediation recipe to the guard (and to `~/.claude/REPO.md` as wall-hit recipe #4). Shape:

1. **Scope:** applies only to designated machine-state files (`settings.json`, and any other tool-mutated tracked file the guard lists). Not a general main-branch edit allowance.
2. **Checkpoint first:** `sha=$(git stash create)` + `git stash store` (the repo's existing non-destructive checkpoint form) or a timestamped `.bak-YYYY-MM-DD` copy, so the pre-repair state is always recoverable.
3. **Repair on the live file** with Edit, allowed by the guard when steps 1-2 are satisfied (e.g. a marker file or a guard-provided wrapper command).
4. **Commit the repaired state on a branch afterward** so the repo history records what was fixed and why, keeping the audit trail the guard exists to protect.

Alternative acceptable shape: a `ldm doctor --fix`-style command owns all settings.json repairs (duplicate hooks, invalid model value, orphaned entries) and the guard whitelists that command. That folds this into the doctor work already scoped in the hook-duplication ticket.

**Partial fix landed 2026-07-04 on this same branch** (PR #1086): `ldm doctor --fix` now owns the duplicate-hook collapse and invalid-model removal with timestamped backups (the alternative shape above). Per CC review, the invalid-model check keys on control characters (ESC 0x1B etc.) and impossible lengths only; printable bracketed IDs like `claude-fable-5[1m]` are legitimate 1M-context variants and pass. Still open: guard-side whitelist of the doctor command for this file class, and the `~/.claude/REPO.md` recipe documentation. Doctor's duplicate collapse keeps the first entry as-is and does not re-canonicalize a stale survivor; `configureSessionStartHook()` owns canonicalizing the boot entry on install.

## Acceptance

- An agent hitting corrupted machine state in `~/.claude/settings.json` can repair it end-to-end without bypassing a guard, hand-editing on main without a recipe, or delegating to Parker's keyboard.
- The recipe is documented in `~/.claude/REPO.md` (deployed via its repo flow) and referenced in the guard block message for this file class.
- Pre-repair state is always recoverable (stash checkpoint or timestamped backup).

## Related

- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md` (first wall-hit, morning)
- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--boot-hook-update-in-place-never-persists.md` (found during the same investigation)
- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md`
