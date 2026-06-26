---
name: shopify-dev-mcp
description: >
  Use when user wants to work with Shopify Admin API, Storefront API, validate Liquid code, explore GraphQL schemas, build Shopify apps, or inspect Shopify documentation and MCP tools.
version: "1.0.0"
---


# Shopify Development MCP (shopify-dev-mcp)

Provides a workflow to interact with Shopify's development ecosystem via the `shopify-dev` MCP server. It enables searching documentation, introspecting GraphQL schemas, validating Liquid/theme code, and building Shopify extensions while avoiding hallucinations.

## Trigger Scenarios
- "How do I create a product using the Admin API?"
- "Show me the fields on the Order GraphQL type."
- "Validate this Liquid snippet for a theme."
- "I need to explore the Storefront API schema."
- "Help me build a Shopify app that uses Polaris components."
- "Debug a GraphQL error from Shopify."

## Core Workflow
1. **Initialize** – Call `learn_shopify_api` for the required technology (admin, storefront-graphql, liquid, polaris) and capture the returned `conversationId`.
2. **Search Documentation** – Use `search_docs_chunks` for semantic search or `fetch_full_docs` for full pages.
3. **Introspect Schema** – Run `introspect_graphql_schema` with the `conversationId` to get up‑to‑date types and fields.
4. **Validate Code** – Depending on the content:
   - GraphQL: `validate_graphql_codeblocks`
   - Polaris UI: `validate_component_codeblocks`
   - Liquid/theme: `validate_theme`
5. **Present Result** – Return the validated code or documentation excerpt to the user.

## Best Practices
- Always start with **step 1** and reuse the same `conversationId` for subsequent calls.
- Wrap MCP CLI commands in **single quotes** when invoking via shell (`'shopify-dev.tool(...)'`).
- Prefer a local installation of `@shopify/dev-mcp` over `npx` for reliability.
- Use absolute paths in the MCP configuration to avoid path resolution issues.
- Validate any generated code before showing it to the user.

## Usage Examples
```bash
# 1. Initialize for Admin GraphQL
learn_shopify_api tech:admin
# ⇒ returns conversationId=abc123

# 2. Search docs for "product creation"
search_docs_chunks query:"product creation" conversationId:abc123

# 3. Introspect the schema
introspect_graphql_schema conversationId:abc123

# 4. Validate a GraphQL mutation
validate_graphql_codeblocks conversationId:abc123 codeblocks:[{content:"mutation { productCreate(input:{title:\"New\"}) { product { id } userErrors { field message } } }"}]

# 5. Validate a Liquid snippet
validate_theme conversationId:abc123 path:"/tmp/theme" files:["snippets/header.liquid"]
```

## References
- See `references/api-guide.md` for full API details, GraphQL schema listings, Liquid validation options, and MCP server setup.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
