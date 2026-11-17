---
title: "shared/ to library/ migration incomplete: two boot-hook deploy writers, hook executes the stale copy"
status: partially-fixed (installer half landed stable 0.4.86, PR #1106: single deploy truth + doctor stale-at-exec check; machine shared/->library/ migration deferred to OS-level 2026-04-14 library-migration-plus-topology ticket, kept OPEN)
priority: P1
owner: cc-mini (Installer CC Coder)
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-07-05
---

## What happened

2026-07-05, after `ldm install --alpha` deployed v0.4.85-alpha.32 and reported "+ Boot hook updated": the live boot payload was still 49KB with none of the alpha.32 trim behavior. Diagnosis:

- `~/.ldm/shared` on the origin machine is still a REAL directory (the shared-to-library rename migration never ran here; the installer code explicitly leaves a real `shared/` untouched pending "a dedicated session").
- `syncBootHook()` in bin/ldm.js deploys the new boot-hook.mjs to `~/.ldm/library/boot/` only.
- The registered SessionStart command points at `~/.ldm/shared/boot/boot-hook.mjs` (BOOT_DIR in src/boot/installer.mjs is `join(LDM_ROOT, 'shared', 'boot')`).
- Net: new code lands in library/, sessions execute the stale copy in shared/. The install lies about the update being active.

Manual recovery that worked: `ldm-boot-install` (which deploys via BOOT_DIR = shared/boot) put current code where the hook actually points; payload dropped 49.0KB to 35.9KB with the trim caps and summary line active.

## Why it matters

Split-brain deploys are silent: version tracking said alpha.32, health check said all healthy, and the user-visible behavior was still the old code. Any future boot-hook fix hits the same wall on machines where the migration hasn't run.

## Fix

1. One BOOT_DIR truth: `syncBootHook()` and `src/boot/installer.mjs` must deploy to the SAME location, and that location must be the one the registered hook command points at. Compute it from the actual settings.json entry when present.
2. Finish the shared-to-library migration on machines with a real `shared/` dir: move contents, replace with symlink, rewrite registered hook commands to the canonical path, timestamped backup first. This is the "dedicated session" the code comment defers to; schedule it.
3. `ldm doctor` check: registered hook command path content differs from the freshest deployed copy (hash compare across shared/ and library/) reports "boot hook stale at execution path" with the fix hint.
4. Regression test: fixture HOME with real shared/boot older than library/boot; assert install updates the execution path (or doctor flags it), not just library/.

## Status (2026-07-05, in review, branch `cc-mini/boot-dir-truth`)

Fix items 1, 3, and 4 shipped in this PR:

- **Item 1:** `syncBootHook()` now resolves its deploy target from the registered SessionStart hook command (`resolveBootExecDir()` in `bin/ldm.js`), falling back to `shared/boot` (matching `src/boot/installer.mjs` `BOOT_DIR` and `configureSessionStartHook()`). Deploy location and execution location can no longer diverge.
- **Item 3:** `ldm doctor` hash-compares the file the registered hook runs against this CLI's `src/boot/boot-hook.mjs` and reports "boot hook stale at execution path"; `--fix` redeploys to the execution path with a timestamped `.bak-*` first.
- **Item 4:** `scripts/test-boot-dir-truth.mjs` (doctor-driven, per the "or doctor flags it" clause).

**Item 2 (machine migration) is intentionally deferred.** Moving `shared/` contents, symlinking, and rewriting registered commands on machines with a real `shared/` dir is the OS-level ticket `2026-04-14 library-migration-plus-topology`, not this one. This PR stops the installer from lying and makes doctor see the drift; it does not migrate machines.

## Related

- `2026-04-30--cc-mini--dev-guide-split-path-migration.md` (same migration debt, different file; the soft deadline in that ticket has long passed)
- `2026-07-05--cc-mini--deploy-hook-ownership-misses-boot-hook.md` (same install, sibling registration bug)
