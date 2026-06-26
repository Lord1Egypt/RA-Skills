# Guard: Open Bugs (April 7 Status)

**Date:** 2026-04-07
**Filed by:** cc-mini
**Repo:** wip-ai-devops-toolbox-private (guard source), wip-ldm-os-private (installer/hooks)
**Priority:** high
**Status:** two bugs open, both reproducible, both cause agent loops or require --no-verify bypass

## Context

The guard master plan (`2026-04-05--cc-mini--guard-master-plan.md`) shipped Phases 1-7 during the Apr 5-7 session. Guard is now at 1.9.74 with stash escape hatch, SessionStart hook, and temp-dir writes. The release pipeline (wip-release) is at 1.9.74 with auto-PR, auto-deploy-public, tag collision pre-flight, and sub-tool drift enforcement.

Two bugs remain. Both were discovered during the Apr 5-7 session. Both have clear root causes and known fixes.

---

## Bug 1: Pre-commit hook blocks first commit on empty repos

**Severity:** medium (blocks repo bootstrap, has workaround)

### Symptom

When you create a new repo and try to make the first commit on main, the pre-commit hook blocks it:

```
BLOCKED: Cannot commit on main.
Create a branch first: git checkout -b cc-mini/your-feature
```

You cannot create a branch because there are no commits. `git checkout -b` on a repo with zero commits creates a branch that is still effectively "main" (no parent). The only workaround is `git commit --no-verify`.

### Root cause

The guard (`guard.mjs` lines 555-561) has a zero-commit exception:

```javascript
// Allow everything in repos with zero commits (bootstrap)
try {
  const hasCommits = execSync('git rev-parse HEAD', { cwd: repoDir, stdio: 'pipe' });
} catch {
  // No commits yet. Allow the first commit so the repo can be bootstrapped.
  process.exit(0);
}
```

The pre-commit hook (`templates/hooks/pre-commit` lines 8-19) does NOT have this exception:

```bash
branch=$(git branch --show-current 2>/dev/null)

if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo ""
  echo "  BLOCKED: Cannot commit on $branch."
  ...
  exit 1
fi
```

The guard and the pre-commit hook have diverged. The guard learned about zero-commit repos. The hook did not.

### Fix

Add the zero-commit check to `templates/hooks/pre-commit` before the branch check:

```bash
# Allow first commit on empty repos (bootstrap)
if ! git rev-parse HEAD >/dev/null 2>&1; then
  exit 0
fi
```

Insert before line 10 (the `if [ "$branch" = "main" ]` check).

### Files to change

| File | Change |
|---|---|
| `templates/hooks/pre-commit` | Add zero-commit check (3 lines) |
| Deployed: `~/.ldm/hooks/pre-commit` | Updated by `ldm install` |

### Testing

1. `mkdir /tmp/test-bootstrap && cd /tmp/test-bootstrap && git init`
2. `echo "hello" > README.md && git add README.md`
3. `git commit -m "Initial commit"` ... should succeed (currently blocked)
4. Verify existing repos on main still block commits (regression check)

---

## Bug 2: Guard resolves cp/mv source paths, blocks based on source repo

**Severity:** high (causes $900 guard loops, no clean workaround)

### Symptom

When copying a file FROM a main-branch repo TO a worktree:

```bash
cp /path/to/main-repo/file.txt /path/to/worktree/dest/
```

The guard blocks the operation because it resolves the SOURCE path first, finds a main-branch repo, and blocks the command. The destination is a worktree (allowed), but the guard never gets that far.

This is the root cause of the $936 session on Apr 5. Parker asked to copy one file. The agent looped for 60 minutes trying path variations.

### Root cause

`guard.mjs` lines 528-538 extract ALL paths from bash commands and resolve the repo from the FIRST match:

```javascript
// Extract absolute paths from the command itself (handles mkdir, cp, mv, etc.)
if (!repoDir) {
  const paths = extractPathsFromCommand(command);
  for (const p of paths) {
    const resolved = findRepoRoot(p);
    if (resolved) {
      repoDir = resolved;
      break;   // <-- stops at first match, which is the SOURCE
    }
  }
}
```

For `cp src dest`, `extractPathsFromCommand` returns `[src, dest]`. The loop finds the source repo first. If that repo is on main, the guard blocks.

The guard should not care where you READ from. It should only protect where you WRITE to. For `cp` and `mv`, the write target is the last argument (the destination).

### Fix

When the command starts with `cp` or `mv`, extract only the destination path (last argument) for repo resolution:

```javascript
// For cp/mv, only check the DESTINATION (last non-flag argument)
const cpMvMatch = command.match(/^\s*(cp|mv)\b/);
if (cpMvMatch && !repoDir) {
  const paths = extractPathsFromCommand(command);
  if (paths.length > 0) {
    // Last path is the destination
    const destPath = paths[paths.length - 1];
    const resolved = findRepoRoot(destPath);
    if (resolved) {
      repoDir = resolved;
    }
  }
} else if (!repoDir) {
  // For other commands, check all paths as before
  const paths = extractPathsFromCommand(command);
  for (const p of paths) {
    const resolved = findRepoRoot(p);
    if (resolved) {
      repoDir = resolved;
      break;
    }
  }
}
```

Edge cases to handle:
- `cp -r src dest` ... flags before paths, dest is still last
- `cp src1 src2 dest/` ... multiple sources, dest is still last
- `mv src dest` ... same as cp
- Pipe chains (`cp ... | ...`) ... only parse before the first pipe

### Files to change

| File | Change |
|---|---|
| `tools/wip-branch-guard/guard.mjs` | Replace lines 528-538 with cp/mv-aware path extraction |
| `tools/wip-branch-guard/test.sh` | Add test cases for cp/mv source-in-main scenarios |

### Testing

1. Create a file in a main-branch repo
2. `cp /main-repo/file.txt /worktree/dest/` ... should succeed (currently blocked)
3. `cp /worktree/file.txt /main-repo/dest/` ... should still block (destination is main)
4. `mv /main-repo/file.txt /worktree/dest/` ... should succeed
5. `mv /worktree/file.txt /main-repo/dest/` ... should block
6. Existing tests still pass (33 cases)

---

## Workarounds (until fixed)

| Bug | Workaround |
|---|---|
| Bootstrap (Bug 1) | `git commit --no-verify` for the initial commit only |
| cp/mv source path (Bug 2) | Route through /tmp: `cp src /tmp/file && cp /tmp/file dest` |

Both workarounds are fragile. Bug 2's workaround cost $936 to discover.

## Related

- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` ... master plan, Phases 1-7 shipped
- `ai/product/bugs/guard/2026-04-05--cc-mini--branch-guard-compaction-loop.md` ... prior loop incident
- `ai/product/bugs/guard/2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md` ... readonly loop class
- Guard source: `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/guard.mjs`
- Pre-commit source: `repos/ldm-os/wip-ldm-os-private/templates/hooks/pre-commit`

## Resolution

Status: Closed on 2026-04-24.

Bug 2 closed by `wip-ai-devops-toolbox-private` PR #386. The Bash parser now treats `cp` destination as the write target and `mv` as source deletion plus destination write. Tests cover `cp main/file worktree/file` allow and `cp worktree/file main/file` deny.

Bug 1 is no longer an active guard blocker in this folder. Empty-repo bootstrap remains covered by the LDM OS pre-commit template behavior and should be tracked in installer/template bugs if it regresses.

Verification:

- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
