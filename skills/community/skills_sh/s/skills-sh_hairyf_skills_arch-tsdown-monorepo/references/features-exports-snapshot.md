---
name: features-exports-snapshot
description: Export snapshot tests per package with vitest-package-exports, tinyexec, runIf(IS_READY)
---

# Exports Snapshot Testing

The starter can include an **exports snapshot** test that asserts each package’s export manifest (e.g. to catch accidental export changes before release). It uses **vitest-package-exports**, **tinyexec**, and **yaml** and can live in a single package (e.g. `packages/core/test/exports.test.ts`) or at root.

## Pattern (Monorepo)

List workspace packages with `pnpm ls --only-projects -r --json`, then for each non-private package call **getPackageExportsManifest** and snapshot the result:

```ts
import { x } from 'tinyexec'
import { describe, expect, it } from 'vitest'
import { getPackageExportsManifest } from 'vitest-package-exports'
import yaml from 'yaml'

const IS_READY = false

describe.runIf(IS_READY)('exports-snapshot', async () => {
  const packages: { name: string, path: string, private?: boolean }[] = JSON.parse(
    await x('pnpm', ['ls', '--only-projects', '-r', '--json']).then(r => r.stdout),
  )

  for (const pkg of packages) {
    if (pkg.private) continue
    it(`${pkg.name}`, async () => {
      const manifest = await getPackageExportsManifest({
        importMode: 'src',
        cwd: pkg.path,
      })
      await expect(yaml.stringify(manifest.exports))
        .toMatchFileSnapshot(`./exports/${pkg.name}.yaml`)
    })
  }
})
```

## Options

| Piece | Purpose |
|--------|--------|
| **describe.runIf(IS_READY)** | Set `IS_READY = true` when you want to enable export snapshots (e.g. before first release); otherwise the test is skipped. |
| **pnpm ls --only-projects -r --json** | List all workspace project roots (name, path, private). |
| **getPackageExportsManifest({ importMode, cwd })** | Build manifest of package exports; **cwd** is the package root (e.g. `pkg.path`). |
| **importMode: 'src'** | Resolve from source; use another mode to assert on built `dist/` output. |
| **toMatchFileSnapshot(`./exports/${pkg.name}.yaml`)** | First run creates `test/exports/<pkg.name>.yaml`; later runs diff against it. |

## Snapshot Location

- If the test lives in **packages/core/test/exports.test.ts**, snapshots go under **packages/core/test/exports/** (e.g. `packages/core/test/exports/@pkg-placeholder-core.yaml`).
- Use a consistent path so CI and local runs match; add **test/exports/** to git and commit snapshot files when you enable the test.

## When to Use

- Enable (**IS_READY = true**) when you want to lock the public export surface and catch unintended changes.
- Keep disabled until the first release so initial snapshot creation is intentional.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://github.com/vitest-dev/vitest-package-exports
-->
