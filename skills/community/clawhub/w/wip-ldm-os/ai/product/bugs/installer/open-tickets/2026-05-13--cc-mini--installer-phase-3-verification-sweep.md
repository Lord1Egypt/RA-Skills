---
title: "Installer: Phase 3 verification sweep (re-validate five older tickets against alpha.27)"
status: open
priority: P2
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: Phase 3 verification sweep

## Problem

The 2026-05-13 master ticket review carried "verify before re-implementing" editorial notes on five older Phase 3 tickets. Each ticket was filed in April or earlier; the installer codebase has changed substantially since then. Some may already be fixed by intervening work; some may still reproduce. Letting them sit in the queue with "verify before re-implementing" is a parking lot.

This ticket is one slice that triages all five in a single sitting, against current alpha.27 (or whatever is current at execution time), and produces clean outcomes for each.

## Tickets to verify

1. **`2026-04-24--codex--installer-deploys-invalid-skill-yaml.md`** — claims "Fix implemented in worktree, pending PR merge and release." **Pre-confirmed by 2026-05-13 codex-reviewer empirical check:** `validateSkillFrontmatter()` exists at `lib/deploy.mjs:62`, called before skill install at `lib/deploy.mjs:1322`, with regression test at `scripts/test-skill-frontmatter.mjs:31`. Sweep just needs to reproduce the original failure scenario against alpha.27 to confirm the fix actually triggers, then close-as-fixed and archive.
2. **`2026-04-10--cc-mini--installer-must-deploy-new-xai-grok.md`** — installer doesn't deploy new `wip-x-xai-grok`. May be partially addressed by intervening rename or repo-manifest work. (Not pre-confirmed by reviewer; full triage needed.)
3. **`2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md`** — `tools.allow` not updated on OpenClaw plugin install. **Pre-confirmed by 2026-05-13 codex-reviewer empirical check:** the `tools.allow` update code is at `lib/deploy.mjs:603`, with a separate `reconcileToolsAllow()` at `lib/deploy.mjs:659`. Sweep needs to confirm this triggers correctly during OpenClaw plugin install in current alpha.27, then close-as-fixed and archive.
4. **`2026-04-03--cc-mini--installer-recreates-renamed-folders.md`** — oldest open ticket here. Installer recreates folders the user renamed. Deploy code has changed substantially since April. (Not pre-confirmed by reviewer; full triage needed.)
5. **`2026-04-24--codex--alpha-install-does-not-refresh-toolbox-subtools.md`** — claims "Fixed in branch. Close after merge and release." Need to verify merge+release happened. (Likely shipped as part of one of the May alphas; full triage needed but expected close-as-fixed.)

**Two of five are already pre-confirmed empirically** (skill-yaml validator and tools.allow updater both have working implementations per the codex-reviewer's grep of `lib/deploy.mjs`). The sweep work for those two is just the live-repro confirmation step, then close-and-archive. The other three need full triage.

## Per-ticket triage procedure

For each ticket, in order:

1. **Read the ticket's repro section.** If no repro section exists, derive from the problem description.
2. **Attempt the repro against current alpha.27.** Use a fresh worktree of `wip-ldm-os-private` and a dry-run install where possible to avoid touching live state.
3. **Decide one of three outcomes:**
   - **Fixed by intervening work:** mark the ticket `status: fixed`, add a "Fix" section citing the responsible PR/release, move to `archive/`.
   - **Still reproduces:** mark the ticket `status: confirmed (2026-05-NN)`, add a Repro Verification section with the current-day command sequence, leave in the open queue.
   - **Obsolete:** mark the ticket `status: obsolete (2026-05-NN)`, add a one-paragraph note explaining why (e.g., "OpenClaw fork moved away from tools.allow enforcement in 2026.X; the bug no longer applies"), move to `archive/`.
4. **Update the master ticket's editorial note** for that ticket with the verification outcome.

## Acceptance

- All five tickets above are walked through the triage procedure.
- Each ticket has a clear post-sweep status: `fixed`, `confirmed (with current repro)`, or `obsolete (with rationale)`.
- Tickets marked fixed or obsolete move to `archive/`.
- Master ticket's editorial notes are updated to reflect the outcomes.
- Sweep produces a summary report (in the ticket body) listing all five outcomes for posterity.

## Why P2

Closing zombie tickets matters for queue health. Without this sweep, every reader of the master ticket sees five "verify before re-implementing" notes and either skips them (perpetuating the parking lot) or tries to re-implement against an obsolete repro (wasted work). One focused triage session converts the parking lot into either a clean queue or a clean archive.

## Out of scope

- Implementing any fixes that the sweep uncovers. If a ticket is `confirmed (with current repro)`, this sweep does NOT fix it; it just sets it up for a future implementation slice with current information.
- Verifying older Phase 4/5 tickets. This sweep is specifically the five tickets named in the master ticket's "verify before re-implementing" editorial notes.

## Recommendation

No release. Tooling/triage work only. Lands as a docs PR; no alpha cut needed.

## Related

- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
