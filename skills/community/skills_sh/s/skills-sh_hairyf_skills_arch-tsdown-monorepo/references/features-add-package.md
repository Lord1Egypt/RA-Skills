---
name: features-add-package
description: Step-by-step adding a new workspace package to the monorepo
---

# Adding a New Package

Follow these steps to add a new publishable or internal package to the monorepo.

## 1. Create Directory and Entry

Create the package root and entry file:

```
packages/<name>/
├── src/
│   └── index.ts
```

Implement the entry (e.g. export functions or types). Use **catalog:** and **workspace:*** in dependencies (see below).

## 2. package.json

Create **packages/<name>/package.json** with the same pattern as existing packages:

```json
{
  "name": "@scope/<name>",
  "type": "module",
  "version": "0.0.0",
  "description": "...",
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
  "dependencies": {},
  "devDependencies": {
    "tsdown": "catalog:cli",
    "typescript": "catalog:cli",
    "vitest": "catalog:testing",
    "@types/node": "catalog:types"
  }
}
```

- Use **catalog:cli**, **catalog:testing**, **catalog:types** for shared versions.
- Add **"@scope/other": "workspace:*"** under `dependencies` if this package depends on another workspace package.
- Omit **publishConfig** and set **"private": true** if the package is internal-only.

## 3. tsdown.config.ts

Create **packages/<name>/tsdown.config.ts**:

```ts
import { defineConfig } from 'tsdown'

export default defineConfig({
  entry: ['src/index.ts'],
  dts: true,
  exports: { devExports: true, enabled: true },
  publint: true,
})
```

Add more entries or subpaths as needed; keep **exports** and **publint** for consistency.

## 4. Tests (Optional)

Create **packages/<name>/test/index.test.ts** and add Vitest tests. The root **vitest.config.ts** uses `projects: ['packages/*']`, so tests under **packages/<name>/test/** are picked up automatically (no per-package vitest.config required unless you need package-specific options).

## 5. Wire Dependencies

- **Other packages depending on this one:** In their `package.json`, add `"@scope/<name>": "workspace:*"` under `dependencies` or `devDependencies`.
- **Root depending on this package:** In root `package.json` `devDependencies`, add `"@scope/<name>": "workspace:*"` if you want root-level tests or scripts to use it.

## 6. Verify

From repo root:

- `pnpm install` — Install and link workspace packages.
- `pnpm run build` — Build all packages (including the new one).
- `pnpm run typecheck` — Type-check all packages.
- `pnpm run test` — Run tests (root + all packages).

No change to **pnpm-workspace.yaml** is needed; `packages/*` already includes any new directory under **packages/**.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
-->
