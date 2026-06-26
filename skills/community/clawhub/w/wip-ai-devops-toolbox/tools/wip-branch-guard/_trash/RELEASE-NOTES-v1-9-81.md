# wip-branch-guard v1.9.81

## Onboarding key is now canonical repo, not absolute worktree path

**Problem.** PR 2's onboarding gate keyed `state.onboarded_repos` by `repoPath` ... the absolute path of the git worktree root. Each `git worktree add .worktrees/repo--featX -b ...` creates a new path, so every worktree of the same repo triggered the onboarding gate independently. During today's guard rollout (~10 worktrees on two repos), I was re-reading the same README + CLAUDE.md files ten times for the same two repos.

**Fix.** Key onboarding by a canonical repo identity. Resolution order:

1. `git remote get-url origin` ... stable across all worktrees of the same repo AND across fresh clones of it.
2. Main working tree path from `git worktree list --porcelain` ... fallback for local-only repos with no remote.
3. `repoPath` itself ... last-resort fallback (equivalent to pre-1.9.81 behavior).

Read-tracking now stores both an absolute path (unchanged) and a `{canonical, relpath}` tuple. `checkOnboarding` checks canonical first. Same repo, same reads, any worktree: onboarded once, covered everywhere.

**Example.**

```
git worktree add .worktrees/repo--featA -b cc-mini/featA
  Read README.md      # canonical: git@github.com:wipcomputer/repo.git, rel README.md
  Read CLAUDE.md      # canonical: ^same, rel CLAUDE.md
  Write ...           # allowed (onboarded)

git worktree add .worktrees/repo--featB -b cc-mini/featB
  Write ...           # ALLOWED (canonical key already onboarded, no re-reads needed)
```

Before v1.9.81 the second Write would have been BLOCKED pending another round of Reads. Now the canonical key shared across worktrees means one onboarding covers all of them.

## State schema additions (backward-compatible)

Two new optional fields in `~/.ldm/state/guard-session.json`:

```json
{
  "read_files_canonical": [
    { "canonical": "git@github.com:wipcomputer/repo.git", "relpath": "README.md" }
  ],
  "onboarded_repos_canonical": {
    "git@github.com:wipcomputer/repo.git": { "onboarded_at_ts": ..., "last_touch_ts": ... }
  }
}
```

The legacy absolute-path fields (`read_files`, `onboarded_repos`) are still written and read for backward compatibility. Existing state files from 1.9.79/1.9.80 keep working; new writes populate both.

## Files

- `tools/wip-branch-guard/guard.mjs`: `canonicalRepoKey()` + `canonicalFileInfo()` helpers; `markReadFile`, `checkOnboarding`, `markOnboarded` all write/read canonical form alongside absolute paths. ~60 lines total.
- `tools/wip-branch-guard/test.sh`: 8 new test cases covering origin-URL-based sharing, fallback to main-worktree path for local-only repos, and regression (different repos don't share onboarding just because session is the same).
- `tools/wip-branch-guard/package.json`: version `1.9.80 -> 1.9.81`.

## Tests

88 passing, 0 failing, 8 main-only skipped. Up from 80.

## Non-goals

- **Cross-session persistence.** A new `session_id` still wipes the onboarded cache.
- **Cross-branch content changes.** If `README.md` differs between branches (rare), the agent re-reads it because the file's content changed; the canonical check matches `relpath` by name, not by hash. If this becomes a friction point, we can tighten with a content hash on stored reads.
- **Submodules.** Each submodule has its own origin URL, so submodules get their own canonical key ... correct behavior.

## Related

- Bug doc: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-onboarding-canonical-key.md` (PR #631)
- Triggered by: today's 10-worktree guard cascade (PRs #353, #355, #357, #358, #360, #361, #362, etc.) where every worktree re-triggered onboarding on the same two repos.
- Parent plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md` (this is a refinement to PR 2's Layer 3; the plan itself is complete).
