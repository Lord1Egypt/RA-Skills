---
title: "Installer CC Coder /goal Operating Procedure"
type: operating-procedure
status: live
owner: any agent acting as Installer CC Coder
repo: wip-ldm-os-private
references: ldmos-bugs-masterticket--installer.md
created: 2026-05-13
---

# Installer CC Coder /goal Operating Procedure

This is the runbook for whichever agent currently holds the **Installer CC Coder** seat. It explains how to drive `ai/product/bugs/installer/ldmos-bugs-masterticket--installer.md` through Claude Code's `/goal` feature, one ticket at a time.

The master ticket is the source of truth for ordering, phase boundaries, and editorial context. This file is the source of truth for the execution discipline applied on top of it.

## Prerequisites

- **Claude Code 2.1.140 or later.** `/goal` was introduced in 2.1.139; 2.1.140 fixed the silent-hang failure when hooks are disabled. Older CC: install/upgrade before continuing.
- **Workspace trust dialog accepted.** `/goal` is part of the hooks system and will not run otherwise.
- **Hooks enabled.** If `disableAllHooks: true` or `allowManagedHooksOnly: true` is set in any settings file (user, project, managed), `/goal` will refuse to start. Fix the offending setting; do not bypass.
- **Repo onboarded.** Read `wip-ldm-os-private/CLAUDE.md`, the relevant Dev Guide, and the master ticket itself before any first write. The branch-guard enforces this.
- **Docs:** https://code.claude.com/docs/en/goal

## How /goal works

`/goal <condition>` puts the session into autonomous multi-turn mode. After every turn, a small fast evaluator (Haiku-class) reads the transcript and current state and decides whether the condition holds. If not, CC starts another turn. Aliases for shutdown: `/goal clear`, `/goal stop`, `/goal off`, `/goal reset`, `/goal none`, `/goal cancel`.

Only one goal can be active at a time. Setting a new one replaces the old one. Condition text supports up to 4,000 characters; use the budget.

## Pipeline and roles

Installer work runs through four seats. The coder is one of them. The other three exist whether or not they're currently staffed; the coder respects the boundaries even when one human (Parker) is spawning every seat as a fresh session.

| Session name | Role |
|---|---|
| `installer-bugs--cc--coder` | Sets `/goal` on a ticket, ships the PR. (This document is its playbook.) |
| `installer-bugs--cc--reviewer` | Claude Code review pass. Comments and change requests on the PR. CC reviewer's final approval is the gate to deploy. |
| `installer-bugs--codex--reviewer` | Codex review pass. Parallel to CC reviewer. Today async / out-of-band until the Codex bridge lands. |
| `installer-bugs--cc--deployer` | Merges the approved PR and runs the appropriate approved release/deploy steps for the target track (alpha/beta/stable via `wip-release`; public mirror via `deploy-public.sh` when the change ships to a paired public repo; private docs / `ai/`-only PRs may not deploy anywhere beyond the merge). Owns release-notes placement. |

**Handoffs flow strictly down the table.** The coder hands to the reviewers. The reviewers hand back to the coder for iteration or forward to the deployer. The deployer ships. Parker dogfoods after deploy. The coder never writes `gh pr merge`, `wip-release`, `ldm install`, or dogfood instructions; those belong to the deployer's playbook.

**Reviewer disagreement is normal, not an escalation.** When CC reviewer and Codex reviewer disagree (one passes, the other flags a blocker), the gate stays closed until the disagreement is reconciled. CC reviewer should not give final approval until Codex reviewer's findings are addressed, or explicitly deferred with rationale recorded in the PR thread or a named follow-up ticket. PR #938 (Phase 1 source.npm cleanup) is the prototype failure mode: Codex caught a data-loss blocker (false phantom deletion of custom-path entries) that CC reviewer missed on first pass; if the coder had taken CC's initial green and shipped, working extensions could have been silently removed. Both perspectives must be reconciled, in PR comments or a follow-up ticket, before the PR moves to the deployer's seat.

## Dogfood gate

Installer work has three distinct validation types. Do not conflate them.

| Type | Participant | Environment | Purpose |
|---|---|---|---|
| **Coder validation** | Agent | Fixtures or disposable state | Prove the code works |
| **Installer validation** | Agent | Disposable installer environment: temp `HOME`, isolated `LDM_ROOT`, container, ephemeral VM, or fresh user account | Prove the installer can update itself and apply migrations |
| **Dogfood validation** | Parker (user) | Real machine, fresh AI session, public install prompt | Prove the AI-driven install path produces the intended end-user experience without insider commands |

Parker's machine is the final dogfood, not the first fixture.

Agents do not run state-mutating installer commands on Parker's production machine for validation. Agents use `--dry-run`, fixtures, or disposable environments. Real installs are reserved for Parker's dogfood unless Parker explicitly delegates the install to the agent.

Default posture: agents do not run state-mutating installer commands on Parker's machine. Per-run delegation is the exception; general scope is not delegation.

### Approved coder-side validation surfaces

- **`ldm install --dry-run`** ... first-class today. Always allowed. Non-state-mutating. Captures the install summary an agent needs for inspection without consuming migration state.
- **Temp `HOME` + isolated `LDM_ROOT` override** ... first-class once the fixture-environment sub-ticket lands. Until then, this is best-effort and not guaranteed clean.
- **Docker, ephemeral VM, or fresh user account** ... first-class today. Slower and more setup than the fixture environment, but available now as disposable installer validation surfaces.
- **Parker's machine** ... not a coder-side validation surface at all. It is the final dogfood. The only path for an agent to run a state-mutating installer command on Parker's machine is Parker's explicit per-run delegation.

### Prototype failure

PR #938 / alpha.28 is the prototype failure. A validating agent ran `ldm install --alpha` on Parker's production machine to "verify" the migration behavior, consumed the one-time migration state, and erased the natural dogfood moment from the public install path. The dogfood gate exists to make that failure structurally less likely.

## The slicing rule

**One `/goal` equals one ticket file.** Never set a `/goal` for "Phase 1" or "the installer overhaul." The evaluator cannot judge multi-PR campaigns. It can judge "a specific file exists with specific content, a specific branch has a specific commit, a specific shell command exits 0."

If a ticket is too big for one `/goal`, the ticket is too big. Split the ticket first (a separate `/goal` of its own, namely "the ticket has been split into N smaller tickets in `ai/product/bugs/installer/` and the master ticket has been updated to reference the children").

## The condition template

A good condition is **observable**. Each clause must be checkable by either:

- Reading a file on disk (e.g. `cat`, `grep`, `rg`).
- Running a deterministic shell command (e.g. `node bin/ldm.js status`, `npm test`).
- Inspecting git/PR state with `gh` (e.g. `gh pr view --json mergeable,statusCheckRollup`).

For an installer ticket, the standard shape is:

> PR is open against `wipcomputer/wip-ldm-os-private` from a `cc-mini/` branch implementing `<TICKET-FILENAME>`; `<BEHAVIORAL OUTCOME visible in 'ldm status' or filesystem>`; `<REGISTRY OR CODE INVARIANT expressed concretely>`; release notes for the alpha are on the branch when this PR is part of an imminent release; CI is green; the master ticket row for this ticket has been edited to reflect the new status.

**Avoid** phrases the evaluator cannot verify:

- "the ticket is done", "the design is good", "reviewer approved", "Parker is happy", "looks clean".

**Prefer** phrases the evaluator can verify:

- `rg -n 'source\.npm' src/` returns no legacy entries.
- `node bin/ldm.js status` exits 0 with 0 rows under "unavailable".
- The frontmatter `status:` field of `<ticket>.md` is `fixed`.
- `gh pr view <num> --json mergeable,statusCheckRollup` shows `mergeable=MERGEABLE` and all checks pass.

## The execution loop, per ticket

1. **Read the ticket.** Extract its real acceptance criteria from the body.
2. **Read the master row.** Editorial notes there often modify scope ("audit-gated", "verify before re-implementing", "scope down to LDM OS only").
3. **Translate to a condition** using the template above. Use the 4,000-char budget; specificity is cheaper than back-and-forth.
4. `/goal <condition>` ... start autonomous work.
5. **Work to satisfaction.** The evaluator drives turn-by-turn. If the same false-negative recurs across multiple turns, the *condition* is wrong, not the work; revise it with `/goal clear` + a new `/goal`.
6. **On satisfaction, in this order:**
   1. Update the master ticket row in place (status, alpha number, editorial note). Master is append-only by convention; edit rows, do not rewrite the file.
   2. Update the individual ticket file's `status:` frontmatter.
   3. `/goal clear`.
7. **Hand off to reviewers.** PR is now in the reviewers' court. The handoff message names `installer-bugs--cc--reviewer` and `installer-bugs--codex--reviewer` for parallel review and stops there. **Do not** write `gh pr merge`, `wip-release`, `ldm install`, or dogfood instructions in the handoff; those belong to the deployer's playbook, not the coder's. The coder's role *pauses* at "PR ready and master updated" ... it does not end here. The coder picks up again in step 8 to iterate on whatever the reviewers flag.
8. **Iterate on review feedback.** If reviewers leave change requests, return to step 1 with a sharpened condition; the PR stays open. Do not merge on the coder's own authority. Do not assume one reviewer's comment is the final word; the gate is CC reviewer's explicit approval after change requests are addressed.
9. **After CC reviewer's final approval** (the gate to deploy), the PR is in the `installer-bugs--cc--deployer` seat's court. Do not set the next `/goal` until the deployer has shipped and Parker has dogfooded.
10. After Parker greenlights the dogfood, return to step 1 with the next ticket.

## Execution order (top-down from the master)

This section restates the master's phase order from the coder's seat. The master remains authoritative; when the two disagree, the master wins and this file gets updated.

### Phase 0 (foundation)

- The master ticket itself is in-flight forever. No `/goal`.
- `2026-05-13--cc-mini--installer-registry-source-types-architecture.md` is a design doc. If reviewer fixes are applied and Parker wants it merged as a doc PR, set one `/goal`: "design doc PR opened and merged into `wip-ldm-os-private/ai/product/bugs/installer/`." Otherwise it stays open as a reference and no `/goal` is needed.

### Phase 1 (P1, one alpha)

- **Goal-1:** `2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md`. Condition must include: false 404 probes go to zero; installed-extension inventory is conserved; phantom-row removals and known-duplicate dedupes are reported separately in the install summary; `Untracked extensions` section exists with remediation hint; `ldm doctor` warning for future `source.npm` drift exists; release notes on branch when the PR is part of an imminent release; CI green. (Do not write "0 unavailable rows" ... `dream-weaver-protocol` returns npm 200 with no `dist-tags.latest`, so Phase 1 correctly leaves it alone and `ldm status` keeps marking it `[unavailable]` until Phase 2's reclassification.)
- **Stop.** Reviewers review, deployer cuts alpha, Parker dogfoods. Then Phase 1 is done and Phase 2 begins.

### Phase 2 (P1-P2, two to three alphas, internal order)

- **Goal-2:** `2026-05-13--cc-mini--installer-source-types-migration.md`. The `ldm doctor --reclassify-sources` command. Non-destructive default; `--yes` for batch apply. Lands with Step 2 or Step 3 alpha, whichever ships first.
- **Goal-3:** `2026-05-13--cc-mini--installer-source-bundled.md`. **Audit gate.** Condition must include: "audit document committed to the branch documenting which extensions are bundled, and the decision to either bundle the toolbox sub-tools into this PR or split them into a follow-up ticket is recorded in the PR body."
- **Goal-4:** `2026-05-13--cc-mini--installer-source-git.md`. Condition must include: `gh api` calls live inside `lib/` only and are not surfaced as agent-callable; forks (local ahead of upstream) reported as "ahead of upstream" via `semverNewer` comparison, not as "update available."
- **Goal-5:** `2026-05-13--cc-mini--installer-status-show-all-extensions.md`. Output reformat. Folds in `source.local` (skip with category) and `source.private` (skip with category). The Phase 1 `Untracked` section is preserved but expected to be mostly empty by the time this ships.
- **Goal-6:** `2026-05-13--cc-mini--installer-registry-hygiene-audit.md`. Pure `ldm doctor` work. Land with whichever Phase 2 alpha is convenient.
- **Stop between alphas.** Each ticket runs the full coder -> reviewers -> deployer -> dogfood loop before the next one starts.

### Phase 3 (verification sweep, then survivors)

- **Goal-7:** `2026-05-13--cc-mini--installer-phase-3-verification-sweep.md`. Condition: "for each of the five listed tickets, a verification note is appended to the ticket file with outcome (`fixed` / `confirmed-still-reproduces` / `obsolete`), and the two pre-confirmed tickets (skill-yaml validator at `lib/deploy.mjs:62`, `tools.allow` updater at `lib/deploy.mjs:603`) are moved to `archive/` if their live-repro confirms the fix."
- **After the sweep:** any ticket marked `confirmed-still-reproduces` gets its own `/goal`, derived from its own acceptance criteria. File those goals as they come; do not pre-write them.

### Phase 4 and Phase 5

Same per-ticket `/goal` pattern. Parker triages priority before each one. Do not auto-sequence Phase 4/5; wait for Parker to say "next is X."

## Don't

- Don't set a `/goal` that spans more than one ticket file.
- Don't try to chain goals automatically. `/goal` is per-session, one-at-a-time.
- Don't skip the master-ticket update step. The master is the source of truth for ordering and rolling context; if it goes stale, the next agent in the chair re-does work.
- Don't dogfood inside a `/goal` session. Dogfood happens **between** goals, with Parker.
- Don't bypass any guard hooks if `/goal` trips them. Treat blocks as information. Fix the underlying issue or tell Parker.
- Don't speculatively add `RELEASE-NOTES-v*.md` to non-release PRs (per repo CLAUDE.md, release notes belong to the PR or batch that actually triggers the release).
- Don't run `wip-release` or install anything globally as part of a `/goal`. Releases are a separate agent action; the coder's `/goal` stops at "PR ready and master updated."
- Don't write merge / deploy / dogfood instructions in your end-of-coding handoff. Name the reviewers (`installer-bugs--cc--reviewer` and `installer-bugs--codex--reviewer`) and stop there. `gh pr merge`, `wip-release`, `ldm install`, and "then dogfood `ldm status`" all belong to the deployer's playbook. Skipping the reviewers to point at merge or deploy collapses the pipeline and removes the gate.

## When to escalate

- If the evaluator repeatedly reports "not satisfied" while the work looks complete, the condition is wrong. Run `/goal` (no args) to see its current view, then `/goal clear` and re-set with a sharper condition.
- If hooks block `/goal` at startup, fix the specific offending setting. Do not disable the hook system.
- If a ticket's scope expands beyond what the condition described, `/goal clear`, rewrite the condition with the new scope, `/goal` again.
- If the master ticket and this file disagree, the master wins. Update this file in a follow-up PR.

## Maintenance

- This document gets edited when the `/goal` feature changes upstream (new aliases, new constraints, new docs URL), when the master ticket's phase structure changes meaningfully, or when the coder discovers a recurring failure mode worth codifying.
- Edits go through the normal `cc-mini/<feature>` branch + PR + master-row-update flow. The operating procedure is governed by itself.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
