---
name: summarize-outstanding-work
description: Summarize all outstanding work not merged into main/default branch (including unmerged branches, open PRs, uncommitted changes, and stashes)
---

# summarize-outstanding-work

Retrieve and generate a comprehensive summary of all outstanding work in the specified (or active) repository that has not yet been merged into the default branch (e.g., `main` or `master`).

## Core Directives

1. **Verify Target Repository & Environment**:
   - Confirm that the target directory is a Git repository.
   - Dynamically identify the default/primary branch name (e.g., `main` or `master`). Do not assume. You can determine it via:
     - `git symbolic-ref refs/remotes/origin/HEAD` (extract the basename)
     - Or fallback by checking if `main` or `master` exists.
   - If permitted, run `git fetch origin --prune` to ensure you are checking the latest remote state. If not permitted or offline, clearly note that the report uses cached/local state.

2. **Collect Local Work-in-Progress**:
   - Run `git status -s` to list any uncommitted (staged or unstaged) and untracked changes in the working tree.
   - Run `git stash list` to inspect any stashes. Note the stash index, description, and creation time.

3. **Check Sync Status of the Default Branch**:
   - Determine if the default branch is in sync with its remote upstream counterpart:
     - `git rev-list --left-right --count <default-branch>...origin/<default-branch>` (if origin is configured).

4. **Collect Open Pull Requests (GitHub CLI)**:
   - If the `gh` command-line tool is installed and authenticated:
     - List open PRs: `gh pr list --state open --json number,title,headRefName,author,updatedAt,isDraft,mergeStateStatus`
     - Get the general PR status and check details: `gh pr status`

5. **Collect Unmerged Branches**:
   - List local branches that are not merged into the default branch:
     - `git branch --no-merged <default-branch>`
   - List remote branches that are not merged into the remote default branch:
     - `git branch -r --no-merged origin/<default-branch>`
   - For each unmerged branch (focusing on unique or active branches, and cross-referencing them with open PRs):
     - Determine the number of commits it is ahead/behind relative to the default branch:
       - `git rev-list --left-right --count origin/<default-branch>...<branch>`
     - Retrieve the author, last commit date, and a snippet of the latest commits:
       - `git log -n 3 origin/<default-branch>..<branch> --oneline --format="%h - %an, %ar : %s"`
     - Display a brief diff stat if the branch is small enough and it adds helpful context:
       - `git diff --stat origin/<default-branch>..<branch>`

6. **Generate the Summary Report**:
   - Structure the output as a clean, professional Markdown report or artifact.
   - Include the following sections:
     - **Repository Overview**: Current branch, detected default branch, remote tracking status.
     - **Local Work-in-Progress**: Lists of modified/untracked files and recent stashes.
     - **Open Pull Requests**: Table of open PRs (number, title, branch, author, last updated, status, draft/ready).
     - **Unmerged Branches (No PR)**: List of branches that are ahead of the default branch but do not have an open PR. Show commit count ahead, last active author, relative time since last commit, and recent commit messages.
     - **Recommendations / Next Steps**: Highlight inactive branches (potential cleanup candidates), PRs with conflicts/failing CI, and branches ready to be merged or have PRs created.
