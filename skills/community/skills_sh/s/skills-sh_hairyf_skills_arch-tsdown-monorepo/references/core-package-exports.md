---
name: core-package-exports
description: package.json exports, dev vs publish, main/module/types, files, sideEffects
---

# Package Exports and Publish Layout

Each publishable package uses a **dual exports** pattern: development points to source, published package points to built output.

## Dual Exports Pattern

**During development** (in the monorepo), `exports` and `main`/`module`/`types` can point to **source** so that edits are reflected without rebuilding and types come from `.ts`:

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./package.json": "./package.json"
  },
  "main": "./dist/index.mjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.mts"
}
```

**When published**, override with **publishConfig** so consumers get built files:

```json
{
  "publishConfig": {
    "exports": {
      ".": "./dist/index.mjs",
      "./package.json": "./package.json"
    }
  }
}
```

- **tsdown** with `exports.devExports: true` can keep dev pointing to `src/` while build produces `dist/`.
- **publishConfig.exports** — What npm publishes; must point to `dist/` for ESM and (if applicable) types.

## main, module, types

| Field | Purpose |
|-------|--------|
| **main** | Fallback for Node/consumers; point to `dist/index.mjs`. |
| **module** | ESM entry; same as main in ESM-only setup. |
| **types** | TypeScript entry; e.g. `dist/index.d.mts`. |

Older tools may use `main`/`module`; modern resolution uses `exports`. Keeping both avoids breakage.

## files and sideEffects

```json
{
  "files": ["dist"],
  "sideEffects": false
}
```

- **files** — Only `dist/` is included in the published tarball; source and tests are not.
- **sideEffects: false** — Enables tree-shaking; no side effects at import time.

## Adding Subpath Exports

When you add entries in **tsdown.config.ts** (e.g. `cli: 'src/cli.ts'`), add matching export conditions:

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./cli": "./src/cli.ts",
    "./package.json": "./package.json"
  },
  "publishConfig": {
    "exports": {
      ".": "./dist/index.mjs",
      "./cli": "./dist/cli.mjs",
      "./package.json": "./package.json"
    }
  }
}
```

Use **publint** (via tsdown’s `publint: true`) to catch export/type issues before publish.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://github.com/rolldown/tsdown
-->
