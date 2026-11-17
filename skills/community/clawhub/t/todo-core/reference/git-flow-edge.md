# Git flow: rare branches

Read on demand from `reference/git-flow.md`, only when its pointers send you here: a tree claim whose fast-forward failed, `--worktree`, or a merge or rebase conflict. Part of the `todo` core skill.

## Failed fast-forward (tree claim step 5)

If the fast-forward in step 4 failed, stay on the base and read `git show <base>:TODO.md` again:

- **Lost or collided:** the root's `State:` there names another branch, or a root absent from the starting base has appeared there with the same ID. If your root branch is a bare claim branch, delete it with `git branch -D` (the only forced delete the skills make). Otherwise leave it and report it; preserve the pending backlog on that branch and print `git checkout <branch> -- <those paths>` so the user can restore it on the base after resolving any ID collision. Report the claimant or collision and stop, on the base.
- **The base only moved:** `git rebase <base> <root branch>` (this checks out the root branch; if it stops on a conflict, resolve `TODO.md`/`CHANGELOG.md` with the conflict rules below and `GIT_EDITOR=true git rebase --continue`, and for any other file `git rebase --abort`, `git switch <base>`, report and stop), lint, then `git switch <base> && git merge --ff-only <root branch>` once more and switch back to the root branch. If the base changed any file other than backlog files, take the baseline again on the root branch; if it is red and the node may not start red (`/todo-continue` step 3), stop and report (the claim stays; `/todo-update <ROOT-ID> --status ready` releases it). If this fails too, stop on the base and tell the user (your unpublished branch may stay; a rerun deletes it at step 2).

## `--worktree`

The main checkout is never switched; its unrelated changes are ignored by the clean-tree check, but pending backlog edits there refuse `--worktree` (stash other changes, run once without it so the claim commits the backlog edits, then restore). For an unclaimed tree: `git branch <root branch> <base>`, `mkdir -p ../<repo>.todo && git worktree add ../<repo>.todo/<ROOT-ID> <root branch>` (`<repo>`: the main checkout's folder name), take the baseline there (red: `git worktree remove` it, `git branch -d` the branch, stop), make the claim commit there, and fast-forward the base from the main checkout when it is on the base (`git merge --ff-only` works beside unrelated changes; otherwise stop and print the command). Create other missing branches with `git branch <branch> <from>`, add the node's worktree (`../<repo>.todo/<ID>`; a leaf root uses the root's) and make the start commit there. A child merge runs inside the node's worktree (if the parent's branch is checked out elsewhere, merge there when that checkout is clean, else stop and print the commands); then `cd` to the main checkout and `git worktree remove` the node's worktree (lane worktrees stay). The tree's next node is started from the root's worktree or branch.

## Git conflicts

- Never take one side wholesale (`--ours`/`--theirs`) on TODO.md or CHANGELOG.md.
- **CHANGELOG.md**: keep both sides' entries, drop duplicates of the same ID.
- **TODO.md**: keep the union of task blocks. If two roots share an ID, keep the one already in the base, renumber the newer one and its subtree, and rewrite every `Depends:` and `From:` that pointed into it; if the renumbered root is claimed, stop and ask instead. If an ID is now in both files, remove it from TODO.md.
- **Source files**: inside the node's scope, resolve minimally and rerun `Done when`; otherwise stop and ask.
- One agent per working tree. Use `--worktree` or lanes (`/todo-continue --all-lanes`) for parallel work.
