# Shopify MCP

Manage your Shopify store directly from Claude / OpenClaw — orders, customers, products, and inventory — using natural language.

Powered by [shopify-mcp](https://github.com/dzunglaviet/shopify-mcp), a Python MCP server connecting to the Shopify Admin REST API. Supports multiple stores, static access tokens, and OAuth client credentials.

## Tools

**Orders** — `shopify_list_orders`, `shopify_get_order`, `shopify_update_order`, `shopify_cancel_order`, `shopify_fulfill_order`

**Customers** — `shopify_list_customers`, `shopify_get_customer`, `shopify_update_customer`

**Products & Inventory** — `shopify_list_products`, `shopify_get_product`, `shopify_update_inventory`

## Setup

### 1. Clone and install

```bash
git clone https://github.com/dzunglaviet/shopify-mcp
cd shopify-mcp
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### 2. Create a Shopify Custom App

1. Shopify Admin → Settings → Apps → **Develop apps** → Create an app
2. **Configuration → Admin API scopes** — enable:
   `read_orders`, `write_orders`, `read_customers`, `write_customers`, `read_products`, `read_inventory`, `write_inventory`, `read_fulfillments`, `write_fulfillments`
3. **API credentials → Install app** → copy the `shpat_...` token

### 3. Configure `.env`

```bash
cp .env.example .env
```

Fill in your credentials:

```bash
SHOPIFY_SHOP_DOMAIN=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_API_VERSION=2026-04
```

### 4. Add to Claude Code / OpenClaw

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "shopify-mcp": {
      "command": "/absolute/path/to/shopify-mcp/venv/bin/python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/shopify-mcp"
    }
  }
}
```

Restart Claude Code / OpenClaw after saving.

## Example prompts

```
List the last 10 open orders
Show me order #1042
Find customer with email: john@example.com
Cancel order 6543210987654 — customer changed their mind
Fulfill order 6543210987654 with GHN tracking number ABC123456789
Set inventory for inventory_item_id 11223344 to 50 units
```

## Multiple stores

```bash
SHOPIFY_STORES=[{"shop_domain":"store-a.myshopify.com","access_token":"shpat_aaa"},{"shop_domain":"store-b.myshopify.com","access_token":"shpat_bbb"}]
```

Pass `shop` to any tool to target a specific store. Omitting `shop` defaults to the first configured store.
