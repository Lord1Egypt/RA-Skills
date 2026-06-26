# ldm install: ensure 1Password SA token is in shell profile

## Summary

`ldm install` now appends a block to the user's shell profile (`~/.zprofile` or `~/.zshrc` for zsh, `~/.bash_profile` or `~/.profile` for bash) that exports `OP_SERVICE_ACCOUNT_TOKEN` from `~/.openclaw/secrets/op-sa-token`. Idempotent via a marker comment. Dry-run honored.

This unblocks Claude Code sessions, MCP servers, cron jobs, and launch agents from reading 1Password secrets on demand via `op`, without a biometric popup.

## What changed

### `bin/ldm.js`

- New function `ensureShellProfileSaToken()` at module level: detects the user's shell, picks the right profile candidate, checks for an idempotency marker, and appends a safe bash block that conditionally exports the SA token only if the token file exists.
- Call site added to `cmdInstallCatalog()` just after the inbox-rewake hook sync and before the git pre-commit hook deploy. Runs on every `ldm install`.
- Appended block:
  ```sh
  # LDM OS: 1Password SA token (for headless op CLI lookups)
  if [ -f "$HOME/.openclaw/secrets/op-sa-token" ]; then
    export OP_SERVICE_ACCOUNT_TOKEN="$(cat "$HOME/.openclaw/secrets/op-sa-token")"
  fi
  ```
- User-facing log on first write: `+ Shell profile updated: appended OP_SERVICE_ACCOUNT_TOKEN export to ~/.zprofile` (or similar) plus a reminder to source it or open a new terminal.

## Why this was needed

The op-secrets plugin injects `OP_SERVICE_ACCOUNT_TOKEN` into the OpenClaw gateway process env at gateway startup. Any process inheriting from the gateway sees it. Claude Code sessions, their hooks, MCP servers, and launch agents do NOT inherit from the gateway ... they inherit from the shell that launched them. So they never saw the token.

That silent gap showed up as "OpenAI API key required" errors in the memory-crystal Stop hook on 2026-04-15 when Parker stopped the OpenClaw gateway. The hook's internal 1Password fallback (`getOpSecret`) tries to use `op` but needs the SA token to authenticate; without it, `op` tries a biometric popup (impossible in a non-interactive hook) and the lookup fails.

Putting the SA token in the shell profile closes the gap. Every future terminal, every CC session, every hook, every MCP server inherits it. Actual API keys (OpenAI, XAI, Anthropic, etc.) stay in 1Password and are fetched per-process per-lookup, which is the intended pattern.

Only the SA token lives in env ... the key that unlocks other keys. This is the sanctioned pattern per the OpenClaw CLAUDE.md rules ("Always use SA token, never call op bare").

## Companion fix

The memory-crystal Stop hook now also fails fast on permanent errors (shipped in `@wipcomputer/memory-crystal@0.7.34-alpha.5`). After this release AND that one install, a CC session with no available key exits the hook in under 200ms with one clean log line instead of hanging for 37s on guaranteed-failing retries.

Both fixes together restore the "capture just works" contract when keys ARE available, and fail gracefully when they're not.

## Verification steps

1. Run `ldm install` ... expect `+ Shell profile updated:` log on first run and no message on subsequent runs.
2. Open a new terminal. `echo $OP_SERVICE_ACCOUNT_TOKEN | head -c 20` should print a token prefix.
3. `op item get "OpenAI API" --vault "Agent Secrets" --fields "api key"` should return the key without a biometric popup.
4. Start a CC session, complete a turn. Stop hook should log `[cc-memory-capture] N chunks (M tokens)` cleanly instead of `[retry 2] [retry 3] Ended for 37s`.

## Backwards compatibility

- Idempotent: marker comment checked before append, no duplication.
- Safe: appended block checks `[ -f ... ]` before exporting, so missing SA token file doesn't break the shell.
- Cross-shell: zsh and bash both handled.
- Dry-run: honored, does not modify the file.

## Related

- Bug ticket: `ai/product/bugs/memory-crystal/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md`
- Companion PR: `wipcomputer/memory-crystal-private#115` (shipped as `@wipcomputer/memory-crystal@0.7.34-alpha.5`)
