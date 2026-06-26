# Case Study: PR #512 - Historical Context in Action

This PR contradicted an existing comment that said "do NOT set BEADS_DIR". Here's how historical context research proved the comment was wrong and got the PR accepted.

## The Problem

The code had a comment: `// do NOT set BEADS_DIR as that overrides routing and breaks resolution of rig-level beads`

But the PR needed to set BEADS_DIR to fix a bug. How to convince reviewers the change doesn't break what the comment warns about?

## Git Archaeology Commands Used

```bash
# 1. Find when the comment was introduced
git log -p --all -S "do NOT set BEADS_DIR" -- internal/cmd/sling_helpers.go

# 2. Find the commit that added it
git show 52ef89c5 --stat
# Result: "fix(sling): use bd native prefix routing instead of BEADS_DIR override"

# 3. Check if there were subsequent fixes
git log --oneline 52ef89c5..HEAD -- internal/beads/beads.go
# Found: 598a39e7 "fix: prevent inherited BEADS_DIR from causing prefix mismatch"

# 4. Compare the approaches
git show 598a39e7 --stat
# Result: This commit ALWAYS sets BEADS_DIR - opposite of what 52ef89c5 said!

# 5. Find who wrote the original helper functions
gh pr list --author boshu2 --state all --limit 20
# Found: PR #149 added ExtractPrefix, GetRigPathForPrefix
```

## Timeline Built

| Date | Commit/PR | Author | What Happened |
|------|-----------|--------|---------------|
| Jan 5 | PR #149 | boshu2 | Added correct helper functions |
| Jan 6 | 52ef89c5 | jack | Wrong fix: "do NOT set BEADS_DIR" (didn't use helpers) |
| Jan 11 | 598a39e7 | joe | Correct fix in beads.go: ALWAYS set BEADS_DIR |
| Jan 14 | PR #512 | boshu2 | Applies correct pattern using original helpers |

## Why This Worked

1. **Proved the comment was outdated** - It was from Jan 6, superseded on Jan 11
2. **Showed the correct pattern existed** - 598a39e7 established ALWAYS setting BEADS_DIR
3. **Connected to original work** - PR #149 had the helpers that should have been used
4. **Provided timeline** - Made it easy for reviewers to verify the history

## Key Takeaway

When contradicting existing code or comments:
1. Trace when it was introduced (`git log -S`)
2. Find if there were subsequent fixes
3. Build a timeline showing the evolution
4. Include this in the PR body
