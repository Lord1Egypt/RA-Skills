---
name: forge-board-admin
description: Manage Forge projects, columns, and team membership. Use when creating or updating boards, reordering or adding columns, or managing team members. NOT for day-to-day ticket work (use forge-dev-workflow for that).
---

# Forge — Board Administration

For setting up and maintaining boards, columns, and team membership. This is Parker/Adam territory — dev agents rarely need this.

## Prerequisite

Forge MCP must be configured. If `forge_health_check` fails, run the `forge-setup` skill first.

## Projects

### Create a project
```
forge_create_project teamId=<id> name="Project Name" prefix="PRJ"
```
`prefix` sets the ticket ID prefix (e.g. `PRJ-1`, `PRJ-2`). Choose something short and unique.

### Update a project
```
forge_update_project projectId=<id> name="New Name"
```

### Delete a project
```
forge_delete_project projectId=<id>
```
⚠️ Irreversible. All tasks and history are gone.

### List all projects in a team
```
forge_list_projects teamId=<id>
```

### Get a project (with columns + tasks)
```
forge_get_project projectId=<id>
```
Use this to retrieve column IDs before creating tasks or building automations.

## Columns

Standard XferOps column order:
**Backlog → Blocked → To Do → In Progress → Code Review → Staging → Ready for Prod → Done**

### Create a column
```
forge_create_column projectId=<id> name="Column Name"
```

### Rename a column
```
forge_update_column columnId=<id> name="New Name"
```

### Reorder columns
```
forge_reorder_columns projectId=<id> columnIds=["<id1>","<id2>","<id3>"]
```
Pass the full ordered list of column IDs.

### Delete a column
```
forge_delete_column columnId=<id>
```
⚠️ Move all tasks out first — tasks in a deleted column may be lost.

## Team Members

### List team members
```
forge_list_team_members teamId=<id>
```

### Add a member
```
forge_add_team_member teamId=<id> email="user@example.com"
```

## Tools used by this skill

| Tool | When |
|------|------|
| `forge_list_teams` | List all teams in the org |
| `forge_list_projects` | List projects in a team |
| `forge_get_project` | Get project details, column IDs, task list |
| `forge_create_project` | Create a new board |
| `forge_update_project` | Rename a project |
| `forge_delete_project` | Delete a project (irreversible) |
| `forge_create_column` | Add a column to a board |
| `forge_update_column` | Rename a column |
| `forge_delete_column` | Remove a column (move tasks first) |
| `forge_reorder_columns` | Change column order |
| `forge_list_team_members` | See who's on the team |
| `forge_add_team_member` | Add a user by email |
| `forge_health_check` | Verify API connectivity |
