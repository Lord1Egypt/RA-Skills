---
name: core-packages
description: Package layout, exports, and inter-package dependencies
---

# Package Layout and Exports

## Per-Package Structure

Each package under `packages/` follows the same shape:

```
packages/<name>/
├── src/
│   └── index.ts      # Entry; add more files as needed
├── test/             # Vitest tests (optional)
├── tsdown.config.ts  # tsdown config (entry, dts, exports, publint)
├── package.json      # name, exports, main/module/types, scripts
└── (optional) tsconfig.json
```

- **Entry:** Typically `src/index.ts`; tsdown builds it to `dist/index.mjs` and `dist/index.d.mts`.
- **Exports:** In development, point to source (`".": "./src/index.ts"`); at publish, use `publishConfig.exports` to point to `dist/`.

## package.json Pattern (Publishable Package)

```json
{
  "name": "@pkg-placeholder/core",
  "type": "module",
  "sideEffects": false,
  "exports": {
    ".": "./src/index.ts",
    "./package.json": "./package.json"
  },
  "main": "./dist/index.mjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.mts",
  "files": ["dist"],
  "scripts": {
    "build": "tsdown",
    "dev": "tsdown --watch",
    "prepublishOnly": "nr build",
    "test": "vitest",
    "typecheck": "tsc"
  },
  "publishConfig": {
    "exports": {
      ".": "./dist/index.mjs",
      "./package.json": "./package.json"
    }
  },
  "dependencies": {
    "@pkg-placeholder/utils": "workspace:*"
  }
}
```

- **exports** — Development: resolve from source for fast iteration and correct types.
- **publishConfig.exports** — Published package: consumers get `dist/index.mjs` and types from `dist/index.d.mts`.
- **files: ["dist"]** — Only `dist/` is shipped to npm.

## Inter-Package Dependencies

- **Core depends on utils:** In `packages/core/package.json`, add `"@pkg-placeholder/utils": "workspace:*"`.
- **Source imports:** In `packages/core/src/index.ts`, use the package name: `import { capitalize } from '@pkg-placeholder/utils'`. TypeScript and tsdown resolve via workspace + exports.
- **Root tests:** Root `test/` can import `@pkg-placeholder/core` and `@pkg-placeholder/utils` if they are in root `devDependencies` as `workspace:*`, so you can test cross-package behavior without building.

## Adding a New Package

1. Create `packages/<name>/` with `src/index.ts`, `tsdown.config.ts`, `package.json` (same pattern as `core` or `utils`).
2. Add `"@scope/name": "workspace:*"` to any other package or root that needs it.
3. Use `catalog:cli` / `catalog:testing` etc. in the new package’s `devDependencies` for consistent versions.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
-->
