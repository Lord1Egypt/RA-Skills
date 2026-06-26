---
name: core-lint-typecheck
description: Always finish meaningful work with lint and typecheck locally and in CI.
---

# Always Finish with Lint + Typecheck

Linting and typechecking are mandatory gates for any non-trivial change, both locally and in continuous integration.

## Usage

### 1. Standard scripts

- Ensure these scripts exist (usually at repo root, and per package where appropriate):

```json
{
  "scripts": {
    "lint": "eslint .",
    "typecheck": "tsc -p ."
  }
}
```

- In hairy’s ecosystem:
  - `nr lint` → ESLint via `@antfu/eslint-config`.
  - `nr typecheck` → TypeScript in strict mode, project-wide.

### 2. Local workflow

- After any non-trivial change:
  - Run `nr lint`.
  - Run `nr typecheck`.
  - Run tests (if present).
- Do not consider the task "done" until all three pass.

### 3. Git hooks

- Use `simple-git-hooks` + `lint-staged` (see the main `hairy` skill) to enforce at least linting on staged files:
  - Pre-commit should run `lint-staged` with ESLint.
  - Optionally, run a fast `tsc --noEmit` or `nr typecheck` for small repos.

### 4. CI pipelines

- In GitHub Actions (or other CI), ensure:
  - Every PR and `main` push runs:
    - `nr lint`
    - `nr typecheck`
    - tests (e.g. `nr test`)
  - Failing lint/typecheck should block merges.

## Key Points

- Lint and typecheck are **gates**, not optional checks.
- Any automation (PR bots, release workflows) should assume lint/typecheck are green.
- Skipping these steps is only acceptable for extremely trivial changes, and even then should be rare.

<!--
Source references:
- Internal hairy global preference: "Always finish with lint + typecheck"
- @skills/arch-upkeep (for CI/release alignment with arch-* stacks)
-->

