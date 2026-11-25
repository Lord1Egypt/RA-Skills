# Model Context Protocol (MCP) & AI Agent Integration

This reference covers the `@wthek` extensions designed for AI coding agents and MCP server architectures:
1. [`@wthek/mcp-error-formatter`](https://www.npmjs.com/package/@wthek/mcp-error-formatter) – Formats errors and `KitHttpError` instances into MCP tool results (`CallToolResult`), JSON-RPC 2.0 errors, or centralized formatter payloads.
2. [`@wthek/mcp`](https://www.npmjs.com/package/@wthek/mcp) – Standalone local MCP server providing AI agents with HTTP standards lookup, framework recipes, and error-handling code audits.

---

## 1. `@wthek/mcp-error-formatter`

### Purpose & Architecture

In Model Context Protocol (MCP) tool handlers, throwing raw errors or returning unstructured text strings degrades AI agent performance. `@wthek/mcp-error-formatter` bridges the `@wthek` error ecosystem into standard MCP tool results (`CallToolResult`), JSON-RPC 2.0 error responses, and `KitHttpErrorConfig` pipelines.

```
       Application / MCP Tool Handler
                    │
            (Error Thrown / Caught)
                    │
                    ▼
       ┌───────────────────────────────┐
       │   @wthek/mcp-error-formatter  │
       └──────────────┬────────────────┘
                      │
     ┌────────────────┼────────────────┐
     ▼                ▼                ▼
toMcpToolResult()  toMcpProtocolError()  mcpErrorFormatter()
     │                │                │
     ▼                ▼                ▼
MCP CallToolResult  JSON-RPC 2.0 Error   http-error-kit Formatter
(isError: true)     (code, message)     (KitHttpErrorConfig)
     │                │                │
     └────────────────┼────────────────┘
                      │
                      ▼
            MCP Client / AI Agent
```

### Installation

```bash
npm install @wthek/mcp-error-formatter http-error-kit http-response-status-code
```

### Key Functions

#### A. `toMcpToolResult(error, options?)`
Transforms any error into a standard MCP `CallToolResult` with `isError: true`, formatted text content, and structured `_meta.error` metadata.

```typescript
import { NotFoundError } from "http-error-kit";
import { toMcpToolResult } from "@wthek/mcp-error-formatter";

try {
  throw new NotFoundError("User not found", { userId: 42 });
} catch (error: unknown) {
  const result = toMcpToolResult(error, {
    includeMeta: true,
    recoveryHint: "Verify the user ID before retrying.",
  });
  return result;
}
```

Result output:
```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "[HTTP 404] User not found\nDetails: {\n  \"userId\": 42\n}"
    }
  ],
  "_meta": {
    "error": {
      "category": "RESOURCE",
      "code": -32004,
      "recoveryHint": "Verify the user ID before retrying.",
      "retryable": false
    }
  }
}
```

#### B. `toMcpProtocolError(error)`
Transforms an error into a standard JSON-RPC 2.0 protocol error object:

```typescript
import { toMcpProtocolError } from "@wthek/mcp-error-formatter";

const rpcError = toMcpProtocolError(new Error("Database connection timed out"));
// { code: -32603, message: "Database connection timed out" }
```

#### C. `mcpErrorFormatter(statusCode, message, details?)`
Plugs into `KitHttpErrorConfig.configureFormatter()` to format all `KitHttpError.toJSON()` calls into MCP-compliant payloads:

```typescript
import { KitHttpErrorConfig, NotFoundError } from "http-error-kit";
import { mcpErrorFormatter } from "@wthek/mcp-error-formatter";

// Configure once at application startup
KitHttpErrorConfig.configureFormatter(mcpErrorFormatter);

const error = new NotFoundError("Document not found");
console.log(error.toJSON());
```

---

## 2. `@wthek/mcp` (Local Agent MCP Server)

### Purpose

`@wthek/mcp` is a local MCP server that gives AI coding agents (Claude Desktop, Cursor, Antigravity) deterministic tools to inspect HTTP standards, generate copy-paste framework setup recipes, and audit source code for error anti-patterns.

### Agent Configuration

Install the package first, then configure the MCP server:

```bash
npm install @wthek/mcp
```

```json
{
  "mcpServers": {
    "wthek": {
      "command": "npx",
      "args": ["@wthek/mcp"]
    }
  }
}
```

> ⚠️ **Security Note:** Do not use `npx -y` for MCP server commands. Always install packages explicitly with `npm install` before running them via `npx`, or review the confirmation prompt when `npx` asks to install a new package. This prevents unvetted code from auto-executing in your environment.

### Available Tools

| Tool | Purpose |
| :--- | :--- |
| `lookup_http_status` | Returns RFC status metadata, required response headers, and class imports for any HTTP status code or name. |
| `get_framework_recipe` | Generates verified, copy-paste error handling recipes for Express, Fastify, Hono, Koa, NestJS, and Restify. |
| `audit_error_handling` | Performs pattern-based heuristic code audits to flag manual status mutations, swallowed logs, or missing `headersSent` checks. |

> ℹ️ **Heuristic Audit Disclaimer:** `audit_error_handling` is a fast pattern-based heuristic check for common error-handling anti-patterns. It is intentionally lightweight and non-intrusive—not a full AST-based static compiler or replacement for developer review or AI contextual reasoning.

