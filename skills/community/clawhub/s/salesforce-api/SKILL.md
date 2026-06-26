---
name: salesforce
description: |
  Salesforce CRM API integration with managed OAuth. Install only if you need Salesforce CRM administration. Connect with the narrowest Salesforce permissions available, prefer sandbox orgs for destructive or batch work, verify the intended connection ID before each request, and revoke unused connections promptly. This integration can mutate CRM records — approve only specific write actions after checking the exact sObject, record IDs, and consequence. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Salesforce

Access the Salesforce REST API with managed OAuth authentication. Query records using SOQL, manage sObjects, and perform CRUD operations on your Salesforce data.

## Quick Start

**CLI:**

```bash
maton salesforce query 'SELECT Id,Name FROM Contact LIMIT 10'
```

```bash
maton api '/salesforce/services/data/v63.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+10'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/salesforce/services/data/v63.0/query?q=SELECT+Id,Name,Email+FROM+Contact+LIMIT+10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/salesforce/{endpoint-path}
```

The gateway proxies requests to `{instance}.salesforce.com` (automatically replaced with your connection config) and injects your access token. Only the endpoints documented in the API Reference section below are supported — always use specific endpoint paths from that section rather than constructing arbitrary paths.

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Salesforce OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list salesforce --status ACTIVE
```

```bash
maton api -X GET /connections -f app=salesforce -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=salesforce&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create salesforce
```

```bash
maton api /connections -f app=salesforce
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'salesforce'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

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
    "app": "salesforce",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Salesforce connections, specify which one to use:

**CLI:**

```bash
maton salesforce query 'SELECT Id,Name FROM Contact LIMIT 10' --connection {connection_id}
```

```bash
maton api /salesforce/services/data/v63.0/sobjects --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/salesforce/services/data/v63.0/sobjects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- **IMPORTANT:** Treat `MATON_API_KEY` as a secret — do not log it, include it in chats or prompts visible to others, or expose it in shared files or outputs. The key authenticates with Maton, and the Salesforce connection is independently scoped via OAuth. Use the narrowest Salesforce permissions available, rotate the key if exposed at [maton.ai/settings](https://maton.ai/settings), and revoke unused connections promptly.
- Access is scoped to the Salesforce resources permitted by the connected account's OAuth scopes. Only install if you need Salesforce CRM administration. Prefer sandbox orgs for destructive or batch testing.
- **Default to read-only operations.** Always start with SOQL queries or GET requests to confirm record IDs and field values before proposing any changes.
- **All write operations require explicit user approval with specific details.** Before executing any POST, PATCH, DELETE, or composite/batch call:
  1. Retrieve and display the target resource (sObject type, record ID, record name) so the user can verify.
  2. Clearly describe the intended effect (e.g., "This will delete Opportunity 'Acme Deal' (ID: 006xx) — this cannot be undone").
  3. Wait for explicit user confirmation before proceeding.
- **Batch and composite operations require extra caution.** These can modify multiple records in a single call. List every affected record and confirm before execution.

## API Reference

### SOQL Query

```bash
GET /salesforce/services/data/v63.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+10
```

Example:

```bash
maton salesforce query 'SELECT Id,Name FROM Contact LIMIT 10'
```

Complex query:

```bash
GET /salesforce/services/data/v63.0/query?q=SELECT+Id,Name,Email+FROM+Contact+WHERE+Email+LIKE+'%25example.com'+ORDER+BY+CreatedDate+DESC
```

Example:

```bash
maton salesforce query "SELECT Id,Name,Email FROM Contact WHERE Email LIKE '%example.com' ORDER BY CreatedDate DESC"
```

### Get Object

```bash
GET /salesforce/services/data/v63.0/sobjects/Contact/0035g00000XYZ
```

Example:

```bash
maton salesforce record view 0035g00000XYZ --type Contact
```

### Create Object

```bash
POST /salesforce/services/data/v63.0/sobjects/Contact
Content-Type: application/json

{
  "FirstName": "John",
  "LastName": "Doe",
  "Email": "john@example.com"
}
```

Example:

```bash
maton salesforce record create --type Contact --data '{"FirstName":"John","LastName":"Doe","Email":"john@example.com"}'
```

### Update Object

```bash
PATCH /salesforce/services/data/v63.0/sobjects/Contact/0035g00000XYZ
Content-Type: application/json

{
  "Phone": "+1234567890"
}
```

Example:

```bash
maton salesforce record update 0035g00000XYZ --type Contact --data '{"Phone":"+1234567890"}'
```

### Delete Object

```bash
DELETE /salesforce/services/data/v63.0/sobjects/Contact/0035g00000XYZ
```

Example:

```bash
maton salesforce record delete 0035g00000XYZ --type Contact
```

### Describe Object (get schema)

```bash
GET /salesforce/services/data/v63.0/sobjects/Contact/describe
```

Example:

```bash
maton salesforce object describe Contact
```

### List Objects

```bash
GET /salesforce/services/data/v63.0/sobjects
```

Example:

```bash
maton salesforce object list
```

### Search (SOSL)

```bash
GET /salesforce/services/data/v63.0/search?q=FIND+{John}+IN+ALL+FIELDS+RETURNING+Contact(Id,Name)
```

Example:

```bash
maton salesforce search 'FIND {John} IN ALL FIELDS RETURNING Contact(Id,Name)'
```

### Get API Limits

```bash
GET /salesforce/services/data/v63.0/limits
```

Example:

```bash
maton salesforce limit view
```

### Get Current User

Example:

```bash
maton salesforce whoami
```

### Composite Request (batch multiple operations)

```bash
POST /salesforce/services/data/v63.0/composite
Content-Type: application/json

{
  "compositeRequest": [
    {
      "method": "GET",
      "url": "/services/data/v63.0/sobjects/Contact/003XXXXXXX",
      "referenceId": "contact1"
    },
    {
      "method": "GET",
      "url": "/services/data/v63.0/sobjects/Account/001XXXXXXX",
      "referenceId": "account1"
    }
  ]
}
```

Example:

```bash
echo '{"compositeRequest":[{"method":"GET","url":"/services/data/v63.0/sobjects/Contact/003XXXXXXX","referenceId":"contact1"},{"method":"GET","url":"/services/data/v63.0/sobjects/Account/001XXXXXXX","referenceId":"account1"}]}' \
  | maton salesforce composite call -F -
```

### Composite Batch Request

```bash
POST /salesforce/services/data/v63.0/composite/batch
Content-Type: application/json

{
  "batchRequests": [
    {"method": "GET", "url": "v63.0/sobjects/Contact/003XXXXXXX"},
    {"method": "GET", "url": "v63.0/sobjects/Account/001XXXXXXX"}
  ]
}
```

Example:

```bash
echo '{"batchRequests":[{"method":"GET","url":"v63.0/sobjects/Contact/003XXXXXXX"},{"method":"GET","url":"v63.0/sobjects/Account/001XXXXXXX"}]}' \
  | maton salesforce composite batch -F -
```

### sObject Collections Create (batch create)

```bash
POST /salesforce/services/data/v63.0/composite/sobjects
Content-Type: application/json

{
  "allOrNone": true,
  "records": [
    {"attributes": {"type": "Contact"}, "FirstName": "John", "LastName": "Doe"},
    {"attributes": {"type": "Contact"}, "FirstName": "Jane", "LastName": "Smith"}
  ]
}
```

Example:

```bash
maton salesforce record create --all-or-none --data '[{"attributes":{"type":"Contact"},"FirstName":"John","LastName":"Doe"},{"attributes":{"type":"Contact"},"FirstName":"Jane","LastName":"Smith"}]'
```

### sObject Collections Delete (batch delete)

```bash
DELETE /salesforce/services/data/v63.0/composite/sobjects?ids=003XXXXX,003YYYYY&allOrNone=true
```

Example:

```bash
maton salesforce record delete 003XXXXX 003YYYYY --all-or-none
```

### Get Updated Records

```bash
GET /salesforce/services/data/v63.0/sobjects/Contact/updated/?start=2026-04-30T00:00:00Z&end=2026-05-05T00:00:00Z
```

Example:

```bash
maton salesforce record list --type Contact --start 2026-04-30T00:00:00Z --end 2026-05-05T00:00:00Z
```

### Get Deleted Records

```bash
GET /salesforce/services/data/v63.0/sobjects/Contact/deleted/?start=2026-04-30T00:00:00Z&end=2026-05-05T00:00:00Z
```

Example:

```bash
maton salesforce record list --type Contact --start 2026-04-30T00:00:00Z --end 2026-05-05T00:00:00Z --changes deleted
```

### List API Versions

```bash
GET /salesforce/services/data/
```

Example:

```bash
maton salesforce version list
```

## Common Objects

- `Account` - Companies/Organizations
- `Contact` - People associated with accounts
- `Lead` - Potential customers
- `Opportunity` - Sales deals
- `Case` - Support cases
- `Task` - To-do items
- `Event` - Calendar events

## Pagination

Salesforce uses cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton salesforce query 'SELECT Id,Name FROM Contact' --paginate
```

## Code Examples

### CLI

```bash
# Query contacts
maton salesforce query 'SELECT Id,Name FROM Contact LIMIT 10'

# View a specific record
maton salesforce record view 0035g00000XYZ --type Contact

# Create a new contact
maton salesforce record create --type Contact --data '{"FirstName":"John","LastName":"Doe"}'

# Describe an object schema
maton salesforce object describe Contact

# Check authenticated user
maton salesforce whoami

# Check API limits
maton salesforce limit view
```

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/salesforce/services/data/v63.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+5',
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
    'https://api.maton.ai/salesforce/services/data/v63.0/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'q': 'SELECT Id,Name FROM Contact LIMIT 5'}
)
```

## Notes

- Use URL encoding for SOQL queries (spaces become `+`)
- Record IDs are 15 or 18 character alphanumeric strings
- API version (v63.0) can be adjusted; latest is v65.0
- Update and Delete operations return HTTP 204 (no content) on success
- Dates for updated/deleted queries use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Use `allOrNone: true` in batch operations for atomic transactions
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Salesforce connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Salesforce API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

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

1. Ensure your URL path starts with `salesforce`. For example:

- Correct: `https://api.maton.ai/salesforce/services/data/v63.0/query`
- Incorrect: `https://api.maton.ai/services/data/v63.0/query`

## Resources

- [REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm)
- [List sObjects](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_describeGlobal.htm)
- [Describe sObject](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_sobject_describe.htm)
- [Get Record](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_sobject_retrieve_get.htm)
- [Create Record](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_create.htm)
- [Update Record](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_update_fields.htm)
- [Delete Record](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_delete_record.htm)
- [Query Records (SOQL)](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_query.htm)
- [Composite Request](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_composite_composite_post.htm)
- [sObject Collections](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_composite_sobjects_collections_create.htm)
- [SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm)
- [SOSL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_sosl.htm)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
