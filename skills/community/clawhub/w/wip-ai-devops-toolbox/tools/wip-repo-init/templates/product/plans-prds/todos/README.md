# todos/

One todo file per person or agent. Three sections per file: To Do, Done, Deprecated.

## What This Folder Is

Todos that are specific to this repo. Each person or agent who works on this repo gets one file. The file tracks what they need to do, what they've done, and what got dropped.

For cross-repo work or bigger items, use GitHub Issues. Todos here are for repo-scoped tasks that don't need the overhead of an issue.

## Files

One file per person/agent. Name it `[Name]-todo.md`.

Example:

| File | Who |
|------|-----|
| `Parker-todo.md` | Parker (human tasks: reviews, credentials, approvals) |
| `CC-Mini-todo.md` | Claude Code on Mac Mini (code, builds, deploys) |

Create the file when that person/agent first has work to do. No empty placeholder files.

## File Format

```markdown
# [Name] Todos

**Last updated:** YYYY-MM-DD

## To Do

- [ ] Task description
- [ ] Task description (blocked by: reason)

## Done

- [x] Task description (YYYY-MM-DD)
- [x] Task description (YYYY-MM-DD)

## Deprecated

- ~~Task description~~ ... reason. (YYYY-MM-DD)
```

## Rules

- **Never delete anything.** Items move between sections, never off the page.
- **To Do** ... work that needs to happen.
- **Done** ... completed work. Check the box, add the date.
- **Deprecated** ... planned but no longer needed. Strikethrough, add the reason and date. Not the same as Done. Done means it shipped. Deprecated means the requirement changed.
- **Update the date** at the top of the file every time you edit it.
- **One file per person/agent.** No dated files, no subfolders, no inboxes.
- **Blocked items** stay in To Do with a `(blocked by: reason)` note. Don't move them to a separate section.

## When to Use Todos vs GitHub Issues

| Use | When |
|-----|------|
| **Todo file** | Quick tasks, repo-scoped work, things you'll do this session or this week |
| **GitHub Issue** | Bugs, feature requests, cross-repo work, things that need tracking or discussion |

Both is fine. File an issue AND add a todo that references it. The todo is your personal checklist. The issue is the team's record.
