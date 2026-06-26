---
name: core-scripts
description: Root and package scripts — build, dev, typecheck, test, release
---

# Scripts (Root and Packages)

## Root package.json Scripts

The root is `private: true` and orchestrates the workspace:

| Script | Command | Purpose |
|--------|---------|---------|
| **build** | `pnpm -r run build` | Run `build` in every workspace package (each runs `tsdown`). |
| **dev** | `pnpm -r run dev` | Run `dev` (tsdown --watch) in every package. |
| **lint** | `eslint .` | Lint the whole repo. |
| **typecheck** | `pnpm -r run typecheck` | Run `typecheck` (tsc) in every package. |
| **test** | `vitest` | Run Vitest; root config uses projects (root tests + packages/*). |
| **release** | `bumpp` | Bump version and create tag (e.g. v*) for CI to publish. |
| **prepare** | `simple-git-hooks` | Install git hooks (e.g. pre-commit). |

- **pnpm -r** — “recursive” run in all workspace packages that define the script.
- **vitest** — Single command; `vitest.config.ts` defines multiple projects (root + each package).

## Per-Package Scripts

Each package typically has:

| Script | Command | Purpose |
|--------|---------|---------|
| **build** | `tsdown` | Build to `dist/`. |
| **dev** | `tsdown --watch` | Watch and rebuild. |
| **typecheck** | `tsc` | Type-check only (noEmit). |
| **test** | `vitest` | Run that package’s tests (when using root vitest projects). |
| **prepublishOnly** | `nr build` | Build before publish. |

Root does not run a single global build script for “one combined dist”; each package owns its own build and output.

## Running Scripts

- From root: `pnpm run build`, `pnpm run test`, etc.
- In one package: `pnpm --filter @pkg-placeholder/core run build`, or `cd packages/core && pnpm run build`.
- Short form with ni: `nr build`, `nr test` (from root).

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
-->
