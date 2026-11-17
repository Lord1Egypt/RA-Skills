---
title: Boot-budget guard for declared boot files (LDM OS / OpenClaw)
date: 2026-04-29
status: open (parked follow-up from 2026-04-28 context-load thread)
severity: P2
component: ldm-installer | openclaw
parent-plan: ../../plans-prds/lesa/2026-04-28--lesa-context-load-optimization.md
related-prs: wipcomputer/lesa-workspace#7
---

# Boot-budget guard for declared boot files

## Context

The 2026-04-28 context-load investigation surfaced that Lēsa's boot contract had drifted into "read everything before acting." The mandatory list grew from continuity scaffolding into 10+ files plus first-heartbeat history, including dead paths (`~/.ldm/DEV-CONVENTIONS.md`, `~/.ldm/memory/daily/`) that no longer exist. The fix in `lesa-workspace#7` switched routine turns to a lean trigger-based boot, but **the underlying drift mechanism is unaddressed**: there's nothing stopping the next contributor from adding "and also read this" to AGENTS.md or CONTEXT.md and growing the contract back over time.

This is the durable systems fix Lēsa called out in her plan doc's "Next Fixes #4":

> Add a boot-budget guard to OpenClaw or LDM OS: when a file says "read every session," require a max line or char budget and flag missing paths.

## What needs to exist

A guard that runs at install time and at doctor time, examining all declared boot files (those marked "read every session" or equivalent in their content) for two failure modes:

1. **Budget overrun.** Each declared boot file gets a max line count (default proposal: 50) and max byte count (default proposal: 4 KB). Files exceeding either threshold flag as a warning.
2. **Stale-path references.** Each path mentioned in a boot file's "read on every session" instructions is checked for existence on disk. Missing paths flag as a warning.

Implementation candidates:

- **OpenClaw plugin** that hooks into `agent_start` or boot validation, reads the workspace's AGENTS.md / CONTEXT.md / SHARED-CONTEXT.md, and emits warnings to the gateway log.
- **LDM CLI doctor check** that walks `~/.openclaw/workspace/` (and equivalent for any future agent home), parses boot files for declared reads, validates each.
- **Per-package `ai/product/boot-manifest.json`** that declares which files are boot-time-read with their budgets, similar to the bin manifest pattern from #717/#718. Then a single guard validates all of them.

## Acceptance criteria

- [ ] Declared boot files that exceed their budget surface a warning at install time and at doctor time.
- [ ] Declared paths referenced by boot files that don't exist on disk surface as warnings.
- [ ] Default budget (line + byte) is documented somewhere reachable.
- [ ] Override mechanism exists for files that legitimately need to be larger (with required justification field).
- [ ] False-positive rate measured against current workspace state (Lēsa's `lesa-workspace#7` should pass cleanly).

## Why P2

This is the durable fix that prevents the boot-drift class from recurring. Without it, the same problem grows back next time someone adds a read. Worth doing before the next OpenClaw/LDM upgrade cycle so the validators are catching drift in real time.

Not P1 because the immediate outage was handled by `lesa-workspace#7`. The system isn't bleeding right now; this is preventive.

## Out of scope

- Per-agent boot contracts beyond Lēsa's. Once the manifest pattern is in place, CC's CLAUDE.md can opt in.
- Enforcement (vs. warning). Start with warnings; add hard fails only if drift continues despite warnings.
