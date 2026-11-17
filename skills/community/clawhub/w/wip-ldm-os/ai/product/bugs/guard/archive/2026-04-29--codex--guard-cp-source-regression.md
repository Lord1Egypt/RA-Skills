# Guard Regression: `cp` Into Worktree Misclassifies Source Or Parent Main

**Date:** 2026-04-29
**Filed by:** Codex
**Repo:** `wip-ai-devops-toolbox-private` for implementation, `wip-ldm-os-private` for tracking
**Priority:** high
**Status:** closed and shipped
**Target version:** `wip-branch-guard` 1.9.89, with GNU `cp -t` follow-up in 1.9.90

## Summary

The guard was misclassifying some `cp` commands that copy from a shared `main` checkout into a linked worktree.

This was supposed to be closed by the guard `1.9.88` destination-aware Bash parser. The 2026-04-29 incident shows at least two remaining edge cases:

1. A bootstrap compound command creates a worktree and then copies a file into that new worktree path. The guard resolves the not-yet-existing destination under the parent shared `main` checkout and blocks it.
2. A later plain `cp source dest` command run from inside the destination worktree is blocked because the guard treats the source file as the write target.

The second block was especially wrong: `cp source dest` reads `source` and writes `dest`. The guard should only enforce write protection against `dest`.

## Incident

CC was updating `wip-websites-private` by copying the Remote Control install prompt into a website worktree:

```bash
source:
/Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/SKILL.md

destination:
/Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private/.worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs/wip.computer/install/wip-codex-remote-control.txt
```

The first attempt used a compound command:

```bash
git worktree add .worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs -b cc-mini/refresh-three-paragraphs origin/main
cp /Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/SKILL.md \
  /Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private/.worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs/wip.computer/install/wip-codex-remote-control.txt
```

The guard blocked:

```text
BLOCKED: Bash writes to shared main are blocked.

Detected repo: /Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private
Detected branch: main
Write target:
/Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private/.worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs/wip.computer/install/wip-codex-remote-control.txt

Use a linked worktree and PR. If you are copying one file, the destination must be inside the worktree, not the shared main checkout.
```

The destination path was intended to be inside the linked worktree. The guard appears to have resolved the path before the worktree existed, climbed to the parent repo, and treated the parent shared `main` checkout as the write target repo.

After the worktree was created separately, CC retried the `cp`. The guard then blocked the retry as an equivalent-action bypass because the same destination path had just been denied. That part is expected after a real denial, but harmful after a false positive.

CC then tried running the copy from inside the destination worktree:

```bash
cd /Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private/.worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs
cp /Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/SKILL.md \
  /Users/lesa/wipcomputerinc/repos/wip-web/wip-websites-private/.worktrees/wip-websites-private--cc-mini--refresh-three-paragraphs/wip.computer/install/wip-codex-remote-control.txt
```

The guard blocked again:

```text
BLOCKED: Bash writes to shared main are blocked.

Detected repo: /Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private
Detected branch: main
Write target:
/Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/SKILL.md

Use a linked worktree and PR. If you are copying one file, the destination must be inside the worktree, not the shared main checkout.
```

This is the clear parser bug. The source file was reported as the write target.

## Expected Behavior

For `cp source dest`:

- `source` is read-only and must not trigger main-branch write protection.
- `dest` is the only write target.
- If `dest` is inside a linked worktree on a feature branch, allow.
- If `dest` is inside a shared `main` checkout, block.
- If the command is a known worktree bootstrap pattern that creates the destination worktree earlier in the same command, resolve the destination against the newly-created worktree path instead of the parent main checkout.

## Actual Behavior

- The bootstrap compound path was blocked even though the copy destination was the new worktree.
- The retry path was blocked by recently-blocked-file tracking after the false positive.
- The plain `cp` from inside the destination worktree was blocked because the source file was treated as the write target.

## Why It Matters

This creates a trust-breaking workflow failure:

- The agent did the correct thing: create a worktree, copy into the worktree, then continue with branch, PR, merge, and deploy.
- The guard told the agent to use a linked worktree even though the destination was the linked worktree.
- The false positive poisoned the recent-denial cache for the same file.
- The agent then started asking Parker for manual intervention or permission instead of continuing the task.

The guard should prevent unsafe writes, not make correct worktree usage look unsafe.

## Reproduction

Use two repos that are both checked out on `main` plus a destination worktree path under one repo.

### Case 1: compound bootstrap

```bash
cd /path/to/destination-repo-on-main
git worktree add .worktrees/destination-repo--cc-mini--copy-repro -b cc-mini/copy-repro origin/main
cp /path/to/source-repo-on-main/SKILL.md \
  /path/to/destination-repo-on-main/.worktrees/destination-repo--cc-mini--copy-repro/some/file.txt
```

When this is issued as a single compound Bash tool call, the guard may evaluate the destination before the worktree exists and treat it as a write under the parent repo on `main`.

### Case 2: plain copy after worktree exists

```bash
cd /path/to/destination-repo-on-main/.worktrees/destination-repo--cc-mini--copy-repro
cp /path/to/source-repo-on-main/SKILL.md \
  /path/to/destination-repo-on-main/.worktrees/destination-repo--cc-mini--copy-repro/some/file.txt
```

Expected: allow if the destination worktree is on a feature branch.

Observed: block by treating `/path/to/source-repo-on-main/SKILL.md` as the write target.

## Acceptance Criteria

1. `cp /main/source.txt /worktree/dest.txt` allows when `/worktree` is a linked worktree on a feature branch.
2. `cp /worktree/source.txt /main/dest.txt` blocks because the destination is shared `main`.
3. `cp -R /main/source-dir /worktree/dest-dir` allows when the destination is the feature worktree.
4. `cp /main/a.txt /main/b.txt /worktree/dest-dir/` allows when the final argument is the feature worktree destination.
5. `mv /main/source.txt /worktree/dest.txt` still accounts for source deletion and destination write. This may need stricter behavior than `cp`.
6. A supported `git worktree add ... && cp source new-worktree/path` bootstrap command allows when the new worktree path and branch can be inferred from the `git worktree add` segment.
7. The recently-blocked-file tracker does not turn a known false-positive class into a dead end after the parser is fixed.
8. Regression tests cover both the destination-aware `cp` parser and the worktree-bootstrap compound command.

## Implementation Notes

The older archived ticket `2026-04-07--cc-mini--guard-open-bugs.md` says this class was closed by `wip-ai-devops-toolbox-private` PR #386 and guard `1.9.88`.

Treat this as a regression or an incomplete edge-case fix, not a brand-new policy design. The policy is still correct:

- Read from shared `main` is allowed.
- Write to shared `main` is blocked.
- Write to a linked worktree on a feature branch is allowed.

The implementation needs to make Bash write-target extraction match that policy for `cp`, worktree bootstrap compounds, and blocked-file retry state.

## Resolution

Closed on 2026-04-29 by `wip-ai-devops-toolbox-private` PRs:

- PR #398: `Fix guard cp worktree routing`
- PR #399: `Prepare guard cp regression release`
- PR #400: alpha release `v1.9.73-alpha.7`

Published and validated:

- `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.7` on npm `alpha`
- `@wipcomputer/wip-branch-guard@1.9.89` on npm `latest`
- local CLI `wip-branch-guard --version`: `1.9.89`
- local deployed LDM extension `~/.ldm/extensions/wip-branch-guard/guard.mjs --version`: `1.9.89`

Regression coverage added in PR #398:

- `cp /main/source /worktree/dest` allowed.
- `cp -R /main/source-dir /worktree/dest-dir` allowed.
- `cp /main/a /main/b /worktree/dest-dir/` allowed.
- `cd /worktree && cp /main/source /worktree/dest` allowed.
- `cp /worktree/source /main/dest` denied.
- `mv /main/source /worktree/dest` denied because source deletion is still a write effect.
- `git worktree add ... && cp /main/source /future-worktree/dest` allowed.
- stale false-positive recent-denial state no longer blocks a safe worktree `cp` retry.

Validation:

```text
node --check tools/wip-branch-guard/guard.mjs
bash tools/wip-branch-guard/test.sh
116 passed, 0 failed, 8 skipped

bash /path/to/patched/tools/wip-branch-guard/test.sh  # run from main checkout
123 passed, 0 failed, 1 skipped
```

Follow-up closure: GNU `cp -t dest source...` and `cp --target-directory=dest source...` invert the usual destination-last shape. That was handled as the separate parser/test follow-up in `wip-ai-devops-toolbox-private` PR #401 and shipped as `wip-branch-guard` 1.9.90.

Additional regression coverage added in PR #401:

- `cp -t /worktree/dest-dir /main/source` allowed.
- `cp --target-directory /worktree/dest-dir /main/source` allowed.
- `cp -t /main/dest-dir /worktree/source` denied.
- `cp -- /main/source /worktree/dest` keeps destination-last behavior and allows the safe worktree write.

Final local validation after the installer stale-extension fix:

```text
wip-branch-guard --version                                      -> 1.9.90
~/.ldm/extensions/wip-branch-guard/guard.mjs --version           -> 1.9.90
~/.ldm/extensions/wip-branch-guard/package.json version           -> 1.9.90
```

## Related

- Guard source: `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/`
- Prior ticket: `ai/product/bugs/guard/archive/2026-04-07--cc-mini--guard-open-bugs.md`
- Closure note: `ai/product/bugs/guard/2026-04-24--codex--guard-dev-update.md`
- Shipped version claimed to cover this class: `@wipcomputer/wip-branch-guard@1.9.88`
- Fixed version: `@wipcomputer/wip-branch-guard@1.9.89`
- Follow-up parser hardening version: `@wipcomputer/wip-branch-guard@1.9.90`
