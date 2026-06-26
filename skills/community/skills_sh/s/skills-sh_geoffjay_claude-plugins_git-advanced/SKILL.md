---
name: git-advanced
description: Advanced git operations including complex rebase strategies, interactive staging, commit surgery, and history manipulation. Use when user needs to perform complex git operations like rewriting history or advanced merging.
---

# Git Advanced Operations Skill

This skill provides comprehensive guidance on advanced git operations, sophisticated rebase strategies, commit surgery techniques, and complex history manipulation for experienced git users.

## When to Use

Activate this skill when:
- Performing complex interactive rebases
- Rewriting commit history
- Splitting or combining commits
- Advanced merge strategies
- Cherry-picking across branches
- Commit message editing in history
- Author information changes
- Complex conflict resolution

## Interactive Rebase Strategies

### Basic Interactive Rebase

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Rebase from specific commit
git rebase -i abc123^

# Rebase entire branch
git rebase -i main
```

### Rebase Commands

```bash
# Interactive rebase editor commands:
# p, pick = use commit
# r, reword = use commit, but edit commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like squash, but discard commit message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
```

### Squashing Commits

```bash
# Example: Squash last 3 commits
git rebase -i HEAD~3

# In editor:
pick abc123 feat: add user authentication
squash def456 fix: resolve login bug
squash ghi789 style: format code

# Squash all commits in feature branch
git rebase -i main
# Mark all except first as 'squash'
```

### Fixup Workflow

```bash
# Create fixup commit automatically
git commit --fixup=abc123

# Autosquash during rebase
git rebase -i --autosquash main

# Set autosquash as default
git config --global rebase.autosquash true

# Example workflow:
git log --oneline -5
# abc123 feat: add authentication
# def456 feat: add authorization
git commit --fixup=abc123
git rebase -i --autosquash HEAD~3
```

### Reordering Commits

```bash
# Interactive rebase
git rebase -i HEAD~5

# In editor, change order:
pick def456 feat: add database migration
pick abc123 feat: add user model
pick ghi789 feat: add API endpoints

# Reorder by moving lines:
pick abc123 feat: add user model
pick def456 feat: add database migration
pick ghi789 feat: add API endpoints
```

### Splitting Commits

```bash
# Start interactive rebase
git rebase -i HEAD~3

# Mark commit to split with 'edit'
edit abc123 feat: add user and role features

# When rebase stops:
git reset HEAD^

# Stage and commit parts separately
git add user.go
git commit -m "feat: add user management"

git add role.go
git commit -m "feat: add role management"

# Continue rebase
git rebase --continue
```

### Editing Old Commits

```bash
# Start interactive rebase
git rebase -i HEAD~5

# Mark commit with 'edit'
edit abc123 feat: add authentication

# When rebase stops, make changes
git add modified-file.go
git commit --amend --no-edit

# Or change commit message
git commit --amend

# Continue rebase
git rebase --continue
```

## Commit Surgery

### Amending Commits

```bash
# Amend last commit (add changes)
git add forgotten-file.go
git commit --amend --no-edit

# Amend commit message
git commit --amend -m "fix: correct typo in feature"

# Amend author information
git commit --amend --author="John Doe <john@example.com>"

# Amend date
git commit --amend --date="2024-03-15 10:30:00"
```

### Changing Commit Messages

```bash
# Change last commit message
git commit --amend

# Change older commit messages
git rebase -i HEAD~5
# Mark commits with 'reword'

# Change commit message without opening editor
git commit --amend -m "new message" --no-edit
```

### Changing Multiple Authors

```bash
# Filter-branch (legacy method, use filter-repo instead)
git filter-branch --env-filter '
if [ "$GIT_COMMITTER_EMAIL" = "old@example.com" ]; then
    export GIT_COMMITTER_NAME="New Name"
    export GIT_COMMITTER_EMAIL="new@example.com"
fi
if [ "$GIT_AUTHOR_EMAIL" = "old@example.com" ]; then
    export GIT_AUTHOR_NAME="New Name"
    export GIT_AUTHOR_EMAIL="new@example.com"
fi
' --tag-name-filter cat -- --branches --tags

# Modern method with git-filter-repo
git filter-repo --email-callback '
    return email.replace(b"old@example.com", b"new@example.com")
'
```

### Removing Files from History

```bash
# Remove file from all history
git filter-branch --tree-filter 'rm -f passwords.txt' HEAD

# Better performance with index-filter
git filter-branch --index-filter 'git rm --cached --ignore-unmatch passwords.txt' HEAD

# Modern method with git-filter-repo (recommended)
git filter-repo --path passwords.txt --invert-paths

# Remove large files
git filter-repo --strip-blobs-bigger-than 10M
```

### BFG Repo-Cleaner

```bash
# Install BFG
# brew install bfg (macOS)
# apt-get install bfg (Ubuntu)

# Remove files by name
bfg --delete-files passwords.txt

# Remove large files
bfg --strip-blobs-bigger-than 50M

# Replace passwords in history
bfg --replace-text passwords.txt

# After BFG cleanup
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## Advanced Cherry-Picking

### Basic Cherry-Pick

```bash
# Cherry-pick single commit
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456 ghi789

# Cherry-pick range of commits
git cherry-pick abc123..ghi789

# Cherry-pick without committing (stage only)
git cherry-pick -n abc123
```

### Cherry-Pick with Conflicts

```bash
# When conflicts occur
git cherry-pick abc123
# CONFLICT: resolve conflicts

# After resolving conflicts
git add resolved-file.go
git cherry-pick --continue

# Or abort cherry-pick
git cherry-pick --abort

# Skip current commit
git cherry-pick --skip
```

### Cherry-Pick Options

```bash
# Edit commit message during cherry-pick
git cherry-pick -e abc123

# Sign-off cherry-picked commit
git cherry-pick -s abc123

# Keep original author date
git cherry-pick --ff abc123

# Apply changes without commit attribution
git cherry-pick -n abc123
git commit --author="New Author <new@example.com>"
```

### Mainline Selection for Merge Commits

```bash
# Cherry-pick merge commit (specify parent)
git cherry-pick -m 1 abc123

# -m 1 = use first parent (main branch)
# -m 2 = use second parent (merged branch)

# Example workflow:
git log --graph --oneline
#   *   abc123 Merge pull request #123
#   |\
#   | * def456 feat: feature commit
#   * | ghi789 fix: main branch commit

# To cherry-pick the merge keeping main branch changes:
git cherry-pick -m 1 abc123
```

## Advanced Merging

### Merge Strategies

```bash
# Recursive merge (default)
git merge -s recursive branch-name

# Ours (keep our changes on conflict)
git merge -s ours branch-name

# Theirs (keep their changes on conflict)
git merge -s theirs branch-name

# Octopus (merge 3+ branches)
git merge -s octopus branch1 branch2 branch3

# Subtree merge
git merge -s subtree branch-name
```

### Merge Strategy Options

```bash
# Ours (resolve conflicts with our version)
git merge -X ours branch-name

# Theirs (resolve conflicts with their version)
git merge -X theirs branch-name

# Ignore whitespace
git merge -X ignore-space-change branch-name
git merge -X ignore-all-space branch-name

# Patience algorithm (better conflict detection)
git merge -X patience branch-name

# Renormalize line endings
git merge -X renormalize branch-name
```

### Three-Way Merge

```bash
# Standard three-way merge
git merge feature-branch

# With custom merge message
git merge feature-branch -m "Merge feature: add authentication"

# No fast-forward (always create merge commit)
git merge --no-ff feature-branch

# Fast-forward only (fail if merge commit needed)
git merge --ff-only feature-branch

# Squash merge (combine all commits)
git merge --squash feature-branch
git commit -m "feat: add complete authentication system"
```

## Advanced Conflict Resolution

### Understanding Conflict Markers

```
<<<<<<< HEAD (Current Change)
int result = add(a, b);
=======
int sum = calculate(a, b);
>>>>>>> feature-branch (Incoming Change)
```

### Conflict Resolution Tools

```bash
# Use mergetool
git mergetool

# Specify merge tool
git mergetool --tool=vimdiff
git mergetool --tool=meld
git mergetool --tool=kdiff3

# Configure default merge tool
git config --global merge.tool vimdiff
git config --global mergetool.vimdiff.cmd 'vimdiff "$LOCAL" "$MERGED" "$REMOTE"'

# Check out specific version
git checkout --ours file.go    # Keep our version
git checkout --theirs file.go  # Keep their version
git checkout --merge file.go   # Recreate conflict markers
```

### Rerere (Reuse Recorded Resolution)

```bash
# Enable rerere
git config --global rerere.enabled true

# Rerere will automatically resolve previously seen conflicts
git merge feature-branch
# Conflict occurs and is resolved
git add file.go
git commit

# Later, same conflict:
git merge another-branch
# Rerere automatically applies previous resolution

# View rerere cache
git rerere status
git rerere diff

# Clear rerere cache
git rerere forget file.go
git rerere clear
```

## Interactive Staging

### Partial File Staging

```bash
# Interactive staging
git add -p file.go

# Patch commands:
# y - stage this hunk
# n - do not stage this hunk
# q - quit (do not stage this and remaining hunks)
# a - stage this and all remaining hunks
# d - do not stage this and all remaining hunks
# s - split the current hunk into smaller hunks
# e - manually edit the current hunk
```

### Interactive Add

```bash
# Interactive mode
git add -i

# Commands:
# 1: status       - show paths with changes
# 2: update       - stage paths
# 3: revert       - unstage paths
# 4: add untracked - stage untracked files
# 5: patch        - partial staging
# 6: diff         - show staged changes
# 7: quit         - exit
```

### Partial Commits

```bash
# Stage part of file interactively
git add -p file.go

# Create commit with partial changes
git commit -m "feat: add validation logic"

# Stage remaining changes
git add file.go
git commit -m "feat: add error handling"
```

## Advanced Reset Operations

### Reset Modes

```bash
# Soft reset (keep changes staged)
git reset --soft HEAD~1

# Mixed reset (keep changes unstaged, default)
git reset --mixed HEAD~1
git reset HEAD~1

# Hard reset (discard all changes)
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard abc123
```

### Reset vs Revert

```bash
# Reset (rewrites history, use for local changes)
git reset --hard HEAD~3

# Revert (creates new commit, safe for shared history)
git revert HEAD
git revert HEAD~3
git revert abc123..def456
```

## Advanced Branch Operations

### Branch from Specific Commit

```bash
# Create branch from commit
git branch new-branch abc123
git checkout new-branch

# Or in one command
git checkout -b new-branch abc123

# Create branch from remote commit
git checkout -b local-branch origin/remote-branch
```

### Orphan Branches

```bash
# Create orphan branch (no parent)
git checkout --orphan new-root
git rm -rf .

# Useful for gh-pages, documentation, etc.
echo "# Documentation" > README.md
git add README.md
git commit -m "docs: initialize documentation"
```

### Branch Tracking

```bash
# Set upstream branch
git branch -u origin/main

# Push and set upstream
git push -u origin feature-branch

# Change upstream
git branch -u origin/develop

# View tracking information
git branch -vv
```

## Advanced Stash Operations

### Stash Specific Files

```bash
# Stash specific files
git stash push -m "WIP: feature work" file1.go file2.go

# Stash with pathspec
git stash push -p

# Stash untracked files
git stash -u

# Stash including ignored files
git stash -a
```

### Stash to Branch

```bash
# Create branch from stash
git stash branch new-branch stash@{0}

# Creates new branch and applies stash
git stash branch feature-work
```

### Partial Stash Application

```bash
# Apply specific files from stash
git checkout stash@{0} -- file.go

# Apply stash without dropping
git stash apply stash@{0}

# Apply and drop
git stash pop stash@{0}
```

## Submodule Management

### Advanced Submodule Operations

```bash
# Update submodule to specific commit
cd submodule-dir
git checkout abc123
cd ..
git add submodule-dir
git commit -m "chore: update submodule to version 1.2.3"

# Update all submodules to latest
git submodule update --remote --merge

# Update specific submodule
git submodule update --remote --merge path/to/submodule

# Run command in all submodules
git submodule foreach 'git checkout main'
git submodule foreach 'git pull'

# Clone with submodules at specific depth
git clone --recurse-submodules --depth 1 repo-url
```

### Submodule to Subtree Migration

```bash
# Remove submodule
git submodule deinit path/to/submodule
git rm path/to/submodule
rm -rf .git/modules/path/to/submodule

# Add as subtree
git subtree add --prefix=path/to/submodule \
    https://github.com/user/repo.git main --squash

# Update subtree
git subtree pull --prefix=path/to/submodule \
    https://github.com/user/repo.git main --squash
```

## Advanced Log and History

### Custom Log Formatting

```bash
# One-line format with custom fields
git log --pretty=format:"%h - %an, %ar : %s"

# Full custom format
git log --pretty=format:"%C(yellow)%h%C(reset) %C(blue)%ad%C(reset) %C(green)%an%C(reset) %s" --date=short

# Aliases for common formats
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
```

### Finding Lost Commits

```bash
# Find commits not in any branch
git log --all --oneline --no-walk --decorate $(git fsck --no-reflog | grep commit | cut -d' ' -f3)

# Find dangling commits
git fsck --lost-found

# Search commit messages
git log --all --grep="search term"

# Find commits by author
git log --author="John Doe"

# Find commits modifying specific code
git log -S "function_name"
git log -G "regex_pattern"
```

### Bisect Automation

```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good abc123

# Automate bisect with script
git bisect run ./test.sh

# test.sh example:
#!/bin/bash
make && make test
exit $?

# Bisect will automatically find first bad commit
```

## Best Practices

1. **Backup Before History Rewriting:** Create backup branch before complex operations
2. **Never Rewrite Published History:** Only rewrite local commits
3. **Communicate Rebases:** Inform team when force-pushing
4. **Use Descriptive Commit Messages:** Even during interactive rebase
5. **Test After Rebase:** Ensure code still works after history changes
6. **Prefer Rebase for Local Branches:** Keep history linear
7. **Use Merge for Shared Branches:** Preserve complete history
8. **Sign Important Commits:** Use GPG signing for releases
9. **Document Complex Operations:** Leave comments for future reference
10. **Know When to Stop:** Sometimes merge commits are clearer than rebased history

## Resources

Additional guides and examples are available in the `assets/` directory:
- `examples/` - Complex rebase and merge scenarios
- `scripts/` - Automation scripts for common operations
- `workflows/` - Advanced workflow patterns

See `references/` directory for:
- Git internals documentation
- Advanced rebasing strategies
- Filter-branch alternatives
- Conflict resolution techniques
