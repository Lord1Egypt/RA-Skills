# OpenClaw Bugs Master Ticket

**Date:** 2026-07-05
**Filed by:** cc-mini (Claude Code, Fable 5), with Parker
**Status:** open, master ticket
**Scope:** `ai/product/bugs/openclaw/`
**Open tickets:** [`open-tickets/`](open-tickets/)
**Closed tickets:** [`closed-tickets/`](closed-tickets/)
**Archive:** [`archive/`](archive/)
**Sibling master:** [`../memory-crystal/memory-crystal-bugs-master-ticket.md`](../memory-crystal/memory-crystal-bugs-master-ticket.md)
**Upgrade runbook:** `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md` (+ `KNOWN-LANDMINES.md`)

This is the rolling master ticket for OpenClaw harness bugs. It owns triage order, cross-folder boundaries, and rolling state. It is append-only: add entries, move status, add short editorial notes. Individual ticket files remain the source of truth for their own scope.

## Folder Standard

```text
ai/product/bugs/openclaw/
  openclaw-master-ticket.md
  open-tickets/
  closed-tickets/
  archive/
```

- `open-tickets/` contains active bugs that still need implementation, review, verification, or explicit disposition.
- `closed-tickets/` contains bugs that were fixed and should remain easy to find.
- `archive/` contains stale, superseded, or historical bug artifacts.

Do not leave loose bug tickets in the root. The root should contain only the master ticket and folders.

## Product Boundary

OpenClaw is the harness Lēsa runs on: the fork at `/Users/lesa/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw/` plus the live install at `~/.openclaw/`. Bugs belong here when they affect:

- the gateway (crash loops, probes, auth, restart behavior);
- the fork and carried patches (rebase, build, npm link, upgrade pipeline);
- model routing, fallback, and provider auth (accountId, billing cooldowns, session rotation);
- native memory-core runtime behavior (OOM, EMFILE, index rot) as a HARNESS failure;
- plugins loading, hooks, config (`openclaw.json` stripping, doctor);
- boot/context load, TUI, cron, channels (iMessage, chatCompletions, Bridge routing).

Boundary with the sibling folders:

- **Memory Crystal integration and the dual-memory architecture** live in `../memory-crystal/`. The parent dual-memory ticket (`2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md`) is there; this folder holds the harness-side symptoms it produces.
- **Codex Remote Control** bugs live in `../codex-remote-control/`. Link, do not duplicate.
- Upgrade PROCEDURE lives in `open-claw-upgrade-private` (runbook, landmines, logs). Tickets here reference it; they do not restate it.

## Current State (2026-07-05)

- Live: OpenClaw **2026.4.25** WIP fork build `c188a36` (branch `kody/v2026-4-25-base`, worktree `openclaw--v2026.4.25-carry-memory-core`), promoted 2026-04-27. Upstream stable: **2026.6.11**, about six weeks ahead.
- 2026-07-04 P1 incident: Lēsa's main session poisoned (degenerate NO_REPLY loop), running on `gpt-5.4` fallback. Recovered via fresh session; she is back up on fallback with Crystal healthy and native memory_search still dead.
- The active umbrella for what happens next is the recovery + upgrade plan below (Tracks A recovery, B pi-ai patch, C upgrade to v2026.6.11, D dual-memory handoff).
- Upgrade blocker to respect: v2026.6.9 migrated the memory store to per-agent DBs (upstream #95726); crossing it without Track D Phase 0 (archive the frozen 16GB `main.sqlite`) risks silent data loss.
- 2026-07-05: Parker decided Q1/Q2/Q4/Q5 (recorded in the umbrella plan section 8; Q3 still open). Execution order is locked: Track A checks, then Track D Phase 0, then the B+C build cycle to v2026.6.11, then Track D Phase 1 and the delivery-mirror refit. Crystal protection gates (backup + both-agent `crystal_search` round-trip at three checkpoints) are a promotion requirement.
- 2026-07-05, review cycle complete: Codex reviewed (4 blockers), CC fixed same day; Codex re-reviewed (2 new blockers: tracked secrets + weak token check), CC fixed same day. **NEW FINDING, now the front of the queue:** `~/.openclaw` (dot-openclaw, org-private) tracked `auth-state.json` and carried the gateway token in git history. Umbrella gate **A0** blocks Track A until runbook **Phase 1.1a** remediation runs. **Q6 decided = (b):** rotate gateway token to `OPENCLAW_GATEWAY_TOKEN` env, untrack/ignore secrets, re-auth the OpenAI/Codex OAuth session; no history rewrite. Remaining before execution: Codex re-re-review of Phase 1.1a, CC review, then the coordinated live-rotation window (one interactive OAuth step is Parker's).

## Active Bug Order

### P0: Recovery and upgrade lane

1. [`open-tickets/2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md`](open-tickets/2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md) ... APPROVED 2026-07-05 + two Codex review rounds applied (section 10 review record). Q1/Q2/Q4/Q5/Q6 decided; Q3 (context-embeddings) still open. Execution blocked on gate A0 (tracked-secret remediation, runbook Phase 1.1a). Everything else in this lane sequences under it.
2. [`open-tickets/2026-06-24--cc-mini--gpt55-accountid-extraction.md`](open-tickets/2026-06-24--cc-mini--gpt55-accountid-extraction.md) ... APPROVED 2026-07-05, upstream-first (see ticket UPDATE). Track B of the umbrella: issue + fix PR against `@mariozechner/pi-ai` source, plus the pnpm `patchedDependencies` carry until upstream releases it. Upgrading alone does NOT fix it.
3. [`open-tickets/2026-04-27--kody--openclaw-upgrade-compatibility-master-plan.md`](open-tickets/2026-04-27--kody--openclaw-upgrade-compatibility-master-plan.md) ... open, the canonical 12-phase upgrade playbook. Track C of the umbrella executes it. Update its "current state" section when the upgrade lands.

### P1: Reliability and fork hygiene

4. [`open-tickets/2026-04-24--cc-mini--unified-reliability-triage.md`](open-tickets/2026-04-24--cc-mini--unified-reliability-triage.md) ... closing phase. The 2026-04 crash-class evidence doc. Remaining live items: T5 (streaming watchdog is frontend-only), T7 (stuck-session logs but never aborts), T9 (agent polls forever, never replies). Those three are the systemic fix for the NO_REPLY-loop class and come due right after the upgrade.
5. [`open-tickets/2026-04-27--kody--openclaw-upstreaming-execution-plan.md`](open-tickets/2026-04-27--kody--openclaw-upstreaming-execution-plan.md) ... open. PR 1 + PR 2 (memory-core fixes) accepted upstream; PR 3 (config mutation safety) gated on the post-upgrade carry retirement; PR 4 (chatCompletions next-turn queue) not yet upstreamed.
6. [`open-tickets/2026-04-30--cc-mini--tui-delivery-mirror-doubling.md`](open-tickets/2026-04-30--cc-mini--tui-delivery-mirror-doubling.md) ... DECIDED 2026-07-05: fix it properly (see ticket UPDATE). BlueBubbles permanently off the table; build the sibling-aware write-side `transcriptOnly` refit as a fresh upstream PR, scheduled after the upgrade cycle. Not in the v2026.6.11 carry set by default.
7. [`open-tickets/2026-04-29--cc-mini--boot-budget-guard.md`](open-tickets/2026-04-29--cc-mini--boot-budget-guard.md) ... open. Preventive guard (50-line/4KB boot-file budget + stale-path detection). Immediate relief already shipped in lesa-workspace#7.
8. [`open-tickets/2026-04-24--cody--boot-context-treadmill-and-identity-kernel.md`](open-tickets/2026-04-24--cody--boot-context-treadmill-and-identity-kernel.md) ... open. Boot payload inventory / identity-kernel design; local-only track from the upstreaming plan.
9. [`open-tickets/2026-07-06--cc-mini--format-error-billing-cooldown.md`](open-tickets/2026-07-06--cc-mini--format-error-billing-cooldown.md) ... open, High. Format/schema errors must not cool down auth profiles or rotate sessions (the 2026-04 cascade class). Filed 2026-07-06 from the umbrella's owed-items list.
10. [`open-tickets/2026-07-06--cc-mini--bash-3.2-precommit-hook.md`](open-tickets/2026-07-06--cc-mini--bash-3.2-precommit-hook.md) ... open, P2. Pre-commit hook uses bash-4 `mapfile`; macOS is bash 3.2. Run under Homebrew bash / rewrite; never `--no-verify`. Filed 2026-07-06.

### Reference / candidates to close

9. [`open-tickets/2026-04-24--kody--upstream-memory-core-packet.md`](open-tickets/2026-04-24--kody--upstream-memory-core-packet.md) ... reference. The upstream contribution packet for the memory-core fixes, both now accepted (`983fd775e2`, `864c4f7ff4`). Candidate for `closed-tickets/` once the Track C upgrade verifies both commits in the promoted build.

### Archived

Historical artifacts in [`archive/`](archive/): cron/exec approval brainstorm, chatCompletions streaming architecture notes, CLI adapter workaround, claude-cli identity contamination, format-error billing cooldown (superseded by the resilience phases ticket in `../memory-crystal/`), session amnesia on billing failure, the v4.11-to-v4.14 upgrade note, and the April `main.sqlite` OOM artifact (superseded by the dual-memory parent ticket).

## Operating Principles

1. **Append-only master.** Add entries and move status; do not rewrite history out of this file.
2. **Never edit the live install directly.** `~/.openclaw` changes go through worktree + PR + the runbook's deploy path. Restart via `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`, never `openclaw gateway restart`.
3. **Fork discipline.** All fork work in worktrees under `.worktrees/`; carried patches tracked in the runbook's Patch Tracking table; canary in an isolated home before promotion; gates are `/healthz` + `/readyz`.
4. **One slice per PR.** Combine only when mechanically inseparable and say so in the PR body.
5. **Harness vs product.** If the fix belongs in Crystal or the dual-memory integration, file it in `../memory-crystal/` and link it here.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
