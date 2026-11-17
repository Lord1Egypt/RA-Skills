Manifest-driven `ldm install` no longer appends a duplicate SessionStart boot-hook entry to `~/.claude/settings.json`. The boot hook now has a single registrar.

`lib/deploy.mjs` `installClaudeCodeHookEvent()` matched existing hook entries by an extension-dir tag (`/<toolName>/` in the command). The boot hook's deployed command is `node ~/.ldm/shared/boot/boot-hook.mjs`, which contains no `/wip-ldm-os/` segment, so the ownership check never recognized the existing entry and appended a fresh one on every manifest-driven install. This was the mechanism behind the ongoing accumulation (10 entries found 2026-07-04, then re-growing 3 -> 4 -> 5 through the day as installs ran); PR #1086 fixed only the `src/boot/installer.mjs` registration path, not this one.

The fix routes boot-hook doors (SessionStart with a command referencing `boot-hook` / `shared/boot`) to `configureSessionStartHook()` in `src/boot/installer.mjs`, the single canonical registrar shipped in PR #1086: it owns the whole boot-hook set, collapses duplicates to one, canonicalizes the command to `BOOT_DIR`, persists, and no-ops when already correct. The deploy path is now one writer, not two. Discrimination is on the command, not the event, so other SessionStart hooks (for example wip-branch-guard's) stay on the normal extension-dir path untouched.

Regression coverage: `scripts/test-deploy-hook-ownership.mjs` (fresh install adds one entry; repeat install is byte-identical; pre-accumulated entries collapse while an unrelated SessionStart hook is preserved; dry run writes nothing).

Ticket:
- `ai/product/bugs/installer/open-tickets/2026-07-05--cc-mini--deploy-hook-ownership-misses-boot-hook.md`
- Master ticket Phase 6: `ai/product/bugs/installer/ldmos-bugs-masterticket--installer.md`
