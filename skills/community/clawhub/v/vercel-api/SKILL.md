---
name: vercel
description: |
  Vercel API integration with managed OAuth. Manage projects, deployments, domains, teams, and environment variables.
  Use this skill when users want to interact with Vercel - deploying apps, managing projects, checking deployment status, or configuring domains.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "▲"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Vercel

Access the Vercel API with managed OAuth authentication. Manage projects, deployments, domains, teams, and environment variables.

## Quick Start

```bash
# List projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/vercel/v9/projects?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/vercel/
```

Only the endpoints listed in the API Reference section below are supported. Maton proxies requests to `api.vercel.com` and automatically injects your OAuth token.

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

Manage your Vercel OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=vercel&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'vercel'}).encode()
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
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "vercel",
    "metadata": {}
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

If you have multiple Vercel connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/vercel/v9/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to projects, deployments, domains, teams, and environment variables within the connected Vercel account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- **Production impact**: Deployments, domain changes, team modifications, and environment variable updates directly affect live applications and collaborators. Confirm before modifying production resources.

## API Reference

### User

#### Get Current User

```bash
GET /vercel/v2/user
```

**Response:**
```json
{
  "user": {
    "id": "srL5ucia16R88imgFgrn9XHH",
    "email": "user@example.com",
    "username": "username",
    "name": "User Name",
    "avatar": null,
    "defaultTeamId": "team_abc123",
    "billing": {
      "plan": "hobby",
      "status": "active"
    }
  }
}
```

### Teams

#### List Teams

```bash
GET /vercel/v2/teams
```

**Response:**
```json
{
  "teams": [
    {
      "id": "team_1xPDNnVvmKxzxPs2x2XQRoKu",
      "slug": "my-team",
      "name": "My Team",
      "createdAt": 1732138693523,
      "membership": {
        "role": "OWNER"
      },
      "billing": {
        "plan": "hobby",
        "status": "active"
      }
    }
  ],
  "pagination": {
    "count": 1,
    "next": null,
    "prev": null
  }
}
```

### Projects

#### List Projects

```bash
GET /vercel/v9/projects?limit=20
```

**Response:**
```json
{
  "projects": [
    {
      "id": "prj_ET9o8o6WAQTfWbtF8NeFe4XF9uYG",
      "name": "my-project",
      "accountId": "team_abc123",
      "framework": "nextjs",
      "nodeVersion": "22.x",
      "createdAt": 1733304037737,
      "updatedAt": 1766947708146,
      "targets": {},
      "latestDeployments": []
    }
  ],
  "pagination": {
    "count": 20,
    "next": 1733304037737,
    "prev": null
  }
}
```

#### Get Project

```bash
GET /vercel/v9/projects/{projectId}
```

**Response:**
```json
{
  "id": "prj_ET9o8o6WAQTfWbtF8NeFe4XF9uYG",
  "name": "my-project",
  "accountId": "team_abc123",
  "framework": "nextjs",
  "nodeVersion": "22.x",
  "createdAt": 1733304037737,
  "updatedAt": 1766947708146,
  "buildCommand": null,
  "devCommand": null,
  "installCommand": null,
  "outputDirectory": null,
  "rootDirectory": null,
  "serverlessFunctionRegion": "iad1"
}
```

#### Create Project

```bash
POST /vercel/v9/projects
Content-Type: application/json

{
  "name": "my-new-project",
  "framework": "nextjs",
  "gitRepository": {
    "type": "github",
    "repo": "username/repo"
  }
}
```

#### Update Project

```bash
PATCH /vercel/v9/projects/{projectId}
Content-Type: application/json

{
  "name": "updated-project-name",
  "buildCommand": "npm run build"
}
```

#### Delete Project

```bash
DELETE /vercel/v9/projects/{projectId}
```

### Deployments

#### List Deployments

```bash
GET /vercel/v6/deployments?limit=20
```

**Query Parameters:**
- `limit` - Number of results (default: 20)
- `projectId` - Filter by project ID
- `target` - Filter by target (`production`, `preview`)
- `state` - Filter by state (`BUILDING`, `READY`, `ERROR`, `CANCELED`)

**Response:**
```json
{
  "deployments": [
    {
      "uid": "dpl_8gFe6M8XZsQ1ohP86VWTemcBAmZJ",
      "name": "my-project",
      "url": "my-project-abc123.vercel.app",
      "created": 1759739951209,
      "state": "READY",
      "readyState": "READY",
      "target": "production",
      "source": "git",
      "creator": {
        "uid": "srL5ucia16R88imgFgrn9XHH",
        "username": "username"
      },
      "meta": {
        "githubCommitRef": "main",
        "githubCommitSha": "6e88c2d..."
      }
    }
  ],
  "pagination": {
    "count": 20,
    "next": 1759739951209,
    "prev": null
  }
}
```

#### Get Deployment

```bash
GET /vercel/v13/deployments/{deploymentId}
```

**Response:**
```json
{
  "id": "dpl_8gFe6M8XZsQ1ohP86VWTemcBAmZJ",
  "name": "my-project",
  "url": "my-project-abc123.vercel.app",
  "created": 1759739951209,
  "buildingAt": 1759739952144,
  "ready": 1759740085170,
  "state": "READY",
  "readyState": "READY",
  "target": "production",
  "source": "git",
  "creator": {
    "uid": "srL5ucia16R88imgFgrn9XHH",
    "username": "username"
  }
}
```

#### Get Deployment Build Logs

```bash
GET /vercel/v3/deployments/{deploymentId}/events
```

**Response:**
```json
[
  {
    "created": 1759739951860,
    "deploymentId": "dpl_8gFe6M8XZsQ1ohP86VWTemcBAmZJ",
    "text": "Running build in Washington, D.C., USA (East) – iad1",
    "type": "stdout",
    "info": {
      "type": "build",
      "name": "bld_b3go7zd2k"
    }
  }
]
```

#### Cancel Deployment

```bash
PATCH /vercel/v12/deployments/{deploymentId}/cancel
```

### Environment Variables

#### List Environment Variables

```bash
GET /vercel/v10/projects/{projectId}/env
```

**Response:**
```json
{
  "envs": [
    {
      "id": "6EwQRCd32PVNHORP",
      "key": "API_KEY",
      "value": "...",
      "type": "encrypted",
      "target": ["production", "preview", "development"],
      "createdAt": 1732148489672,
      "updatedAt": 1745542152381
    }
  ]
}
```

#### Create Environment Variable

```bash
POST /vercel/v10/projects/{projectId}/env
Content-Type: application/json

{
  "key": "MY_ENV_VAR",
  "value": "my-value",
  "type": "encrypted",
  "target": ["production", "preview"]
}
```

#### Update Environment Variable

```bash
PATCH /vercel/v10/projects/{projectId}/env/{envId}
Content-Type: application/json

{
  "value": "updated-value"
}
```

#### Delete Environment Variable

```bash
DELETE /vercel/v10/projects/{projectId}/env/{envId}
```

### Domains

#### List Domains

```bash
GET /vercel/v5/domains
```

**Response:**
```json
{
  "domains": [
    {
      "name": "example.com",
      "apexName": "example.com",
      "projectId": "prj_abc123",
      "verified": true,
      "createdAt": 1732138693523
    }
  ],
  "pagination": {
    "count": 10,
    "next": null,
    "prev": null
  }
}
```

#### Get Domain

```bash
GET /vercel/v5/domains/{domain}
```

#### Add Domain

```bash
POST /vercel/v5/domains
Content-Type: application/json

{
  "name": "example.com"
}
```

#### Remove Domain

```bash
DELETE /vercel/v6/domains/{domain}
```

### Artifacts (Remote Caching)

#### Get Artifacts Status

```bash
GET /vercel/v8/artifacts/status
```

**Response:**
```json
{
  "status": "enabled"
}
```

## Pagination

Vercel uses cursor-based pagination with `next` and `prev` cursors:

```bash
GET /vercel/v9/projects?limit=20&until=1733304037737
```

**Parameters:**
- `limit` - Results per page (varies by endpoint, typically max 100)
- `until` - Cursor for next page (use `next` from response)
- `since` - Cursor for previous page (use `prev` from response)

**Response includes:**
```json
{
  "pagination": {
    "count": 20,
    "next": 1733304037737,
    "prev": 1759739951209
  }
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/vercel/v9/projects?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/vercel/v9/projects',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
```

### List Deployments for a Project

```python
import os
import requests

project_id = 'prj_abc123'
response = requests.get(
    'https://api.maton.ai/vercel/v6/deployments',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'projectId': project_id, 'limit': 10}
)
deployments = response.json()['deployments']
```

## Notes

- API versions vary by endpoint (v2, v5, v6, v9, v10, v13, etc.)
- Timestamps are in milliseconds since Unix epoch
- Project IDs start with `prj_`, deployment IDs start with `dpl_`, team IDs start with `team_`
- Deployment states: `BUILDING`, `READY`, `ERROR`, `CANCELED`, `QUEUED`
- Environment variable types: `plain`, `encrypted`, `secret`, `sensitive`
- Environment targets: `production`, `preview`, `development`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Vercel connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Vercel API |

## Resources

- [Vercel REST API Documentation](https://vercel.com/docs/rest-api)
- [Vercel API Reference](https://vercel.com/docs/rest-api/endpoints)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
