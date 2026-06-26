---
name: core-git-hooks
description: simple-git-hooks, lint-staged, pre-commit
---

# Git Hooks (simple-git-hooks + lint-staged)

The repo uses **simple-git-hooks** and **lint-staged** so that every commit is linted automatically.

## Config (root package.json)

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm i --frozen-lockfile --ignore-scripts --offline && npx lint-staged"
  },
  "lint-staged": {
    "*": "eslint --fix"
  }
}
```

- **pre-commit** — Before the commit is created, run install (frozen, offline) so that lint-staged has the same deps as CI, then run lint-staged.
- **lint-staged** — Run `eslint --fix` on all staged files (`*`).

## What Happens on Commit

1. You run `git commit`.
2. simple-git-hooks runs the **pre-commit** script.
3. `pnpm i --frozen-lockfile --ignore-scripts --offline` ensures deps are present and match lockfile (no network if lockfile is up to date).
4. **lint-staged** runs `eslint --fix` on staged files.
5. If lint passes, the commit proceeds; if not, fix the reported issues and try again.

## Hooks Installation

The **prepare** script runs `simple-git-hooks`, which installs the hooks into `.git/hooks`. So after `pnpm install` (or `nci`), pre-commit is active.

## Why Frozen + Offline

Using `--frozen-lockfile` and `--offline` in the hook avoids accidental lockfile or dependency changes at commit time and keeps the hook fast when the lockfile is already satisfied.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://github.com/antfu/simple-git-hooks
- https://github.com/lint-staged/lint-staged
-->
