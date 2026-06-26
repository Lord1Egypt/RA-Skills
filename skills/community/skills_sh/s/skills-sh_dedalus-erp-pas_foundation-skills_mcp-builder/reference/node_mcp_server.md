# Node/TypeScript MCP Server Implementation Guide

## Overview

This document provides Node/TypeScript-specific best practices and examples for implementing MCP servers using the MCP TypeScript SDK.

---

## Quick Reference

### Key Imports
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"
import express from "express"
import { z } from "zod"
```

### Server Initialization
```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0"
})
```

### Tool Registration Pattern
```typescript
server.registerTool(
  "tool_name",
  {
    title: "Tool Display Name",
    description: "What the tool does",
    inputSchema: { param: z.string() },
    outputSchema: { result: z.string() }
  },
  async ({ param }) => {
    const output = { result: `Processed: ${param}` }
    return {
      content: [{ type: "text", text: JSON.stringify(output) }],
      structuredContent: output
    }
  }
)
```

---

## Project Structure

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts          # Main entry point
│   ├── types.ts          # TypeScript type definitions
│   ├── tools/            # Tool implementations
│   ├── services/         # API clients and utilities
│   ├── schemas/          # Zod validation schemas
│   └── constants.ts      # Shared constants
└── dist/                 # Built JavaScript files
```

---

## Zod Schemas for Input Validation

```typescript
import { z } from "zod"

const CreateUserSchema = z.object({
  name: z.string()
    .min(1, "Name is required")
    .max(100, "Name must not exceed 100 characters"),
  email: z.string()
    .email("Invalid email format"),
  age: z.number()
    .int("Age must be a whole number")
    .min(0, "Age cannot be negative")
}).strict()

// Enums
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const SearchSchema = z.object({
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("Output format")
})
```

---

## Package Configuration

### package.json

```json
{
  "name": "{service}-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "axios": "^1.7.9",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Quality Checklist

- [ ] All tools registered using `registerTool` with complete configuration
- [ ] All tools include `title`, `description`, `inputSchema`, and `annotations`
- [ ] All Zod schemas have proper constraints and error messages
- [ ] Error messages are clear and actionable
- [ ] `npm run build` completes successfully
- [ ] No use of `any` type
- [ ] Pagination properly implemented where applicable
