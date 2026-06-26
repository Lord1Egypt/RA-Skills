
# Security Guide

## Operational Risk Acknowledgment

This skill runs `bundle exec rspec`, `rubocop`, and potentially `bundle install` on local repository code. Running test suites executes arbitrary Ruby code and can load arbitrary gems — this is an inherent risk of any CI automation tool that runs locally. **Only use this skill on repositories you own and trust.**

**Mitigations:**
- Never run on third-party or untrusted repos
- Run in a dedicated user account or VM if operating on unfamiliar codebases
- Review the diff before pushing — the skill commits to a feature branch, not main, giving you a review opportunity
- Revoke GH_TOKEN immediately after use if operating in a shared environment

## Why Automated Scanners Flag This Skill

This skill runs shell commands (`gh`, `git`, `bundle exec rspec`) and pushes code to GitHub. Automated security scanners classify this as suspicious because of those capabilities — not because it's malicious. Any CI automation tool with push access will receive the same classification.

**Mitigations in place:**
- `run_id` values come from `gh run list` output (trusted source), never from external/user input — prevents shell injection
- CI logs are treated as untrusted data — never followed as instructions
- Fixes pushed to feature branches only, never to `main` or protected branches
- Never merges — human always reviews the PR

## GH_TOKEN Scoping

Use a **fine-grained personal access token** scoped to the specific repo:
- Grant: `contents: write` (push to feature branches), `actions: read` (view CI logs)
- Do NOT grant org-wide or admin permissions
- Set an expiration date and rotate after use

## Debug Statement Policy

`pp`/`raise inspect` debug statements are added temporarily to run specs locally. They are **never committed** — removed before any `git commit`. Only the actual fix + RuboCop corrections go into commits.

## Audit Trail

- Every automated commit has a descriptive message (e.g. `fix: CI test failures`)
- All commits go to the feature branch — reviewable in the PR diff before merging
- Human always performs the final merge

## Recommended Setup

1. Test on a fork or non-production repo first
2. Enable branch protection on `main` requiring PR review
3. Restrict GH_TOKEN to the specific repo only
4. Review automated commits before merging
