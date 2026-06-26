# v1.9.71-alpha.8

## wip-release: automatic PR flow for protected main (Phase 4)

When `git push origin main` fails with GitHub's "protected branch" rejection (`GH006: Changes must be made through a pull request`), wip-release now automatically:

1. Creates a release branch `cc-mini/release-v<version>` at the current commit
2. Pushes the branch to origin
3. Opens a PR via `gh pr create` with title `release: v<version>`
4. Merges the PR via `gh pr merge --merge --delete-branch`
5. Pushes the tag separately (tags bypass branch protection on most GitHub setups)
6. Fast-forwards local main so downstream steps (deploy-public, etc.) have a clean state

Previously this was a 4-command manual workflow every release:

```
git branch cc-mini/release-alpha-N
git push -u origin cc-mini/release-alpha-N
gh pr create --base main --head cc-mini/release-alpha-N --title '...'
gh pr merge <pr> --merge --delete-branch
git push origin v<version>
```

Every release. Every time. Eliminated.

## Fallback behavior

If any step of the auto-PR flow fails (gh CLI missing, PR create failure, merge failure, tag push failure), wip-release logs a concrete recovery command for the exact failure mode and continues (non-fatal, matches prior push-failed behavior). The user can always complete the remaining steps manually.

## Direct push still works

If the repo allows direct push to main (typical for private staging repos), wip-release tries direct push first and only falls back to the PR flow on the specific GH006 / "protected branch" error. No behavioral change for unprotected repos.

## Files changed

- `tools/wip-release/core.mjs`: new `pushReleaseWithAutoPr(repoPath, newVersion, level)` and `logPushFailure(result, tag)` helpers. Three push sites in `release()`, `releaseHotfix()`, `releasePrerelease()` migrated to use the helper.
- `tools/wip-release/package.json`: 1.9.72 -> 1.9.73
- `CHANGELOG.md`: entry added

## Verified

- Module imports cleanly via `node -e "import('./tools/wip-release/core.mjs')"`.
- Error detection regex handles GH006 variants: `/protected branch|GH006|Changes must be made through a pull request/i`.
- All three release tracks (stable, prerelease, hotfix) use the same helper.

## Cross-references

- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` Phase 4 (Incident 4)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-002.md` Wave 2 phase 7
- Prior ship: alpha.7 closed Phases 1, 2, 8 of the same plan.
