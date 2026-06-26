---
name: ship
description: Use when implementation is complete, tests pass, and code needs to reach main — via PR with auto-merge (CI up) or local shallow-clone merge (CI down)
---

# Ship

Get the branch onto main. Two paths: PR (CI up) or local merge (CI down).

**Announce:** "Using /ship to integrate this branch."

## Prerequisites

1. On a feature branch (not main).
2. `/review` (Step 6) passed, or user explicitly approved.
3. Worktree path is known (needed for cleanup).
4. **No pending tasks.** Run `TaskList` (Claude Code) or check `.branch-context.md` checklist (Codex). If any step is still `pending` or `in_progress`, that step was skipped — go back and complete it before shipping.

If any prerequisite is missing, say which and stop.

## Step 1: Validate

```bash
pnpm validate
```

If validation fails, stop. Fix first.

## Step 2: Determine target branch

Resolution order (use the first that succeeds):

1. **Plan file frontmatter** — read the `Target:` field from `ai-workspace/plans/<name>.md` if a plan exists.
2. **Reflog parent** — the branch's reflog records what it was created from:
   ```bash
   TARGET=$(
     git -C <worktree> reflog show HEAD --pretty=format:'%gs' \
       | grep "^branch: Created from" \
       | head -1 \
       | sed 's/branch: Created from //' \
       | sed 's|^origin/||'
   )
   ```
3. **Remote HEAD** — `git -C <worktree> symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'`
4. **Default `main`** — final fallback. If ambiguous between sources, ask.

## Step 3: Present options

CI status comes from conversation context — if the user has said CI is down, frozen, or at billing cap, treat as down. No auto-detection.

**CI up (default):**

```
Ready to ship.

1. Open PR + auto-merge
2. Keep branch as-is
3. Discard
```

**CI down:**

```
Ready to ship (CI down — local merge with review gate).

1. Local merge to main
2. Keep branch as-is
3. Discard
```

## Option 1a: PR + auto-merge (CI up)

```bash
git -C <worktree> push -u origin <branch>

GH_REPO=<owner/repo> gh pr create \
  --base "$TARGET" \
  --title "<conventional-commit-title>" \
  --body "$(cat <<'EOF'
## Summary
<2-3 bullets>

## Test plan
- [ ] <verification steps>
EOF
)"

GH_REPO=<owner/repo> gh pr merge --auto --merge
```

Report the PR URL. Proceed to worktree cleanup.

**If CI blocks or fails after PR is up:** STOP. Ask the user. No self-rescue, no local merge fallback, no force-merge.

## Option 1b: Local merge (CI down)

Dispatch the `code-reviewer` agent on the diff first — all autonomous code must be reviewed before merge:

```bash
claude --agent code-reviewer "Review diff: git -C <worktree> diff $TARGET..HEAD"
```

If reviewer returns P0/P1 findings, STOP. Fix before proceeding.

Invoke `/local-merge` with BRANCH=`<branch>`, TARGET=`$TARGET`, PRIMARY=`<primary-worktree-path>`, MESSAGE=`"merge: <branch> into $TARGET"`. It handles the shallow clone, push with retry, and non-destructive propagation to primary.

## Option 2: Keep as-is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

Do not clean up.

## Option 3: Discard

Require typed "discard" confirmation. Show branch name, commit list, worktree path.

```bash
git -C <primary> worktree remove <worktree-path>
git -C <primary> branch -d <branch>
```

If `branch -d` fails (unmerged work), warn the user and stop — do NOT use `branch -D`. Only delete the remote branch after local delete succeeds:

```bash
git push origin --delete <branch>
```

## Worktree Cleanup

After PR (1a) or local merge (1b):

```bash
# Unlock first (matches the lock applied by /isolate)
git -C <primary> worktree unlock <worktree-path> 2>/dev/null || true
git -C <primary> worktree remove <worktree-path>
```

Then prune the dead branch from local refs if `git-trim` is installed (handles squash-merged, rebase-merged, and `[gone]` upstream cases):

```bash
if command -v git-trim >/dev/null 2>&1; then
  git -C <primary> trim --delete
fi
```

| Path | Cleanup worktree? |
|---|---|
| PR + auto-merge | Yes |
| Local merge | Yes |
| Discard | Yes (in discard step) |
| Keep as-is | No |

## Integration

**Called by:** /task (Step 8)
**Pairs with:** /isolate (cleans up worktree it created), /review (must pass before /ship)
