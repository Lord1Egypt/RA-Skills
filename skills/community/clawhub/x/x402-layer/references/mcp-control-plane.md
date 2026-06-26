# Singularity MCP Control Plane

Use this reference when the user wants optional dashboard-level access through Singularity MCP instead of only local scripts.

## What MCP Is For

Singularity MCP is the owner-scoped control plane for:

- listing dashboard-owned endpoints and products
- listing and managing dashboard-owned fundraiser campaigns
- reading endpoint details and stats
- updating endpoints and products
- setting or removing webhooks
- requesting endpoint creation and endpoint top-up payment challenges

This is the right path when the user says things like:

- "use my dashboard access"
- "manage everything from the platform"
- "list all my endpoints"
- "update this endpoint without using the raw API key path"

## What Stays Script-First

Keep the local x402-layer scripts for:

- direct pay-per-request execution
- local wallet signing and `X-Payment` generation
- Coinbase AWAL flows
- support auth / support thread / XMTP messaging
- wallet-first ERC-8004 or Solana-8004 registration and management

MCP complements the skill. It does not replace the signing-heavy or wallet-first parts.

## Endpoint

Production MCP server:

```text
https://mcp.x402layer.cc/mcp
```

## Authentication

PAT access is optional.

If the user provides a dashboard MCP personal access token, it should look like:

```text
sgl_pat_...
```

Recommended convenience variable:

```bash
export SINGULARITY_PAT="sgl_pat_..."
```

Important:

- do not treat `SINGULARITY_PAT` as globally required for skill installation
- MCP management tools accept PATs as `accessToken` input
- some tools also accept legacy endpoint API keys for endpoint-scoped fallback access
- the direct worker management routes can also use an owner-linked `X-API-Key` outside MCP, including fundraiser campaign routes

## Minimal PAT Scopes

- `mcp:read`:
  list endpoints/products and read endpoint details/stats
- `mcp:endpoints:write`:
  update endpoints, create endpoints, top up endpoints, manage webhooks
- `mcp:campaigns:write`:
  create and update fundraiser campaigns
- `mcp:products:write`:
  update products
- `mcp:*`:
  full MCP access

Choose the narrowest scope needed.

## Recommended Tool Mapping

Use MCP first for these skill intents:

- inventory:
  `list_my_endpoints`, `list_my_campaigns`, `list_my_products`
- fundraiser campaign changes:
  `create_campaign`, `update_campaign`
- endpoint inspection:
  `get_endpoint_details`, `get_endpoint_stats`
- endpoint changes (including API schema):
  `update_endpoint`, `set_webhook`, `remove_webhook`, `delete_endpoint`
- product changes:
  `update_product`
- payment-backed endpoint provisioning:
  `request_endpoint_creation_payment`, `create_endpoint_with_payment`
- payment-backed endpoint top-ups:
  `request_endpoint_topup_payment`, `topup_endpoint_with_payment`

Use direct worker API-key scripts first for:

- `manage_campaign.py`
- `manage_endpoint.py`
- `manage_webhook.py`

Use direct scripts first for:

- `pay_base.py`
- `pay_solana.py`
- `consume_credits.py`
- `consume_product.py`
- `support_auth.py`
- `support_threads.py`
- `xmtp_support.mjs`
- `register_agent.py`
- `update_agent.py`

## Generic MCP Client Example

If the host supports MCP configuration, add the server:

```json
{
  "mcpServers": {
    "singularity": {
      "url": "https://mcp.x402layer.cc/mcp",
      "transport": "http"
    }
  }
}
```

Then provide the PAT to MCP management tools as `accessToken` when owner-scoped access is needed.

## Decision Rule

Use this simple rule inside the skill:

- if the task is marketplace discovery or public consumption, the normal scripts are enough
- if the task is owner-scoped dashboard inventory or configuration, prefer Singularity MCP when a PAT is available
- if the task already has an owner-linked `X-API-Key`, direct worker management routes can be simpler than MCP
- if the task requires local wallet signing or chain-specific execution, stay with the scripts
