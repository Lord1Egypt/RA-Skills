---
name: wrike
description: Manage Wrike tasks, projects, folders, and comments via the Wrike REST API.
metadata: {"openclaw": {"emoji": "📋", "requires": {"bins": ["claw-wrike"], "env": ["WRIKE_TOKEN"]}, "primaryEnv": "WRIKE_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "claw-wrike", "bins": ["claw-wrike"], "label": "Install claw-wrike (npm)"}]}}
---

# Wrike CLI

Manage Wrike tasks, projects, folders, and comments. All commands return JSON: `{"ok": true, "data": ...}` on success, `{"ok": false, "error": "..."}` on failure.

## Setup

```bash
claw-wrike config set --token <WRIKE_TOKEN>
# Auto-detects US/EU data center. Token is stored in ~/.claw-wrike/config.json
```

## Quick Reference

```bash
claw-wrike <entity> <command> [--flags]
```

### Account & Spaces

```bash
claw-wrike account                          # Account info (name, root folder ID, etc.)
claw-wrike space list                       # List all spaces
claw-wrike space get --id <id>              # Get a space
```

### Folders & Projects

Wrike treats folders and projects as the same entity. Projects are folders with extra properties (owners, dates, status).

```bash
claw-wrike folder list                      # List all folders (tree structure)
claw-wrike folder list --space <id>         # List folders in a space
claw-wrike folder list --parent <id>        # List child folders
claw-wrike folder get --id <id>             # Get folder details

claw-wrike folder create --parent <id> --title "Folder name"
claw-wrike folder create --parent <id> --title "Project name" --project
claw-wrike folder create --parent <id> --title "Project name" --project --owner <contactId> --start-date 2026-03-01 --end-date 2026-06-01
claw-wrike folder create --parent <id> --title "Folder name" --dry-run   # Preview without creating

claw-wrike folder update --id <id> --title "New title"
claw-wrike folder update --id <id> --description "New description"
claw-wrike folder update --id <id> --add-parent <folderId>              # Move into another parent
claw-wrike folder update --id <id> --remove-parent <folderId>           # Remove from a parent
claw-wrike folder update --id <id> --dry-run                            # Preview without updating

claw-wrike folder delete --id <id>                                      # Moves to recycle bin
claw-wrike folder delete --id <id> --dry-run                            # Preview without deleting
```

### Tasks

```bash
claw-wrike task list                        # List tasks (default: 100, Active)
claw-wrike task list --folder <id>          # Tasks in a folder/project
claw-wrike task list --space <id>           # Tasks in a space
claw-wrike task list --status Active        # Filter: Active|Completed|Deferred|Cancelled
claw-wrike task list --assignee "Jane"      # Filter by assignee name
claw-wrike task list --importance High      # Filter: High|Normal|Low
claw-wrike task list --limit 20             # Limit results

claw-wrike task get --id <id>               # Full task details (description, custom fields, etc.)

claw-wrike task create --folder <id> --title "Task name"
claw-wrike task create --folder <id> --title "Task name" --assignee "Jane" --due 2026-03-01 --importance High
claw-wrike task create --folder <id> --title "Task name" --dry-run   # Preview without creating

claw-wrike task update --id <id> --title "New title"
claw-wrike task update --id <id> --add-assignee "Jane"
claw-wrike task update --id <id> --remove-assignee "Jane"
claw-wrike task update --id <id> --due 2026-04-01 --importance Low
claw-wrike task update --id <id> --status <customStatusId>
claw-wrike task update --id <id> --dry-run                           # Preview without updating

claw-wrike task delete --id <id>                                     # Moves to recycle bin
claw-wrike task delete --id <id> --dry-run                           # Preview without deleting
```

### Comments

```bash
claw-wrike comment list --task <id>         # List comments on a task
claw-wrike comment add --task <id> --text "Comment text"
claw-wrike comment update --id <id> --text "Updated text"
claw-wrike comment delete --id <id>
```

### Contacts, Workflows, Custom Fields

```bash
claw-wrike contact list                     # All contacts (users) in the account
claw-wrike contact get --id <id>            # Single contact details
claw-wrike workflow list                    # Workflows with custom statuses
claw-wrike customfield list                 # All custom field definitions
```

### Utilities

```bash
claw-wrike lookup --permalink <url>         # Resolve a Wrike permalink to task details
claw-wrike cache refresh                    # Force refresh cached contacts/workflows/fields
claw-wrike config show                      # Show current config (token masked)
```

## Important Notes

- **IDs:** Wrike API IDs are alphanumeric strings like `IEABMHYCI5P7AYDW`. They are NOT the numeric IDs in permalink URLs.
- **Assignee resolution:** Use names ("Jane", "Jane Doe") or IDs. Names are resolved via cached contacts.
- **Custom statuses:** Use `claw-wrike workflow list` to find custom status IDs, then pass them to `--status`.
- **Folders = Projects:** A project is a folder with a `project` property. Use `folder` commands for both.
- **Tasks can have multiple parents:** A task can belong to multiple folders/projects.
- **Dry run:** Use `--dry-run` on create/update commands to see the API call without executing it.
- **Rate limit:** ~400 requests/minute. The CLI handles rate limiting and retries automatically.

## Before Any Operation

1. Use `claw-wrike space list` or `claw-wrike folder list` to find the right container ID.
2. Use `claw-wrike workflow list` to understand available statuses before changing task status.
3. Use `claw-wrike task get --id <id>` to read current state before updating.

## NEVER

- Never guess task or folder IDs. Always look them up first.
- Never update tasks without reading their current state.
- Never bulk-modify tasks without user confirmation.
