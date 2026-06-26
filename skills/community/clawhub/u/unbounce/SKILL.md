---
name: unbounce
description: |
  Unbounce API integration with managed OAuth. Build and manage landing pages, track leads, and analyze conversion data.
  Use this skill when users want to interact with Unbounce for landing page management and lead tracking.
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

# Unbounce

Access Unbounce landing pages and leads via managed OAuth.

## Quick Start

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/unbounce/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/unbounce/{native-api-path}
```

Maton proxies requests to `api.unbounce.com` and automatically injects your credentials.

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

Manage your Unbounce OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=unbounce&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'unbounce'}).encode()
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
    "creation_time": "2026-03-04T10:54:06.615371Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "unbounce",
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

- Access is scoped to Unbounce landing pages and leads via managed OAuth within the connected Unbounce account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Accounts

#### List Accounts

```bash
GET /unbounce/accounts
```

Query parameters:
- `sort_order` - `asc` or `desc` (default: desc by creation date)

**Response:**
```json
{
  "metadata": {
    "count": 1,
    "location": "https://api.unbounce.com/accounts"
  },
  "accounts": [
    {
      "id": 4967935,
      "name": "My Account",
      "createdAt": "2026-03-04T10:54:34Z",
      "state": "active",
      "options": {}
    }
  ]
}
```

#### Get Account

```bash
GET /unbounce/accounts/{account_id}
```

**Response:**
```json
{
  "id": 4967935,
  "name": "My Account",
  "createdAt": "2026-03-04T10:54:34Z",
  "state": "active",
  "options": {}
}
```

#### List Account Pages

```bash
GET /unbounce/accounts/{account_id}/pages
```

#### List Account Sub-Accounts

```bash
GET /unbounce/accounts/{account_id}/sub_accounts
```

---

### Sub-Accounts

#### Get Sub-Account

```bash
GET /unbounce/sub_accounts/{sub_account_id}
```

**Response:**
```json
{
  "id": 5699747,
  "accountId": 4967935,
  "name": "ChrisKim",
  "createdAt": "2026-03-04T10:54:35Z",
  "website": null,
  "uuid": "cf72cbb6-17fd-44d1-bbe4-d25dcad6354a",
  "domainsCount": 0
}
```

#### List Sub-Account Pages

```bash
GET /unbounce/sub_accounts/{sub_account_id}/pages
```

#### List Sub-Account Domains

```bash
GET /unbounce/sub_accounts/{sub_account_id}/domains
```

#### List Sub-Account Page Groups

```bash
GET /unbounce/sub_accounts/{sub_account_id}/page_groups
```

---

### Pages

#### List All Pages

```bash
GET /unbounce/pages
```

Query parameters:
- `role` - Filter by user role: `viewer` or `author`
- `with_stats` - Include A/B test statistics when `true`
- `limit` - Results per page (default: 50, max: 1000)
- `offset` - Skip first N results
- `sort_order` - `asc` or `desc`
- `count` - When `true`, only return count in metadata
- `from` - Start date (RFC 5322 format)
- `to` - End date (RFC 5322 format)

**Response:**
```json
{
  "metadata": {
    "count": 1,
    "location": "https://api.unbounce.com/pages"
  },
  "pages": [
    {
      "id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
      "subAccountId": 5699747,
      "name": "Training Template",
      "url": "http://unbouncepages.com/training-template/",
      "state": "unpublished",
      "domain": "unbouncepages.com",
      "createdAt": "2026-03-04T10:56:54Z",
      "lastPublishedAt": null,
      "variantsCount": 0,
      "integrationsCount": 0,
      "integrationsErrorsCount": 0
    }
  ]
}
```

#### Get Page

```bash
GET /unbounce/pages/{page_id}
```

Includes test statistics (A/B testing data):

**Response:**
```json
{
  "id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "name": "Training Template",
  "url": "http://unbouncepages.com/training-template/",
  "state": "unpublished",
  "tests": {
    "current": {
      "champion": "a",
      "hasResults": "false",
      "conversionRate": "0",
      "conversions": "0",
      "visitors": "0",
      "visits": "0"
    }
  }
}
```

#### List Page Form Fields

```bash
GET /unbounce/pages/{page_id}/form_fields
```

Query parameters:
- `include_sub_pages` - Include sub-page form fields when `true`
- `sort_order` - `asc` or `desc`
- `count` - When `true`, only return count

**Response:**
```json
{
  "metadata": {
    "count": 3
  },
  "formFields": [
    {
      "id": "name",
      "name": "Name",
      "type": "text",
      "validations": {
        "required": false
      }
    },
    {
      "id": "email",
      "name": "Email",
      "type": "text",
      "validations": {
        "required": false,
        "email": true
      }
    },
    {
      "id": "telephone",
      "name": "Telephone",
      "type": "text",
      "validations": {
        "required": false,
        "phone": true
      }
    }
  ]
}
```

---

### Leads

#### List Page Leads

```bash
GET /unbounce/pages/{page_id}/leads
```

Query parameters:
- `limit` - Results per page (default: 50, max: 1000)
- `offset` - Skip first N results
- `sort_order` - `asc` or `desc`
- `from` - Start date (RFC 5322 format)
- `to` - End date (RFC 5322 format)

**Response:**
```json
{
  "metadata": {
    "count": 0,
    "delete": {
      "href": "https://api.unbounce.com/pages/{page_id}/lead_deletion_request",
      "method": "POST"
    }
  },
  "leads": []
}
```

#### Get Lead

```bash
GET /unbounce/pages/{page_id}/leads/{lead_id}
```

or directly:

```bash
GET /unbounce/leads/{lead_id}
```

**Response:**
```json
{
  "id": "f79d7b6e-b3e8-484c-9584-d21c7afba238",
  "created_at": "2026-03-04T11:52:50.705Z",
  "page_id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "variant_id": "a",
  "submitter_ip": "127.0.0.1",
  "form_data": {
    "name": "Test User",
    "email": "test@example.com",
    "telephone": "1234567890"
  },
  "extra_data": {
    "cookies": {}
  }
}
```

#### Create Lead

```bash
POST /unbounce/pages/{page_id}/leads
Content-Type: application/json
```

**Request Body:**
```json
{
  "conversion": true,
  "visitor_id": "127.0.0.1234567890",
  "form_submission": {
    "variant_id": "a",
    "submitter_ip": "127.0.0.1",
    "form_data": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone_number": "1234567890"
    }
  }
}
```

**Response:**
```json
{
  "id": "f79d7b6e-b3e8-484c-9584-d21c7afba238",
  "created_at": "2026-03-04T11:52:50.705Z",
  "page_id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "variant_id": "a",
  "submitter_ip": "127.0.0.1",
  "form_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "1234567890"
  }
}
```

Leads created via the API have `"created_by": "api"` in their `extra_data`.

---

### Domains

#### Get Domain

```bash
GET /unbounce/domains/{domain_id}
```

#### List Domain Pages

```bash
GET /unbounce/domains/{domain_id}/pages
```

---

### Page Groups

#### List Page Group Pages

```bash
GET /unbounce/page_groups/{page_group_id}/pages
```

Query parameters:
- `limit` - Results per page (default: 50, max: 1000)
- `offset` - Skip first N results
- `sort_order` - `asc` or `desc`
- `from` / `to` - Date range filter

---

### Users

#### Get Current User

```bash
GET /unbounce/users/self
```

**Response:**
```json
{
  "id": 5031726,
  "email": "user@example.com",
  "firstName": "Chris",
  "lastName": "Kim",
  "metadata": {
    "related": {
      "subAccounts": ["https://api.unbounce.com/sub_accounts/5699747"],
      "accounts": ["https://api.unbounce.com/accounts/4967935"]
    }
  }
}
```

#### Get User by ID

```bash
GET /unbounce/users/{user_id}
```

---

## Pagination

Unbounce uses offset-based pagination:

```bash
GET /unbounce/pages?limit=50&offset=0
```

**Parameters:**
- `limit` - Number of results per page (default: 50, max: 1000)
- `offset` - Number of results to skip
- `sort_order` - Sort direction: `asc` or `desc`

**Response metadata includes:**
```json
{
  "metadata": {
    "count": 100
  }
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://api.maton.ai/unbounce/pages', {
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
    'https://api.maton.ai/unbounce/pages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

## Notes

- All responses include `metadata` with HATEOAS links for navigation
- Date format: RFC 5322 (e.g., `2026-03-04T10:54:34Z`)
- Page IDs are UUIDs, account/sub-account IDs are integers
- Page states: `published` or `unpublished`
- Account states: `active` or `suspended`

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 401 | Invalid or missing authentication |
| 404 | Resource not found |
| 429 | Rate limited |

## Resources

- [Unbounce API Documentation](https://developer.unbounce.com/api_reference/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
