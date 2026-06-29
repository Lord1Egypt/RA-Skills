---
name: trello
description: |
  Trello API integration with managed OAuth. Manage boards, lists, cards, members, and labels. Use this skill when users want to interact with Trello for project management. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Trello

Access the Trello API with managed OAuth authentication. Manage boards, lists, cards, checklists, labels, and members for project and task management.

## Quick Start

**CLI:**

```bash
maton trello board list
```

```bash
maton api '/trello/1/members/me/boards'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/trello/1/members/me/boards')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/trello/{native-api-path}
```

Maton proxies requests to `api.trello.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton/cli
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

Manage your Trello OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list trello --status ACTIVE
```

```bash
maton api -X GET /connections -f app=trello -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=trello&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create trello
```

```bash
maton api /connections -f app=trello
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'trello'}).encode()
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
    "app": "trello",
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

If you have multiple Trello connections, specify which one to use:

**CLI:**

```bash
maton trello board list --connection {connection_id}
```

```bash
maton api /trello/1/members/me/boards --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/trello/1/members/me/boards')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to boards, lists, cards, members, and labels within the connected Trello account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Members

#### Get Current Member

```bash
GET /trello/1/members/me
```

Example:

```bash
maton trello whoami
```

#### Get a Member

```bash
GET /trello/1/members/{id}
```

Example:

```bash
maton trello member view me
maton trello member view 5f1a2b3c4d5e6f7a8b9c0d1e
```

#### Get Member's Boards

```bash
GET /trello/1/members/me/boards
```

Query parameters:
- `filter` - Filter boards: `all`, `open`, `closed`, `members`, `organization`, `starred`
- `fields` - Comma-separated fields to include

Example:

```bash
maton trello board list --filter all
```

### Boards

#### Get Board

```bash
GET /trello/1/boards/{id}
```

Query parameters:
- `fields` - Comma-separated fields
- `lists` - Include lists: `all`, `open`, `closed`, `none`
- `cards` - Include cards: `all`, `open`, `closed`, `none`
- `members` - Include members: `all`, `none`

Example:

```bash
maton trello board view BOARD_ID --lists open --cards open
```

#### Create Board

```bash
POST /trello/1/boards
Content-Type: application/json

{
  "name": "Project Alpha",
  "desc": "Main project board",
  "defaultLists": false,
  "prefs_permissionLevel": "private"
}
```

Example:

```bash
maton trello board create --name 'Project Alpha' --desc 'Main project board' --permission private
```

#### Update Board

```bash
PUT /trello/1/boards/{id}
Content-Type: application/json

{
  "name": "Project Alpha - Updated",
  "desc": "Updated description"
}
```

Example:

```bash
maton trello board update BOARD_ID --name 'Project Alpha - Updated' --desc 'Updated description'
```

#### Delete Board

```bash
DELETE /trello/1/boards/{id}
```

Example:

```bash
maton trello board delete BOARD_ID
```

#### Get Board Lists

```bash
GET /trello/1/boards/{id}/lists
```

Query parameters:
- `filter` - Filter: `all`, `open`, `closed`, `none`

Example:

```bash
maton trello list list --board BOARD_ID --filter open
```

#### Get Board Cards

```bash
GET /trello/1/boards/{id}/cards
```

Example:

```bash
maton trello card list --board BOARD_ID
```

#### Get Board Members

```bash
GET /trello/1/boards/{id}/members
```

Example:

```bash
maton trello member list --board BOARD_ID
```

### Lists

#### Get List

```bash
GET /trello/1/lists/{id}
```

Example:

```bash
maton trello list view LIST_ID
```

#### Create List

```bash
POST /trello/1/lists
Content-Type: application/json

{
  "name": "To Do",
  "idBoard": "BOARD_ID",
  "pos": "top"
}
```

Example:

```bash
maton trello list create --board BOARD_ID --name 'To Do' --pos top
```

#### Update List

```bash
PUT /trello/1/lists/{id}
Content-Type: application/json

{
  "name": "In Progress"
}
```

Example:

```bash
maton trello list update LIST_ID --name 'In Progress'
```

#### Archive List

```bash
PUT /trello/1/lists/{id}/closed
Content-Type: application/json

{
  "value": true
}
```

Example:

```bash
maton trello list update LIST_ID --closed
```

#### Get Cards in List

```bash
GET /trello/1/lists/{id}/cards
```

Example:

```bash
maton trello card list --list LIST_ID
```

#### Move All Cards in List

```bash
POST /trello/1/lists/{id}/moveAllCards
Content-Type: application/json

{
  "idBoard": "BOARD_ID",
  "idList": "TARGET_LIST_ID"
}
```

Example:

```bash
maton trello card move --from-list LIST_ID --to-list TARGET_LIST_ID --to-board BOARD_ID
```

### Cards

#### Get Card

```bash
GET /trello/1/cards/{id}
```

Query parameters:
- `fields` - Comma-separated fields
- `members` - Include members (true/false)
- `checklists` - Include checklists: `all`, `none`
- `attachments` - Include attachments (true/false)

Example:

```bash
maton trello card view CARD_ID --members --checklists all
```

#### Create Card

```bash
POST /trello/1/cards
Content-Type: application/json

{
  "name": "Implement feature X",
  "desc": "Description of the task",
  "idList": "LIST_ID",
  "pos": "bottom",
  "due": "2025-03-30T12:00:00.000Z",
  "idMembers": ["MEMBER_ID"],
  "idLabels": ["LABEL_ID"]
}
```

Example:

```bash
maton trello card create --list LIST_ID --name 'Implement feature X' --desc 'Description of the task' --due 2025-03-30T12:00:00.000Z --member-ids MEMBER_ID --label-ids LABEL_ID
```

#### Update Card

```bash
PUT /trello/1/cards/{id}
Content-Type: application/json

{
  "name": "Updated card name",
  "desc": "Updated description",
  "due": "2025-04-15T12:00:00.000Z"
}
```

Example:

```bash
maton trello card update CARD_ID --name 'Updated card name' --desc 'Updated description' --due 2025-04-15T12:00:00.000Z
```

#### Move Card to List

```bash
PUT /trello/1/cards/{id}
Content-Type: application/json

{
  "idList": "NEW_LIST_ID"
}
```

Example:

```bash
maton trello card update CARD_ID --list NEW_LIST_ID
```

#### Archive Card

Example:

```bash
maton trello card update CARD_ID --closed
```

#### Delete Card

```bash
DELETE /trello/1/cards/{id}
```

Example:

```bash
maton trello card delete CARD_ID
```

#### Add Comment to Card

```bash
POST /trello/1/cards/{id}/actions/comments
Content-Type: application/json

{
  "text": "This is a comment"
}
```

Example:

```bash
maton trello card comment CARD_ID --text 'This is a comment'
```

#### Add Member to Card

```bash
POST /trello/1/cards/{id}/idMembers
Content-Type: application/json

{
  "value": "MEMBER_ID"
}
```

Example:

```bash
maton trello card assign CARD_ID --member MEMBER_ID
```

#### Remove Member from Card

```bash
DELETE /trello/1/cards/{id}/idMembers/{idMember}
```

Example:

```bash
maton trello card unassign CARD_ID --member MEMBER_ID
```

#### Add Label to Card

```bash
POST /trello/1/cards/{id}/idLabels
Content-Type: application/json

{
  "value": "LABEL_ID"
}
```

Example:

```bash
maton trello card label CARD_ID --label LABEL_ID
```

### Checklists

#### Get Checklist

```bash
GET /trello/1/checklists/{id}
```

Example:

```bash
maton trello checklist view CHECKLIST_ID
```

#### Create Checklist

```bash
POST /trello/1/checklists
Content-Type: application/json

{
  "idCard": "CARD_ID",
  "name": "Task Checklist"
}
```

Example:

```bash
maton trello checklist create --card CARD_ID --name 'Task Checklist'
```

#### Create Checklist Item

```bash
POST /trello/1/checklists/{id}/checkItems
Content-Type: application/json

{
  "name": "Subtask 1",
  "pos": "bottom"
}
```

Example:

```bash
maton trello checkitem create --checklist CHECKLIST_ID --name 'Subtask 1' --pos bottom
```

#### Update Checklist Item

```bash
PUT /trello/1/cards/{cardId}/checkItem/{checkItemId}
Content-Type: application/json

{
  "state": "complete"
}
```

Example:

```bash
maton trello checkitem update CHECKITEM_ID --card CARD_ID --state complete
```

#### Delete Checklist

```bash
DELETE /trello/1/checklists/{id}
```

Example:

```bash
maton trello checklist delete CHECKLIST_ID
```

### Labels

#### Get Board Labels

```bash
GET /trello/1/boards/{id}/labels
```

Example:

```bash
maton trello label list --board BOARD_ID
```

#### Create Label

```bash
POST /trello/1/labels
Content-Type: application/json

{
  "name": "High Priority",
  "color": "red",
  "idBoard": "BOARD_ID"
}
```

Colors: `yellow`, `purple`, `blue`, `red`, `green`, `orange`, `black`, `sky`, `pink`, `lime`, `null` (no color)

Example:

```bash
maton trello label create --board BOARD_ID --name 'High Priority' --color red
```

#### Update Label

```bash
PUT /trello/1/labels/{id}
Content-Type: application/json

{
  "name": "Critical",
  "color": "red"
}
```

Example:

```bash
maton trello label update LABEL_ID --name Critical --color red
```

#### Delete Label

```bash
DELETE /trello/1/labels/{id}
```

Example:

```bash
maton trello label delete LABEL_ID
```

### Search

#### Search All

```bash
GET /trello/1/search?query=keyword&modelTypes=cards,boards
```

Query parameters:
- `query` - Search query (required)
- `modelTypes` - Comma-separated: `actions`, `boards`, `cards`, `members`, `organizations`
- `board_fields` - Fields to return for boards
- `card_fields` - Fields to return for cards
- `cards_limit` - Max cards to return (1-1000)

Example:

```bash
maton trello search --query keyword --models cards,boards
```

## Code Examples

### CLI

```bash
# List boards as JSON
maton trello board list --json

# Filter with jq — e.g., only open boards by name
# Note: --jq requires --json
maton trello board list --json --jq '.[] | select(.closed == false) | .name'

# Extract specific fields from cards in a list
maton trello card list --list LIST_ID --json --jq '.[] | {id, name, due}'
```

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// Get boards
const boards = await fetch(
  'https://api.maton.ai/trello/1/members/me/boards',
  { headers }
).then(r => r.json());

// Create card
await fetch(
  'https://api.maton.ai/trello/1/cards',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'New Task',
      idList: 'LIST_ID',
      desc: 'Task description'
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Get boards
boards = requests.get(
    'https://api.maton.ai/trello/1/members/me/boards',
    headers=headers
).json()

# Create card
response = requests.post(
    'https://api.maton.ai/trello/1/cards',
    headers=headers,
    json={
        'name': 'New Task',
        'idList': 'LIST_ID',
        'desc': 'Task description'
    }
)
```

## Notes

- IDs are 24-character alphanumeric strings
- Use `me` to reference the authenticated user
- Dates are in ISO 8601 format
- `pos` can be `top`, `bottom`, or a positive number
- Card positions within lists are floating point numbers
- Use `fields` parameter to limit returned data and improve performance
- Archived items can be retrieved with `filter=closed`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Trello connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 404 | Board, list, or card not found |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Trello API |

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

1. Ensure your URL path starts with `trello`. For example:

- Correct: `https://api.maton.ai/trello/1/members/me/boards`
- Incorrect: `https://api.maton.ai/1/members/me/boards`

## Resources

- [Trello API Overview](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)
- [Boards](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)
- [Lists](https://developer.atlassian.com/cloud/trello/rest/api-group-lists/)
- [Cards](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)
- [Checklists](https://developer.atlassian.com/cloud/trello/rest/api-group-checklists/)
- [Labels](https://developer.atlassian.com/cloud/trello/rest/api-group-labels/)
- [Members](https://developer.atlassian.com/cloud/trello/rest/api-group-members/)
- [Search](https://developer.atlassian.com/cloud/trello/rest/api-group-search/)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
