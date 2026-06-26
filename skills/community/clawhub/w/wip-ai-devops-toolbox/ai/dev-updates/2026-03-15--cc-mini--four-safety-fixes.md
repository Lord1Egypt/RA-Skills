# Four Safety Fixes

**Date:** 2026-03-15

## What changed

Four safety improvements across the toolbox. All gates, no new features.

### #135: Release notes template scaffold
When wip-release blocks on bad notes, it now scaffolds a `RELEASE-NOTES-v{version}.md` template with sections for what changed, why, and how to verify. The agent fills it in instead of guessing what format to use. No more blank-page problem.

### #136: Verify merged before branch delete
`post-merge-rename.sh --prune` now verifies each branch is actually merged into main before deleting, even if it has a `--merged-` suffix in its name. Previously it deleted based on position in a sorted list. A branch named `--merged-2026-03-14` that was never actually merged would have been deleted.

### #138: deploy-public.sh --dry-run
`deploy-public.sh` now supports `--dry-run`. Shows what files would change, the commit message, and the target repo without pushing anything. Agents kept running it without being asked. Now you can preview first.

### #139: wip-readme-format deploy review gate
`wip-readme-format --deploy` now blocks if all README-init-*.md files are untracked (just generated, never reviewed). You must `git add` or commit them first. Prevents agents from generating init files and immediately deploying them without human review.

## Why

All four were process violations that happened repeatedly. The rules existed in documentation. The code didn't enforce them. Now it does.
