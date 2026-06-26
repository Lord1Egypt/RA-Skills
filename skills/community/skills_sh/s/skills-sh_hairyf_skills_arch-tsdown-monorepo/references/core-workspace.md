---
name: core-workspace
description: pnpm workspace, catalogs, and workspace dependencies
---

# pnpm Workspace and Catalogs

## Workspace Layout

In `pnpm-workspace.yaml`:

```yaml
catalogMode: prefer
ignoreWorkspaceRootCheck: true
shellEmulator: true
trustPolicy: no-downgrade

packages:
  - packages/*

catalogs:
  cli:
    '@antfu/eslint-config': ^7.2.0
    bumpp: ^10.3.2
    eslint: ^9.39.2
    tsdown: ^0.17.3
    typescript: ^5.9.3
    vite: ^7.2.7
    # ...
  testing:
    vitest: ^4.0.15
    vitest-package-exports: ^0.1.1
    # ...
  inlined:
    '@antfu/utils': ^9.3.0
  types:
    '@types/node': ^25.0.1
```

- **packages:** `packages/*` — every directory under `packages/` is a workspace package.
- **catalogMode: prefer** — use catalog versions when resolving; packages reference them with `catalog:cli`, `catalog:testing`, etc.
- **ignoreWorkspaceRootCheck:** allows root to have devDependencies without a `package.json` “name” that would be published.

## Using Catalogs in Packages

In root or package `package.json`:

```json
{
  "devDependencies": {
    "tsdown": "catalog:cli",
    "vitest": "catalog:testing",
    "@types/node": "catalog:types",
    "@antfu/utils": "catalog:inlined"
  }
}
```

- **catalog:cli** — build/lint/tooling (tsdown, eslint, typescript, etc.)
- **catalog:testing** — vitest, vitest-package-exports, tinyexec, yaml
- **catalog:types** — `@types/node`
- **catalog:inlined** — inlined runtime-ish deps used by tooling (e.g. @antfu/utils)

Centralizing versions in catalogs keeps all packages on the same tool versions and simplifies upgrades.

## Workspace Dependencies

Packages depend on each other with `workspace:*`:

```json
{
  "name": "@pkg-placeholder/core",
  "dependencies": {
    "@pkg-placeholder/utils": "workspace:*"
  }
}
```

Root can depend on workspace packages for tests or tooling:

```json
{
  "devDependencies": {
    "@pkg-placeholder/core": "workspace:*",
    "@pkg-placeholder/utils": "workspace:*"
  }
}
```

- **workspace:*** — always use the current workspace version; pnpm resolves it to the local package.
- At publish time, `workspace:*` is replaced with a concrete version (e.g. same as the published package version).

## onlyBuiltDependencies

Optional in `pnpm-workspace.yaml`:

```yaml
onlyBuiltDependencies:
  - esbuild
  - simple-git-hooks
```

Limits which dependencies are built in the workspace; keeps installs fast and deterministic.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://pnpm.io/workspaces
- https://pnpm.io/catalogs
-->
