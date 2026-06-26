---
name: twenty
description: |
  Twenty CRM API integration with managed authentication. Manage companies, people, opportunities, notes, and tasks.
  Use this skill when users want to interact with Twenty CRM data - contacts, deals, activities, and workflows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 📊
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Twenty CRM

Access the Twenty CRM API with managed authentication. Manage companies, people, opportunities, notes, tasks, and workflows.

## Quick Start

```bash
# List companies
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/twenty/rest/companies?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/twenty/rest/
```

Only the endpoints listed in the API Reference section below are supported. Maton proxies requests to `api.twenty.com/rest/` and automatically injects your API token.

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

Manage your Twenty connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=twenty&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'twenty'}).encode()
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
    "app": "twenty",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete authorization.

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

If you have multiple Twenty connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/twenty/rest/companies?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to companies, people, opportunities, notes, tasks, and workflows within the connected Twenty CRM.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the exact record ID and intended effect with the user.
- **CRM data scope**: Mutations directly affect live CRM records and workflows shared across the workspace. Prefer list/get calls to verify target records before making changes.

## API Reference

### Companies

#### List Companies

```bash
GET /twenty/rest/companies?limit=20
```

**Response:**
```json
{
  "data": {
    "companies": [
      {
        "id": "06290608-8bf0-4806-99ae-a715a6a93fad",
        "name": "Acme Corp",
        "domainName": {
          "primaryLinkUrl": "https://acme.com"
        },
        "employees": 100,
        "address": {
          "addressCity": "San Francisco",
          "addressState": "CA",
          "addressCountry": "United States"
        },
        "createdAt": "2026-03-20T23:59:52.906Z",
        "updatedAt": "2026-03-20T23:59:52.906Z"
      }
    ]
  },
  "pageInfo": {
    "hasNextPage": true,
    "startCursor": "06290608-8bf0-4806-99ae-a715a6a93fad",
    "endCursor": "1f70157c-4ea5-4d81-bc49-e1401abfbb94"
  },
  "totalCount": 50
}
```

#### Get Company

```bash
GET /twenty/rest/companies/{id}
```

#### Create Company

```bash
POST /twenty/rest/companies
Content-Type: application/json

{
  "name": "New Company",
  "domainName": {
    "primaryLinkUrl": "https://newcompany.com"
  },
  "employees": 50
}
```

#### Update Company

```bash
PATCH /twenty/rest/companies/{id}
Content-Type: application/json

{
  "name": "Updated Company Name",
  "employees": 100
}
```

#### Delete Company

```bash
DELETE /twenty/rest/companies/{id}
```

### People

#### List People

```bash
GET /twenty/rest/people?limit=20
```

**Response:**
```json
{
  "data": {
    "people": [
      {
        "id": "7a93d1e5-3f74-4945-8a65-d7f996083f72",
        "name": {
          "firstName": "John",
          "lastName": "Doe"
        },
        "emails": {
          "primaryEmail": "john@company.com"
        },
        "phones": {
          "primaryPhoneNumber": "5551234567",
          "primaryPhoneCallingCode": "+1"
        },
        "jobTitle": "CEO",
        "city": "San Francisco",
        "companyId": "06290608-8bf0-4806-99ae-a715a6a93fad"
      }
    ]
  },
  "pageInfo": {...},
  "totalCount": 100
}
```

#### Get Person

```bash
GET /twenty/rest/people/{id}
```

#### Create Person

```bash
POST /twenty/rest/people
Content-Type: application/json

{
  "name": {
    "firstName": "Jane",
    "lastName": "Smith"
  },
  "emails": {
    "primaryEmail": "jane@company.com"
  },
  "jobTitle": "CTO",
  "companyId": "06290608-8bf0-4806-99ae-a715a6a93fad"
}
```

#### Update Person

```bash
PATCH /twenty/rest/people/{id}
Content-Type: application/json

{
  "jobTitle": "VP of Engineering"
}
```

#### Delete Person

```bash
DELETE /twenty/rest/people/{id}
```

### Opportunities

#### List Opportunities

```bash
GET /twenty/rest/opportunities?limit=20
```

**Response:**
```json
{
  "data": {
    "opportunities": [
      {
        "id": "2beb07b0-340c-41d7-be33-5aa91757f329",
        "name": "Enterprise Deal",
        "amount": {
          "amountMicros": 75000000000,
          "currencyCode": "USD"
        },
        "closeDate": "2026-01-25T16:26:00.000Z",
        "stage": "SCREENING",
        "companyId": "1f70157c-4ea5-4d81-bc49-e1401abfbb94",
        "pointOfContactId": "edf6d445-13a7-4373-9a47-8f89e8c0a877"
      }
    ]
  },
  "pageInfo": {...},
  "totalCount": 25
}
```

**Note:** Amount is stored in micros (divide by 1,000,000 for actual value).

#### Get Opportunity

```bash
GET /twenty/rest/opportunities/{id}
```

#### Create Opportunity

```bash
POST /twenty/rest/opportunities
Content-Type: application/json

{
  "name": "New Deal",
  "amount": {
    "amountMicros": 50000000000,
    "currencyCode": "USD"
  },
  "stage": "SCREENING",
  "closeDate": "2026-06-01T00:00:00.000Z",
  "companyId": "06290608-8bf0-4806-99ae-a715a6a93fad"
}
```

#### Update Opportunity

```bash
PATCH /twenty/rest/opportunities/{id}
Content-Type: application/json

{
  "stage": "MEETING",
  "amount": {
    "amountMicros": 60000000000,
    "currencyCode": "USD"
  }
}
```

#### Delete Opportunity

```bash
DELETE /twenty/rest/opportunities/{id}
```

### Notes

#### List Notes

```bash
GET /twenty/rest/notes?limit=20
```

#### Get Note

```bash
GET /twenty/rest/notes/{id}
```

#### Create Note

```bash
POST /twenty/rest/notes
Content-Type: application/json

{
  "title": "Meeting Notes",
  "body": "Discussed Q2 roadmap and partnership opportunities."
}
```

#### Update Note

```bash
PATCH /twenty/rest/notes/{id}
Content-Type: application/json

{
  "body": "Updated meeting notes with action items."
}
```

#### Delete Note

```bash
DELETE /twenty/rest/notes/{id}
```

### Tasks

#### List Tasks

```bash
GET /twenty/rest/tasks?limit=20
```

#### Get Task

```bash
GET /twenty/rest/tasks/{id}
```

#### Create Task

```bash
POST /twenty/rest/tasks
Content-Type: application/json

{
  "title": "Follow up with client",
  "body": "Send proposal and schedule demo",
  "dueAt": "2026-04-01T00:00:00.000Z",
  "status": "TODO"
}
```

#### Update Task

```bash
PATCH /twenty/rest/tasks/{id}
Content-Type: application/json

{
  "status": "DONE"
}
```

#### Delete Task

```bash
DELETE /twenty/rest/tasks/{id}
```

### Workspace Members

#### List Workspace Members

```bash
GET /twenty/rest/workspaceMembers?limit=20
```

## Filtering

Use the `filter` query parameter to narrow results:

```bash
GET /twenty/rest/companies?filter=employees[gte]:100
GET /twenty/rest/opportunities?filter=stage[eq]:"MEETING"
GET /twenty/rest/people?filter=name.firstName[ilike]:"%john%"
```

**Comparators:**
- `eq`, `neq` - Equal, not equal
- `gt`, `gte`, `lt`, `lte` - Greater/less than
- `in` - In array: `id[in]:["id-1","id-2"]`
- `is` - Null check: `deletedAt[is]:NULL`
- `like`, `ilike` - Pattern match (case-sensitive/insensitive)
- `startsWith` - Prefix match
- `contain`, `notContain` - Contains value

**Advanced filtering:**
```bash
filter=or(stage[eq]:"MEETING",stage[eq]:"SCREENING")
filter=and(employees[gte]:100,idealCustomerProfile[eq]:true)
```

## Pagination

Twenty uses cursor-based pagination:

```bash
GET /twenty/rest/companies?limit=20&starting_after={endCursor}
```

**Parameters:**
- `limit` - Results per page (default: 60, max: 60)
- `starting_after` - Cursor for next page (use `endCursor` from response)
- `ending_before` - Cursor for previous page (use `startCursor` from response)

**Response includes:**
```json
{
  "pageInfo": {
    "hasNextPage": true,
    "hasPreviousPage": false,
    "startCursor": "uuid-1",
    "endCursor": "uuid-2"
  },
  "totalCount": 150
}
```

## Ordering

Use `order_by` to sort results:

```bash
GET /twenty/rest/companies?order_by=createdAt[DescNullsLast]
GET /twenty/rest/opportunities?order_by=closeDate,amount[DescNullsFirst]
```

**Directions:** `AscNullsFirst`, `AscNullsLast`, `DescNullsFirst`, `DescNullsLast`

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/twenty/rest/companies?limit=10',
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
    'https://api.maton.ai/twenty/rest/companies',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
```

### Create Company

```python
import os
import requests

response = requests.post(
    'https://api.maton.ai/twenty/rest/companies',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'New Company',
        'domainName': {'primaryLinkUrl': 'https://newcompany.com'},
        'employees': 50
    }
)
```

## Notes

- All IDs are UUIDs
- Timestamps are in ISO 8601 format
- Amount fields use micros (multiply by 1,000,000)
- Opportunity stages: `SCREENING`, `MEETING`, `PROPOSAL`, `NEGOTIATION`, `WON`, `LOST`
- Task statuses: `TODO`, `IN_PROGRESS`, `DONE`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Twenty connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Twenty API |

## Resources

- [Twenty API Documentation](https://twenty.com/developers/rest-api)
- [Twenty GitHub](https://github.com/twentyhq/twenty)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
