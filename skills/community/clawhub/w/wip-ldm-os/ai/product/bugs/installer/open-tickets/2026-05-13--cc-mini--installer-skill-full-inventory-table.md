---
title: "Installer SKILL.md must specify full-inventory table with status per row"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

## Problem

The alpha.29 dogfood revealed a real spec ambiguity. Two AIs (Claude Code and Codex) followed the same install prompt from `https://wip.computer/install/wip-ldm-os.txt` and produced materially different summaries:

- Claude Code: 6 rows (updates only). Omitted current extensions. Omitted the Untracked extensions section.
- Codex: 16 rows (full inventory with status per row). Listed the Untracked section.

The user cannot tell which behavior is canonical. The spec says "every component with an update gets a row," which Claude Code interpreted as "only updates." Both readings are defensible.

The user-facing impact: a user pasting the install prompt may see only the diffs and lose visibility into what is actually installed on their machine. Phase 1's "no inventory hidden" rule (which moved 404-source entries to a visible "Untracked" section) is also defeated at the summary layer if the AI omits Untracked from its response.

## Required behavior

Update `wip-ldm-os-private/SKILL.md`:

1. "Already installed → Show update table" must require a FULL INVENTORY table, with one row per installed extension and a Status column showing current / update available / unavailable / untracked. Not "updates only."
2. The summary must also explicitly surface the Untracked extensions section from `ldm status` output, with the `ldm doctor --reclassify-sources` remediation pointer. Phase 1 made those rows visible in the registry; the SKILL.md must keep them visible in the AI's reply.

## Acceptance

- SKILL.md "2. Show update table" section rewritten to specify full inventory with status column.
- SKILL.md explicitly tells the AI to surface the Untracked extensions section in its summary.
- Update `wip-ldm-os-private/scripts/test-readme-install-prompt.mjs` (or `test-install-prompt-policy.mjs`) to assert SKILL.md contains the "full inventory" + "Untracked section surfaced" instructions.
- Dogfood-gate validation: paste the prompt into both Claude Code and Codex; both produce full inventories with the Untracked section visible.

## Out of scope

- Implementing this fix; ticket-maker files the ticket only. A coder picks up `/goal` later.
- Changing the `ldm status` command output itself. The bug is in the SKILL.md's summary instructions, not in the CLI.
