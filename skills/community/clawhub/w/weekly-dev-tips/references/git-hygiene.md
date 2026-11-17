# Git Hygiene Tips

## 1. Commit in small, logical chunks
One change per commit. It makes review, revert, and bisect far easier.

## 2. Write messages that explain *why*, not *what*
The diff already shows what. The message should explain the reasoning.

```
fix(auth): refresh token before expiry to avoid 401 storms

The old code waited for a 401 then retried, which caused a thundering
herd under load. Proactively refreshing 30s before expiry smooths it out.
```

## 3. Prefer `rebase` over `merge` for local branches
Keeps history linear. But **never rebase shared branches**.

## 4. `git add -p` for partial staging
Review each hunk before staging. Catches accidental debug prints.

## 5. Clean up merged branches
```bash
git branch --merged | grep -v main | xargs git branch -d
```

## 6. `git stash -u` includes untracked files
Plain `git stash` won't grab new files. `-u` does.

## 7. Use `git worktree` for parallel work
Work on two branches at once without stashing:
```bash
git worktree add ../feature-x feature/x
```
