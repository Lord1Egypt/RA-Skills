---
name: local-merge
description: Use when landing a branch onto a target branch requires a safe local-git merge path that avoids mutating active worktrees directly, such as /ship, /reflect, or autonomous-mode integration work.
---

# /local-merge

Land a source branch onto a target branch through a disposable shallow clone, then update the `PRIMARY` worktree only if that worktree is already on the target branch.

Default target is `main`.

## Inputs

| Input | Required | Default | Example |
|---|---|---|---|
| `BRANCH` | yes | — | `feat/local-merge-skill` |
| `TARGET` | no | `main` | `develop`, `release/v2` |
| `PRIMARY` | no | primary worktree path | `/Users/you/projects/repo` |
| `MESSAGE` | no | `merge: $BRANCH into $TARGET` | `merge: feat/auth into main` |

## Operating model

Treat this as two separate problems:

1. **Remote integration**: merge the source branch into the target branch inside a disposable shallow clone, then push the updated target branch.
2. **Local propagation**: if `PRIMARY` is already on the target branch, update that worktree safely.

Do not assume that a successful remote integration means local propagation is also safe.

## Core invariants

- Use local git only for merge and publish operations.
- Prefer a disposable shallow clone as the integration workspace.
- Never discard tracked local state.
- Never silently choose merge versus rebase when a checked-out local target branch has local-only commits.
- Fast-forward automatically only when the local target is simply behind and otherwise cleanly updateable.
- Conflict means stop and return control to the user.
- Never force-push.
- Use absolute paths and `git -C <abs-path>` for state-changing commands.
- Validate refs before constructing shell commands.

## Primary resolution

Use the repo's primary worktree as `PRIMARY`.

If the primary worktree path is ambiguous, stop and ask the user instead of guessing from incidental ordering.

## Tracked-state shelter

When this skill needs to preserve tracked local changes before mutating a checked-out target branch, use one recipe consistently:

- stage tracked changes only
- create a temporary WIP commit
- record the temporary commit ref before continuing
- perform the branch update
- restore the exact tracked state with a soft reset of that temporary commit

Do not silently include untracked files in this sheltering step.

## Phase 1 — Remote integration

### 1. Resolve state

Determine:

- repo root
- source branch
- target branch
- remote name
- primary worktree path
- whether `PRIMARY` is currently on the target branch

Validate:

- source and target are valid branch refs
- the remote refs for both branches exist

Stop if:

- the source branch is detached
- the source branch is not published and cannot be pushed cleanly

If the source branch is unpublished but can be pushed cleanly, push it first and continue. The source branch must be published before remote integration begins.

If the source worktree has tracked local changes that are not represented in the published branch, stop. `local-merge` integrates published branch state only; it does not shelter or merge source-side dirty state as part of Phase 1.

### 2. Build the integration workspace

Create a disposable shallow clone from the repo's remote URL.

Fetch only what is needed:

- `<remote>/$TARGET`
- `<remote>/$BRANCH`

Ensure the clone has enough history to merge and, if needed, retry safely. If shallow history is insufficient, deepen deliberately or stop and report the limitation.

### 3. Merge source into target

Check out the target branch in the shallow clone and merge the source branch into it.

Default to a normal merge. If the merge is already a fast-forward, accept it.

If there is a conflict:

- stop immediately
- surface the conflict clearly
- do not auto-resolve
- do not continue to push

### 4. Push target

Push the updated target branch from the shallow clone.

If the push is rejected because the remote moved, one retry strategy is allowed:

- refresh the target branch in the shallow clone
- rebuild the integration commit or rebase only inside the disposable clone
- retry only if the refreshed state does not introduce a new human-choice point

Stop immediately if the retry itself conflicts or becomes ambiguous.

Maximum retries: 3. Never force-push.

Cleanup failure for the disposable clone is non-blocking.

## Phase 2 — Local propagation

Only run this phase if `PRIMARY` is already on the target branch.

If `PRIMARY` is on some other branch, report that remote integration succeeded and leave local propagation untouched.

### 1. Inspect local target state

Gather enough evidence to classify the local target state:

- whether the worktree has tracked local changes
- whether local `$TARGET` is behind `<remote>/$TARGET`
- whether local `$TARGET` has commits not on `<remote>/$TARGET`
- whether the branch is fast-forwardable or diverged
- whether incoming and local-only changes overlap in a way that is operationally risky even if git would merge cleanly

Use standard git evidence:

- status
- ahead and behind counts
- incoming commit log
- local-only commit log
- diff stat

### 2. Update local target branch

**Case: clean and only behind**

Fast-forward automatically to `<remote>/$TARGET`.

**Case: tracked local changes and only behind**

Use the tracked-state shelter, fast-forward to `<remote>/$TARGET`, then restore the sheltered tracked state.

**Case: local target has commits not on `<remote>/$TARGET`**

Do not silently rewrite or merge.

Ask the user whether to:

- rebase local commits onto the updated remote target
- merge the updated remote target into the local target

If tracked local changes are also present, use the tracked-state shelter before that operation and restore it afterward.

Once the user chooses merge or rebase, the agent may execute that choice. If the chosen operation conflicts, stop immediately, preserve the shelter reference if one exists, and return control to the user.

This is an intentional policy tightening from the current skill. Even if a low-risk auto-merge might be possible, this version treats any local-only target commits as a human-choice point.

**Case: semantic risk or ambiguity**

If git says a merge is possible but the overlapping area is operationally risky, stop and escalate instead of treating "no textual conflict" as "safe."

Examples:

- related config spread across files
- hooks and supporting scripts changed in parallel
- command contract changes that may invalidate local assumptions

## Finish

Report:

- whether remote integration succeeded
- whether local propagation ran
- whether the local target was fast-forwarded, escalated, or left untouched
- whether tracked state was sheltered
- any user decision still required

## Safety rules

- No force-push
- No hard reset unless explicitly directed
- No silent conflict resolution
- No silent merge-versus-rebase choice for divergent local target branches
- Preserve human state over automation

## Output format

```text
Source branch: <branch>
Target branch: <target>
Remote: <remote>

Remote integration:
- source branch published: yes/no
- shallow clone merge: clean/conflict
- target pushed: yes/no

Local propagation:
- primary on target: yes/no
- tracked state shelter used: yes/no
- result: fast-forward / user decision required / conflict / skipped

If action is required:
- reason
- exact worktree or branch involved
- whether tracked state is currently sheltered
```
