---
title: "Install prompt's user-facing summary should explain bundled extensions and what each extension does"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

## What it does

The install-prompt-driven AI summary explains that bundled extensions ship with their parent package (e.g., `lesa-bridge` is part of LDM OS itself, not a separate install) AND tells the user in plain English what each installed extension does, not just its name and version.

## What it fixes

Today's dogfood (2026-05-13, alpha.28 → alpha.30): the AI listed `lesa-bridge` under "Untracked extensions" with a `ldm doctor --reclassify-sources` remediation that doesn't actually do anything for bundled entries today, AND failed to tell Parker that `lesa-bridge` IS part of LDM OS (he asked "why is it telling me it can't tell me the Bridge version when Bridge is part of LDM OS?"). The user has no mental model for "what is bundled vs what is a separate npm package," and the AI presents update-availability rows without explaining what each extension does.

## How to dogfood

1. Paste the install prompt into a fresh AI session.
2. The AI should tell you in plain English what features LDM OS includes (Bridge, dedup-trash, dogfood-gate playbook, track-aware install, etc.) AND label bundled extensions as "ships with `@wipcomputer/wip-ldm-os`" instead of "untracked, reclassification suggested."
3. If `lesa-bridge` still shows as "Untracked" with no explanation, this ticket has NOT shipped.
4. If you see "Bridge ... ships with LDM OS, updates with the parent package" (or equivalent product language), it has shipped.

## Problem (deeper)

Two layered bugs from the 2026-05-13 dogfood:

1. Bundled extensions are labeled "untracked" because Phase 2's source-bundled ticket has not shipped. Until it does, the AI's user-facing output mislabels real LDM OS components as "untracked, reclassification suggested," and the suggested remediation doesn't help.

2. The AI's summary is update-availability-centric, not feature-installed-centric. Even for non-bundled extensions, the user sees package names and version numbers, not descriptions of what each extension does. The npm `description` field is pulled when available but is not always there, and bundled entries have no npm package to pull from.

## Fix

Two parts, can land separately:

1. Once Phase 2 `installer-source-bundled.md` ships, the AI's output labels bundled extensions correctly ("ships with `<parent>`"). The SKILL.md "How to phrase the track to the user" section grows a bundled-extension display rule.

2. SKILL.md grows a "Tell the user what each extension does" rule. The AI pulls plain-English descriptions from:
   - npm `description` field where available.
   - LDM OS-internal catalog of descriptions for bundled extensions (new; ships in SKILL.md as a reference table OR a JSON catalog deployed to `~/.ldm/library/`).
   - Fallback: "no description available" for unknown extensions.

## Acceptance

- Phase 2 source-bundled lands first (prerequisite for part 1).
- SKILL.md teaches the AI to identify bundled extensions and label them "ships with `<parent>`" instead of "untracked."
- SKILL.md teaches the AI to include a one-line plain-English description per installed extension when showing inventory.
- Catalog of bundled-extension descriptions ships (location TBD: SKILL.md reference, library doc, or deployed JSON).
- Regression test: paste the prompt, AI's output includes "Bridge: agent-to-agent communication, ships with LDM OS" (or equivalent) somewhere in the inventory.

## Out of scope

- The npm description quality itself (those are owned by each package's own SKILL.md / `package.json`; not changed here).
- A full per-extension help system. This ticket just adds plain-English one-liners to the install-prompt summary.

## Related

- Phase 2 source-bundled ticket: `installer-source-bundled.md` (prerequisite).
- Full-inventory-table ticket: `installer-skill-full-inventory-table.md` (lands first; this builds on the inventory rows it produces).
