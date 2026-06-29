# Branch protection guide

Use this after the workflows have run at least once on GitHub so the status checks exist.

## Goal
Require the automated checks before anything merges to `master`.

## Recommended GitHub settings
Path: GitHub repo → Settings → Rules → Rulesets (or Branches) → `master`

Enable:
- Require a pull request before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Block force pushes
- Block deletions

## Required status checks
Add these checks:
- `CI / validate`
- `CodeQL / Analyze (python)`
- `CodeQL / Analyze (javascript)`

## Notes
- If GitHub shows slightly different check names, use the exact names from the first successful workflow run.
- If the default branch changes from `master`, update the workflow branch filters too.
- If you later add tests or lint jobs, add them here as required checks as well.
