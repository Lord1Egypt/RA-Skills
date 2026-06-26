# Release Notes: wip-ai-devops-toolbox v1.9.62

**Fix wip-release leaving dirty state on main after every release.**

## The story

wip-release writes to 15+ files during a release (root package.json, 12 sub-tool package.json files, SKILL.md, CHANGELOG.md, product docs, trashed release notes). But gitCommitAndTag() only staged 3 files (package.json, CHANGELOG.md, SKILL.md). The other 12+ files were left modified on disk, uncommitted. This blocked git pull on the next operation and required manual `git checkout -- .` every time.

Fix: stage all files that wip-release modifies. Sub-tool package.json files, product docs (ai/product/), and trashed release notes (_trash/) are now included in the release commit.

## Issues closed

- #231 (wip-release rollback version bumps on failure)

## How to verify

```bash
wip-release patch
git status
# Should show clean working tree after release
```
