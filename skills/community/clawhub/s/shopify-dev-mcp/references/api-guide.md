# Shopify Development MCP API Guide

This document provides the detailed reference material for the `shopify-dev-mcp` skill. It includes the list of supported APIs, GraphQL schema overview, Liquid validation options, and MCP server configuration.

## Supported APIs & Technologies

| Technology | Description |
|------------|-------------|
| Admin GraphQL | Full‑featured GraphQL API for managing store data (products, orders, customers, etc.). |
| Storefront GraphQL | Public GraphQL API for building custom storefronts and fetching catalog data. |
| Liquid | Theme templating language used in Shopify themes. |
| Polaris | React component library for building Shopify admin UI extensions. |
| Functions | Serverless functions that run on Shopify's backend. |
| Webhooks | Event‑driven HTTP callbacks for store events. |

## MCP Server Configuration

```json
{
  "mcpServers": {
    "shopify-dev": {
      "command": "node",
      "args": ["/absolute/path/to/node_modules/@shopify/dev-mcp/dist/index.js"],
      "env": {
        "LIQUID_VALIDATION_MODE": "full",
        "SHOPIFY_API_KEY": "<your‑api‑key>",
        "SHOPIFY_API_SECRET": "<your‑api‑secret>",
        "SHOPIFY_STORE_URL": "https://your-store.myshopify.com"
      }
    }
  }
}
```

- Use **absolute paths** for the `args` entry to avoid relative resolution failures.
- Set `LIQUID_VALIDATION_MODE` to `full` for full theme checks or `partial` for isolated snippets.
- Store sensitive credentials in environment variables, not in the JSON file.

## GraphQL Schema Introspection

The `introspect_graphql_schema` tool returns a JSON description of the current schema. Key sections:

- **Types** – Objects, interfaces, enums, and unions available.
- **Queries** – Root query fields (e.g., `products`, `orders`).
- **Mutations** – Root mutation fields (e.g., `productCreate`, `orderCancel`).
- **Directives** – GraphQL directives supported by Shopify.

Example response snippet:

```json
{
  "types": [{"name":"Product","fields":[{"name":"id","type":"ID!"},{"name":"title","type":"String"}]}],
  "queries": [{"name":"products","args":[{"name":"first","type":"Int"}],"type":"ProductConnection"}],
  "mutations": [{"name":"productCreate","args":[{"name":"input","type":"ProductInput!"}],"type":"ProductCreatePayload"}]
}
```

Use this data to generate accurate GraphQL queries and validate them with `validate_graphql_codeblocks`.

## Liquid Validation

`validate_theme` runs the **Theme Check** linter on a given theme directory.

- **Full mode** (`LIQUID_VALIDATION_MODE=full`) scans the entire theme, reporting errors such as undefined objects, syntax errors, and best‑practice warnings.
- **Partial mode** validates only the provided files, useful for quick snippet checks.

Common error categories:

1. **Undefined object** – Accessing a variable that is not guaranteed in the given context.
2. **Syntax error** – Missing `{% endif %}`, unmatched brackets, etc.
3. **Deprecated filter** – Using a filter that has been removed.

## Polaris Component Validation

`validate_component_codeblocks` checks React component code using the Polaris component schema.

- Ensures required props are provided.
- Validates prop types against the Polaris spec.
- Flags usage of deprecated components.

Example validation request:

```json
{
  "codeblocks": [{"content": "<Button primary>Save</Button>"}]
}
```

## Webhook Management

Use the `mcporter` CLI to list, register, or delete webhooks.

```bash
mcporter call shopify-dev webhookList
mcporter call shopify-dev webhookCreate topic:orders/create address:https://example.com/webhook
mcporter call shopify-dev webhookDelete id:1234567890
```

## Example Use Cases

- **Create a product** – Initialize `admin` tech, introspect schema, validate GraphQL mutation, then execute via the Shopify API.
- **Validate a theme snippet** – Initialize `liquid` tech, run `validate_theme` in partial mode on the snippet file.
- **Build a POS UI extension** – Initialize `polaris` tech, validate component code, then generate scaffolding using `shopify-dev.tool scaffolding`.
- **Explore Storefront schema** – Initialize `storefront-graphql`, introspect, and query available fields for custom storefront development.

## Helpful Commands Summary

| Command | Purpose |
|---------|---------|
| `learn_shopify_api tech:<technology>` | Initialize MCP session for a technology and get `conversationId`. |
| `search_docs_chunks query:<text> conversationId:<id>` | Semantic search of Shopify docs. |
| `fetch_full_docs path:<url> conversationId:<id>` | Retrieve full documentation page. |
| `introspect_graphql_schema conversationId:<id>` | Get live GraphQL schema JSON. |
| `validate_graphql_codeblocks conversationId:<id> codeblocks:<array>` | Validate GraphQL against schema. |
| `validate_theme conversationId:<id> path:<dir> files:<array>` | Run Theme Check on theme files. |
| `validate_component_codeblocks conversationId:<id> codeblocks:<array>` | Validate Polaris component code. |
| `mcporter call shopify-dev <subcommand>` | Direct MCP CLI operations (webhooks, scaffolding, etc.). |

---

*Keep this reference file up‑to‑date as Shopify APIs evolve. The skill relies on accurate schema and validation information to avoid hallucinations.*
