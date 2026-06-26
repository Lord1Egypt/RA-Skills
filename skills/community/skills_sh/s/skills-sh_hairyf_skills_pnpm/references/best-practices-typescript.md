---
name: best-practices-typescript
description: TypeScript with pnpm (preserveSymlinks, workspace types, packageExtensions)
---

# TypeScript with pnpm

pnpm works with TypeScript out of the box. A few settings avoid common issues.

## preserveSymlinks

Do **not** set TypeScript `preserveSymlinks` to `true`. TypeScript will not resolve types correctly in pnpm's symlinked `node_modules`. If you must preserve symlinks, set pnpm's `nodeLinker` to `hoisted` in `.npmrc` or `pnpm-workspace.yaml`.

## Workspace @types Conflicts

Different workspace packages can pull in different versions of `@types/*`. If a dependency (e.g. `antd`) relies on `@types/react` without listing it in peerDependencies, you may see type errors when multiple `@types/react` versions exist.

**Fix 1 – packageExtensions** (in `pnpm-workspace.yaml`):

```yaml
packageExtensions:
  antd:
    peerDependencies:
      '@types/react': '*'
```

**Fix 2 – config dependency**:

```bash
pnpm add @pnpm/plugin-types-fixer --config
```

The plugin fixes common type resolution issues in workspaces.

## Key Points

- Keep `preserveSymlinks` false (or use `nodeLinker: hoisted` if you need symlink preservation).
- Use `packageExtensions` to add missing peer deps (e.g. `@types/react`) for packages that don't declare them.
- `@pnpm/plugin-types-fixer` can automate type fixes across the workspace.

<!--
Source references:
- https://pnpm.io/typescript
- sources/pnpm/docs/typescript.md
-->
