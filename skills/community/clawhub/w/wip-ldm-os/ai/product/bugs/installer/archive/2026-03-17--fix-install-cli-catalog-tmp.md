# Plan: Fix ldm install ... CLIs, catalog, /tmp/ symlinks, help (#81, #82, #32)

**Issues:** https://github.com/wipcomputer/wip-ldm-os/issues/81, https://github.com/wipcomputer/wip-ldm-os/issues/82
**Status:** Implemented
**Date:** 2026-03-17

## Problems Found (Dogfood March 16-17)

| # | Problem | Root Cause |
|---|---------|-----------|
| 1 | Global CLIs not updated by `ldm install` | Update loop only scans registry, not global npm |
| 2 | Extensions with no catalog match skipped | No fallback to package.json repository.url |
| 3 | /tmp/ symlinks created on every install | installCLI() falls back to `npm install -g .` from /tmp/ clones |
| 4 | /tmp/ clones never cleaned up | No cleanup after installFromPath() |
| 5 | `ldm install --help` triggers real install | --help not handled |

## Fixes Applied

### Fix 1: CLI update loop (bin/ldm.js)
Added second pass after extension loop checking `state.cliBinaries` against catalog `cliMatches`. CLIs get `npm install -g @scope/pkg@version` directly.

### Fix 2: Catalog fallback (bin/ldm.js)
When catalogEntry is null, extracts repo from `extPkg.repository.url`. Also added `wip-branch-guard` to catalog.json registryMatches/cliMatches.

### Fix 3: /tmp/ symlink prevention (lib/deploy.mjs)
installCLI() now tries latest npm version before falling back to local install. Only uses `npm install -g .` when package isn't published at all.

### Fix 4: /tmp/ cleanup (bin/ldm.js)
After installFromPath() completes, /tmp/ clones are rm -rf'd.

### Fix 5: --help (bin/ldm.js)
Added help text handler before target parsing.

## Files Modified

- `bin/ldm.js`: Fixes 1, 2, 4, 5
- `lib/deploy.mjs`: Fix 3
- `catalog.json`: Added wip-branch-guard to registryMatches/cliMatches

## Verification

```bash
ldm install --help        # shows usage
ldm install --dry-run     # shows CLI updates
ldm install               # updates CLIs + extensions, no /tmp/ symlinks
ls /tmp/ldm-install-*     # should be empty after install
```
