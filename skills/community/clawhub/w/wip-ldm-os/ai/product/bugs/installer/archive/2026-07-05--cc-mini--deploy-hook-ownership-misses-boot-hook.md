---
title: "deploy.mjs hook ownership check cannot recognize the boot hook as its own; every manifest-driven install appends a duplicate"
status: fixed (landed stable 0.4.86, PR #1105; validated on origin machine 2026-07-06: clean install, CLI self-updated first, no duplicate boot hook)
priority: P1
owner: cc-mini (Installer CC Coder)
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-05
---

## What happened

2026-07-05, with the alpha.31 fix to `src/boot/installer.mjs` `configureSessionStartHook()` merged (dedupe + persist, PR #1086): `ldm install --alpha` STILL appended a duplicate SessionStart boot-hook entry (settings went from 4 to 5 entries before `ldm doctor --fix` collapsed them).

Root cause: there are TWO registration paths for the boot hook, and only one was fixed.

1. `src/boot/installer.mjs` `configureSessionStartHook()` ... fixed in PR #1086: owns all entries matching `boot-hook` / `shared/boot`, dedupes, persists, no-ops when identical. `ldm-boot-install` uses this path and correctly reported "SessionStart hook already configured."
2. `lib/deploy.mjs` `installClaudeCodeHookEvent()` ... the generic path used when the wip-ldm-os package's `claudeCode` hook manifest is processed during `ldm install`. Its ownership check finds existing entries by extension-dir tag: `command.includes("/" + toolName + "/")`. The boot hook's registered command is `node ~/.ldm/shared/boot/boot-hook.mjs`, which contains no `/wip-ldm-os/` segment, so `ownedIdxs` is always empty and the code APPENDS a fresh entry on every manifest-driven install.

This is the actual mechanism behind the ongoing accumulation (10 entries found 2026-07-04, then 3, 4, 5 through the day as installs ran). The `configureSessionStartHook` fix removes duplicates when ITS path runs, but the deploy.mjs path re-adds one per install.

## Fix

1. `installClaudeCodeHookEvent()` ownership matching must handle hooks whose deployed command lives outside the extension dir: match on the manifest's declared command basename/path (e.g. `boot-hook.mjs`) in addition to the extension-dir tag, or let the manifest declare an explicit `ownsPattern`.
2. Decide the single owner: either the package manifest stops declaring the boot hook (ldm-boot-install/`configureSessionStartHook` is the sole registrar), or deploy.mjs delegates boot-hook registration to `configureSessionStartHook`. One writer, not two.
3. Regression test: fixture with an existing `shared/boot/boot-hook.mjs` SessionStart entry; run the manifest-driven install path twice; assert exactly one boot entry, byte-identical file on the second run.

## Interim protection

`ldm doctor --fix` (alpha.31+) collapses the duplicates with a timestamped backup, so the damage is recoverable, but it re-accumulates one entry per `ldm install` until this ships.

## Related

- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--boot-hook-update-in-place-never-persists.md` (the fixed sibling path)
- The 2026-07-04 duplicate-registration ticket (10-entry incident; in Parker's open-tickets reorg)
