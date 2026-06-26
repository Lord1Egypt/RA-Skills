---
name: zoho-projects
description: Manage Zoho Projects — list portals/projects, create/update/complete tasks, add comments, log time, manage milestones, and query your task list. Requires ZOHO_ACCESS_TOKEN and ZOHO_PORTAL_ID environment variables.
metadata: {"openclaw":{"emoji":"📋","requires":{"env":["ZOHO_ACCESS_TOKEN","ZOHO_PORTAL_ID"]},"primaryEnv":"ZOHO_ACCESS_TOKEN","homepage":"https://projects.zoho.com/api-docs"}}
---

# Zoho Projects Skill

Use the Zoho Projects V3 REST API (base: `https://projectsapi.zoho.com/api/v3`) to manage projects, tasks, milestones, and time logs.

## Authentication

Every request must include:
```
Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN
```

Access tokens expire **hourly**. If you get a 401, tell the user their token has expired and they need to refresh it using their refresh token (see Setup below). Store the refreshed token with:
```bash
openclaw config set skills.entries.zoho-projects.apiKey NEW_TOKEN
```

## Environment Variables

| Variable | Description |
|---|---|
| `ZOHO_ACCESS_TOKEN` | OAuth2 access token from Zoho (expires hourly) |
| `ZOHO_PORTAL_ID` | Your portal ID (get it from the List Portals call below) |
| `ZOHO_REFRESH_TOKEN` | (optional) Stored refresh token for auto-renewal |
| `ZOHO_CLIENT_ID` | (optional) OAuth client ID for token refresh |
| `ZOHO_CLIENT_SECRET` | (optional) OAuth client secret for token refresh |
| `ZOHO_DC` | (optional) Data center domain, e.g. `zoho.eu` or `zoho.com` (default: `zoho.com`) |

## Setup (First Time)

1. Go to https://api-console.zoho.com/ → Create a **Self Client** application
2. Grant scopes: `ZohoProjects.portals.READ,ZohoProjects.projects.ALL,ZohoProjects.tasks.ALL,ZohoProjects.milestones.ALL,ZohoProjects.timesheets.ALL,ZohoProjects.bugs.ALL`
3. Generate a grant token (duration: 10 minutes is fine for initial setup)
4. Exchange it for access + refresh tokens:
```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "redirect_uri=https://localhost" \
  -d "code=YOUR_GRANT_TOKEN"
```
5. Save the `access_token` as `ZOHO_ACCESS_TOKEN` and `refresh_token` as `ZOHO_REFRESH_TOKEN`
6. Get your portal ID by calling **List Portals** below, then set `ZOHO_PORTAL_ID`

## Refreshing an Expired Token

If you get a 401 Unauthorized error, refresh the token:
```bash
curl -X POST "https://accounts.${ZOHO_DC:-zoho.com}/oauth/v2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN"
```
Parse the `access_token` from the JSON response and update `ZOHO_ACCESS_TOKEN`.

---

## API Reference

### 🏢 Portals

**List Portals** (use this to find your ZOHO_PORTAL_ID)
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portals" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

### 📁 Projects

**List all projects**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

**Get a specific project**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

**Create a project**
```bash
curl -s -X POST "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Name",
    "description": "Optional description",
    "start_date": "2026-03-24T00:00:00Z",
    "end_date": "2026-06-30T00:00:00Z"
  }'
```

**Update a project** (PATCH updates only specified fields)
```bash
curl -s -X PATCH "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "status": "active"}'
```

---

### ✅ Tasks

**Get my tasks (across all projects)**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/mytasks" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```
Optional query params: `?status=open` | `status=closed` | `due_date=2026-03-24`

**List tasks in a project**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```
Optional: `?status=open&sort_column=due_date&sort_order=asc`

**Get task details**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks/$TASK_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

**Create a task**
```bash
curl -s -X POST "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Task name",
    "description": "Task details",
    "due_date": "2026-04-15T00:00:00Z",
    "priority": "high"
  }'
```
Priority values: `none`, `low`, `medium`, `high`

**Update / complete a task**
```bash
curl -s -X PATCH "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks/$TASK_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "closed"}'
```
Use `"status": "open"` to reopen a task.

**Delete a task**
```bash
curl -s -X DELETE "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks/$TASK_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

**Add a comment to a task**
```bash
curl -s -X POST "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks/$TASK_ID/comments" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Your comment here"}'
```

---

### 🎯 Milestones

**List milestones in a project**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/milestones" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

**Create a milestone**
```bash
curl -s -X POST "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/milestones" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Milestone name",
    "end_date": "2026-05-01T00:00:00Z",
    "flag": "internal"
  }'
```

---

### ⏱ Time Logs

**Log time on a task**
```bash
curl -s -X POST "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/tasks/$TASK_ID/logs" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-03-24T00:00:00Z",
    "hours": "02:30",
    "notes": "Worked on API integration",
    "bill_status": "Billable"
  }'
```

**Get time logs for a project**
```bash
curl -s "https://projectsapi.zoho.com/api/v3/portal/$ZOHO_PORTAL_ID/projects/$PROJECT_ID/logs" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

## Tips

- All dates must be ISO 8601 format: `2026-03-24T00:00:00Z`
- Rate limit: 100 requests per 2 minutes. If you hit 429, wait 30 seconds before retrying.
- Use `| python3 -m json.tool` after curl commands to pretty-print JSON responses.
- For EU/AU/IN/JP Zoho accounts, set `ZOHO_DC` to the correct domain (e.g., `zoho.eu`) and use `projectsapi.zoho.eu` as the API base URL instead.
- When listing projects or tasks, extract the `id` or `id_string` field to use in subsequent calls.
- If the user asks to "show all open tasks", call the mytasks endpoint with `?status=open` and format the results as a readable list.
- When creating tasks for sarvahealth.ai or Katprotech work, apply appropriate project IDs stored in memory.
