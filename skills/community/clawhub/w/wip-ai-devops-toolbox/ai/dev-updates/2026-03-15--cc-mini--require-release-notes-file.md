# Release notes must be a file on disk

**Date:** 2026-03-15

## What changed

wip-release no longer accepts the `--notes` flag. Release notes MUST come from a file on disk:

1. `RELEASE-NOTES-v{version}.md` in repo root (auto-detected)
2. `ai/dev-updates/YYYY-MM-DD--description.md` (auto-detected)
3. `--notes-file=path` (explicit file path)

If no file exists, the release is blocked. The gate scaffolds a template (`RELEASE-NOTES-v{version}.md`) so the agent has something to fill in.

## Why

The `--notes` flag was the root cause of every bad release note. Agents passed one-liners like `--notes="fix bug"` and the gate let them through. Even after we added length checks and changelog detection, agents found ways around it. The flag was an escape hatch that undermined the entire system.

The file-on-disk requirement solves three problems:
1. **Reviewability.** The file is on the branch. It shows up in the PR diff. Parker can read and approve the release notes before merge.
2. **Quality.** Writing a file forces the agent to think about what changed and why. A flag encourages one-liners.
3. **History.** The file is committed to git. The release notes are part of the repo history, not a transient CLI argument.

## What agents need to do

Before running `wip-release`:
1. Write `RELEASE-NOTES-v{version}.md` or `ai/dev-updates/YYYY-MM-DD--description.md`
2. Commit it on the branch
3. The file shows up in the PR for review
4. After merge to main, `wip-release` auto-detects it

If the agent forgets, `wip-release` blocks and scaffolds a template.
