---
name: core-deps-taze
description: Keep dependencies continuously fresh using taze with controlled, scripted upgrades.
---

# Keep Dependencies Fresh with `taze`

Use `taze` as the primary tool to keep dependencies up to date in a controlled, repeatable way, instead of hand-editing version ranges.

## Usage

### 1. Audit outdated dependencies

- Run `taze` (usually via `nr` script) at the repo root:
  - In single-package repos: upgrade directly in the root `package.json`.
  - In monorepos: run in combination with pnpm workspaces so that versions stay aligned across packages.

### 2. Apply upgrades in controlled batches

- Prefer:
  - **Regular minor/patch upgrades** (small, low-risk PRs).
  - **Focused major upgrades** (one or a small group of majors per PR, with extra testing).
- Typical workflow:
  1. Run `taze` with appropriate flags (e.g. only patch/minor).
  2. Review the diff in `package.json` and lockfile.
  3. Run `nr lint`, `nr typecheck`, and tests before committing.

### 3. Align monorepo versions

- In pnpm workspaces:
  - Use `taze` to keep shared tooling and core libraries on the same versions across all packages.
  - Combine with pnpm catalogs when appropriate so that upgrades are driven from a single place.

### 4. Avoid manual version edits

- Do **not** manually bump versions in `package.json` except when:
  - Pinning a version for a known regression.
  - Working around a specific ecosystem issue.
- Even then, document the reason in the PR or commit message.

## Key Points

- Treat `taze` runs as routine maintenance, not rare events.
- Always pair `taze` changes with lint, typecheck, and tests before merging.
- Use `taze` output as the source of truth for version bumps instead of guessing ranges.

<!--
Source references:
- Internal hairy global preference: "Keep dependencies fresh with `taze`"
- @skills/taze
-->

