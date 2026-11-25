---
name: use-upgrow-agent-api
description: Connect to UpGrow's public MCP server, A2A agent and REST API to read plans, shop products, free tools and blog search results.
---

# Use the UpGrow agent API

UpGrow publishes a read-only, no-login interface for AI agents. Everything below is public and free to call. Full documentation: https://www.upgrow.com/developers

## MCP server (Streamable HTTP, stateless)

- URL: https://www.upgrow.com/mcp
- Add it to an MCP client as a remote HTTP server. No API key.
- Tools: `list_plans`, `list_products`, `list_free_tools`, `search_blog` (arguments `q`, `limit`), `get_company_facts`, `get_signup_link`.
- Each tool returns readable text plus `structuredContent`.
- Server card: https://www.upgrow.com/.well-known/mcp/server-card.json

## A2A agent

- Agent card: https://www.upgrow.com/.well-known/agent-card.json
- Endpoint: https://www.upgrow.com/a2a (JSON-RPC). Send a message with `SendMessage` (or `message/send` for v0.3 clients); the reply is a message with a text part and a data part.
- Ask about plans and pricing, the one-time shop, free tools, blog articles, or how to get started.

## REST API

Base: https://www.upgrow.com/api/public/v1 (OpenAPI: https://www.upgrow.com/openapi.json)

| Method and path | Returns |
|---|---|
| GET /plans | Basic, Pro and Turbo with first-month price, what each includes and the sign-up link |
| GET /products | One-time shop products with tiers, starting prices and product page links |
| GET /free-tools | Free Instagram tools with a one-line description and link |
| GET /blog/search?q=&limit= | Blog posts matching `q` (2 to 100 characters), up to `limit` results (1 to 10) |
| GET /health | `{"status":"ok"}` |

Example:

```
curl 'https://www.upgrow.com/api/public/v1/blog/search?q=instagram%20reels&limit=3'
```

Errors come back as JSON with an `error` field; a bad `q` or `limit` is a 400. Responses allow any origin (CORS) and are cacheable except `/health`.

## Good practice

- Cache responses for a few minutes; plans and products change rarely.
- Plan prices are first-month prices; shop prices are one-time. Quote them as the API returns them.
- Send users to https://www.upgrow.com/setup to start. Never ask for an Instagram password.
