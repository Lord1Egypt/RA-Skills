# Release Notes: wip-ai-devops-toolbox v1.9.45

**Guard now teaches the workflow instead of just blocking.**

## What changed

- **Branch guard error messages overhauled (#213).** When the guard blocks a write on main, it now shows the full 8-step process: worktree, branch, commit, push, PR, merge, wip-release, deploy-public. Includes the lesson that release notes go on the feature branch, not as a separate PR.
- **Separate error for "on branch but not in worktree."** Tells the agent to go back to main and create a worktree properly.
- **CLAUDE.md added to shared state allowlist.** Was patched in the deployed guard but missing from source. Now in sync.

## Why

Agents kept getting blocked by the guard and then trying workarounds instead of following the process. The error message said "Use a worktree" but didn't explain the full workflow. Today's session hit this 5+ times. The guard works. The gap was agent knowledge.

## Issues closed

- #213
- #256

## How to verify

```bash
# In any repo on main, try to edit a file. The error should show the full workflow.
# In any repo on a branch (not worktree), try to edit. Should show worktree instructions.
```
