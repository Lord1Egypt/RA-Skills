---
name: core-testing
description: Vitest setup — root config, projects (root + packages/*)
---

# Testing (Vitest)

## Root vitest.config.ts

Tests are run from the root with a single Vitest config that defines **projects**:

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    projects: [
      {
        test: {
          name: 'root',
          include: ['test/**/*.test.ts'],
        },
      },
      'packages/*',
    ],
  },
})
```

- **root project** — Runs `test/**/*.test.ts` at repo root (e.g. cross-package imports).
- **packages/*** — Each directory under `packages/` can have its own vitest config or inherit root; Vitest runs tests per package.

So one command from root (`pnpm run test` / `vitest`) runs both root-level and package-level tests.

## Root-Level Tests

Root `test/` can import workspace packages (if they are in root `devDependencies` as `workspace:*`):

```ts
import { hello, two } from '@pkg-placeholder/core'
import { capitalize } from '@pkg-placeholder/utils'
import { describe, expect, it } from 'vitest'

describe('root-level', () => {
  it('can import and use core', () => {
    expect(hello).toBe('Hello world')
    expect(two).toBe(2)
  })
  it('can import and use utils', () => {
    expect(capitalize('hello')).toBe('Hello')
  })
})
```

This verifies that workspace resolution and exports work and that packages integrate correctly.

## Per-Package Tests

Each package can have `packages/<name>/test/*.test.ts`. With `projects: ['packages/*']`, Vitest will run those when the project config is picked up (either from a local `vitest.config.ts` in the package or from the root config’s project glob).

Use the same patterns as arch-tsdown: `describe`/`it`/`expect`, and optionally vitest-package-exports or tinyexec for testing built output.

## Running Tests

- **All:** From root, `pnpm run test` or `vitest`.
- **Filter by name:** `vitest --project root` or run from a specific package directory if your setup supports it.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://vitest.dev/
-->
