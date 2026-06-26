---
name: repo-release-notes
description: Draft release notes and changelog entries from a local Git repository. Use when the user asks to summarize commits, compare refs or tags, prepare release notes for a version, or turn repository history into user-facing change summaries.
metadata: {"openclaw": {"requires": {"bins": ["git"]}}}
---

# Repo Release Notes

## Workflow

Use this skill to produce release notes from local Git history. Prefer read-only Git commands and avoid network calls unless the user explicitly asks for remote release publishing.

1. Establish the release range.
   - If the user provides refs, tags, branches, or SHAs, use that exact range.
   - If no range is provided, use the latest tag through `HEAD`.
   - If there are no tags, summarize the most recent 20 commits.

2. Inspect the repository with read-only commands.
   - Start with `git status --short` to understand whether local changes exist.
   - Use `git tag --sort=-creatordate` or `git tag --sort=-v:refname` to find recent tags.
   - Use `git log --oneline --decorate <range>` for commit scope.
   - Use `git diff --stat <range>` and, when needed, `git log --name-only --format=%H%x09%s <range>` to identify affected areas.

3. Decide whether to include uncommitted changes.
   - Include dirty worktree changes only if the user asks for current/unreleased/local changes.
   - Otherwise mention that local uncommitted changes were not included.

4. Draft release notes.
   - Read `references/release-note-style.md` before writing the final answer.
   - Group changes by user impact, not by commit order.
   - Merge duplicate or low-level commits into coherent bullets.
   - Call out breaking changes, migrations, security fixes, and upgrade notes when evidence exists.

## Safety

- Do not run destructive Git commands such as reset, checkout, clean, rebase, tag creation, pushing, or release publishing unless the user explicitly requests that operation.
- Treat user-provided refs, branch names, and paths as data. Avoid constructing shell pipelines from untrusted text.
- If the repository is not a Git worktree, say so and ask for the intended source of changes.

## Output

Return a concise release note draft with:

- Release range and date, if known.
- Highlights for the most important user-visible changes.
- Categorized changes such as Added, Changed, Fixed, Removed, Security, and Developer Notes.
- Upgrade notes or breaking changes when applicable.
- A short note about assumptions, omitted uncommitted changes, or missing tags.
