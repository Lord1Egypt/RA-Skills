---
title: "Installer dogfood gate: three validation types plus system fix"
status: in-review
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer Dogfood Gate: Three Validation Types Plus System Fix

## Problem

PR review passing + CI green + deployer-clean-merge does not guarantee that the end-user install path actually works. The 2026-05-13 alpha.28 incident is the prototype failure:

- PR #938 (Phase 1 source.npm honest-cleanup) shipped through review and release cleanly.
- A validating agent ran `ldm install --alpha` on Parker's production machine to "verify" the alpha.28 behavior.
- That install consumed the one-time migration state (legacy bad-source.npm rows reclassified to `updateSource: { type: "untracked" }`, phantom rows pruned, duplicates deduped). The clean user-facing dogfood moment was erased; the registry can no longer be observed in its pre-migration shape from this machine.
- Layered failure: the public install prompt is hard-coded to `@latest` (stable), so the AI-driven path from `https://wip.computer/install/wip-ldm-os.txt` cannot reach alpha.28's behavior at all. Even if the state had been preserved, a fresh AI session pasting the public prompt would not have exercised the artifact under test.

Two distinct failures, one root cause: we conflated three different kinds of validation, and the system did not make it structurally impossible to consume Parker's one-time dogfood state during agent validation.

## Three validation types (do not conflate)

| Type | Participant | Environment | Purpose |
|---|---|---|---|
| **Coder validation** | Agent | Fixtures or disposable state | Prove the code works |
| **Installer validation** | Agent | Disposable installer environment: temp `HOME`, isolated `LDM_ROOT`, container, ephemeral VM, or fresh user account | Prove the installer can update itself and apply migrations |
| **Dogfood validation** | Parker (user) | Real machine, fresh AI session, public install prompt | Prove the AI-driven install path produces the intended end-user experience without insider commands |

Parker's machine is the **final** dogfood, not the first fixture. Disposable environments validate first; Parker is the canary at the end, not the petri dish at the start.

## Dogfood gate

A PR is not done when CI is green and reviewers approve and the deployer can merge. It is done when the AI-driven install path from the public prompt produces the intended end-user experience without insider commands.

This is a new gate, distinct from review and release. It is owned by Parker (or whoever holds the dogfood seat for a given release).

**Default posture: agents do not run state-mutating installer commands on Parker's machine.** The exception is Parker's explicit per-run delegation ("run the install for me this time"). The default is "no"; the exception is a specific, scoped, verbal authorization. A general "you're authorized to do installer work" is not delegation for any specific state-mutating run.

## Acceptance

To close this ticket, the implementing agent (a future coder seat picking up `/goal`) must:

1. Add a **Dogfood gate** section to `ai/product/bugs/installer/ldmos-bugs-operating-procedure--installer-coder.md`.
2. In that section, define the three validation types (coder / installer / dogfood) and state that they must not be conflated.
3. Add this operating rule to the coder playbook: **agents do not run state-mutating installer commands on Parker's production machine for validation. Agents use `--dry-run`, fixtures, or disposable environments. Real installs are reserved for Parker's dogfood unless Parker explicitly delegates the install to the agent.** Include the default-posture statement from the Dogfood gate section above.
4. **Enumerate the approved coder-side validation surfaces** with first-class designation. The playbook section should list each surface and what it is approved for:
   - **`ldm install --dry-run`** ... first-class **today**. Always allowed. Non-state-mutating. Captures the install summary an agent needs for inspection without consuming the migration state.
   - **Temp `HOME` + isolated `LDM_ROOT` override** ... first-class **once the fixture-environment sub-ticket lands**. Until then, this is best-effort and not guaranteed clean. The fixture environment is listed in "Named follow-ups" below and is the structural prerequisite for this surface.
   - **Docker container, ephemeral VM, or fresh user account** ... first-class disposable-environment options **today**. Slower and more setup than the fixture environment, but available before the fixture-environment sub-ticket ships. Agents may use any of these for installer validation; the choice is the agent's.
   - **Parker's machine** ... not a coder-side validation surface at all. It is the final dogfood (see three-types table). The only path for an agent to run a state-mutating installer command on Parker's machine is Parker's explicit per-run delegation.
5. Reference PR #938 / alpha.28 as the prototype failure that motivated the gate, with a short summary of what went wrong.
6. (Ticket-maker work, lands in this PR): add a row for this ticket to `ldmos-bugs-masterticket--installer.md` in Phase 0.

## Named follow-ups (do not file or implement in this PR)

These sub-tickets are the eventual system fix that makes the dogfood gate enforceable. They are named here so the concept stays whole, but each gets filed as its own ticket only when its dependency forces it. Filing them all now would generate five rounds of review-and-merge ceremony for work we are not committing to implement this week.

- **Fixture environment.** `LDM_ROOT` override and seedable synthetic registry. Coder validation and installer validation happen in this fixture, not on Parker's machine. This is the structural fix that makes the discipline rule (Acceptance #3) enforceable rather than aspirational.
- **`ldm doctor --restore-backup <timestamp>`.** First-class restore from `registry.json.bak-*` files. Makes dogfood repeatable: run install, observe, restore, hand to another observer, restore again. Closest approximation of "Apple's beta testers run the same install you did" achievable with one machine.
- **`ldm doctor --show-last-migration`.** Reads the most recent `registry.json.bak-*` and prints what changed against current state. Lets post-state machines observe a past migration as text, after the fact.
- **Track-aware install prompt.** Already filed as `2026-05-11--codex--installer-track-selection-and-release-note-placement.md`. Re-scope note: it is not just a UX improvement; it is a dogfood-gate prerequisite. Until the public install prompt is track-aware, no installer migration that targets alpha (like PR #938) can be dogfooded through the public AI-driven path.

## Out of scope

- No fixture implementation in this ticket.
- No restore command implementation in this ticket.
- No migration replay command implementation in this ticket.
- No install, dogfood, release, or deploy action in this ticket.
- The 2026-05-11 track-aware install prompt ticket stays in flight separately; it is referenced here, not re-scoped in this file.

The goal of this ticket is to land the **concept and the operating rule** so a recurrence of the 2026-05-13 incident becomes structurally less likely, then stop installer expansion so the team can return to Remote Control.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
