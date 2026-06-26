# Release Notes: wip-ai-devops-toolbox v1.9.65

**Fix release notes scaffold on protected branches**

When `wip-release patch` runs on main without a RELEASE-NOTES file, it used to scaffold a
template directly in the working tree. On repos with branch guards (pre-commit hooks that
block commits to main), this scaffolded file could not be removed or committed. It would
block `git pull` and leave the working tree dirty. This has happened multiple times across
different repos.

The fix adds a branch check before scaffolding. If the current branch is main or master,
wip-release now prints a clear error telling the user to write release notes on their
feature branch before merging, then exits non-zero without creating any files. The scaffold
behavior still works on feature branches, where it's actually useful.

## Issues closed

- Closes #223

## How to verify

```bash
# On main, without release notes: should error, NOT scaffold
cd any-repo && git checkout main
wip-release patch
# Expected: "Release notes missing. Write RELEASE-NOTES-v*.md on your feature branch before merging."
# Expected: no RELEASE-NOTES file created in working tree

# On a feature branch: should scaffold as before
git checkout -b test/scaffold-check
wip-release patch
# Expected: scaffolded template created
```
