---
name: core-ci
description: GitHub Actions CI — lint, typecheck, test matrix
---

# CI (GitHub Actions)

The repo uses two workflows: **CI** (on push/PR) and **Release** (on tag push). Both assume `@antfu/ni` and pnpm.

## CI Workflow (.github/workflows/ci.yml)

### Lint Job

- **Trigger:** Push or PR to `main`.
- **Steps:** Checkout → pnpm setup (no install) → setup-node (lts/*, cache pnpm) → install @antfu/ni globally → `nci` (install deps) → `nr lint` → `nr typecheck`.
- **Purpose:** Fast feedback on lint and type-check without running tests on multiple OSes.

### Test Job

- **Trigger:** Same as lint.
- **Matrix:** `node: [lts/*]`, `os: [ubuntu-latest, windows-latest, macos-latest]`, `fail-fast: false`.
- **Steps:** Checkout → pnpm setup → setup-node (matrix node, cache pnpm) → install @antfu/ni → `nci` → `nr build` → `nr test`.
- **Purpose:** Ensure build and tests pass on current LTS Node across Windows, macOS, and Linux.

## Commands Used

| Command | Meaning |
|---------|--------|
| **nci** | `ni`’s CI install (e.g. `pnpm install --frozen-lockfile`). |
| **nr** | Run npm script (e.g. `nr lint` → `pnpm run lint`). |

## Template

A ready-to-use CI workflow is in **assets/ci.yml**. Copy it to `.github/workflows/ci.yml` in your monorepo root so it runs lint/typecheck/test for the whole workspace.

## Release Workflow

See [core-release](core-release.md): release runs on tag push (`v*`) and uses `sxzz/workflows` to publish to npm (e.g. with npm Trusted Publisher).

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
-->
