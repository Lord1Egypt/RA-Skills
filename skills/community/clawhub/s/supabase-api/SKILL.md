---
name: supabase
description: |
  Supabase API integration with managed authentication. Access database tables via PostgREST, manage auth users, and handle storage buckets.
  Use this skill when users want to interact with Supabase projects - querying database tables, managing users, or working with storage.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "⚡"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Supabase

Access the Supabase API with managed authentication. Query database tables via PostgREST, manage auth users, and handle storage buckets.

## Quick Start

```bash
# List storage buckets
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/supabase/storage/v1/bucket')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/supabase/
```

Only the endpoints listed in the API Reference section below are supported. Maton proxies requests to your connected Supabase project using these service prefixes:
- `rest/v1` - PostgREST API (database tables)
- `auth/v1` - GoTrue authentication API
- `storage/v1` - Storage API

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

Manage your Supabase connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=supabase&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'supabase'}).encode()
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
    "creation_time": "2026-03-29T22:47:35.570344Z",
    "last_updated_time": "2026-03-29T22:48:23.435225Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "supabase",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete authentication setup.

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

If you have multiple Supabase connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/supabase/storage/v1/bucket')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended project.

## Security & Permissions

- Access is scoped to database tables, auth users, and storage buckets within the connected Supabase project.
- **All write operations require explicit user approval.** Before executing any POST, PATCH, or DELETE call, confirm the target table/resource, filter conditions, and intended effect with the user. DELETE and PATCH without narrow filters can affect many rows.
- **Production data scope**: Database mutations, auth user changes, and storage operations directly affect the connected project's live data. Prefer staging/test projects for exploratory work.

## API Reference

### Database (PostgREST)

The PostgREST API auto-generates endpoints based on your database schema. Access tables and views in the `public` schema.

#### Get OpenAPI Schema

```bash
GET /supabase/rest/v1/
```

Returns the OpenAPI specification describing all available tables and endpoints.

#### List Records from Table

```bash
GET /supabase/rest/v1/{table_name}
```

**Query Parameters:**
- `select` - Columns to return (e.g., `select=id,name,email`)
- `order` - Sort order (e.g., `order=created_at.desc`)
- `limit` - Maximum records to return
- `offset` - Number of records to skip

**Example:**
```bash
GET /supabase/rest/v1/users?select=id,email&order=created_at.desc&limit=10
```

#### Get Single Record

```bash
GET /supabase/rest/v1/{table_name}?id=eq.{id}&select=*
```

#### Insert Records

```bash
POST /supabase/rest/v1/{table_name}
Content-Type: application/json
Prefer: return=representation

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### Update Records

```bash
PATCH /supabase/rest/v1/{table_name}?id=eq.{id}
Content-Type: application/json
Prefer: return=representation

{
  "name": "Jane Doe"
}
```

#### Delete Records

```bash
DELETE /supabase/rest/v1/{table_name}?id=eq.{id}
```

#### Filtering Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `eq` | Equals | `?status=eq.active` |
| `neq` | Not equals | `?status=neq.deleted` |
| `gt` | Greater than | `?age=gt.18` |
| `gte` | Greater than or equal | `?age=gte.18` |
| `lt` | Less than | `?age=lt.65` |
| `lte` | Less than or equal | `?age=lte.65` |
| `like` | Pattern match | `?name=like.*john*` |
| `ilike` | Case-insensitive pattern | `?name=ilike.*john*` |
| `in` | In list | `?status=in.(active,pending)` |
| `is` | Is null/true/false | `?deleted_at=is.null` |

### Auth (GoTrue)

#### Get Auth Health

```bash
GET /supabase/auth/v1/health
```

**Response:**
```json
{
  "version": "v2.188.1",
  "name": "GoTrue",
  "description": "GoTrue is a user registration and authentication API"
}
```

#### Get Auth Settings

```bash
GET /supabase/auth/v1/settings
```

**Response:**
```json
{
  "external": {
    "email": true,
    "phone": false,
    "google": false,
    "github": false
  },
  "disable_signup": false,
  "mailer_autoconfirm": false
}
```

#### List Users (Admin)

```bash
GET /supabase/auth/v1/admin/users
```

**Response:**
```json
{
  "users": [
    {
      "id": "8974a9fa-95c4-4839-8d50-76f4666d2113",
      "email": "user@example.com",
      "email_confirmed_at": "2026-03-29T23:01:46.718322Z",
      "created_at": "2026-03-29T23:01:46.689584Z"
    }
  ],
  "aud": "authenticated"
}
```

#### Get User (Admin)

```bash
GET /supabase/auth/v1/admin/users/{user_id}
```

#### Create User (Admin)

```bash
POST /supabase/auth/v1/admin/users
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "email_confirm": true
}
```

**Response:**
```json
{
  "id": "8974a9fa-95c4-4839-8d50-76f4666d2113",
  "email": "newuser@example.com",
  "email_confirmed_at": "2026-03-29T23:01:46.718322Z",
  "role": "authenticated",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  }
}
```

#### Update User (Admin)

```bash
PUT /supabase/auth/v1/admin/users/{user_id}
Content-Type: application/json

{
  "email": "updated@example.com",
  "user_metadata": {
    "name": "Updated Name"
  }
}
```

#### Delete User (Admin)

```bash
DELETE /supabase/auth/v1/admin/users/{user_id}
```

### Storage

#### List Buckets

```bash
GET /supabase/storage/v1/bucket
```

**Response:**
```json
[
  {
    "id": "avatars",
    "name": "avatars",
    "public": true,
    "created_at": "2026-03-29T23:01:06.638Z",
    "updated_at": "2026-03-29T23:01:06.638Z"
  }
]
```

#### Get Bucket

```bash
GET /supabase/storage/v1/bucket/{bucket_id}
```

#### Create Bucket

```bash
POST /supabase/storage/v1/bucket
Content-Type: application/json

{
  "id": "documents",
  "name": "documents",
  "public": false,
  "file_size_limit": 10485760,
  "allowed_mime_types": ["application/pdf", "image/png"]
}
```

#### Update Bucket

```bash
PUT /supabase/storage/v1/bucket/{bucket_id}
Content-Type: application/json

{
  "public": true
}
```

#### Delete Bucket

```bash
DELETE /supabase/storage/v1/bucket/{bucket_id}
```

#### List Objects in Bucket

```bash
POST /supabase/storage/v1/object/list/{bucket_id}
Content-Type: application/json

{
  "prefix": "",
  "limit": 100,
  "offset": 0
}
```

#### Upload Object

```bash
POST /supabase/storage/v1/object/{bucket_id}/{path}
Content-Type: {mime_type}

{binary_data}
```

#### Download Object

```bash
GET /supabase/storage/v1/object/{bucket_id}/{path}
```

#### Delete Object

```bash
DELETE /supabase/storage/v1/object/{bucket_id}/{path}
```

## Pagination

### PostgREST Pagination

Use `limit` and `offset` query parameters:

```bash
GET /supabase/rest/v1/users?limit=10&offset=20
```

Use the `Range` header for range-based pagination:

```bash
GET /supabase/rest/v1/users
Range: 0-9
```

### Auth User Pagination

```bash
GET /supabase/auth/v1/admin/users?page=1&per_page=50
```

## Code Examples

### JavaScript

```javascript
// List storage buckets
const response = await fetch(
  'https://api.maton.ai/supabase/storage/v1/bucket',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const buckets = await response.json();
```

### Python

```python
import os
import requests

# Query database table
response = requests.get(
    'https://api.maton.ai/supabase/rest/v1/users',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'select': 'id,email', 'limit': 10}
)
users = response.json()
```

### Create User and Storage Bucket

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create auth user
user_resp = requests.post(
    'https://api.maton.ai/supabase/auth/v1/admin/users',
    headers=headers,
    json={
        'email': 'test@example.com',
        'password': 'securepass123',
        'email_confirm': True
    }
)
user = user_resp.json()

# Create storage bucket
bucket_resp = requests.post(
    'https://api.maton.ai/supabase/storage/v1/bucket',
    headers=headers,
    json={
        'id': 'user-uploads',
        'name': 'user-uploads',
        'public': False
    }
)
bucket = bucket_resp.json()
```

## Notes

- The connection routes to a specific Supabase project configured during setup
- PostgREST endpoints are auto-generated from your database schema
- Use `Prefer: return=representation` header to get created/updated records back
- Storage bucket names must be unique within the project
- Auth admin endpoints require service role permissions
- Database queries support complex filtering, ordering, and joins via PostgREST syntax
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets or special characters
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Supabase connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 404 | Table or resource not found |
| 409 | Conflict (e.g., duplicate bucket name) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Supabase API |

### PostgREST Errors

```json
{
  "code": "PGRST205",
  "details": null,
  "hint": null,
  "message": "Could not find the table 'public.users' in the schema cache"
}
```

## Resources

- [Supabase REST API Guide](https://supabase.com/docs/guides/api)
- [PostgREST Documentation](https://postgrest.org/en/stable/)
- [Supabase Auth API](https://supabase.com/docs/reference/javascript/auth-api)
- [Supabase Storage API](https://supabase.com/docs/reference/javascript/storage-api)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
