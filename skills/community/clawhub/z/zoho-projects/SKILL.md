---
name: zohoprojects
description: |
  Zoho Projects API V3 integration with managed OAuth. Manage projects, tasks, milestones, tasklists, and team collaboration.
  Use this skill when users want to manage project tasks, track time, organize milestones, or collaborate on projects.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Security: The MATON_API_KEY authenticates with Maton.ai but grants NO access to Zoho Projects by itself. Zoho access requires explicit OAuth authorization by the user through Maton's connect flow. Access is strictly scoped to the Zoho Projects account the user has authorized.
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "2.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Zoho Projects

Access the Zoho Projects API V3 with managed OAuth authentication. Manage projects, tasks, milestones, tasklists, and team collaboration.

## Quick Start

```bash
# List all portals
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/zoho-projects/api/v3/portals')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/zoho-projects/api/v3/{endpoint}
```

The gateway proxies requests to `projectsapi.zoho.com` and automatically injects your OAuth token.

**Important:**
- V3 endpoints use `/api/v3/` prefix (not `/restapi/`)
- No trailing slashes on endpoint paths
- Request bodies are JSON (`Content-Type: application/json`)
- Updates use PATCH method (not POST)

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Zoho Projects OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=zoho-projects&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-projects'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-28T00:12:25.223434Z",
    "last_updated_time": "2026-02-28T00:16:32.882675Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-projects",
    "metadata": {},
    "method": "OAUTH2"
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Zoho Projects connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/zoho-projects/api/v3/portals')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- **No implicit access:** The MATON_API_KEY alone cannot access Zoho Projects. The user must explicitly authorize via OAuth through Maton's connect flow.
- **Scoped access:** Access is limited to the specific Zoho Projects account the user authorized.
- **Write safeguards:** All write operations (POST, PATCH, DELETE) require explicit user approval. Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Portals

#### List Portals

```bash
GET /zoho-projects/api/v3/portals
```

**Response:**
```json
[
  {
    "id": "916020774",
    "portal_name": "mycompany",
    "org_name": "mycompany",
    "timezone": "PST",
    "project_plan": "Free",
    "owner": {
      "zpuid": "2644874000000085003",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "profile": {
      "name": "Portal Owner",
      "id": 2644874000000085084
    }
  }
]
```

---

### Projects

#### List Projects

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects
```

Query parameters: `page`, `per_page`, `status` (`active`, `archived`, `template`)

**Response:**
```json
[
  {
    "id": "2644874000000089119",
    "key": "NU-1",
    "name": "My Project",
    "project_type": "active",
    "description": "Project description",
    "owner": {
      "zpuid": "2644874000000085003",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "is_public_project": false,
    "created_time": "2026-02-27T10:20:22.421Z",
    "modified_time": "2026-02-27T10:20:22.421Z"
  }
]
```

#### Get Project Details

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}
```

#### Create Project

```bash
POST /zoho-projects/api/v3/portal/{portal_id}/projects
Content-Type: application/json

{
  "name": "New Project",
  "description": "Project description"
}
```

**Response (201):**
```json
{
  "id": "2644874000000096003",
  "key": "NU-2",
  "name": "New Project",
  "project_type": "active",
  "description": "Project description",
  "owner": {
    "zpuid": "2644874000000085003",
    "name": "John Doe"
  },
  "created_time": "2026-05-17T22:08:52.537Z"
}
```

#### Update Project

```bash
PATCH /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}
```

#### Delete Project

```bash
DELETE /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}
```

Returns 204 No Content on success.

---

### Tasks

#### List Tasks

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks
```

Query parameters: `page`, `per_page`, `owner`, `status`, `priority`, `tasklist_id`, `sort_by`

**Response:**
```json
{
  "page_info": {
    "page": 1,
    "per_page": 100,
    "page_count": 3,
    "has_next_page": false
  },
  "tasks": [
    {
      "id": "2644874000000089247",
      "prefix": "EZ1-T1",
      "name": "Task 1",
      "status": {
        "id": "2644874000000016068",
        "name": "Open",
        "is_closed_type": false
      },
      "priority": "none",
      "project": {
        "id": "2644874000000089119",
        "name": "My Project"
      },
      "tasklist": {
        "id": "2644874000000089245",
        "name": "General"
      },
      "milestone": {
        "id": "2644874000000000073",
        "name": "None"
      }
    }
  ]
}
```

#### Get Task Details

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}
```

#### Create Task

```bash
POST /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks
Content-Type: application/json

{
  "name": "New Task",
  "priority": "high",
  "description": "Task description",
  "tasklist_id": "{tasklist_id}"
}
```

Optional fields: `person_responsible`, `tasklist_id`, `start_date`, `end_date`, `priority`, `description`

**Response (201):** Returns the created task object.

#### Update Task

```bash
PATCH /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}
Content-Type: application/json

{
  "name": "Updated Task Name",
  "priority": "medium"
}
```

#### Delete Task

```bash
DELETE /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}
```

Returns 204 No Content on success.

---

### Task Comments

#### List Comments

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments
```

**Response:**
```json
{
  "page_info": {
    "per_page": 100,
    "has_next_page": false,
    "count": 1,
    "page": 1
  },
  "comments": [
    {
      "id": "2644874000000094015",
      "comment": "This is a comment",
      "created_time": "2026-05-17T22:08:51.264Z",
      "created_by": {
        "zpuid": "2644874000000085003",
        "name": "John Doe"
      }
    }
  ]
}
```

#### Add Comment

```bash
POST /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments
Content-Type: application/json

{
  "comment": "This is a comment"
}
```

**Note:** The field name is `comment`, not `content`.

**Response (201):** Returns the created comment object.

#### Delete Comment

```bash
DELETE /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}
```

Returns 204 No Content on success.

---

### Tasklists

#### List Tasklists

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasklists
```

**Response:**
```json
{
  "page_info": {
    "page": 1,
    "per_page": 200,
    "page_count": 1,
    "has_next_page": false
  },
  "tasklists": [
    {
      "id": "2644874000000089245",
      "name": "General",
      "flag": "internal",
      "status": "active",
      "milestone": {
        "id": "2644874000000000073",
        "name": "None"
      },
      "created_time": "2026-02-27T10:20:24.426Z"
    }
  ]
}
```

#### Create Tasklist

```bash
POST /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasklists
Content-Type: application/json

{
  "name": "New Tasklist",
  "flag": "internal"
}
```

Optional fields: `milestone_id`, `flag` (`internal` or `external`)

**Response (201):** Returns the created tasklist object.

#### Update Tasklist

```bash
PATCH /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasklists/{tasklist_id}
Content-Type: application/json

{
  "name": "Updated Tasklist Name"
}
```

#### Delete Tasklist

```bash
DELETE /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasklists/{tasklist_id}
```

Returns 204 No Content on success.

---

### Milestones

#### List Milestones

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/milestones
```

**Response:**
```json
{
  "page_info": [
    {
      "per_page": 100,
      "has_next_page": false,
      "page": 1
    }
  ],
  "milestones": [
    {
      "id": "2644874000000096133",
      "name": "Phase 1",
      "start_date": "2026-05-17",
      "end_date": "2026-06-01",
      "flag": "internal",
      "owner": {
        "zpuid": "2644874000000085003",
        "name": "John Doe"
      },
      "created_time": "2026-05-17T22:09:13.771Z"
    }
  ]
}
```

#### Create Milestone

```bash
POST /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/milestones
Content-Type: application/json

{
  "name": "Phase 1",
  "start_date": "06-01-2026",
  "end_date": "06-15-2026",
  "flag": "internal",
  "owner_zpuid": "{user_zpuid}"
}
```

Required fields: `name`, `start_date`, `end_date`, `flag`, `owner_zpuid`

**Note:** Date format for creating milestones is `MM-dd-yyyy`.

**Response (201):** Returns the created milestone object.

#### Update Milestone

```bash
PATCH /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/milestones/{milestone_id}
Content-Type: application/json

{
  "name": "Updated Phase",
  "end_date": "06-20-2026"
}
```

#### Delete Milestone

```bash
DELETE /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/milestones/{milestone_id}
```

Returns 204 No Content on success.

---

### Users

#### List Users

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/users
```

**Response:**
```json
{
  "page_info": {
    "per_page": 100,
    "has_next_page": false,
    "count": 1,
    "page": 1
  },
  "users": [
    {
      "zpuid": "2644874000000085003",
      "name": "John Doe",
      "email": "john@example.com",
      "is_active": true,
      "role": {
        "name": "Administrator",
        "id": "2644874000000085005"
      },
      "added_time": "2026-02-27T10:19:11.719Z"
    }
  ]
}
```

---

## Pagination

V3 uses page-based pagination with `page` and `per_page` parameters:

```bash
GET /zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks?page=1&per_page=50
```

**Response includes `page_info`:**
```json
{
  "page_info": {
    "page": 1,
    "per_page": 50,
    "page_count": 25,
    "has_next_page": true
  },
  "tasks": [...]
}
```

When `has_next_page` is `true`, increment `page` to get the next batch.

## Code Examples

### JavaScript

```javascript
// List tasks in a project
const response = await fetch(
  'https://api.maton.ai/zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.tasks);
```

### Python

```python
import os
import requests

# Create a task
response = requests.post(
    'https://api.maton.ai/zoho-projects/api/v3/portal/{portal_id}/projects/{project_id}/tasks',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'name': 'New Task', 'priority': 'high'}
)
task = response.json()
print(task['id'])
```

## Notes

- V3 API uses `/api/v3/` prefix — do NOT use trailing slashes
- All POST/PATCH requests use `application/json` content type (not form-urlencoded like V2)
- Updates use PATCH method (not POST like V2)
- Portal ID is required for most endpoints — obtain from `GET /api/v3/portals`
- Date format for milestone creation: `MM-dd-yyyy` (e.g., `06-01-2026`)
- Pagination uses `page` + `per_page` (not `index` + `range` like V2)
- Delete operations return 204 No Content
- Create operations return 201 Created

## Error Handling

| Status | Meaning |
|--------|---------|
| 201 | Resource created successfully |
| 204 | Success with no content (delete operations) |
| 400 | Missing/invalid input parameter or invalid URL |
| 401 | Invalid or missing API key, or invalid OAuth scope |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Zoho Projects API |

V3 error format:
```json
{
  "error": {
    "status_code": "400",
    "title": "LESS_THAN_MIN_OCCURANCE",
    "error_type": "FIELDS_VALIDATION_ERROR",
    "details": [
      {
        "message": "Input Parameter Missing",
        "field_name": "comment"
      }
    ]
  }
}
```

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

Ensure your URL path starts with `zoho-projects`. For example:

- Correct: `https://api.maton.ai/zoho-projects/api/v3/portals`
- Incorrect: `https://api.maton.ai/api/v3/portals`

### Troubleshooting: Trailing Slashes

V3 does NOT allow trailing slashes. For example:

- Correct: `https://api.maton.ai/zoho-projects/api/v3/portal/{portal_id}/projects`
- Incorrect: `https://api.maton.ai/zoho-projects/api/v3/portal/{portal_id}/projects/`

## Resources

- [Zoho Projects API V3 Documentation](https://projects.zoho.com/api-docs)
- [Zoho Projects Developer Portal](https://www.zoho.com/projects/help/rest-api/zohoprojectsapi.html)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
