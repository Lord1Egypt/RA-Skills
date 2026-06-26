# Guard: Onboarding key should be canonical repo, not absolute worktree path

**Date:** 2026-04-20
**Filed by:** cc-mini
**Authors:** Parker Todd Brooks, Claude Code (cc-mini, Opus 4.7)
**Repo:** `wip-ai-devops-toolbox-private` (fix target), `wip-ldm-os-private` (doc)
**Status:** plan ... fix implementation in flight on `cc-mini/guard-canonical-repo-key`.

## Symptom

Through today's `wip-branch-guard 1.9.76 → 1.9.80` rollout, I opened roughly ten git worktrees across `wip-ai-devops-toolbox-private` and `wip-ldm-os-private`. Each worktree tripped the new Layer 3 onboarding gate independently even though I had already read each repo's `README.md` + `CLAUDE.md` in an earlier worktree of the same repo in the same session.

The friction pattern:

```
git worktree add .worktrees/repo--featA -b cc-mini/featA
  Read README.md    # satisfies onboarding for repo--featA
  Read CLAUDE.md
  Edit ...           # allowed

git worktree add .worktrees/repo--featB -b cc-mini/featB
  Edit ...           # BLOCKED: onboarding required
  Read README.md    # satisfies onboarding for repo--featB (again)
  Read CLAUDE.md
  Edit ...           # allowed
```

Same repo, same docs, same session. Agent has demonstrably read them. The guard re-asks because it keys onboarding by the worktree's absolute path, not the repo's identity.

## Impact

Cumulative per-session friction roughly proportional to the number of worktrees created. For today's cascade of guard hotfix PRs ... which required a new worktree per PR ... it was roughly 10x the intended onboarding burden. In active development, three or four concurrent feature worktrees on the same repo is normal; this multiplies every session's onboarding by 3-4x with no corresponding safety benefit.

## Root cause

`tools/wip-branch-guard/guard.mjs` Layer 3:

- `state.onboarded_repos` is keyed by `repoPath`, the absolute path returned by `findRepoRoot()`.
- `state.read_files` stores absolute paths of files read.
- `getRequiredReads(repoPath)` returns absolute paths inside `repoPath` (e.g. `/path/to/worktree/README.md`).
- `checkOnboarding()` compares required-absolute-paths to `read_files`, also absolute.

A git worktree at `.worktrees/repo--featA` has a different absolute path than `.worktrees/repo--featB`, so nothing matches across them. Each worktree is treated as if it were a different repository.

## Design: canonicalize the repo identity

Key `onboarded_repos` (and file-read tracking) by a stable identity that collapses across worktrees of the same repo.

Canonical key resolution (first match wins):

1. **`git remote get-url origin`** - the remote URL is stable across all worktrees of the same repo and also across fresh clones.
2. **Main working tree path** via `git worktree list --porcelain` (first entry). Works for local-only repos without a remote.
3. **`repoPath` itself** - last resort, preserves current behavior when neither (1) nor (2) returns a value.

Read tracking:

- `markReadFile(absPath)` stores both `absPath` AND a `{canonical, relpath}` tuple.
- `checkOnboarding(repoPath, requiredReads)` converts required absolute paths to `relpath` and matches against the canonical tuples.

Effect: onboarding in worktree A satisfies worktree B of the same repo. Fresh clones in different locations also satisfy if origin URL matches (nice but secondary).

## Non-goals for this PR

- **Cross-session persistence.** Fresh `session_id` still wipes the cache; that's intentional (new session = new context = re-verify).
- **Cross-branch content changes.** If `README.md` differs between branches, that's fine: the agent re-reads it via the Read tool if the branch itself changed. We're not trying to skip re-reading when the docs change; we're trying to skip re-reading when the docs are the same.
- **Submodules.** Each submodule has its own origin; canonical keys differ; behavior stays correct.

## Implementation sketch

```javascript
function canonicalRepoKey(repoPath) {
  try {
    const url = execSync('git remote get-url origin 2>/dev/null', {
      cwd: repoPath, encoding: 'utf8', timeout: 3000,
    }).trim();
    if (url) return url;
  } catch {}
  try {
    const raw = execSync('git worktree list --porcelain 2>/dev/null', {
      cwd: repoPath, encoding: 'utf8', timeout: 3000,
    });
    const m = raw.match(/^worktree\s+(.+)$/m);
    if (m) return m[1];
  } catch {}
  return repoPath;
}
```

State schema gets two new optional fields:

```json
{
  "read_files": ["/abs/path/README.md", ...],
  "read_files_canonical": [
    { "canonical": "git@github.com:wipcomputer/repo.git", "relpath": "README.md" }
  ],
  "onboarded_repos": { "/abs/repo/path": {...} },
  "onboarded_repos_canonical": {
    "git@github.com:wipcomputer/repo.git": { "onboarded_at_ts": ..., "last_touch_ts": ... }
  }
}
```

Both the absolute-path and canonical-key representations are kept. Old entries remain valid; new entries have both. `checkOnboarding` prefers canonical when both are available, falls back to absolute-path matching otherwise.

## Tests

Add to `tools/wip-branch-guard/test.sh`:

- Setup: create a tmp git repo with a fake remote origin URL. Add two worktrees off main to different paths.
- Test: onboard in worktree A (Read README + CLAUDE from worktree A), then Write in worktree B of the same repo. Expected: allow (onboarding satisfied via canonical key).
- Regression: Read in worktree A does not satisfy onboarding for a DIFFERENT repo that happens to have the same relpath reads. Expected: deny.
- Fallback: repo with no origin URL falls back to main-working-tree path, and the two worktrees of that repo still share onboarding.

## Version bump

`tools/wip-branch-guard/package.json`: `1.9.80 -> 1.9.81`.

## Release notes

`tools/wip-branch-guard/RELEASE-NOTES-v1-9-81.md` on the feature branch.

## Rollout

Same as every PR today: branch + PR + merge + `publishNpm` + `ldm install`. The content-hash check in `wip-ldm-os 0.4.77`'s `deployExtension` will detect the file change and redeploy correctly.

## Related

- Plan: `ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md` (PR 1-3 shipped; this is a follow-up refinement).
- Triggering observation: mid-rollout friction during PRs #353/#355/#357/#358/#360/#361/#362/etc. where every new cc-mini/* worktree re-triggered onboarding.

## Resolution

Status: Closed on 2026-04-24.

Canonical onboarding behavior remains covered in the guard regression suite and was preserved while adding explicit `wip-branch-guard onboard <repo>` in PR #386.

Verification:

- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
