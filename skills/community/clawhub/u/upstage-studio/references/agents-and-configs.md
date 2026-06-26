# Agents & Configs API

## Agents

### POST /v2/agents — Create Agent

```json
{
  "name": "invoice-processor",
  "visibility": "private",
  "expires_after": 86400
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Agent name |
| `visibility` | `"public"` \| `"readonly"` \| `"private"` | No | Access control. Default: `"private"` |
| `expires_after` | integer \| null | No | Job expiry policy in seconds. Positive integer only. null = permanent |
| `clone` | object | No | Clone an existing Agent |

**Response:**

```json
{
  "id": "agt_xxx",
  "object": "agent",
  "name": "invoice-processor",
  "visibility": "private",
  "expires_after": 86400,
  "description": null,
  "category": null,
  "thumbnail": null,
  "language": null,
  "supported_doc_types": [],
  "copy_count": 0,
  "source_agent_id": null,
  "published_config_id": null,
  "published_config_external_id": null,
  "like_count": 0,
  "liked": false,
  "created_at": 1700000000,
  "updated_at": 1700000000
}
```

#### Cloning an Agent

Clone an existing Agent's Configs (and optionally Job data):

```json
{
  "name": "cloned-agent",
  "clone": {
    "agent_id": "agt_src",
    "with_jobs": true,
    "config_id": "cfg_xxx",
    "source": "studio"
  }
}
```

| Field | Description |
|-------|-------------|
| `clone.agent_id` | Source Agent ID (required) |
| `clone.with_jobs` | Include Job data (default: false) |
| `clone.config_id` | Clone only this specific Config |
| `clone.source` | Clone only Jobs with this source |

### GET /v2/agents — List Agents

Cursor pagination applied.

### GET /v2/agents/library — List Public Agents

Lists published public agents for the library UI.

**Query parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | No | Filter by category |
| `language` | string | No | Filter by language |
| `after` | string | No | Cursor: return results after this ID |
| `before` | string | No | Cursor: return results before this ID |
| `limit` | integer | No | Maximum number of results |
| `order` | `"asc"` \| `"desc"` | No | Sort by `created_at`. Default: `"asc"` |

### GET /v2/agents/{agent_id} — Get Agent

### POST /v2/agents/{agent_id} — Update Agent

Legacy update endpoint kept for backward compatibility.

Can change only `name`, `visibility`, `expires_after`.

```json
{ "name": "new-name", "visibility": "public", "expires_after": null }
```

For library metadata and publish flow, prefer `PATCH /v2/agents/{agent_id}` and `PUT /v2/agents/{agent_id}/visibility`.

### PATCH /v2/agents/{agent_id} — Patch Agent Metadata

Partial update endpoint for library-facing metadata.

```json
{
  "name": "invoice-processor",
  "expires_after": null,
  "description": "Extracts structured invoice fields",
  "category": "finance",
  "language": "en",
  "supported_doc_types": ["invoice", "receipt"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string \| null | No | Agent name |
| `expires_after` | integer \| null | No | Job expiry policy in seconds. `null` disables expiry |
| `description` | string \| null | No | Library description |
| `category` | string \| null | No | Library category |
| `language` | string \| null | No | Language metadata |
| `supported_doc_types` | array[string] \| null | No | Supported document types |

Only provided fields are updated.

### PUT /v2/agents/{agent_id}/visibility — Publish / Unpublish Agent

Dedicated publish-state endpoint. Use this instead of the legacy `POST /v2/agents/{agent_id}` when managing library visibility.

```json
{
  "visibility": "public",
  "published_config_id": "cfg_xxx"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `visibility` | `"public"` \| `"readonly"` \| `"private"` | Yes | Target visibility |
| `published_config_id` | string \| null | Conditional | Config to publish. Required when `visibility = "public"` |

Notes:
- When switching to `public`, `published_config_id` is required.
- When switching to `private`, `published_config_id` is cleared automatically.
- Response includes `published_config_external_id` for UI-friendly display.

### POST /v2/agents/{agent_id}/thumbnail — Upload Thumbnail

Multipart upload endpoint for agent library thumbnails.

**Request:**
- `Content-Type: multipart/form-data`
- form field: `file`

Returns the updated Agent with `thumbnail` set to a presigned URL.

### DELETE /v2/agents/{agent_id}/thumbnail — Delete Thumbnail

Removes the current thumbnail and returns the updated Agent.

### DELETE /v2/agents/{agent_id} — Delete Agent

```json
{ "id": "agt_xxx", "object": "agent", "deleted": true }
```

### POST /v2/agents/{agent_id}/likes — Like Agent

Idempotent like endpoint.

**Response:**

```json
{
  "agent_id": "agt_xxx",
  "liked": true,
  "like_count": 12
}
```

### DELETE /v2/agents/{agent_id}/likes — Unlike Agent

Idempotent unlike endpoint.

**Response:**

```json
{
  "agent_id": "agt_xxx",
  "liked": false,
  "like_count": 11
}
```

### Agent Response Fields

Agent responses now include library and social metadata in addition to core execution fields.

| Field | Type | Description |
|-------|------|-------------|
| `description` | string \| null | Library description |
| `category` | string \| null | Library category |
| `thumbnail` | string \| null | Presigned thumbnail URL |
| `language` | string \| null | Language metadata |
| `supported_doc_types` | array[string] | Supported document types |
| `copy_count` | integer | Number of times the agent has been copied |
| `source_agent_id` | string \| null | Source agent ID if cloned |
| `published_config_id` | string \| null | Currently published config ID |
| `published_config_external_id` | string \| null | Human-friendly published config index |
| `like_count` | integer | Total likes |
| `liked` | bool | Whether the current user liked the agent |

---

## Configs

A Config defines the workflow for an Agent — the execution order of Steps and conditional branching rules.

### POST /v2/agents/{agent_id}/configs — Create Config

```json
{
  "name": "parse-classify-extract",
  "is_default": true,
  "steps": [
    {
      "name": "parse",
      "type": "document-parse",
      "data": { "ocr": "auto", "coordinates": true },
      "is_first": true,
      "next_steps": [{ "step_name": "classify" }]
    },
    {
      "name": "classify",
      "type": "document-classify",
      "data": { "confidence": true },
      "next_steps": [
        { "step_name": "extract-invoice", "condition": { "field": "document_type", "operator": "==", "value": "Invoice" } },
        { "step_name": "extract-default" }
      ]
    },
    {
      "name": "extract-invoice",
      "type": "information-extract",
      "data": { "confidence": true, "location": true, "mode": "enhanced" },
      "next_steps": []
    },
    {
      "name": "extract-default",
      "type": "information-extract",
      "data": {},
      "next_steps": []
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Config name |
| `is_default` | bool | No | Default Config. Setting true auto-unsets the previous default |
| `steps` | array | Yes | Step definitions |

**Step Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique within Config. Referenced by next_steps |
| `type` | string | Yes | Step type (see [step-types.md](step-types.md)) |
| `data` | object | Yes | Type-specific parameters |
| `is_first` | bool | No | Starting Step. Exactly **one** must be true |
| `next_steps` | array | Yes | Next Steps. Empty array = workflow ends |

**Validation Rules:**
- Exactly one Step must have `is_first: true`
- Step names must be unique within a Config
- `next_steps` step_name references must exist in the same Config
- Circular references are not allowed

**Step Ordering Rules:**
- `document-parse` (DP) is **required** as the first step in every Config. All workflows must start with DP.
- Steps must follow the order: `document-parse` → `document-classify` → `information-extract` (DP → DC → IE).
  - `document-classify` and `information-extract` are optional, but when used they must respect this order.
  - `document-classify` cannot appear after `information-extract`.
- `instruct` steps can be inserted **anywhere after** `document-parse`. Common patterns:
  - DP → Instruct
  - DP → IE → Instruct
  - DP → DC → IE → Instruct
  - DP → DC → Instruct → IE (Instruct between DC and IE)
- Multiple `instruct` steps can be chained: `instruct` → `instruct`.

**Response:**

```json
{
  "id": "cfg_xxx",
  "external_id": "1",
  "object": "config",
  "agent_id": "agt_xxx",
  "name": "parse-classify-extract",
  "is_default": true,
  "steps": [...],
  "created_at": 1700000000,
  "updated_at": 1700000000
}
```

`external_id` is a sequential index within the Agent. You can use this number instead of `cfg_xxx` when querying.

### GET /v2/agents/{agent_id}/configs — List Configs

### GET /v2/agents/{agent_id}/configs/{config_id} — Get Config

`config_id` accepts either `cfg_xxx` or a numeric index (`"1"`, `"2"`).

### POST /v2/agents/{agent_id}/configs/{config_id} — Update Config

Only `name` and `is_default` can be changed. **Steps cannot be modified.**

```json
{ "name": "new-name", "is_default": true }
```

### DELETE /v2/agents/{agent_id}/configs/{config_id} — Delete Config

### Conditional Branching (next_steps)

Branch to different Steps based on `document-classify` results:

```json
"next_steps": [
  {
    "step_name": "extract-invoice",
    "condition": {
      "field": "document_type",
      "operator": "==",
      "value": "Invoice"
    }
  },
  {
    "step_name": "extract-default"
  }
]
```

- Items with `condition`: proceed only when condition is true
- Items without `condition`: **fallback** (used when no condition matches)
- Supported operators: `==`, `!=`, `in`, `not in`, `contains`
- `field` supports nested access: `"user.profile.name"`, `"documents[0].name"`
