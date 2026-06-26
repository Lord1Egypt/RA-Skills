---
name: hairy
description: Hairy's {Opinionated} preferences and best practices for web development
metadata:
  author: Hairyf
  version: "2026.1.28"
---

# Hairyf's Preferences

This skill covers Hairyf's preferred tooling, configurations, and best practices for web development. This skill is opinionated.

## Quick Summary

| Category | Preference |
|----------|------------|
| Package Manager | pnpm |
| Language | TypeScript (strict mode) |
| Module System | ESM (`"type": "module"`) |
| Linting & Formatting | @antfu/eslint-config (no Prettier) |
| Testing | Vitest |
| Git Hooks | simple-git-hooks + lint-staged |
| Documentation | VitePress (in `docs/`) |

---

## Global Preferences

High-level cross-cutting preferences that should be respected whenever possible:

### "specify" keyword

When a task is marked with **"specify"** (for example: "specify this repo according to hairy"):

- Treat it as a request to **inspect the current project** and **optimize it until it matches these preferences as much as reasonably possible**.
- Concretely, this should trigger:
  - Architecture detection and upgrade planning via `@skills/arch-upkeep` and the relevant `arch-*` skills.
  - Preference-aware stack choices (prefer unjs ecosystem via `@skills/unjs`).
  - Dependency freshness checks and upgrades via `@skills/taze`.
  - A final pass of `lint` + `typecheck` (and tests if present) before considering the "specify" task done.

### Prefer unjs ecosystem frameworks

- When choosing frameworks or runtimes (SSR, API, tooling, dev server, etc.), **prefer unjs ecosystem projects** first (for example Nuxt, Nitro, h3, unstorage, unplugin, unocss, ofetch, and other unjs-maintained tools).
- Only fall back to non-unjs options when there is a clear, justified reason (missing feature, ecosystem constraint, or legacy requirements).
- For concrete choices, recipes, and defaults, **delegate to `@skills/unjs`** and follow its recommendations.

### Architecture must map to `arch-*` skills

- A project’s architecture should always map to one of the canonical `arch-*` stacks (tsdown library, CLI, monorepo, unplugin, webext, vscode, etc.).
- When the current shape does not match any target cleanly, **treat it as an upgrade opportunity** and plan a migration instead of adding more ad‑hoc structure.
- Use **`@skills/arch-upkeep`** to:
  - Detect the current architecture.
  - Choose the best target `arch-*` skill(s).
  - Orchestrate an incremental migration to that architecture.

### Keep dependencies fresh with `taze`

- Dependencies should be kept **continuously fresh**, not only during big refactors.
- Prefer using **`taze`** (see `@skills/taze`) to:
  - Audit outdated dependencies.
  - Perform controlled upgrades (minor/patch regularly; majors with explicit review).
  - Align versions across a monorepo using pnpm workspaces and catalogs.
- Avoid hand-editing versions in `package.json` unless there is a specific reason not to follow `taze`’s suggestions.

### Always finish with lint + typecheck

- After implementing any non-trivial change (feature, refactor, config change, dependency upgrade, CI change, etc.), **always run lint and typecheck** before considering the task done.
- Standard scripts:
  - `nr lint` → ESLint via `@antfu/eslint-config`.
  - `nr typecheck` → TypeScript in strict mode (project-wide).
- For CI and Git hooks:
  - Ensure pre-commit hooks at least run `lint` on staged files.
  - Ensure GitHub Actions (or other CI) run both `lint` and `typecheck` on PRs and `main` pushes.

---

## Core Stack

### Package Manager (pnpm)

Use pnpm as the package manager.

For monorepo setups, use pnpm workspaces:

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
```


Use pnpm named catalogs in `pnpm-workspace.yaml` to manage dependency versions:

| Catalog | Purpose |
|---------|---------|
| `prod` | Production dependencies |
| `inlined` | Dependencies inlined by bundler |
| `dev` | Development tools (linter, bundler, testing, dev-server) |
| `frontend` | Frontend libraries bundled into frontend |

Catalog names are not limited to the above and can be adjusted based on needs. Avoid using default catalog.

#### @antfu/ni

Use `@antfu/ni` for unified package manager commands. It auto-detects the package manager (pnpm/npm/yarn/bun) based on lockfile.

| Command | Description |
|---------|-------------|
| `ni` | Install dependencies |
| `ni <pkg>` | Add dependency |
| `ni -D <pkg>` | Add dev dependency |
| `nr <script>` | Run script |
| `nu` | Upgrade dependencies |
| `nun <pkg>` | Uninstall dependency |
| `nci` | Clean install (like `pnpm i --frozen-lockfile`) |
| `nlx <pkg>` | Execute package (like `npx`) |

Install globally with `pnpm i -g @antfu/ni` if the commands are not found.

### TypeScript (Strict Mode)

Always use TypeScript with strict mode enabled.

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

### ESM (ECMAScript Modules)

Always work in ESM mode. Set `"type": "module"` in `package.json`.

---

## Code Quality

### ESLint (@antfu/eslint-config)

Use `@antfu/eslint-config` for both formatting and linting. This eliminates the need for Prettier.

Create `eslint.config.js` with `// @ts-check` comment:

```js
// @ts-check
import antfu from '@antfu/eslint-config'

export default antfu()
```

Add script to `package.json`:

```json
{
  "scripts": {
    "lint": "eslint ."
  }
}
```

When getting linting errors, try to fix them with `nr lint --fix`. Don't add `lint:fix` script.

### Git Hooks (simple-git-hooks + lint-staged)

Use `simple-git-hooks` with `lint-staged` for pre-commit linting:

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm i --frozen-lockfile --ignore-scripts --offline && npx lint-staged"
  },
  "lint-staged": {
    "*": "eslint --fix"
  },
  "scripts": {
    "prepare": "npx simple-git-hooks"
  }
}
```

### Unit Testing (Vitest)

Use Vitest for unit testing.

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

**Conventions:**

- Place test files next to source files: `foo.ts` → `foo.test.ts` (same directory)
- High-level tests go in `tests/` directory in each package
- Use `describe` and `it` API (not `test`)
- Use `expect` API for assertions
- Use `assert` only for TypeScript null assertions
- Use `toMatchSnapshot` for complex output assertions
- Use `toMatchFileSnapshot` with explicit file path and extension for language-specific output (exclude those files from linting)

---

## Project Setup

### Publishing (Library Projects)

For library projects, publish through GitHub Releases triggered by `bumpp`:

```json
{
  "scripts": {
    "release": "bumpp -r"
  }
}
```

### Documentation (VitePress)

Use VitePress for documentation. Place docs under `docs/` directory.

```
docs/
├── .vitepress/
│   └── config.ts
├── index.md
└── guide/
    └── getting-started.md
```

Add script to `package.json`:

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs"
  }
}
```

---

## References

### Global Preferences

| Topic | Description | Reference |
|-------|-------------|-----------|
| Prefer unjs ecosystem | Prefer unjs ecosystem frameworks and tooling; delegate to `@skills/unjs` | [core-unjs-preferences](references/core-unjs-preferences.md) |
| Architecture via arch-* | Map repo shape to canonical `arch-*` skills and upgrade via `arch-upkeep` | [core-arch-upkeep-routing](references/core-arch-upkeep-routing.md) |
| Fresh dependencies with taze | Keep dependencies continuously fresh using `taze` and controlled upgrades | [core-deps-taze](references/core-deps-taze.md) |
| Lint + typecheck as gate | Always finish with lint + typecheck locally and in CI | [core-lint-typecheck](references/core-lint-typecheck.md) |

### Project Setup

| Topic | Description | Reference |
|-------|-------------|-----------|
| @antfu/eslint-config | ESLint flat config for formatting and linting | [antfu-eslint-config](references/antfu-eslint-config.md) |
| VS Code Extensions | Recommended extensions for development | [vscode-extensions](references/vscode-extensions.md) |

### Development

| Topic | Description | Reference |
|-------|-------------|-----------|
| App Development | Preferences for Vue/Vite/Nuxt/UnoCSS web applications | [app-development](references/app-development.md) |
