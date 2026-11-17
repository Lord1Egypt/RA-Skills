`ldm install` no longer deploys the boot hook to a location the SessionStart hook does not execute. The boot hook now has one deploy truth: wherever the registered hook command actually points.

`syncBootHook()` in `bin/ldm.js` hardcoded `~/.ldm/library/boot/boot-hook.mjs`, while the registered SessionStart command executes `~/.ldm/shared/boot/boot-hook.mjs` (`BOOT_DIR` in `src/boot/installer.mjs`). On machines where `shared/` is still a real directory, new code landed in `library/` while sessions kept running the stale copy in `shared/`, and the install reported "Boot hook updated." On 2026-07-05 this made alpha.32's boot-payload trim silently inactive (live payload stayed at 49KB instead of 35.9KB) until `ldm-boot-install` re-deployed to the execution path.

`syncBootHook()` now resolves its deploy target from the registered SessionStart hook command (`resolveBootExecDir()`), falling back to `shared/boot` (matching `BOOT_DIR` and `configureSessionStartHook()`) when no hook is registered yet. The deploy location and the execution location can no longer diverge.

`ldm doctor` gains a "boot hook stale at execution path" check: it hash-compares the file the registered hook actually runs against this CLI's `src/boot/boot-hook.mjs` (the code the installer would deploy) and reports when they differ, naming a current copy under `shared/boot` or `library/boot` if one exists. `ldm doctor --fix` redeploys the current boot hook to the execution path, writing a timestamped `.bak-*` copy of the stale file first.

Out of scope (tracked separately): the full `shared/` to `library/` machine migration is the OS-level ticket `2026-04-14 library-migration-plus-topology`. This change stops the installer from lying and lets doctor see the drift; it does not migrate machines.

Regression coverage: `scripts/test-boot-dir-truth.mjs` (stale exec path reported not written without `--fix`; `--fix` redeploys and backs up; in-sync path not flagged; no registered hook is a clean no-op).

Ticket:
- `ai/product/bugs/installer/open-tickets/2026-07-05--cc-mini--shared-library-split-brain-boot-deploy.md`
- Master ticket Phase 6: `ai/product/bugs/installer/ldmos-bugs-masterticket--installer.md`
