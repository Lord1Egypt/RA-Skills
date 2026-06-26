---
name: core-tsdown-per-package
description: tsdown config per package — entry, dts, exports, publint
---

# tsdown Config (Per Package)

Each package has its own `tsdown.config.ts` at the package root (e.g. `packages/core/tsdown.config.ts`). The pattern matches arch-tsdown.

## Example

```ts
import { defineConfig } from 'tsdown'

export default defineConfig({
  entry: ['src/index.ts'],
  dts: true,
  exports: {
    devExports: true,
    enabled: true,
  },
  publint: true,
})
```

## Options

| Option | Purpose |
|--------|--------|
| **entry** | Source entry file(s); output goes to `dist/` (e.g. `dist/index.mjs`). |
| **dts** | Emit `.d.mts` (or equivalent) for types. |
| **exports.enabled** | tsdown can generate/validate `package.json` exports from config. |
| **exports.devExports** | In dev, exports point to source (e.g. `./src/index.ts`) when used with package.json that has both dev and publishConfig exports. |
| **publint** | Run publint as part of build to catch publish-time issues. |

## Multiple Entries

To ship multiple entrypoints (e.g. subpaths):

```ts
export default defineConfig({
  entry: {
    index: 'src/index.ts',
    cli: 'src/cli.ts',
  },
  dts: true,
  exports: { devExports: true, enabled: true },
  publint: true,
})
```

Then in `package.json` exports, add corresponding conditions for `./cli` etc., or rely on tsdown’s export generation if enabled.

## Running Build

- **Single package:** `cd packages/core && pnpm run build` (or `nr build`).
- **All packages:** From repo root, `pnpm run build` (runs `pnpm -r run build`), which builds every workspace package that has a `build` script.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://github.com/rolldown/tsdown
-->
