# wip-branch-guard v1.9.78

## Hotfix: inline lib/ into guard.mjs

v1.9.77 shipped with `lib/session-state.mjs` and `lib/approval-backend.mjs` as separate ES modules imported by `guard.mjs`. The npm tarball was correct (lib/ is in `files` per `npm pack --dry-run`). However, `ldm install` at `wip-ldm-os-private/bin/ldm.js` line 2608 invokes `ldm install <source>` whose underlying copy mechanism does not recurse subdirectories. Every extension before this one was flat (root-level `guard.mjs` + `package.json`), so the bug was latent.

Net effect: after `ldm install --yes`, `~/.ldm/extensions/wip-branch-guard/` had `guard.mjs` + `package.json` but no `lib/`. On every PreToolUse call, node threw `ERR_MODULE_NOT_FOUND` for `./lib/session-state.mjs`. Claude Code treated the hook crash as fail-open, so tools kept working — but the branch-guard was effectively off.

## Fix

- `tools/wip-branch-guard/guard.mjs`: inlined the contents of `lib/session-state.mjs` and `lib/approval-backend.mjs` into the top of guard.mjs as plain functions + constants. Imports removed. No behavior change.
- `tools/wip-branch-guard/lib/`: directory deleted.
- `tools/wip-branch-guard/test.sh`: dropped the standalone approval-backend import-test (the module no longer exists). Approval behavior remains covered end-to-end by the onboarding override tests (target-match, boolean, wrong-target).
- `tools/wip-branch-guard/package.json`: `1.9.77 -> 1.9.78`.

## Tests

67 passing, 0 failing, 8 main-only skipped. Down from 68 (the dropped unit test).

## Root cause (tracked separately)

The installer's subdir-flatten bug is real and will bite any future sub-tool that wants to organize code under `lib/` or any other subdir. A separate PR on `wipcomputer/wip-ldm-os-private` fixes `installFromPath` in `lib/deploy.mjs` to recurse subdirectories. Once that lands and is installed, this inline block can move back into dedicated modules and be re-imported.

## Why inline instead of wait for the installer fix

1. Every PreToolUse in Claude Code was crashing between v1.9.77 install and now. Fail-open meant no visible errors, but the branch-guard was effectively disabled. Restoring protection immediately took precedence over architectural cleanliness.
2. The installer fix ships from a different repo (wip-ldm-os-private). Getting that landed + released + installed is at least another PR-merge-release-install cycle. Inlining is one small PR.
3. Future re-separation is mechanical: move the `---- session-state + approval-backend (inlined) ----` block to lib/*.mjs, restore the imports. Tests already exercise the behavior.

## Related

- PR 2 original plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
- Installer subdir fix (follow-up PR): to be filed on wip-ldm-os-private.
