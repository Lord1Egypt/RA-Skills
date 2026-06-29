# GitHub Interaction Developer Helper

## What It Does

Build reliable GitHub issue, pull request, review, and automation workflows with safe API usage, clear repository context, and reproducible local checks.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Developers, maintainers, release engineers, and agent builders who automate github work without losing review context.

## Workflow Summary

1. Identify the repository, target issue or PR, branch, permissions, desired action, and whether the operation is read-only or mutating.
2. Fetch metadata first: title, body, labels, status, linked checks, changed files, review comments, and timeline context.
3. For code changes, inspect the local worktree and existing user changes before editing.
4. Choose the safest API path: GitHub app connector, gh CLI, REST/GraphQL call, or local git command, and record why.
5. Verify results with tests, diff checks, status checks, or a second metadata fetch before posting comments or requesting review.
6. Summarize exact GitHub state changes, links, remaining blockers, and anything intentionally left untouched.

## Deliverables

- A GitHub triage summary with concrete next actions.
- Safe commands or API calls for issue, PR, branch, review, or CI workflows.
- A scoped patch plan and verification checklist.
- A concise comment or PR update ready to post.

## Quality Bar

- Repository, PR/issue number, branch, and permission assumptions are explicit.
- Mutating operations happen only after enough context has been fetched.
- Local user changes are not reverted or overwritten.
- The final state is verified through metadata, git diff, tests, or CI output.

## Trigger Examples

- `Use $software-data-github-interact-developer-helper to summarize this PR and its unresolved comments.`
- `Automate a safe GitHub issue triage workflow for this repository.`
- `Create commands for rerunning failed checks and reporting the result.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
