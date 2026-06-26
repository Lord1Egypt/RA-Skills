# Release Notes: wip-ai-devops-toolbox v1.9.66

Auto-combine release notes when batching multiple PRs into a single release.

## The story

When multiple PRs merge to main before wip-release runs, the release had no good way to gather all their stories. Each PR might have its own RELEASE-NOTES file committed on the branch, but once the branch merges and the file gets trashed, the next release only sees an empty repo root. The agent had to write a new RELEASE-NOTES file from scratch, losing the narrative that was already reviewed in each PR.

Now wip-release looks back through git history. It finds every merge commit since the last tag, checks each one for RELEASE-NOTES files via `git diff-tree` and `git show`, and combines them into a single document. If only one PR had notes, it uses them as-is (fully backwards compatible). If multiple PRs had notes, it wraps them with per-PR section headers, strips duplicate top-level headings, and collects all issue references into a combined list at the end.

The detection sits at priority 2.5 in the release notes cascade: after the single-file check (RELEASE-NOTES-v{ver}.md on disk) but before the dev-update fallback. A file on disk always wins. The merged-PR scan only kicks in when nothing is found on disk.

## What changed

- New exported function `collectMergedPRNotes()` in `core.mjs` that scans git merge history for RELEASE-NOTES files
- Updated `cli.js` to call it at priority 2.5 in the notes detection cascade
- Updated help text to document the new detection path
- Zero breaking changes. Single-file detection still works exactly as before.

## Issues closed

- Closes #237

## How to verify

```bash
# In any repo with multiple merged PRs since last tag, each having RELEASE-NOTES files:
wip-release patch --dry-run
# Should show: "Combined release notes from N merged PRs"
```
