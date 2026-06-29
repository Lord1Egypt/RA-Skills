# Zoho CRM Connector Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `zoho-crm-connector`

x402 availability: not enabled for this product.

## `create_records`

Action slug: `create-records`

Price: `5` credits

Create one or more records in a CRM module. Provide either record (single) or records (batch, max 100). Requires 'add' permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apply_feature_execution` | `array` | no | Feature execution keys to apply (e.g., layout_rules) |
| `lar_id` | `string` | no | Assignment rule ID |
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional body parameters to pass through |
| `record` | `object` | no | Single record payload with field name/value pairs |
| `records` | `array` | no | List of record payloads (max 100) |
| `trigger` | `array` | no | Workflow/automation triggers to fire (e.g., workflow, approval) |

Sample parameters:

```json
{
  "apply_feature_execution": [
    "example apply feature execution"
  ],
  "lar_id": "example lar id",
  "module_api_name": "example module api name",
  "options": {},
  "record": {},
  "records": [
    {}
  ],
  "trigger": [
    "example trigger"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "apply_feature_execution": {
    "description": "Feature execution keys to apply (e.g., layout_rules)",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "lar_id": {
    "description": "Assignment rule ID",
    "required": false,
    "type": "string"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional body parameters to pass through",
    "required": false,
    "type": "object"
  },
  "record": {
    "description": "Single record payload with field name/value pairs",
    "required": false,
    "type": "object"
  },
  "records": {
    "description": "List of record payloads (max 100)",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "trigger": {
    "description": "Workflow/automation triggers to fire (e.g., workflow, approval)",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `delete_records`

Action slug: `delete-records`

Price: `5` credits

Delete one or more CRM records. Provide exactly one of record_id (single) or record_ids (bulk, max 100). Requires 'delete' permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional query parameters to pass through |
| `record_id` | `string` | no | Single record ID to delete |
| `record_ids` | `array` | no | List of record IDs for bulk delete (max 100) |
| `wf_trigger` | `boolean` | no | Whether to trigger workflows on delete (defaults to true in Zoho) |

Sample parameters:

```json
{
  "module_api_name": "example module api name",
  "options": {},
  "record_id": "example record id",
  "record_ids": [
    "example record id"
  ],
  "wf_trigger": true
}
```

Generated JSON parameter schema:

```json
{
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  },
  "record_id": {
    "description": "Single record ID to delete",
    "required": false,
    "type": "string"
  },
  "record_ids": {
    "description": "List of record IDs for bulk delete (max 100)",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "wf_trigger": {
    "description": "Whether to trigger workflows on delete (defaults to true in Zoho)",
    "required": false,
    "type": "boolean"
  }
}
```

## `describe_action`

Action slug: `describe-action`

Price: `5` credits

Get the parameter schema for any action. Useful for discovering required and optional fields before calling an action.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `action_to_describe` | `string` | no | The action name to describe. Omit to get schemas for all actions. |

Sample parameters:

```json
{
  "action_to_describe": "list_records"
}
```

Generated JSON parameter schema:

```json
{
  "action_to_describe": {
    "description": "The action name to describe. Omit to get schemas for all actions.",
    "enum": [
      "list_records",
      "get_record",
      "search_records",
      "query_records",
      "create_records",
      "update_records",
      "delete_records",
      "list_modules",
      "fields_metadata"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `fields_metadata`

Action slug: `fields-metadata`

Price: `5` credits

Retrieve field definitions for a CRM module, or a single field by ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `field_id` | `string` | no | Specific field ID for metadata lookup. Omit to get all fields. |
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional query parameters to pass through |

Sample parameters:

```json
{
  "field_id": "example field id",
  "module_api_name": "example module api name",
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "field_id": {
    "description": "Specific field ID for metadata lookup. Omit to get all fields.",
    "required": false,
    "type": "string"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  }
}
```

## `get_record`

Action slug: `get-record`

Price: `5` credits

Fetch a single CRM record by its ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `fields` | `array` | no | Specific fields to retrieve |
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional query parameters to pass through |
| `record_id` | `string` | yes | The record ID to fetch |

Sample parameters:

```json
{
  "fields": [
    "example field"
  ],
  "module_api_name": "example module api name",
  "options": {},
  "record_id": "example record id"
}
```

Generated JSON parameter schema:

```json
{
  "fields": {
    "description": "Specific fields to retrieve",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  },
  "record_id": {
    "description": "The record ID to fetch",
    "required": true,
    "type": "string"
  }
}
```

## `list_modules`

Action slug: `list-modules`

Price: `5` credits

List all available modules in the Zoho CRM account.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters to pass through |

Sample parameters:

```json
{
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  }
}
```

## `list_records`

Action slug: `list-records`

Price: `5` credits

Retrieve records from a CRM module with optional filtering, sorting, and pagination. Maximum 50 fields per request. Use page_token for records beyond page 2000.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `converted` | `string` | no | Filter by converted status |
| `cvid` | `string` | no | Custom view ID. Cannot be used with sort_by. |
| `fields` | `array` | no | Fields to retrieve (max 50). Required unless ids is provided. |
| `ids` | `array` | no | Specific record IDs to fetch |
| `include_child` | `boolean` | no | Include child territory records when territory_id is set |
| `module_api_name` | `string` | yes | Zoho CRM module API name (e.g., Leads, Contacts, Deals) |
| `options` | `object` | no | Additional query parameters to pass through |
| `page` | `integer` | no | Page number (1-based). Cannot be used with page_token. |
| `page_token` | `string` | no | Page token for records beyond page 2000. Cannot be used with page. |
| `per_page` | `integer` | no | Records per page (1-200) |
| `sort_by` | `string` | no | Field API name to sort by. Cannot be used with cvid. |
| `sort_order` | `string` | no | Sort direction |
| `territory_id` | `string` | no | Territory ID filter |

Sample parameters:

```json
{
  "converted": "true",
  "cvid": "example cvid",
  "fields": [
    "example field"
  ],
  "ids": [
    "example id"
  ],
  "include_child": true,
  "module_api_name": "example module api name",
  "options": {},
  "page": 1
}
```

Generated JSON parameter schema:

```json
{
  "converted": {
    "description": "Filter by converted status",
    "enum": [
      "true",
      "false",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "cvid": {
    "description": "Custom view ID. Cannot be used with sort_by.",
    "required": false,
    "type": "string"
  },
  "fields": {
    "description": "Fields to retrieve (max 50). Required unless ids is provided.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "ids": {
    "description": "Specific record IDs to fetch",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include_child": {
    "description": "Include child territory records when territory_id is set",
    "required": false,
    "type": "boolean"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name (e.g., Leads, Contacts, Deals)",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  },
  "page": {
    "description": "Page number (1-based). Cannot be used with page_token.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "page_token": {
    "description": "Page token for records beyond page 2000. Cannot be used with page.",
    "required": false,
    "type": "string"
  },
  "per_page": {
    "description": "Records per page (1-200)",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "sort_by": {
    "description": "Field API name to sort by. Cannot be used with cvid.",
    "required": false,
    "type": "string"
  },
  "sort_order": {
    "description": "Sort direction",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "territory_id": {
    "description": "Territory ID filter",
    "required": false,
    "type": "string"
  }
}
```

## `query_records`

Action slug: `query-records`

Price: `5` credits

Run a COQL (CRM Object Query Language) query for advanced record retrieval. Follows SQL-like syntax: select Field1, Field2 from Module where condition limit N.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional body parameters to pass through |
| `select_query` | `string` | yes | COQL select query string |

Sample parameters:

```json
{
  "options": {},
  "select_query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional body parameters to pass through",
    "required": false,
    "type": "object"
  },
  "select_query": {
    "description": "COQL select query string",
    "required": true,
    "type": "string"
  }
}
```

## `search_records`

Action slug: `search-records`

Price: `5` credits

Search for CRM records using exactly one search method: criteria, email, phone, or word.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `approved` | `string` | no | Filter by approved status |
| `converted` | `string` | no | Filter by converted status |
| `criteria` | `string` | no | Search criteria string (e.g., ((Stage:equals:Closed Won)and(Amount:greater_than:10000))) |
| `email` | `string` | no | Search by email address |
| `fields` | `array` | no | Fields to retrieve (max 50) |
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional query parameters to pass through |
| `page` | `integer` | no | Page number (1-based) |
| `per_page` | `integer` | no | Records per page (1-200) |
| `phone` | `string` | no | Search by phone number |
| `record_type` | `string` | no | Users module type filter (e.g., AllUsers, ActiveUsers) |
| `word` | `string` | no | Search by keyword across fields |

Sample parameters:

```json
{
  "approved": "true",
  "converted": "true",
  "criteria": "example criteria",
  "email": "user@example.com",
  "fields": [
    "example field"
  ],
  "module_api_name": "example module api name",
  "options": {},
  "page": 1
}
```

Generated JSON parameter schema:

```json
{
  "approved": {
    "description": "Filter by approved status",
    "enum": [
      "true",
      "false",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "converted": {
    "description": "Filter by converted status",
    "enum": [
      "true",
      "false",
      "both"
    ],
    "required": false,
    "type": "string"
  },
  "criteria": {
    "description": "Search criteria string (e.g., ((Stage:equals:Closed Won)and(Amount:greater_than:10000)))",
    "required": false,
    "type": "string"
  },
  "email": {
    "description": "Search by email address",
    "required": false,
    "type": "string"
  },
  "fields": {
    "description": "Fields to retrieve (max 50)",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters to pass through",
    "required": false,
    "type": "object"
  },
  "page": {
    "description": "Page number (1-based)",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Records per page (1-200)",
    "maximum": 200,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "phone": {
    "description": "Search by phone number",
    "required": false,
    "type": "string"
  },
  "record_type": {
    "description": "Users module type filter (e.g., AllUsers, ActiveUsers)",
    "required": false,
    "type": "string"
  },
  "word": {
    "description": "Search by keyword across fields",
    "required": false,
    "type": "string"
  }
}
```

## `update_records`

Action slug: `update-records`

Price: `5` credits

Update one or more existing CRM records. Provide record or records (max 100). Use record_id for single-record updates. Requires 'edit' permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `append_values` | `object` | no | Append values for multi-select picklist fields. Keys are field names, values are boolean true. |
| `apply_feature_execution` | `array` | no | Feature execution keys to apply (e.g., layout_rules) |
| `lar_id` | `string` | no | Assignment rule ID |
| `module_api_name` | `string` | yes | Zoho CRM module API name |
| `options` | `object` | no | Additional body parameters to pass through |
| `record` | `object` | no | Single record payload with field name/value pairs |
| `record_id` | `string` | no | Record ID for single-record update. When provided, only one record is allowed. |
| `records` | `array` | no | List of record payloads (max 100). Each must include its 'id' for batch updates. |
| `trigger` | `array` | no | Workflow/automation triggers to fire |

Sample parameters:

```json
{
  "append_values": {},
  "apply_feature_execution": [
    "example apply feature execution"
  ],
  "lar_id": "example lar id",
  "module_api_name": "example module api name",
  "options": {},
  "record": {},
  "record_id": "example record id",
  "records": [
    {}
  ]
}
```

Generated JSON parameter schema:

```json
{
  "append_values": {
    "description": "Append values for multi-select picklist fields. Keys are field names, values are boolean true.",
    "required": false,
    "type": "object"
  },
  "apply_feature_execution": {
    "description": "Feature execution keys to apply (e.g., layout_rules)",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "lar_id": {
    "description": "Assignment rule ID",
    "required": false,
    "type": "string"
  },
  "module_api_name": {
    "description": "Zoho CRM module API name",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional body parameters to pass through",
    "required": false,
    "type": "object"
  },
  "record": {
    "description": "Single record payload with field name/value pairs",
    "required": false,
    "type": "object"
  },
  "record_id": {
    "description": "Record ID for single-record update. When provided, only one record is allowed.",
    "required": false,
    "type": "string"
  },
  "records": {
    "description": "List of record payloads (max 100). Each must include its 'id' for batch updates.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "trigger": {
    "description": "Workflow/automation triggers to fire",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```
