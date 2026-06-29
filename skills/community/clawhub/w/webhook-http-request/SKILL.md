---
name: webhook-http-request
description: "Webhook - HTTP Request: Make HTTP requests (GET, POST, PUT, DELETE, etc.). Use when an agent needs webhook http request, webhook http request, fetching data from third party rest apis for aggregation or transformation pipelines, submitting form data or json payloads to webhook endpoints for event driven workflows, authenticating with oauth protected services using bearer tokens for secure integrations, polling external services for status updates or job completion in asynchronous workflows."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/webhook-http-request
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/webhook-http-request"}}
---
# Webhook - HTTP Request

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A flexible and secure HTTP client designed for agent-driven API integrations and web service interactions. This function supports all standard HTTP methods including GET, POST, PUT, PATCH, DELETE, HEAD, and OPTIONS, enabling comprehensive RESTful API communication. Users can configure requests with custom headers, query parameters, and request bodies in JSON, plain text, or base64-encoded binary formats. The tool provides four authentication modes: none for public endpoints, basic for username/password credentials automatically encoded to Base64, bearer for OAuth-style token authentication, and header for custom API key or signature-based authentication schemes. Built-in security features include URL validation that blocks private and loopback IP addresses by default (configurable via allow_private), configurable timeouts from 1 to 120 seconds, and response size limits up to 20MB to prevent memory issues. Response handling offers four modes—auto, json, text, and base64—with auto-detection intelligently parsing responses based on content-type headers. The function returns comprehensive response metadata including status code, headers, final URL after redirects, and the parsed body, making it an essential building block for workflows that need to interact with external APIs, webhooks, or web services.

## Product Instructions
### Webhook - HTTP Request

#### Overview
A general-purpose HTTP client that can make requests to any public URL. Supports all standard HTTP methods, multiple authentication schemes, flexible body formats, and configurable response handling. Use it to call REST APIs, fetch web resources, post webhooks, or interact with any HTTP-based service.

#### Actions

##### request
Make an HTTP request to a specified URL.

**Required Fields:**
- `url` — the full URL to send the request to (must be http or https)

**Optional Fields:**
- `request_method` — HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` (default: `GET`)
- `headers` — object of custom HTTP headers (e.g., `{"Accept": "application/xml"}`)
- `query_params` — object of URL query parameters (e.g., `{"page": "2", "limit": "10"}`)
- `body_json` — JSON object body (sets Content-Type to application/json automatically)
- `body_text` — plain text body
- `body_base64` — base64-encoded binary body (for file uploads or binary data)
- `auth_type` — authentication scheme: `"none"`, `"basic"`, `"bearer"`, or `"header"` (default: `"none"`)
- `auth_username` — username for basic auth (required when auth_type is `"basic"`)
- `auth_password` — password for basic auth (required when auth_type is `"basic"`)
- `auth_token` — token for bearer auth (required when auth_type is `"bearer"`)
- `auth_header_name` — custom header name for header auth (required when auth_type is `"header"`)
- `auth_header_value` — custom header value for header auth (required when auth_type is `"header"`)
- `timeout_seconds` — request timeout in seconds, 1-120 (default: 30)
- `response_mode` — how to return the response body: `"auto"`, `"json"`, `"text"`, `"base64"` (default: `"auto"`)
- `max_response_bytes` — maximum response size in bytes, 1024-20971520 (default: 1048576 / 1 MB)
- `allow_private` — set to `true` to allow requests to private/loopback IPs (default: `false`)

**Note:** Only one body field can be used per request (`body_json`, `body_text`, or `body_base64`).

**Example — Simple GET request:**
```json
{
  "action": "request",
  "request_method": "GET",
  "url": "https://api.example.com/data",
  "query_params": {"format": "json"}
}
```

**Example — POST with JSON body:**
```json
{
  "action": "request",
  "request_method": "POST",
  "url": "https://api.example.com/items",
  "headers": {"X-Custom-Header": "my-value"},
  "body_json": {"name": "Widget", "quantity": 5}
}
```

**Example — Bearer token authentication:**
```json
{
  "action": "request",
  "request_method": "GET",
  "url": "https://api.example.com/protected/resource",
  "auth_type": "bearer",
  "auth_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Example — Basic authentication:**
```json
{
  "action": "request",
  "request_method": "GET",
  "url": "https://api.example.com/account",
  "auth_type": "basic",
  "auth_username": "myuser",
  "auth_password": "mypassword"
}
```

**Example — Custom header authentication (API key):**
```json
{
  "action": "request",
  "request_method": "GET",
  "url": "https://api.example.com/v2/search",
  "auth_type": "header",
  "auth_header_name": "X-API-Key",
  "auth_header_value": "abc123def456"
}
```

**Example — PUT to update a resource:**
```json
{
  "action": "request",
  "request_method": "PUT",
  "url": "https://api.example.com/items/42",
  "body_json": {"name": "Updated Widget", "quantity": 10}
}
```

**Example — DELETE a resource:**
```json
{
  "action": "request",
  "request_method": "DELETE",
  "url": "https://api.example.com/items/42"
}
```

**Example — Get binary response as base64:**
```json
{
  "action": "request",
  "request_method": "GET",
  "url": "https://example.com/image.png",
  "response_mode": "base64"
}
```

#### Response Format
Successful requests return:
- `status_code` — HTTP status code (e.g., 200, 404)
- `headers` — response headers as an object
- `content_type` — the Content-Type header value
- `url` — the final URL (after any redirects)
- `body_json`, `body_text`, or `body_base64` — response body in the format determined by `response_mode`

#### Common Workflows

1. **Call a REST API** — Use GET/POST/PUT/DELETE with `body_json` and `auth_type` to interact with any REST service.
2. **Send a webhook** — POST a JSON payload to a webhook URL to trigger external automations.
3. **Fetch a web page** — GET any public URL and receive the HTML as text.
4. **Download binary content** — GET a file URL with `response_mode: "base64"` to receive binary data encoded for further processing.
5. **Check endpoint availability** — Use HEAD or OPTIONS to verify a service is reachable without downloading the full response body.

#### Important Notes
- Only `http` and `https` URLs are supported.
- Requests to private or loopback IP addresses are blocked by default. Set `allow_private` to `true` to override.
- Only one body type can be provided per request. Supplying more than one of `body_json`, `body_text`, or `body_base64` will cause an error.
- When `response_mode` is `"auto"`, JSON responses are parsed automatically; otherwise text is returned, or base64 for binary content.
- Responses exceeding `max_response_bytes` will be rejected. Increase the limit (up to ~20 MB) for larger payloads.
- The maximum timeout is 120 seconds.

## When To Use
- Use this skill for `Webhook - HTTP Request` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: webhook   http request, webhook http request, fetching data from third party rest apis for aggregation or transformation pipelines, submitting form data or json payloads to webhook endpoints for event driven workflows, authenticating with oauth protected services using bearer tokens for secure integrations, polling external services for status updates or job completion in asynchronous workflows, request, url.
- Supported action names: `request`.

## Use Cases
- Fetching data from third-party REST APIs for aggregation or transformation pipelines
- submitting form data or JSON payloads to webhook endpoints for event-driven workflows
- authenticating with OAuth-protected services using bearer tokens for secure integrations
- polling external services for status updates or job completion in asynchronous workflows
- posting structured data to CRM or marketing automation platforms
- retrieving remote configuration files or feature flags from external services
- sending notifications to Slack or Discord webhooks with custom message payloads
- interacting with payment gateways or e-commerce APIs for order processing
- fetching remote JSON schemas or API specifications for validation workflows
- integrating with legacy systems via custom header-based authentication for enterprise data exchange

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `request` (action slug: `request`): Make an HTTP request to a specified URL. Supports all standard HTTP methods, multiple authentication schemes, and flexible body/response formats. Price: `5` credits. Parameters: `allow_private`, `auth_header_name`, `auth_header_value`, `auth_password`, `auth_token`, `auth_type`, `auth_username`, `body_base64`, plus 9 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "webhook-http-request"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "webhook-http-request"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "webhook-http-request"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "webhook-http-request"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "webhook-http-request"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "webhook-http-request"
  }
}
```

## Call This Tool
Product slug: `webhook-http-request`

Marketplace page: https://www.agentpmt.com/marketplace/webhook-http-request

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
    "name": "Webhook---HTTP-Request",
    "arguments": {
      "action": "request",
      "allow_private": false,
      "auth_header_name": "example auth header name",
      "auth_header_value": "example auth header value",
      "auth_password": "example auth password",
      "auth_token": "example auth token",
      "auth_type": "none",
      "auth_username": "example auth username",
      "body_base64": "example body base64"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "webhook-http-request",
  "parameters": {
    "action": "request",
    "allow_private": false,
    "auth_header_name": "example auth header name",
    "auth_header_value": "example auth header value",
    "auth_password": "example auth password",
    "auth_token": "example auth token",
    "auth_type": "none",
    "auth_username": "example auth username",
    "body_base64": "example body base64"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `request` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/webhook-http-request
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
