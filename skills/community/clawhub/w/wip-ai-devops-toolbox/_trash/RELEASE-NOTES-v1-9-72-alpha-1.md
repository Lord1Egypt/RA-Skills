# v1.9.72-alpha.1

## wip-branch-guard: unblock native escape hatch for clearing untracked files on main

**Problem.** When an untracked file exists in main's working tree (for example, content Parker saved manually before a PR merged, or a deployed artifact the pipeline dropped there), `git pull` refuses to proceed because it would overwrite the untracked file. Every command that could clear the file was blocked by the guard: `rm`, `mv`, `git stash push`, `git clean`, `git reset`, `git restore`. No native escape hatch existed. Agents (and humans) lost hours looping: retry rm, retry mv, tool-swap to Write/Edit to bypass the guard, rationalize, spiral. One session today burned $936 on the loop before the bug was isolated.

**Fix.** Add `git stash push` / `git stash save` / bare `git stash` to `ALLOWED_GIT_PATTERNS`. Stashing is non-destructive because `git stash drop`, `git stash pop`, and `git stash clear` remain in `DESTRUCTIVE_PATTERNS` (blocked on any branch). The stash survives as a safety net; nothing is ever lost.

**New workflow for this failure mode:**

```
git stash push -u -- path/to/untracked-file    # move untracked file aside
git pull                                        # pulls cleanly
git stash list                                  # file preserved in stash
```

**Error message improvement.** The `WORKFLOW_ON_MAIN` block now includes a concrete, copy-pasteable stash workaround so future sessions don't loop. LLMs and humans both follow concrete commands more reliably than abstract workflow steps.

**Test coverage added.** `test.sh` now asserts `git stash push`, `git stash save`, and bare `git stash` all return `allow`. All 33 tests pass.

## Why this matters

This is the third time in five days that the guard loop has trapped a session. The prior bug files (`ai/product/bugs/guard/2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md`, `2026-04-05--cc-mini--branch-guard-compaction-loop.md`) document the pattern. This fix closes one specific failure mode (untracked-stub-blocks-pull). Other guard loop failure modes remain and will be addressed separately.

## Files changed

- `tools/wip-branch-guard/guard.mjs`: two new `ALLOWED_GIT_PATTERNS` entries, expanded `WORKFLOW_ON_MAIN` with stash workaround
- `tools/wip-branch-guard/package.json`: 1.9.71 -> 1.9.72
- `tools/wip-branch-guard/test.sh`: three new passing test cases
- `CHANGELOG.md`: entry for 1.9.72-alpha.1
