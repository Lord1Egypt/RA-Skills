---
name: zoho-crm-connector
description: "Zoho CRM Connector: Zoho CRM: search and retrieve leads, contacts, accounts, deals. Use when an agent needs zoho crm connector, automated lead qualification and scoring based on crm data, customer support agents retrieving account history and contact details, sales pipeline reporting and deal stage analysis, lead enrichment workflows that query and update prospect information, create records, module api name, record through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/zoho-crm-connector
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/zoho-crm-connector"}}
---
# Zoho CRM Connector

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
The Zoho CRM Connector enables AI agents to seamlessly interact with Zoho CRM data, allowing businesses to automate customer relationship workflows without manual intervention. Agents can retrieve and search leads, contacts, accounts, and deals using flexible query options including COQL queries, email lookups, and criteria-based searches, while also accessing module schemas and field metadata to understand the CRM structure. The connector features a secure permission-gating system that explicitly controls write operations—agents can only create, update, or delete records when specifically authorized with add, edit, or delete permissions—ensuring that automated workflows respect data governance policies. This makes it ideal for building intelligent sales assistants that can look up customer information on demand, automated lead qualification systems that query and analyze prospect data, reporting agents that aggregate CRM metrics, and customer service bots that retrieve account history to provide personalized support.

## Product Instructions
### Zoho CRM Connector

Manage records, search, query, and explore metadata in Zoho CRM.

#### Permissions

- `permissions` is a multi-select array of exact scopes: `read`, `add`, `edit`, `delete`.
- Include every scope the agent is allowed to use.
- `list_records`, `get_record`, `search_records`, `query_records`, `list_modules`, and `fields_metadata` require `read`.
- `create_records` requires `add`.
- `update_records` requires `edit`.
- `delete_records` requires `delete`.
- If `permissions` is omitted, the tool allows read-only actions.

#### Actions

##### list_records
Retrieve records from a module with optional filtering, sorting, and pagination.

**Required:** `module_api_name`, `fields` (unless `ids` is provided)
**Optional:** `ids`, `per_page` (1-200), `page`, `page_token`, `sort_by`, `sort_order` (asc/desc), `cvid`, `converted` (true/false/both), `territory_id`, `include_child`

##### get_record
Fetch a single record by its ID.

**Required:** `module_api_name`, `record_id`
**Optional:** `fields`

##### search_records
Search for records using exactly one search method: `criteria`, `email`, `phone`, or `word`.

**Required:** `module_api_name`, and exactly one of: `criteria`, `email`, `phone`, `word`
**Optional:** `fields` (max 50), `per_page` (1-200), `page`, `converted` (true/false/both), `approved` (true/false/both), `type`

##### query_records
Run a COQL query for advanced record retrieval.

**Required:** `select_query`

##### create_records
Create one or more records in a module.

**Required:** `module_api_name`, and one of: `record`, `records`

##### update_records
Update one or more existing records.

**Required:** `module_api_name`, and one of: `record`, `records`

##### delete_records
Delete one or more records.

**Required:** `module_api_name`, and exactly one of: `record_id`, `record_ids`

##### list_modules
List all available modules in the Zoho CRM account.

##### fields_metadata
Retrieve field definitions for a module, or a single field by ID.

**Required:** `module_api_name`

##### describe_action
Get the parameter schema for any action.

```json
{
  "action": "describe_action",
  "action_to_describe": "search_records"
}
```

## When To Use
- Use this skill for `Zoho CRM Connector` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: zoho crm connector, automated lead qualification and scoring based on crm data, customer support agents retrieving account history and contact details, sales pipeline reporting and deal stage analysis, lead enrichment workflows that query and update prospect information, create records, module api name, record.
- Supported action names: `create_records`, `delete_records`, `describe_action`, `fields_metadata`, `get_record`, `list_modules`, `list_records`, `query_records`, `search_records`, `update_records`.

## Use Cases
- Automated lead qualification and scoring based on CRM data
- Customer support agents retrieving account history and contact details
- Sales pipeline reporting and deal stage analysis
- Lead enrichment workflows that query and update prospect information
- Customer onboarding automation with record creation and status updates
- Duplicate contact detection and data cleanup operations
- Intelligent meeting prep assistants that pull relevant customer context before calls

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `10`.
x402 availability: not enabled for this product.

- `create_records` (action slug: `create-records`): Create one or more records in a CRM module. Provide either record (single) or records (batch, max 100). Requires 'add' permission. Price: `5` credits. Parameters: `apply_feature_execution`, `lar_id`, `module_api_name`, `options`, `record`, `records`, `trigger`.
- `delete_records` (action slug: `delete-records`): Delete one or more CRM records. Provide exactly one of record_id (single) or record_ids (bulk, max 100). Requires 'delete' permission. Price: `5` credits. Parameters: `module_api_name`, `options`, `record_id`, `record_ids`, `wf_trigger`.
- `describe_action` (action slug: `describe-action`): Get the parameter schema for any action. Useful for discovering required and optional fields before calling an action. Price: `5` credits. Parameters: `action_to_describe`.
- `fields_metadata` (action slug: `fields-metadata`): Retrieve field definitions for a CRM module, or a single field by ID. Price: `5` credits. Parameters: `field_id`, `module_api_name`, `options`.
- `get_record` (action slug: `get-record`): Fetch a single CRM record by its ID. Price: `5` credits. Parameters: `fields`, `module_api_name`, `options`, `record_id`.
- `list_modules` (action slug: `list-modules`): List all available modules in the Zoho CRM account. Price: `5` credits. Parameters: `options`.
- `list_records` (action slug: `list-records`): Retrieve records from a CRM module with optional filtering, sorting, and pagination. Maximum 50 fields per request. Use page_token for records beyond page 2000. Price: `5` credits. Parameters: `converted`, `cvid`, `fields`, `ids`, `include_child`, `module_api_name`, `options`, `page`, plus 5 more.
- `query_records` (action slug: `query-records`): Run a COQL (CRM Object Query Language) query for advanced record retrieval. Follows SQL-like syntax: select Field1, Field2 from Module where condition limit N. Price: `5` credits. Parameters: `options`, `select_query`.
- `search_records` (action slug: `search-records`): Search for CRM records using exactly one search method: criteria, email, phone, or word. Price: `5` credits. Parameters: `approved`, `converted`, `criteria`, `email`, `fields`, `module_api_name`, `options`, `page`, plus 4 more.
- `update_records` (action slug: `update-records`): Update one or more existing CRM records. Provide record or records (max 100). Use record_id for single-record updates. Requires 'edit' permission. Price: `5` credits. Parameters: `append_values`, `apply_feature_execution`, `lar_id`, `module_api_name`, `options`, `record`, `record_id`, `records`, plus 1 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "zoho-crm-connector"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "zoho-crm-connector"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "zoho-crm-connector"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "zoho-crm-connector"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "zoho-crm-connector"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "zoho-crm-connector"
  }
}
```

## Call This Tool
Product slug: `zoho-crm-connector`

Marketplace page: https://www.agentpmt.com/marketplace/zoho-crm-connector

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Zoho-CRM-Connector",
    "arguments": {
      "action": "create_records",
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
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "zoho-crm-connector",
  "parameters": {
    "action": "create_records",
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
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_records` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/zoho-crm-connector
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
