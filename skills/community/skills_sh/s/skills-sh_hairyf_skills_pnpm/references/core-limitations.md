---
name: pnpm-limitations
description: Known limitations and edge cases when using pnpm
---

# pnpm Limitations

## npm Lockfile Ignored

pnpm ignores `npm-shrinkwrap.json` and `package-lock.json`. npm can install the same `name@version` multiple times with different dependency sets; its lockfile reflects a flat layout. pnpm uses an isolated layout and cannot use npm's lockfile format.

**Fix:** Use `pnpm import` to convert an existing lockfile to pnpm format.

## Binstubs Are Shell Files

Files in `node_modules/.bin` are shell wrappers, not symlinks to JS. This helps pluggable CLIs find plugins in pnpm's structure. Rarely an issue—if you need the original JS file, reference it directly.

## Symlink-Unfriendly Environments

Some tools don't work with symlinks (React Native, serverless, AWS Lambda). Use `node-linker=hoisted` in `.npmrc` for a flat `node_modules`.

## Windows Long Paths

On Windows, long paths can cause issues. Set `virtualStoreDirMaxLength` lower or use `virtualStoreDir` at a shorter path (e.g. `C:\pnpm-store`).

<!--
Source references:
- https://pnpm.io/limitations
-->
