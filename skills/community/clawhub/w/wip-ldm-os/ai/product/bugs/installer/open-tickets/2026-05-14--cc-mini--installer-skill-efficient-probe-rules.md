---
title: "Install prompt SKILL.md should trust ldm status classification and avoid speculative npm probes"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

## What it does

The AI following the install prompt only probes npm for packages it has reason to believe are on npm. It trusts `ldm status`'s classification of untracked / unavailable / bundled and does not re-probe those entries. It also doesn't speculate on non-existent npm fields like `changelog` or `releaseNotes`.

## What it fixes

Today's dogfood (2026-05-13/14): Codex took 5 minutes for the same prompt Claude Code completed in under a minute, because Codex re-probed every installed extension via raw `npm view` (producing E404 noise for the 7+ extensions `ldm status` had already correctly classified as untracked) and tried `npm view <pkg> changelog releaseNotes changes notes --json` on several packages (none are real npm fields; all returned empty). The user saw a wall of error logs and a long wait for the same answer.

## How to dogfood

1. Paste the install prompt into a fresh AI session, in BOTH Claude Code and Codex.
2. Both should complete in roughly the same time (under 90 seconds).
3. Neither should surface raw `npm error 404` lines for packages that `ldm status` already marked as untracked or unavailable.
4. Neither should run `npm view ... changelog releaseNotes changes notes` (those aren't real npm fields).

## Problem

SKILL.md's "Check available npm tracks" instruction doesn't bound which packages to probe. Codex interprets it broadly (probe everything); Claude Code interprets it narrowly (probe what `ldm status` flags as trackable). Same prompt, materially different experience.

This is the same dogfood-gate pattern as the full-inventory-table ticket: SKILL.md ambiguity, different AIs produce different experiences, the user gets confused.

## Fix

Add explicit rules to SKILL.md:

1. **Trust `ldm status`'s classification.** If `ldm status` lists an extension under "Untracked extensions" or marks its update check as `[unavailable]`, do NOT re-probe it via `npm view`. The classification is the answer.
2. **Bound the npm probe scope.** Only run `npm view <pkg> dist-tags --json` on:
   - The LDM OS package itself (always).
   - Extensions `ldm status` flags as having updates available (their npm names are already in the status output).
3. **Never query npm for fields that aren't standard.** `changelog`, `releaseNotes`, `changes`, `notes` are not real npm package fields. If release notes aren't in npm metadata's `description` or in local package metadata, say "release notes not available" and stop.

## Acceptance

- SKILL.md adds a section (probably under "Source of truth" or as a new "Probe efficiency rules" section) codifying the three rules above.
- Regression test in `scripts/test-readme-install-prompt.mjs` asserts SKILL.md contains those instructions.
- Dogfood: paste the prompt in Codex; complete in under 90 seconds; no E404 spam.

## Out of scope

- Changing `ldm status` output format. The bug is in SKILL.md's probe instructions, not in the CLI.
- Implementing a new changelog/release-notes source of truth. If release notes are unavailable from local or npm metadata, say "release notes not available from local metadata" and stop. This ticket does not change the existing explicit-user-request path for release notes. (Per the install-prompt policy: GitHub releases are not fetched during install-state detection.)

## Related

- `installer-skill-full-inventory-table.md` (sibling; same dogfood-gate pattern of SKILL.md spec ambiguity producing AI-divergent experiences).
- `installer-user-language-bundled-extensions.md` (sibling; same 2026-05-13 dogfood surfaced user-language gap).
