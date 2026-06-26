---
name: advanced-limitations
description: pnpm limitations (npm lockfile, binstubs)
---

# Limitations

Known limitations when using pnpm.

## npm Lockfiles Ignored

`npm-shrinkwrap.json` and `package-lock.json` are **not** used by pnpm. npm can install the same `name@version` multiple times with different dependency sets; its lockfile reflects a flat `node_modules` layout. pnpm uses an isolated layout and its own lockfile format (`pnpm-lock.yaml`), so it cannot honor npm's lockfile. To migrate, use `pnpm import` to convert an existing lockfile to pnpm's format.

## Binstubs Are Shell Scripts

Files in `node_modules/.bin` are **shell scripts**, not symlinks to JS files. pnpm creates them so that pluggable CLIs can find their plugins in pnpm's non-flat `node_modules` structure. If you expect a binary to be a JS file, reference the actual script (e.g. `node node_modules/pkg/cli.js`) instead. See [pnpm#736](https://github.com/pnpm/pnpm/issues/736) for context.

## Key Points

- Do not rely on `package-lock.json` or `npm-shrinkwrap.json`; use `pnpm-lock.yaml`. Use `pnpm import` when converting.
- `.bin` executables are shell wrappers; use the real script path when you need a JS file.

<!--
Source references:
- https://pnpm.io/limitations
- sources/pnpm/docs/limitations.md
-->
