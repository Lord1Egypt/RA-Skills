---
name: core-tooling
description: ESLint, TypeScript, .gitignore, and .vscode in the monorepo
---

# Tooling Configuration

## ESLint

Root **eslint.config.js** uses **@antfu/eslint-config** with library and pnpm presets:

```js
// eslint.config.js
// @ts-check
import antfu from '@antfu/eslint-config'

export default antfu(
  {
    type: 'lib',
    pnpm: true,
  },
)
```

- **type: 'lib'** — Rules tuned for library code (not an app).
- **pnpm: true** — pnpm-aware resolution and workspace support; lint applies to the whole repo.

Run from root: `pnpm run lint` (or `nr lint`).

## TypeScript (Root tsconfig.json)

The root **tsconfig.json** is shared for type-checking and editor support. Packages can extend it or use their own; the starter uses a single root config with **noEmit** (tsdown emits build output):

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["ESNext"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "strict": true,
    "strictNullChecks": true,
    "noEmit": true,
    "esModuleInterop": true,
    "verbatimModuleSyntax": true,
    "skipDefaultLibCheck": true,
    "skipLibCheck": true
  }
}
```

| Option | Purpose |
|--------|--------|
| **noEmit** | No JS from tsc; tsdown emits. |
| **moduleResolution: "Bundler"** | Matches tsdown/bundler resolution. |
| **verbatimModuleSyntax** | Enforces explicit `type` imports. |

Run typecheck: `pnpm run typecheck` (runs `pnpm -r run typecheck` in each package).

## .gitignore

Typical ignores at repo root:

```
.cache
.DS_Store
.idea
*.log
*.tgz
coverage
dist
lib-cov
logs
node_modules
temp
```

- **dist** — Build output; each package’s `dist/` is gitignored.
- **node_modules** — Dependencies; pnpm installs at root and links into packages.
- **coverage** — Vitest coverage output.

## .vscode (Optional)

Recommended extensions and settings for consistent editing across the monorepo.

**extensions.json:**

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "antfu.pnpm-catalog-lens"
  ]
}
```

- **ESLint** — Lint and fix on save.
- **pnpm Catalog Lens** — View and edit catalog versions in `pnpm-workspace.yaml`.

**settings.json:**

- Disable Prettier; use ESLint for formatting and fix on save.
- **editor.codeActionsOnSave:** `source.fixAll.eslint: "explicit"`, `source.organizeImports: "never"`.
- **eslint.rules.customizations:** Turn off stylistic rule severity in the IDE (e.g. style/*, *-indent, *-spacing, *-quotes, *-semi) so the editor doesn’t show noise; ESLint still auto-fixes on save.
- **eslint.validate:** Enable for javascript, typescript, vue, json, jsonc, yaml, markdown, html.

This keeps formatting and linting consistent with the repo’s ESLint config.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
-->
