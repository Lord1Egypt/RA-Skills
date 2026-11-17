---
title: "LDM OS OS-Level Master Ticket"
status: in-flight
priority: P1
owner: unassigned (coder) + OS-Level CC Partner (review)
repo: wip-ldm-os-private
created: 2026-07-05
---

# LDM OS OS-Level Master Ticket

Rolling index for OS-level work: the machine-wide substrate underneath the installer and the individual extensions. Directory topology (`~/.ldm`, `~/.claude`, `~/.openclaw`), git tracking contracts for the tracked homes, path hygiene, LaunchAgents, credential lifecycle, and workspace-wide git hygiene. Append-only, same operating principles as `../installer/ldmos-bugs-masterticket--installer.md`: individual ticket files in `open-tickets/` are the source of truth for their own scope; this master owns ordering, dependencies, and rolling context.

## Scope boundary

Installer behavior bugs (what `ldm install` / `ldm doctor` DO) belong in `../installer/`. OS-level owns what the machine IS: where things live, what git tracks, what rots over time (tokens, stashes, worktrees, hardcoded paths), and which system services exist outside the installer's reach. When a ticket needs both (the shared/library migration), the installer ticket owns the code change and the os-level ticket owns the topology decision; cross-reference both ways.

## Execution order

### Phase 1: Topology and tracking contracts (do first, they gate everything else)

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-04-14--cc-mini--library-migration-plus-topology.md` | open / P1 | The parent question: `~/.ldm/shared` vs `~/.ldm/library`, what deploys where, and the deployment topology doc. Became urgent 2026-07-05: the half-done migration caused a live split-brain where `ldm install` deployed new boot-hook code to `library/` while sessions executed the stale copy in `shared/` (see `../installer/open-tickets/2026-07-05--cc-mini--shared-library-split-brain-boot-deploy.md` for the incident and code fix). Finish the migration ON the origin machine as part of this ticket; the installer ticket owns preventing recurrence. |
| `open-tickets/2026-07-05--cc-mini--dotldm-repo-tracking-strategy.md` | open / P1 | `~/.ldm` repo drowned in installer churn: 3.5K deletions + 7K untracked after one install day. Define the tracking contract (config and identity tracked; deploy artifacts, _trash/, logs ignored), one reviewed untracking commit, backup-coverage check. Do together with the library-migration ticket above: same "what lives where" decision. |
| `open-tickets/2026-07-05--cc-mini--deployed-state-drift-commit-policy.md` | open / P2 | Tracked homes (~/.claude, ~/.openclaw) accumulate tool-written drift nobody owns committing; pulls wedge (observed: ~/.claude 3 behind, unpullable, 2026-07-05). Three-class policy (transient/deployed/personal), gitignore transient, sanctioned installer-owned commit path, guard integration. Third face of the live-state problem; siblings are the guard no-blessed-recipe ticket and the dotldm tracking ticket. |

### Phase 2: Rot control (recurring decay, needs structural answers)

| Ticket | Status | Notes |
|---|---|---|
| `open-tickets/2026-07-05--cc-mini--git-hygiene-worktree-stash-backlog.md` | open / P2 | Hundreds of stale merged worktrees (200+ in wip-ldm-os-private alone, 80KB `git worktree list`) and ~50 orphan stashes across repos. One-time merged-check sweep script (dry-run, report-first, never force) + post-merge routine so it does not regrow. 2026-07-05 sprint cleanup proved the pattern at small scale. |
| `open-tickets/2026-04-05--cc-mini--day24-anthropic-api-key-rotation.md` | open / VERIFY | April ticket: exposed Anthropic API key needed rotation. Likely OBE: the 2026-06-23 config removed Anthropic from Lēsa's stack entirely (dot-openclaw PR #17). Verify the exposed key was actually revoked at Anthropic, then close to archive. Broader lesson got fresh evidence 2026-07-05: the npm token rotted and broke the release train for hours (see `../installer/open-tickets/2026-07-05--cc-mini--npm-trusted-publishing-migration.md`). Credential lifecycle is an os-level recurring theme; if a third credential rots, file a dedicated credential-inventory ticket. |

### Archive (closed historical, `archive/`)

| Ticket | Notes |
|---|---|
| `2026-03-17--dogfood-bug-sweep.md` | March dogfood sweep; the /tmp-symlink packages finding foreshadowed the no-/tmp rule. |
| `2026-03-27--cc-mini--launchagents-not-managed.md` | LaunchAgents placed by hand, not by `ldm install`. Closed, but `ldm doctor` still reports plist drift on fixture runs (seen 2026-07-04 in test output); if that resurfaces on the real machine, reopen as a fresh ticket rather than editing this one. |
| `2026-03-30--cc-mini--hardcoded-paths-audit.md` | The audit that found hardcoded user paths across plugins/extensions. |
| `2026-03-30--cc-mini--full-hardcoded-path-cleanup.md` | The cleanup pass for the audit above. |

## Cross-repo dependencies, named

- **`../installer/` master ticket Phase 6** ... the 2026-07-05 release-train fallout tickets. The shared/library split-brain lives on both lists deliberately (code fix there, topology decision here).
- **`../guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md`** ... the guard-side half of the deployed-state drift policy.
- **dot-claude / dot-openclaw / dot-ldm home repos** ... Phase 1's contracts land as .gitignore + docs changes in those repos, PR'd per their own conventions.

## How to use this file

New os-level ticket: add a row in the right phase, one line of context. Status moves: edit the row. Work order: top-down, Phase 1 gates Phase 2. Scope doubt: read the scope boundary above; when in doubt between installer and os-level, the deciding question is "is this about what the tool does, or about what the machine is?"

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
