---
name: pnpm-git-branch-lockfiles
description: Branch-specific lockfiles to avoid merge conflicts
---

# pnpm Git Branch Lockfiles

Branch lockfiles use per-branch lockfiles to avoid merge conflicts. Merge when ready.

## Enable

```yaml
# pnpm-workspace.yaml
gitBranchLockfile: true
```

Lockfile name becomes `pnpm-lock.<branch>.yaml`. Branch `feature/1` → `pnpm-lock.feature!1.yaml` (slash → `!`).

## Merge Lockfiles

```bash
pnpm install --merge-git-branch-lockfiles
```

Merges all branch lockfiles into `pnpm-lock.yaml`.

## Auto-merge by Branch Pattern

```yaml
# pnpm-workspace.yaml
mergeGitBranchLockfilesBranchPattern:
  - main
  - release*
```

`pnpm install` on `main` or branches matching `release*` will auto-merge.

<!--
Source references:
- https://pnpm.io/git_branch_lockfiles
-->
