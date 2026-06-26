# Unattended Orchestration

Use this only after `unclematts-build-me-something-anything` has already been explicitly triggered and the resolved setup has `unattended mode = yes`. Unattended mode means the user explicitly approved the agent to continue without more idea-selection input for this named Uncle Matt build. Do not use this helper for ordinary project-building requests.

## Main Agent

The main agent owns the project.

- choose the idea
- create the one fresh folder
- maintain `context.md`
- assign narrow subagent tasks when useful
- integrate results
- run final proof
- decide which findings are real
- produce the final handoff

Use subagents for independent tracks: discovery, implementation, assets, copy, tests, browser/game QA, or review finding verification.

If subagents are unavailable, do the same work sequentially and keep moving.

## Child Task Template

```text
Use <project>/context.md. Continue inside the existing project folder.

Read scope:
- <project>/context.md
- <other allowed paths>

Write scope:
- <specific project paths or none>

Rules:
- read scope is exactly the paths above
- write scope is exactly the paths above
- publishing, deployment, commits, pushes, paid actions, credential inspection, and destructive cleanup stay with the main agent after explicit user approval

Task:
- <specific job>

Return:
- files changed
- commands run
- evidence found
- risks
- next recommended fix
```

## Loop

1. Create project folder and `context.md`.
2. Run discovery.
3. Assign at most one owner for the main app/runtime.
4. Assign independent work for assets, copy, tests, QA, or fixes.
5. Merge deliberately; inspect files before accepting or rejecting contradictory edits.
6. Run the project yourself.
7. Fix real bugs.
8. Repeat until complete or blocked.

Default unattended budgets; use bigger budgets when the user provides them:

- max 3 full implementation/review/fix cycles after first runnable proof
- max 2 retries for the same failing command or same reviewer finding
- ordinary shell commands should use a timeout or cancellable session when practical

When blocked, update `context.md` with the exact failing command, observed output, attempted fixes, blocker, and next command.
