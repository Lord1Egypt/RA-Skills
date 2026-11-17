## Installer and boot reliability (P1 batch)

This release promotes the 0.4.85 alpha line to stable and folds in a batch of installer and boot-hook reliability fixes that were validated on the alpha track.

- **Single-owner boot-hook registration.** `lib/deploy.mjs` no longer appends a duplicate SessionStart boot-hook entry to `~/.claude/settings.json` on every manifest-driven `ldm install`. Boot-hook doors now route to the single canonical registrar (`configureSessionStartHook()`), which collapses duplicates, canonicalizes the command, and no-ops when already correct. This was the mechanism behind the 10-entry accumulation seen 2026-07-04.
- **One boot-hook deploy truth + doctor stale-at-exec check.** `syncBootHook()` now deploys to the location the registered SessionStart hook actually executes (`resolveBootExecDir()`) instead of a hardcoded path, so new code can no longer land where the running session never reads it. `ldm doctor` gains a "boot hook stale at execution path" check with `--fix` (timestamped backup before redeploy).
- **SessionStart dedupe + doctor settings repairs.** `configureSessionStartHook()` owns the full set of boot-hook entries, collapses duplicates, and persists in-place (the previous update path reported success without writing). `ldm doctor --fix` collapses duplicate hook entries and removes invalid `model` values (control-char detection only; printable bracketed 1M-context IDs like `claude-fable-5[1m]` are valid and pass untouched).
- **Boot-hook payload trim.** The SessionStart boot context now trims itself with per-step line caps, a staleness cutoff for most-recent journals, and a one-line payload summary. Defaults are active in code so existing installs benefit without config changes (~42% smaller on the measured 2026-07-04 fixture).
- **Bin ownership manifest + install-time self-heal + prepublish gate.** `~/.ldm/bin/` gains an explicit ownership model: declarers list files, install aborts on conflict before side effects, missing/non-executable files self-heal from their declared source, and a prepublish validator blocks broken declarations from reaching npm.
- **MCP install hardening (phases 3a-3d).** `registerMCP` verifies the entrypoint exists and parses before touching `~/.claude.json` (loud-stop instead of silent-wrong); stale MCP entries are unregistered on deploy; `ldm doctor` checks MCP paths under the extension roots; and `buildSourceInfo` no longer walks up into the parent git repo, so registry `source.repo` values stop capturing the LDM system repo.
- **Dev guide into the installer library.** The private WIP dev guide now has a versioned source template and deploys to `~/.ldm/library/documentation/` alongside the human library.
- **Universal Installer doc alignment.** SPEC, TECHNICAL, and README in `docs/universal-installer/` align on the eight canonical interfaces (adding Remote MCP and Claude Code Plugin) and the install-spec URL contract.

Tickets: `ai/product/bugs/installer/` Phase 6 of the master ticket. The `shared/` to `library/` machine migration remains tracked separately under the OS-level `2026-04-14 library-migration-plus-topology` ticket.

---

## Kaleidoscope, Chat UI, and hosted surface

Align the Universal Installer documentation and active WIP AI Chat UI tickets with the public npm package path. The skill source remains in the private WIP Inc repo, while LDM OS installs the public `@wipcomputer/wip-ai-chat-ui` tarball onto supported agent skill surfaces.

Also updates the installed WIP-specific development guide template so future `ldm install` runs preserve the current attribution model: Parker Todd Brooks, Lēsa, Claude Code on Opus 4.7, and Codex on GPT 5.5. This prevents the installer from restoring stale Claude Opus 4.6 or three-contributor co-author blocks.

The Kaleidoscope launch path now uses the updated onboarding copy, keeps returning-user copy separate from first-run account creation copy, and preserves the No thanks branch as a simple Kaleidoscope generation path without wallet receipt copy. The paid image-generation branch now demonstrates a one-cent wallet authorization against a ten-dollar starter balance, and in-chat passkey authorization rejects a different account before image generation or wallet deduction can run.

The hosted demo now resets existing demo wallet balances to the ten-dollar starter balance once during deployment, so returning smoke-test accounts show `$10.00` and the first authorized image receipt shows `Cost: $0.01. Balance: $9.99.` The paid and No thanks paths also share one approved outro sequence after image generation, keeping copy and styling aligned.

The demo wallet reset now covers the JSON fallback wallet registry as well as Prisma and normalizes `acct:` tenant IDs before Prisma wallet lookups. This prevents the login balance from showing the starter balance while image generation continues decrementing stale JSON wallet balances.

Returning users now get a shorter Kaleidoscope opening that skips first-run passkey setup copy and does not show the wallet balance before the choice prompt. The returning-user No thanks branch ends with Parker's shorter product outro without generating another image, while the returning-user Yes path keeps the existing authorization and generation mechanics and shows the same receipt before a returning-user-specific outro.

The hosted legal page footers now link only the `WIP Computer, Inc.` brand line back to `https://wip.computer/`, while keeping `Learning Dreaming Machines` and `Made in California.` as plain text.

The hosted legal pages now share the V05 WIP header treatment used by the public website: fixed 55px bar, animated Kaleidoscope sprite, `WORK IN PROGRESS` wordmark, and scroll-state translucency. The legal body copy and footer taxonomy remain unchanged.

Grouped hosted footers now include a same-tab `Visualizations` link under Tools that points to the Kaleidoscope live wall, without changing Local passkeys, agent links, login behavior, legal body copy, or live-wall data behavior.

The hosted login footer now matches the rest of the public site by linking only the `WIP Computer, Inc.` brand line to `https://wip.computer/`, while keeping `Learning Dreaming Machines` and `Made in California.` as plain text.

The hosted login footer brand link now uses the same non-underlined footer presentation as the public homepage.

Hosted login and legal shell brand links now match the public homepage rollover behavior for the WIP Computer brand treatment.

Kaleidoscope QR approval now keeps the requester and authenticator devices separate: the device that started External QR login still opens chat after approval, while the phone that scanned and approved the QR lands on a Kaleidoscope confirmation screen until the user explicitly opens Kaleidoscope there.

Refs #1029.
Refs #1037.
Refs #1060.
