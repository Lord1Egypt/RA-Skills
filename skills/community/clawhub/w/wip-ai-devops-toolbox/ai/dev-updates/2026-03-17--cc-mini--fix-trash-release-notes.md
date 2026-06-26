# Fix trashReleaseNotes crash on untracked files

**Problem:** When a previous release failed and left a scaffolded `RELEASE-NOTES-v*.md` that was never committed, the next release's `trashReleaseNotes()` tries `git rm --cached` on an untracked file. This crashes and aborts the entire release pipeline. Parker has to manually clean up.

**Fix:** Check if the file is tracked (`git ls-files --error-unmatch`) before running `git rm --cached`. If untracked, the rename to `_trash/` already handled it.

**File:** `tools/wip-release/core.mjs` line 138

Closes #78 (partial: the trashReleaseNotes sub-bug)
