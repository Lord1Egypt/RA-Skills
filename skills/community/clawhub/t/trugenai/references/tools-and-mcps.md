# Tools & MCPs API Reference

## Tools — Function Calling

Tools allow agents to call external APIs or trigger client-side actions during a conversation.

**Two tool types:**
- `tool.api` — Agent calls your server-side endpoint (HTTP GET/POST/etc.)
- `tool.client` — Agent triggers a client-side function in the browser/frontend

### Create a Tool

`POST /v1/ext/tool`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/tool \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "type": "tool.api",
    "schema": {
      "type": "function",
      "name": "get_customer_order",
      "description": "Fetches order details for a customer by order ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "order_id": {
            "type": "string",
            "description": "The order ID to look up"
          }
        },
        "required": ["order_id"]
      }
    },
    "request_config": {
      "method": "GET",
      "url": "https://api.yourcompany.com/orders",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "Accept": "application/json"
      }
    },
    "event_messages": {
      "on_start": { "message": "Let me look up that order for you." },
      "on_success": { "message": "I found your order details." },
      "on_delay": { "delay": 3, "message": "Still looking, just a moment..." },
      "on_error": { "message": "I was unable to retrieve your order at this time." }
    }
  }'
```

### Key Tool Fields

| Field | Description |
|-------|-------------|
| `type` | `"tool.api"` (server-side) or `"tool.client"` (browser-side) |
| `schema.name` | Function name the LLM calls |
| `schema.description` | How the LLM decides when to use this tool |
| `schema.parameters` | JSON Schema for the function arguments |
| `request_config.method` | HTTP method (`GET`, `POST`, etc.) |
| `request_config.url` | Your endpoint URL |
| `request_config.headers` | Request headers (auth tokens, etc.) |
| `event_messages.on_start` | What the avatar says when tool starts |
| `event_messages.on_success` | What the avatar says on success |
| `event_messages.on_delay` | Message if taking longer than `delay` seconds |
| `event_messages.on_error` | What the avatar says on failure |

### Attach Tool to Agent

Pass the tool `id` in the `tool` array when creating/updating an agent:
```json
"tool": [
  { "id": "611eaabb-0884-440f-a4f1-a04b9ad8a597", "name": "get_customer_order", "description": "Fetches customer order info" }
]
```

### Other Tool Operations

```bash
# Get tool by ID
curl -X GET https://api.trugen.ai/v1/ext/tool/{id} -H 'x-api-key: <api-key>'

# List all tools
curl -X GET https://api.trugen.ai/v1/ext/tool -H 'x-api-key: <api-key>'

# Update tool
curl -X PUT https://api.trugen.ai/v1/ext/tool/{id} -H 'Content-Type: application/json' -H 'x-api-key: <api-key>' --data '{...}'

# Delete tool
curl -X DELETE https://api.trugen.ai/v1/ext/tool/{id} -H 'x-api-key: <api-key>'
```

---

## MCPs — Model Context Protocol Servers

MCPs integrate external MCP-compatible server endpoints into your agents, enabling access to a broad ecosystem of tools and data sources via the Model Context Protocol standard.

### Create an MCP

`POST /v1/ext/mcp`

```bash
curl --request POST \
  --url https://api.trugen.ai/v1/ext/mcp \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '{
    "name": "Livekit Docs",
    "description": "MCP server to get livekit info",
    "type": "shttp/sse",
    "request_config": {
      "url": "https://your-mcp-server.com/sse",
      "headers": {
        "User-Agent": "Trugen Avatar",
        "Accept": "application/json"
      }
    }
  }'
```

**Response:**
```json
{
  "id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
  "name": "Livekit Docs",
  "description": "MCP server to get livekit info",
  "type": "shttp/sse",
  "created_at": "2023-11-07T05:31:56Z"
}
```

### Key MCP Fields

| Field | Description |
|-------|-------------|
| `name` | Human-readable name for the MCP server |
| `description` | What this MCP server provides |
| `type` | Protocol type (e.g. `"shttp/sse"` for Streamable HTTP/SSE) |
| `request_config.url` | The MCP server SSE endpoint URL |
| `request_config.headers` | Authentication/custom headers |

### Attach MCP to Agent

Pass the MCP `id` in the `mcp` array when creating/updating an agent:
```json
"mcp": [
  { "id": "dcf04568-6bf5-40cf-bd6f-d68e4cb5b216", "name": "Livekit Docs", "description": "MCP for livekit info" }
]
```

### Other MCP Operations

```bash
# Get MCP by ID
curl -X GET https://api.trugen.ai/v1/ext/mcp/{id} -H 'x-api-key: <api-key>'

# List all MCPs
curl -X GET https://api.trugen.ai/v1/ext/mcp -H 'x-api-key: <api-key>'

# Update MCP
curl -X PUT https://api.trugen.ai/v1/ext/mcp/{id} -H 'Content-Type: application/json' -H 'x-api-key: <api-key>' --data '{...}'

# Delete MCP
curl -X DELETE https://api.trugen.ai/v1/ext/mcp/{id} -H 'x-api-key: <api-key>'
```
