---
name: best-practices-git
description: Lockfile commit and merge conflict resolution
---

# Git and Lockfile

## Commit the Lockfile

Always commit `pnpm-lock.yaml`:

- Enables faster installs in CI and production (resolution can be skipped).
- Ensures the same dependency tree in dev, test, and production.

## Merge Conflicts in pnpm-lock.yaml

pnpm can resolve merge conflicts in the lockfile automatically. If you have conflicts:

1. Run `pnpm install`.
2. pnpm will regenerate the lockfile; review the result.
3. Commit the updated lockfile.

Note: pnpm merges by building from the **most updated** lockfile; it does not guarantee that it picks the “correct” head. Review the diff before committing.

## Key Points

- Commit `pnpm-lock.yaml`; use `--frozen-lockfile` in CI.
- On lockfile merge conflicts, run `pnpm install` and then review and commit.

<!--
Source references:
- https://pnpm.io/git
- sources/pnpm/docs/git.md
-->
