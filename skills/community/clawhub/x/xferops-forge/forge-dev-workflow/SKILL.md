---
name: forge-dev-workflow
description: Pick up, work, move, and comment on Forge tasks during the dev loop. Use when claiming a ticket, moving it through columns, linking a PR, or adding status comments. NOT for managing projects, columns, or team membership (use forge-board-admin for that).
---

# Forge — Dev Workflow

The standard loop for development work: find a ticket → claim it → ship code → move it through review → done.

## Prerequisite

Forge MCP must be configured. If `forge_health_check` fails, run the `forge-setup` skill first.

## The Dev Loop

### 1. Find your next ticket

```
forge_search_tasks query="ADM-12"          # look up a specific ticket
forge_list_tasks projectId=<id>            # browse a board
```

Use `forge_get_task` to read full details, description, and existing comments before starting.

### 2. Claim it — move to In Progress

```
forge_move_task taskId=<id> columnId=<in-progress-col-id>
```

Always comment when you start:
```
forge_create_comment taskId=<id> content="Picking this up now."
```

### 3. During work — comment on blockers or context

If you hit a blocker, comment immediately and move to Blocked:
```
forge_create_comment taskId=<id> content="Blocked: <reason>. Needs input from <person>."
forge_move_task taskId=<id> columnId=<blocked-col-id>
```

### 4. PR ready — move to Code Review

```
forge_move_task taskId=<id> columnId=<code-review-col-id>
forge_create_comment taskId=<id> content="PR open: <url>. Ready for review."
```

### 5. Feedback addressed — re-request review

Push fixes, then comment:
```
forge_create_comment taskId=<id> content="Addressed review feedback (see PR). Re-requesting review."
```

### 6. Merged → Staging

After merge and successful staging deploy:
```
forge_move_task taskId=<id> columnId=<staging-col-id>
forge_create_comment taskId=<id> content="Merged and deployed to staging. Test at <url>."
```

### 7. Staging verified → Ready for Prod

```
forge_move_task taskId=<id> columnId=<ready-for-prod-col-id>
```

### 8. Released → Done

```
forge_move_task taskId=<id> columnId=<done-col-id>
```

## Column IDs

Column IDs vary by project. Get them with:
```
forge_get_project projectId=<id>   # returns columns[] with id + name
```

Common column names (in order): **Backlog → Blocked → To Do → In Progress → Code Review → Staging → Ready for Prod → Done**

## Assigning tasks

```
forge_update_task taskId=<id> assigneeId=<userId>
```

- Assign to yourself when starting
- Assign to `quinn-xferops-ai` when moving to Staging (QA ownership)
- Assign to `adam-xferops-ai` when you need a senior unblock
- Leave unassigned when parking in Backlog

## Task types

- `TASK` — discrete work item
- `BUG` — something broken
- `STORY` — larger initiative

## Priority order

Always work: **Critical → High → Medium → Low**

## Tools used by this skill

| Tool | When |
|------|------|
| `forge_search_tasks` | Find tickets by title, description, or ID (e.g. "ADM-5") |
| `forge_list_tasks` | Browse all tasks in a project |
| `forge_get_task` | Read full task details before starting |
| `forge_create_task` | Create a ticket for work that doesn't have one |
| `forge_update_task` | Update fields, assignee, priority, type |
| `forge_move_task` | Move between columns |
| `forge_create_comment` | Leave status updates, PR links, blocker notes |
| `forge_list_comments` | Read existing comments for context |
| `forge_health_check` | Verify API connectivity |
