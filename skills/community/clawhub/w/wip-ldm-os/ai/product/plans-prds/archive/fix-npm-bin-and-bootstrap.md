# Plan: Fix npm bin entries + enable LDM OS bootstrap

**Date:** 2026-03-13
**Issue:** #32
**Status:** Ready

## Problem

`npm publish` strips all four bin entries from `@wipcomputer/wip-ldm-os`:
```
npm warn publish "bin[ldm]" script name bin/ldm.mjs was invalid and removed
npm warn publish "bin[wip-ldm-os]" script name bin/ldm.mjs was invalid and removed
npm warn publish "bin[ldm-scaffold]" script name bin/scaffold.sh was invalid and removed
npm warn publish "bin[ldm-boot-install]" script name src/boot/install-cli.mjs was invalid and removed
```

This means `npm install -g @wipcomputer/wip-ldm-os` doesn't create the `ldm` command. This blocks the entire "silent bootstrap" feature where Memory Crystal and DevOps Toolbox auto-install LDM OS.

## Why this matters

Memory Crystal and DevOps Toolbox both want to run `npm install -g @wipcomputer/wip-ldm-os` when `ldm` isn't on PATH. If that doesn't create a working `ldm` binary, the bootstrap fails and the user gets the old "tip" behavior.

## Investigation

1. Run `npm pack --dry-run` to check tarball contents
2. Run `npm pkg fix` to see what npm wants changed
3. Check if `.mjs` extension is the issue (npm may reject `.mjs` as bin scripts)
4. Check shebangs: `#!/usr/bin/env node` on .mjs files, `#!/usr/bin/env bash` on .sh
5. Check if `"type": "module"` in package.json conflicts with bin resolution
6. Test with minimal package.json to isolate

## Likely fix

Rename bin files from `.mjs` to `.js`. With `"type": "module"` in package.json, `.js` files are already treated as ESM. The `.mjs` extension may trigger npm's "invalid script name" validation.

Alternative: add thin `.js` wrappers that import the `.mjs` files.

## Files

- `package.json` ... fix bin entries
- `bin/ldm.mjs` ... rename to `bin/ldm.js` (or add wrapper)
- `bin/scaffold.sh` ... verify shebang
- `src/boot/install-cli.mjs` ... rename or add wrapper

## Verify

```bash
npm pack --dry-run           # bin entries in tarball
npm install -g .             # ldm command created
ldm --version                # responds
which ldm                    # correct location
npm publish --dry-run        # no bin stripping warnings
```

## Release

- Branch: `cc-mini/fix-npm-bin`
- PR to main, merge
- `wip-release patch --notes="Fix npm bin entries stripped during publish"`
- Deploy to public via `deploy-public.sh`

## Depends on

Nothing. This is the blocker for Plans 2 and 3.

## Unblocks

- memory-crystal-private: silent LDM OS bootstrap in `crystal init`
- wip-ai-devops-toolbox-private: silent LDM OS bootstrap in `wip-install`
