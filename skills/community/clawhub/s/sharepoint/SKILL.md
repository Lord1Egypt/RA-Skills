---
name: sharepoint
description: |
  SharePoint API integration via Microsoft Graph with managed OAuth. Access SharePoint sites, lists, document libraries, and files.
  Use this skill when users want to interact with SharePoint for document management, list operations, or site content.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# SharePoint

Access SharePoint via Microsoft Graph API with managed OAuth authentication.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/sharepoint/v1.0/sites/root')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/sharepoint/{native-api-path}
```

Maton proxies requests to `graph.microsoft.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key:

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

Manage your SharePoint OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=sharepoint&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sharepoint'}).encode()
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
    "status": "PENDING",
    "creation_time": "2026-03-05T08:00:00.000000Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sharepoint",
    "method": "OAUTH2",
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

---

## Security & Permissions

- Access is scoped to SharePoint sites, lists, document libraries, and files within the connected SharePoint account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Sites

#### Get Root Site

```bash
GET /sharepoint/v1.0/sites/root
```

**Response:**
```json
{
  "id": "contoso.sharepoint.com,guid1,guid2",
  "displayName": "Communication site",
  "name": "root",
  "webUrl": "https://contoso.sharepoint.com"
}
```

#### Get Site by ID

```bash
GET /sharepoint/v1.0/sites/{site_id}
```

Site IDs follow the format: `{hostname},{site-guid},{web-guid}`

#### Get Site by Hostname and Path

```bash
GET /sharepoint/v1.0/sites/{hostname}:/{site-path}
```

Example: `GET /sharepoint/v1.0/sites/contoso.sharepoint.com:/sites/marketing`

#### Search Sites

```bash
GET /sharepoint/v1.0/sites?search={query}
```

#### List Subsites

```bash
GET /sharepoint/v1.0/sites/{site_id}/sites
```

#### Get Site Columns

```bash
GET /sharepoint/v1.0/sites/{site_id}/columns
```

#### Get Followed Sites

```bash
GET /sharepoint/v1.0/me/followedSites
```

---

### Lists

#### List Site Lists

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists
```

**Response:**
```json
{
  "value": [
    {
      "id": "b23974d6-a0aa-4e9b-9535-25393598b973",
      "name": "Events",
      "displayName": "Events",
      "webUrl": "https://contoso.sharepoint.com/Lists/Events"
    }
  ]
}
```

#### Get List

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}
```

#### List Columns

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/columns
```

#### List Content Types

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/contentTypes
```

#### List Items

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items
```

With field values (use `$expand=fields`):

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items?$expand=fields
```

**Response:**
```json
{
  "value": [
    {
      "id": "1",
      "createdDateTime": "2026-03-05T08:00:00Z",
      "fields": {
        "Title": "Team Meeting",
        "EventDate": "2026-03-10T14:00:00Z",
        "Location": "Conference Room A"
      }
    }
  ]
}
```

#### Get List Item

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}?$expand=fields
```

#### Create List Item

```bash
POST /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items
Content-Type: application/json

{
  "fields": {
    "Title": "New Event",
    "EventDate": "2026-04-01T10:00:00Z",
    "Location": "Main Hall"
  }
}
```

#### Update List Item

```bash
PATCH /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/fields
Content-Type: application/json

{
  "Title": "Updated Event Title"
}
```

#### Delete List Item

```bash
DELETE /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}
```

Returns `204 No Content` on success.

---

### Drives (Document Libraries)

#### List Site Drives

```bash
GET /sharepoint/v1.0/sites/{site_id}/drives
```

#### Get Default Drive

```bash
GET /sharepoint/v1.0/sites/{site_id}/drive
```

#### Get Drive by ID

```bash
GET /sharepoint/v1.0/drives/{drive_id}
```

**Note:** Drive IDs containing `!` (e.g., `b!abc123`) must be URL-encoded: `b%21abc123`

---

### Files and Folders

#### List Root Contents

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/children
```

**Response:**
```json
{
  "value": [
    {
      "id": "01WBMXT7NQEEYJ3BAXL5...",
      "name": "Documents",
      "folder": { "childCount": 5 },
      "webUrl": "https://contoso.sharepoint.com/Shared%20Documents/Documents"
    },
    {
      "id": "01WBMXT7LISS5OMIG4CZ...",
      "name": "report.docx",
      "file": { "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
      "size": 25600
    }
  ]
}
```

#### Get Item by ID

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
```

#### Get Item by Path

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{path}
```

Example: `GET /sharepoint/v1.0/drives/{drive_id}/root:/Reports/Q1.xlsx`

#### List Folder Contents

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{folder_id}/children
```

Or by path:

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{folder_path}:/children
```

#### Download File

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/content
```

Or by path:

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{path}:/content
```

Returns a redirect to the download URL (follow redirects to get file content).

#### Upload File (Simple - up to 4MB)

```bash
PUT /sharepoint/v1.0/drives/{drive_id}/root:/{filename}:/content
Content-Type: application/octet-stream

<file content>
```

Example:
```bash
curl -X PUT "https://api.maton.ai/sharepoint/v1.0/drives/{drive_id}/root:/documents/report.txt:/content" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: text/plain" \
  -d "File content here"
```

#### Create Folder

```bash
POST /sharepoint/v1.0/drives/{drive_id}/root/children
Content-Type: application/json

{
  "name": "New Folder",
  "folder": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

Or in a specific folder:

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{parent_id}/children
```

#### Rename/Move Item

```bash
PATCH /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
Content-Type: application/json

{
  "name": "new-filename.txt"
}
```

To move to another folder:

```bash
PATCH /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
Content-Type: application/json

{
  "parentReference": {
    "id": "{target_folder_id}"
  }
}
```

#### Copy Item

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/copy
Content-Type: application/json

{
  "name": "copied-file.txt"
}
```

This is an async operation - returns `202 Accepted` with a `Location` header for progress tracking.

#### Delete Item

```bash
DELETE /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
```

Returns `204 No Content` on success. Deleted items go to the recycle bin.

#### Search Files

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/search(q='{query}')
```

**Response:**
```json
{
  "value": [
    {
      "id": "01WBMXT7...",
      "name": "quarterly-report.xlsx",
      "webUrl": "https://contoso.sharepoint.com/..."
    }
  ]
}
```

#### Track Changes (Delta)

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/delta
```

Returns changed items and a `@odata.deltaLink` for subsequent requests.

---

### Sharing and Permissions

#### Get Item Permissions

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/permissions
```

#### Create Sharing Link

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/createLink
Content-Type: application/json

{
  "type": "view",
  "scope": "organization"
}
```

**Parameters:**
- `type`: `view`, `edit`, or `embed`
- `scope`: `anonymous`, `organization`, or `users`

**Response:**
```json
{
  "id": "f0cfb2bd-ef5f-4451-9932-8e9a3e219aaa",
  "roles": ["read"],
  "link": {
    "type": "view",
    "scope": "organization",
    "webUrl": "https://contoso.sharepoint.com/:t:/g/..."
  }
}
```

---

### Versions

#### List File Versions

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions
```

**Response:**
```json
{
  "value": [
    {
      "id": "2.0",
      "lastModifiedDateTime": "2026-03-05T08:07:12Z",
      "size": 25600,
      "lastModifiedBy": {
        "user": { "displayName": "John Doe" }
      }
    },
    {
      "id": "1.0",
      "lastModifiedDateTime": "2026-03-04T10:00:00Z",
      "size": 24000
    }
  ]
}
```

#### Get Specific Version

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions/{version_id}
```

#### Download Version Content

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions/{version_id}/content
```

---

### Thumbnails

#### Get Item Thumbnails

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/thumbnails
```

**Response:**
```json
{
  "value": [
    {
      "id": "0",
      "small": { "height": 96, "width": 96, "url": "..." },
      "medium": { "height": 176, "width": 176, "url": "..." },
      "large": { "height": 800, "width": 800, "url": "..." }
    }
  ]
}
```

---

## OData Query Parameters

SharePoint/Graph API supports OData query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `$select` | Select specific properties | `?$select=id,name,size` |
| `$expand` | Expand related entities | `?$expand=fields` |
| `$filter` | Filter results | `?$filter=name eq 'Report'` |
| `$orderby` | Sort results | `?$orderby=lastModifiedDateTime desc` |
| `$top` | Limit results | `?$top=10` |
| `$skip` | Skip results (pagination) | `?$skip=10` |

Example with multiple parameters:

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items?$expand=fields&$top=50&$orderby=createdDateTime desc
```

---

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/sharepoint/v1.0/sites/root', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  }
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/sharepoint/v1.0/sites/root',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

---

## Notes

- Site IDs follow the format: `{hostname},{site-guid},{web-guid}`
- Drive IDs with `!` (e.g., `b!abc123`) must be URL-encoded (`b%21abc123`)
- Item IDs are opaque strings (e.g., `01WBMXT7NQEEYJ3BAXL5...`)
- File uploads via PUT are limited to 4MB; use upload sessions for larger files
- Copy operations are asynchronous - check the Location header for progress
- Deleted items go to the SharePoint recycle bin
- Some admin operations require elevated permissions (Sites.FullControl.All)

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (async operation started) |
| 204 | No Content (successful delete) |
| 400 | Bad request / Invalid JSON |
| 401 | Invalid or missing authentication |
| 403 | Access denied / Insufficient permissions |
| 404 | Resource not found |
| 409 | Conflict (e.g., item already exists) |
| 429 | Rate limited |

## Resources

- [SharePoint Sites API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint)
- [DriveItem API](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [List API](https://learn.microsoft.com/en-us/graph/api/resources/list)
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
