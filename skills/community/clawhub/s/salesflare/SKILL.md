---
name: salesflare
description: Work with Salesflare CRM through its native OAuth MCP connection for accounts, contacts, opportunities, tasks, pipelines, users, tags, and account feeds.
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
      },
  }
---

# Salesflare CRM

## Overview

Use Salesflare's native OAuth MCP connection for CRM work. Users connect through their host's normal OAuth flow.

Production MCP endpoint: `https://mcp.salesflare.com/mcp`

## Workflow

1. Find the Salesflare MCP tools available in the current runtime.
2. Verify the connection with a small read-only request, such as listing pipelines or fetching the current user.
3. Select tools by entity and action description; tool prefixes can differ by host.
4. Use native tools for supported reads and writes.
5. Confirm mutations before execution and report compact results with IDs.

Prefer native MCP operations for accounts, contacts, opportunities, tasks, pipelines, users, tags, and account feeds. Saved connection metadata alone is not proof that the connection works; verify one actual read.

## Mutation Safety Rules

- **Create and update operations:** require explicit user confirmation before execution. Never infer consent.
- **Delete operations:** always require explicit confirmation. Never infer consent from prior conversation.
- Do not perform bulk mutations without explicit confirmation.
- Prefer single-record updates before bulk updates.
- Include affected record IDs in write results for traceability.
- On rate limiting, respect retry guidance from the MCP tool. If retries exhaust, stop and report clearly.

## Output Rules

- Default to a concise summary with key IDs and changed fields.
- Provide raw JSON only when the user asks for the full payload.
- For large result sets, return the most relevant subset and mention the total when available.

## Connection and test safety

Use only native Salesflare MCP tools. Do not request or copy OAuth tokens, alter existing connections, or substitute another transport when an operation is unavailable. Report the missing capability.

Before creating test fixtures, verify that native tools can clean them up. If cleanup is unavailable, do not create records without explicit approval to leave labeled test fixtures behind. Never test updates on existing records.
