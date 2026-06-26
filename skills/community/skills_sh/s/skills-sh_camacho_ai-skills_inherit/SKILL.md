---
name: inherit
description: Use when pulling/syncing/updating/absorbing changes from a branch's parent (typically main) into the current branch, or cascading parent changes through a stack of dependent branches. Triggers on "pull from main", "merge main in", "update from parent", "sync from base", "catch up to main", "absorb parent changes", "rebase onto main" (intent only — implementation uses merge), "update the stack", "/inherit", or "my branch is behind". Pairs with /isolate (forks from parent) and /ship (pushes to target).
---

# inherit

Mental model: **"I am the child. I want what my parent has."**

Brings the current branch (and optionally its descendants) up to date with its parent. Inbound counterpart to `/ship` (outbound to a target) and `/isolate` (forks a new child from a parent).

## When to use

- Current branch is stale relative to its base.
- A stack of dependent branches needs the parent's latest commits cascaded down.
- Web sessions or minimal environments where `wt`, `git-trim`, `gh` aren't available.

**Do NOT use** to send changes upward — that's `/ship`. Do NOT use to create a new branch — that's `/isolate`.

## Why merge, not rebase

Autonomous mode's `git-rewrite-guard.sh` blocks `git rebase`, `--amend`, `reset --hard`, and `push --force*`. Merge is also the parallel-worktree community standard for syncing from base — non-destructive, composes with stacks, never requires a force-push, safe under shared checkouts. **Always `git merge`, never `git rebase`** in this skill.

## Constraints

- Pure git only. No `wt`, `git-trim`, or `gh` for the merge step. Works in web sandboxes.
- Always `git -C <abs-path>` for state-mutating ops. `cd` does not persist between Claude Code Bash calls; bare `git` from session CWD hits the primary worktree.
- Never auto-resolve conflicts. The user owns conflict resolution.

## Inputs

| Flag | Purpose |
|---|---|
| `--stack` | Cascade the merge bottom-up through dependent branches |
| `--parent <name>` | Override auto-detected parent |
| `--no-push` | Skip the push step (commits stay local) |

CI-down signal: same convention as `/ship` — if user has signaled CI is down, substitute `/local-merge` for each `git push`.

## Procedure

### 1. Resolve current branch + repo root

```bash
REPO="$(git rev-parse --show-toplevel)"
CURRENT="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
```

Pre-flight aborts:
- `CURRENT` is `HEAD` (detached) → "No current branch — checkout a branch first."
- Working tree dirty (`git -C "$REPO" status --porcelain` non-empty) → "Commit or stash local changes before inheriting."

### 2. Detect parent (unless `--parent` was passed)

```bash
PARENT=$(git -C "$REPO" reflog show HEAD --pretty=format:'%gs' \
  | grep -m1 '^branch: Created from ' \
  | sed -E 's/^branch: Created from //; s|^origin/||')
PARENT="${PARENT:-main}"
```

- `grep -m1` picks the most recent "Created from" — that's the actual fork point.
- Strip leading `origin/` so we work in branch-name space.
- Fall back to `main` when reflog is empty (web sessions, fresh clones, branches created via fetch). Tell the user it was a fallback so they can correct via `--parent`.
- If `PARENT == CURRENT` after resolution → "Already on parent branch; nothing to inherit."

Echo before mutating: `Detected parent: <PARENT> (current: <CURRENT>). Inheriting from origin/<PARENT>.`

### 3. Fetch the parent

```bash
git -C "$REPO" fetch origin "$PARENT"
```

If fetch fails (offline, ref missing, parent deleted on origin): surface the error verbatim. Do NOT silently substitute another branch.

### 4. Merge parent into current

```bash
git -C "$REPO" merge --no-edit "origin/$PARENT"
```

Outcomes:
- **Clean (real merge or fast-forward)** → proceed.
- **No-op (already up to date)** → say so plainly and skip the push.
- **Conflict** → stop, show `git status`, list conflicted paths, hand control back. Do NOT attempt automatic resolution.

### 5. Cascade through stack (only if `--stack`)

A "dependent" is a local branch with `CURRENT` as an ancestor. The user supplies the candidate set after `--stack` (or names them inline); don't guess silently — if the user didn't name them, ask once.

**Order: bottom-up, parent-first.** Use pairwise `git merge-base --is-ancestor` to find topological order — at each step, pick a branch in the remaining set that no other remaining branch is an ancestor of. That branch goes next:

```bash
# B is downstream of A iff A is an ancestor of B
git -C "$REPO" merge-base --is-ancestor "$A" "$B"  # exit 0 = yes
```

For each branch in that order, merge its **direct parent in the chain** (the previous branch processed) — NOT `origin/main` again. The whole point of cascading is that the parent already absorbed main, and now the child absorbs the updated parent:

```bash
PREV="$CURRENT"
for child in "${ordered[@]}"; do
  git -C "$REPO" checkout "$child"
  git -C "$REPO" merge --no-edit "$PREV"   # stop on conflict
  PREV="$child"
done
git -C "$REPO" checkout "$CURRENT"
```

On conflict: stop the cascade. Report which branch wedged and which paths conflict. Do NOT skip forward.

### 6. Push (or `/local-merge` if CI is down)

For each branch that received commits (`CURRENT` plus any cascaded children):

```bash
git -C "$REPO" push origin "$BRANCH"
```

If user has signaled CI is down: invoke `/local-merge` per branch instead.
If `--no-push` was passed: skip entirely; tell the user the branch(es) have local merge commits awaiting publish.
If push is rejected (remote moved): do NOT force. Report the rejection; the user decides whether to re-run `/inherit`.

### 7. Report

Concise summary, not paragraphs:

```
Inherited from <PARENT> into:
  - <CURRENT>   (merge <sha>, pushed)
  - <child-1>   (merge <sha>, pushed)
```

On conflict:

```
Inherit halted on <branch>: conflicts in <files>. Resolve, commit, then re-run /inherit.
```

## Quick reference

| Step | Command |
|---|---|
| Detect parent | `git reflog show HEAD --pretty=format:'%gs' \| grep -m1 '^branch: Created from'` |
| Fetch | `git -C "$REPO" fetch origin "$PARENT"` |
| Merge in | `git -C "$REPO" merge --no-edit "origin/$PARENT"` |
| Stack order | `git merge-base --is-ancestor <a> <b>` pairwise, root-first |
| Push | `git -C "$REPO" push origin <branch>` |
| CI down | `/local-merge` per branch |

## Failure modes — explicit counters

| Rationalization | Counter |
|---|---|
| "Rebase is cleaner — I'll just rebase onto main" | **Forbidden.** Rewrite-guard blocks it in autonomous mode. Use merge. |
| "Reflog is empty, I'll guess from branch-name patterns" | Fall back to `main`. Tell the user. Do not infer from naming. |
| "I'll force-push after a tidy rebase" | **Forbidden.** No `--force`, `--force-with-lease`, or `--amend` in this skill. |
| "I'll use `git pull --rebase`" | Same prohibition as `git rebase`. Use plain `git merge`. |
| "I'll use `wt sync` / `git-trim`" | Pure git only — those binaries aren't in web sessions. |
| "Stack order doesn't matter, I'll merge in any order" | Merge bottom-up (root-adjacent first) so each child sees its updated parent. |
| "I'll skip the push" | Push each updated branch unless CI-down or `--no-push` applies. |
| "Conflict? I'll auto-resolve with `-X theirs`" | **Never.** The user owns conflict resolution. Stop and report. |

## Red flags — STOP

- About to type `git rebase`, `--amend`, `reset --hard`, or `--force` → wrong skill.
- Parent detection silently returned empty and you didn't fall back to `main`.
- Merging top-down through a stack (parent-most last) → reverse the order.
- Bare `git` without `-C` from session CWD on a non-primary worktree.
- Modifying files outside git operations — this skill is pure git.

## Companion skills

- **`/isolate`** — forks a new child off a parent.
- **`/inherit`** (this skill) — pulls parent → child. **Inbound.**
- **`/ship`** — pushes child → target. **Outbound.**

Three directions a branch moves: fork off, sync down, ship up.

## Example invocations

- "pull main into this branch" → `/inherit`
- "update my stack from main" → `/inherit --stack`
- "sync from base but don't push yet" → `/inherit --no-push`
- "catch up to develop instead of main" → `/inherit --parent develop`
