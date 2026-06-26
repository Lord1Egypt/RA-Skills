---
name: structuring-git-workflow
description: Use when working in a git repository and about to start new work, complete a module, commit, push, merge, or rebase. Use before any destructive git operation. Use when you need to decide what branch to work on or how to structure commits.
---

# Structuring Git Workflow

## Overview

Imposes branch discipline, commit structure, and safety checks at every git decision point. The skill acts as a gate: it does not execute commands, it asks the right questions before you do.

**Violating the letter of these rules is violating the spirit of these rules.**

## When to Use

```
Starting new work?
  ├─ Yes → Create branch (Rule 1)
  └─ No → Continue

Module/feature complete?
  ├─ Yes → Remind about commit (Rule 2)
  └─ No → Continue

About to commit/push/merge/rebase?
  ├─ Yes → Run safety checklist (Rule 4)
  └─ No → Continue
```

## Core Rules

### Rule 1: Never Commit to Main/Master

All work happens on branches. When starting any task (feature, fix, refactor), create a branch first:

| Task type | Branch pattern | Example |
|-----------|---------------|---------|
| Feature | `feature/<name>` | `feature/user-login` |
| Bug fix | `fix/<name>` | `fix/login-timeout` |
| Refactor | `refactor/<name>` | `refactor/auth-middleware` |

If you catch yourself about to commit on main/master, stop and create a branch. If work already started on main, stash it, create a branch, then unstash.

### Rule 2: Remind About Commit at Module Boundaries

When a discrete unit of work is complete (a function, a component, a feature slice), proactively ask: "This module is complete. Commit it?"

Do not wait for the user to remember. The default answer is yes — most modules should be committed. If the user says no, respect it and move on.

### Rule 3: Structured Commit Messages

Commit messages follow a consistent format. The default format is:

```
<type>: <description>
```

Types: `feat`, `fix`, `refactor`, `style`, `docs`, `test`, `chore`

- First line under 72 characters
- Use imperative mood ("add" not "added")
- If the project CLAUDE.md or CONTRIBUTING.md specifies a different convention, follow that instead

### Rule 4: Safety Checklist Before Destructive Operations

Before `reset --hard`, `rebase`, `force push`, or `branch -D`:

1. Is this a shared branch? → Do not rewrite history
2. Do I have uncommitted changes? → Stash or commit first
3. Am I on the right branch? → `git branch` to verify
4. Is remote up to date? → `git fetch` first

State each check result explicitly before proceeding.

### Rule 5: Push Is a Separate Decision

Commit and push are distinct steps. Commit accumulates locally. After commits are verified (tests pass, no regressions), ask: "Ready to push?"

Never push automatically after commit. Never force-push to shared branches. Use `--force-with-lease` on feature branches only.

## Quick Reference

| Trigger | Action |
|---------|--------|
| Starting new work | Create `feature/` or `fix/` branch from main |
| Module complete | Remind user about commit |
| About to commit | Use structured message format |
| About to push | Verify first, ask user |
| Force push needed | `--force-with-lease` on feature branches only |
| Destructive operation | Run 4-point safety checklist |
| Work accidentally on main | Stash → create branch → unstash |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Committing directly to main | Always create a branch first |
| Commit message "fix stuff" | Describe the specific change |
| Pushing immediately after commit | Accumulate, verify, then push |
| Force push without checking | Run safety checklist first |
| Skipping branch for "small fix" | Small fixes go on `fix/` branches too |
| Amend pushed commits | Only amend local, unpushed commits |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| User insists on committing to main | Push back once: "This should go on a branch. Sure you want it on main?" If they confirm, comply. |
| Project initialization (first commit) | The initial commit (README, scaffold) is the only exception to Rule 1 |
| Collaborating on an existing branch | No need to create a new branch — commit to the existing feature/fix branch |
| Local repo, no remote | Rules 1-3 still apply. Rules 4-5 (push safety) are dormant until a remote is added |
| User's CLAUDE.md specifies different convention | Follow the project convention. This skill is the default, not an override |

## Red Flags — STOP

- "This is too small for a branch" → Even one-line fixes go on a branch
- "I'll branch after I start" → Branch first, then work
- "Nobody else works on this repo" → Discipline is habit, not circumstance-dependent
- "The user seems in a hurry" → Urgency is when mistakes happen. Follow the rules
- "The user told me to skip the branch" → Push back once, then comply if they insist
- "It's just a config tweak" → Config changes can break things. Use a branch

**All of these mean: Create the branch. Write the structured message. Run the checklist.**
