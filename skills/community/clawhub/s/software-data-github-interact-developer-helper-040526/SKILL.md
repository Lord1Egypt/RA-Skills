---
name: software-data-github-interact-developer-helper
description: >-
  Build reliable GitHub issue, pull request, review, and automation workflows with safe API usage, clear repository context, and reproducible local checks. Use when a user asks for GitHub, pull request, issue, review comments, CI, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# GitHub Interaction Developer Helper

## Purpose

Use this skill when a user needs to inspect or act on GitHub issues, PRs, checks, comments, branches, or repository files while preserving contributor intent and avoiding accidental destructive changes.

Audience: developers, maintainers, release engineers, and agent builders who automate GitHub work without losing review context.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Identify the repository, target issue or PR, branch, permissions, desired action, and whether the operation is read-only or mutating.
2. Fetch metadata first: title, body, labels, status, linked checks, changed files, review comments, and timeline context.
3. For code changes, inspect the local worktree and existing user changes before editing.
4. Choose the safest API path: GitHub app connector, gh CLI, REST/GraphQL call, or local git command, and record why.
5. Verify results with tests, diff checks, status checks, or a second metadata fetch before posting comments or requesting review.
6. Summarize exact GitHub state changes, links, remaining blockers, and anything intentionally left untouched.

## Expected Outputs

- A GitHub triage summary with concrete next actions.
- Safe commands or API calls for issue, PR, branch, review, or CI workflows.
- A scoped patch plan and verification checklist.
- A concise comment or PR update ready to post.

## Validation

- Repository, PR/issue number, branch, and permission assumptions are explicit.
- Mutating operations happen only after enough context has been fetched.
- Local user changes are not reverted or overwritten.
- The final state is verified through metadata, git diff, tests, or CI output.

## Triggers

Keywords: `GitHub`, `pull request`, `issue`, `review comments`, `CI`, `gh`, `repository automation`

Example trigger sentences:

- `Use $software-data-github-interact-developer-helper to summarize this PR and its unresolved comments.`
- `Automate a safe GitHub issue triage workflow for this repository.`
- `Create commands for rerunning failed checks and reporting the result.`
