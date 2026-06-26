---
name: responses-third-party-prompt-cache-patch
description: Patch an installed OpenClaw dist bundle so third-party OpenAI-compatible Responses endpoints keep prompt_cache_key and prompt_cache_retention instead of having them stripped. Use when the user wants a local patch on a machine running OpenClaw, not an upstream refactor or config change, and needs a workflow with dry-run, backup, rollback, syntax validation, and upgrade-aware reapply.
---

# Responses Third Party Prompt Cache Patch

Patch the installed OpenClaw dist bundle so `shouldStripResponsesPromptCache(model)` stops deleting `prompt_cache_key` and `prompt_cache_retention` for third-party OpenAI-compatible Responses endpoints.

Source: https://github.com/tsunheimat/openclaw-responses-prompt-cache-patch

## Quick install for OpenClaw

```bash
clawhub install responses-third-party-prompt-cache-patch --workdir ~/.openclaw/workspace
```

## Risks

- Write directly into the OpenClaw installation directory under `dist/`.
- Require Python 3 and Node.js on the target machine.
- Need a gateway restart after apply or rollback for the change to take effect.

## Quick start

Run from this skill directory:

```bash
python3 scripts/patch_prompt_cache.py --dry-run
python3 scripts/patch_prompt_cache.py
openclaw gateway restart
```

## Roll back

```bash
python3 scripts/revert_prompt_cache.py
openclaw gateway restart
```

## Target selection

- Default to the currently installed OpenClaw root by resolving the `openclaw` executable.
- Accept `--root /path/to/openclaw` to patch a copied fixture or a different installation.
- Scan `dist/pi-embedded-*.js` first, then fall back to other `dist/*.js` bundles only if the target function moved.

## What the scripts do

### `scripts/patch_prompt_cache.py`

- Support `--dry-run`
- Create timestamped backups before writing
- Apply a narrow patch only inside `shouldStripResponsesPromptCache(model)`
- Run `node --check` after writing
- Auto-restore the fresh backup if syntax validation fails
- Detect already-patched bundles and upgrade-style reapply situations

### `scripts/revert_prompt_cache.py`

- Restore the latest matching backup for each currently patched bundle
- Support `--dry-run`
- Validate restored files with `node --check`

## Recommended verification flow

1. Run `--dry-run` on the real installation.
2. Copy the target bundle into a fixture and run `--root <fixture>` for real apply testing.
3. Run apply again to confirm idempotency.
4. Run rollback on the same fixture.
