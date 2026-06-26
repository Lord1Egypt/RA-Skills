---
name: windows-git-ops
description: Use this skill when performing Git operations in a Windows PowerShell workspace, especially for branch creation, staging, commit, merge, status inspection, and command construction that must avoid bash-only syntax and reduce shell mistakes.
---

# Windows Git Ops

## Overview

Use this skill when the task involves Git commands on Windows PowerShell. It prevents shell-specific mistakes, keeps Git operations auditable, and favors simple non-interactive command sequences over clever chained commands.

## Hard Rules

- Assume the shell is PowerShell unless the environment clearly says otherwise.
- Do not use bash-only chaining or redirection syntax such as `&&`, `||`, `<<EOF`, or other POSIX-only forms.
- Prefer one command per shell invocation for Git operations. Do not compress unrelated steps into a single shell string.
- Use non-interactive Git commands only. Avoid commands that open editors or interactive prompts.
- Before mutating Git state, inspect it with targeted commands such as `git status --short`, `git branch --show-current`, `git diff --name-only`, or `git diff --cached --name-only`.
- Stage only intended files. Never use broad staging when the change set should stay narrow.
- When committing from a dirty worktree, confirm the staged set matches the intended change before `git commit`.
- Do not revert, reset, or discard user changes unless the user explicitly asked for it.
- When creating a branch in Codex, use the required `codex/` prefix.

## PowerShell-Safe Patterns

- For sequential Git steps, run separate commands in separate tool calls.
- When an environment variable is needed for one command, set it explicitly in PowerShell form, for example ``$env:PYTHONPATH='.'``.
- When quoting commit messages or paths, use PowerShell-safe quoting and avoid shell tricks copied from bash examples.
- If a command would be easier in bash but the environment is PowerShell, rewrite it for PowerShell instead of assuming bash compatibility.

## Standard Workflow

### Inspect

Use this sequence before any branch, staging, commit, or merge action:

1. `git branch --show-current`
2. `git status --short`
3. `git diff --name-only`
4. `git diff --cached --name-only`

### Create Branch

1. Inspect current branch and worktree state.
2. Create the branch with `git checkout -b codex/<name>`.
3. Re-check `git branch --show-current` if the branch matters to the task.

### Commit

1. Inspect unstaged and staged files separately.
2. Stage only the intended paths with explicit `git add <path>`.
3. Verify staged content with `git diff --cached --name-only` and, when needed, `git diff --cached`.
4. Commit with a non-interactive message such as `git commit -m "fix: ..."` .

### Merge Back

1. Ensure the feature branch is committed.
2. `git checkout main`
3. Confirm main branch state.
4. Merge with `git merge --no-ff <branch> -m "<message>"` unless the user asked for a different strategy.
5. Confirm final branch and worktree state.

## Common Failure Prevention

- If you catch yourself writing `cmd1 && cmd2`, split it into separate commands.
- If you are unsure whether a helper method or Git flag is valid in this shell, check the real definition or help output before using it.
- If the worktree contains unrelated files, leave them untouched and call them out explicitly in the final summary.
- If a command fails because of shell syntax, rewrite it in native PowerShell form instead of retrying the same pattern.

## Output Expectations

- State the current branch when it matters.
- State exactly which files were staged or committed.
- Mention untracked or unrelated files that were intentionally left alone.
- When merge or commit succeeds, report the resulting commit hash if available.
