---
title: "configureSessionStartHook() update-in-place branch never writes settings.json to disk"
status: fixed (alpha.31, shipped alpha.32, promoted to stable 0.4.86; PR #1086; validated on origin machine 2026-07-05 via doctor --fix)
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-04
---

## What happened

Found while investigating the SessionStart hook duplication on 2026-07-04. In `src/boot/installer.mjs`, `configureSessionStartHook()` has two branches:

```js
if (existingIdx >= 0) {
  // Update in place
  settings.hooks.SessionStart[existingIdx] = hookEntry;
  return 'SessionStart hook updated in settings.json';   // <-- never persisted
} else {
  // Append
  settings.hooks.SessionStart.push(hookEntry);
  writeJSON(CC_SETTINGS, settings);                       // <-- only branch that writes
  return 'SessionStart hook added to settings.json';
}
```

The update branch mutates the settings object in memory, returns "updated in settings.json", and never calls `writeJSON`. The install output reports success, but the file on disk is unchanged.

Verified in both the repo working tree and the installed package (`/opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/src/boot/installer.mjs`, v0.4.85-alpha.30). Same code both places.

## Impact

Any change routed through the update path silently does not land. Concretely: if `BOOT_DIR` moves (the `shared/` to `library/` rename is in progress and the matcher explicitly matches both `boot-hook` and `shared/boot`), or the hook `timeout`/`matcher` changes, every `ldm install` will claim the hook was updated while the old command path stays in `~/.claude/settings.json` forever. The boot hook then runs stale or breaks entirely when the old path is removed, and the install log gives no signal.

## Fix

Call `writeJSON(CC_SETTINGS, settings)` in the update branch too (or hoist a single write below the branch, writing only when the entry actually changed; skip and report "already configured" when identical, matching the pattern in `lib/deploy.mjs` `installClaudeCodeHookEvent()`).

**Fix landed 2026-07-04 on this same branch** (`cc-mini/guard-and-boothook-tickets`, PR #1086): update branch persists, identical entry is a no-op, duplicate boot-hook entries collapse to one on install, and `ldm doctor` gained a duplicate-hook + invalid-model check with `--fix` collapse and timestamped backup. Per CC review: the invalid-model check keys on control characters only (bracketed 1M-context IDs are valid), and doctor's duplicate collapse intentionally keeps the first entry as-is without re-canonicalizing a stale survivor... `configureSessionStartHook()` owns canonicalization on install. Regression coverage in `scripts/test-boot-hook-registration.mjs` and `scripts/test-doctor-hook-dedupe.mjs`. Status moves to closed when the release ships and the origin machine validates.

## Acceptance

- On a fixture HOME with an existing boot-hook entry whose command path or timeout differs from current, `ldm install` rewrites the entry on disk; a second run is a byte-identical no-op reported as already configured.
- Regression test covers all three cases: append (new install), update (changed entry, persisted), no-op (identical entry, no write).

## Related

- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md` (same function; the doctor dedupe pass scoped there should land together with this persist fix)
- `ai/product/bugs/guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md` (found in the same investigation)
