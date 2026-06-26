---
name: snowsand-jira
version: 1.0.0
description: Interact with Jira Cloud via REST API. Use for searching issues (JQL), viewing issue details, creating/updating issues, adding comments, transitioning status, querying sprints/boards, and logging work. Triggers on Jira issue operations, sprint queries, JQL searches, worklog tracking, or any Atlassian Jira Cloud task.
---

# Jira Cloud Integration

Jira Cloud REST API integration for issue tracking, sprint management, and worklog operations.

## Authentication

Jira Cloud uses API token authentication. Required environment variables:

- `JIRA_BASE_URL` - Your Jira instance (e.g., `https://yourcompany.atlassian.net`)
- `JIRA_USER_EMAIL` - Atlassian account email
- `JIRA_API_TOKEN` - API token from https://id.atlassian.com/manage-profile/security/api-tokens

Test connection:
```bash
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/myself" | jq .
```

## Quick Reference

All operations use the `scripts/jira.py` script:

| Operation | Command |
|-----------|---------|
| Search (JQL) | `jira.py search "project = PROJ AND status = Open"` |
| View issue | `jira.py get PROJ-123` |
| Create issue | `jira.py create PROJ --type Task --summary "Title" --description "Body"` |
| Update issue | `jira.py update PROJ-123 --summary "New title"` |
| Add comment | `jira.py comment PROJ-123 "Comment text"` |
| Transition | `jira.py transition PROJ-123 "In Progress"` |
| List boards | `jira.py boards` |
| Get sprints | `jira.py sprints BOARD_ID` |
| Sprint issues | `jira.py sprint-issues SPRINT_ID` |
| Log work | `jira.py worklog PROJ-123 --time "2h 30m" --comment "Work done"` |
| Get worklogs | `jira.py worklogs PROJ-123` |

## Common Workflows

### Search Issues

JQL (Jira Query Language) supports powerful filtering:

```bash
# Open issues assigned to me
jira.py search "assignee = currentUser() AND status != Done"

# Issues updated this week
jira.py search "project = PROJ AND updated >= startOfWeek()"

# High priority bugs
jira.py search "type = Bug AND priority in (High, Highest)"

# Issues in current sprint
jira.py search "sprint in openSprints() AND project = PROJ"
```

Output: JSON array of issues with key, summary, status, assignee, priority.

### Create Issues

```bash
# Basic task
jira.py create PROJ --type Task --summary "Implement feature X"

# Bug with description and priority
jira.py create PROJ --type Bug \
  --summary "Login fails on mobile" \
  --description "Steps to reproduce: 1. Open app 2. Enter credentials" \
  --priority High

# Story with labels and components
jira.py create PROJ --type Story \
  --summary "User profile page" \
  --labels "frontend,ui" \
  --components "Web App"
```

### Update Issues

```bash
# Update summary
jira.py update PROJ-123 --summary "Updated title"

# Update multiple fields
jira.py update PROJ-123 \
  --description "New description" \
  --priority Medium \
  --labels "backend,api"

# Assign to user
jira.py update PROJ-123 --assignee "user@company.com"
```

### Status Transitions

Transitions depend on workflow configuration. Get available transitions first:

```bash
# List available transitions
jira.py transitions PROJ-123

# Move to status
jira.py transition PROJ-123 "In Progress"
jira.py transition PROJ-123 "Done"
```

### Sprint Management

```bash
# List all boards
jira.py boards

# Get sprints for a board
jira.py sprints 42

# Get active sprint issues
jira.py sprint-issues 100

# Filter: only active sprints
jira.py sprints 42 --state active
```

### Work Logging

```bash
# Log time spent
jira.py worklog PROJ-123 --time "1h 30m" --comment "Code review"

# Log with specific date
jira.py worklog PROJ-123 --time "4h" --started "2024-03-14T09:00:00.000+0000"

# View existing worklogs
jira.py worklogs PROJ-123
```

## Field Reference

See `references/fields.md` for:
- Standard field names and IDs
- Custom field handling
- ADF (Atlassian Document Format) for rich text

## Error Handling

Common errors:
- **401 Unauthorized**: Check JIRA_USER_EMAIL and JIRA_API_TOKEN
- **404 Not Found**: Issue key or project doesn't exist
- **400 Bad Request**: Invalid field values or missing required fields

## Raw API Access

For operations not covered by the script:

```bash
# GET request
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123" | jq .

# POST request
curl -s -X POST -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Comment"}]}]}}' \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123/comment" | jq .
```

API docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
