---
name: yundian-woo-importer
description: Import products from Shopify, Wix, WordPress, and Amazon directly into WooCommerce via natural language.
version: 1.0.0
metadata: { "openclaw": { "requires": { "env": ["YUNDIAN_WOO_IMPORTER_API_KEY"], "bins": ["node", "npm", "npx"] }, "primaryEnv": "YUNDIAN_WOO_IMPORTER_API_KEY", "emoji": "🛍️", "homepage": "https://ydplus.net", "install": "npm install" } }
---

# Yundian+ WooCommerce Importer Skill

This skill enables your OpenClaw agent to seamlessly import products from various e-commerce platforms (Shopify, Wix, WordPress, Amazon) directly into a WooCommerce store using the Yundian+ API and MCP Server.

## Setup

Since this skill relies on an underlying MCP server, you need to configure your OpenClaw settings to point to it.

Add the following to your OpenClaw MCP configuration (`~/.openclaw/config.json`):

```json
{
  "mcpServers": {
    "yundian-woo-importer": {
      "command": "npx",
      "args": ["-y", "tsx", "{baseDir}/mcp-server.ts"],
      "env": {
        "YUNDIAN_WOO_IMPORTER_API_KEY": "${YUNDIAN_WOO_IMPORTER_API_KEY}",
        "YUNDIAN_WOO_IMPORTER_API_URL": "https://ydplus.net"
      }
    }
  }
}
```


## Available Tools

The bundled MCP server exposes the following tools to the agent:

### 1. `import_products`
Queue products for import from a source platform to WooCommerce.
- **Parameters**:
  - `platform` (string, required): The source platform. Enum: `shopify`, `wix`, `wordpress`, `amazon`.
  - `shopifyBaseUrl` (string): Required if platform is `shopify`. (e.g., `https://example.myshopify.com`)
  - `wixUrl` (string): Required if platform is `wix`.
  - `productLinks` (array of strings): List of product URLs or handles to import.
  - `mode` (string): Set to `all` to discover and import all products (Supported for Shopify only).

### 2. `check_import_status`
Check the status and results of an ongoing or completed import job.
- **Parameters**:
  - `requestId` (string, required): The unique request ID returned when `import_products` was successfully called.

## Agent Instructions

When the user asks you to import products:
1. **Identify Requirements**: Determine the source platform (Shopify, Wix, WordPress, or Amazon) and the target URLs from the user's prompt.
2. **Execute Import**: Call the `import_products` tool with the appropriate parameters. Ensure you provide the necessary base URL or specific product links.
3. **Report Status**: Once the import is successfully queued, provide the user with the `requestId`.
4. **Follow-up**: If the user asks for an update on the import, or if you want to verify completion, use the `check_import_status` tool with the `requestId` to fetch the latest progress, including how many products were successfully imported or failed.

## Error Handling
- If you receive an "Unauthorized" error, inform the user that their `YUNDIAN_WOO_IMPORTER_API_KEY` might be invalid or expired.
- If credits are insufficient, prompt the user to recharge their account on the Yundian+ dashboard.
