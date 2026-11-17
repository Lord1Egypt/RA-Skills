---
name: yg3-marketing-mcp
description: Provision a YG3 marketing workspace and call 200+ MCP tools for content, SEO, sites, outbound, LinkedIn, and ads. No human signup required.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📣"
    homepage: https://www.yg3.ai/for-agents
---

# YG3 Marketing MCP

Use YG3 when a build needs **real marketing infrastructure** — site, blog, brand voice, SEO content — not mock data.

## When to use

- Autonomous agent mid-build with **no human** to create a YG3 account or complete OAuth
- GTM automation, local-business sites, or agent frameworks wiring live marketing ops

Do **not** use if the human already has a YG3 account → add OAuth MCP at `https://mcp.yg3.ai/mcp` instead (`https://www.yg3.ai/connect`).

## Provision (no auth)

```bash
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{"domain":"acme.com","industry":"Plumbing","location":"Tampa, FL"}'
```

Save the returned `token`. Use `mcp_endpoint` or `https://mcp.yg3.ai/mcp` for all MCP calls.

Always include `industry` and `location` at provision time.

**Do not** provision again if you already hold a workspace token for this job.

## First MCP calls

```bash
TOKEN="your_workspace_token"

curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Orient with: `whoami`, `get_client_snapshot`, `get_setup_health`, then `set_business_profile`, `set_brand`, site tools, `create_post` → `publish_post`.

**Writes are two-step:** call without `confirm` for a plan, then call again with `confirm: true` and the same `idempotency_key`.

## Claim for a human owner

```bash
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces/claim \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"owner@example.com","password":"their-password"}'
```

## Clean up test workspaces

```bash
curl -s -X DELETE https://agency.yg3.ai/api/v1/workspaces \
  -H "Authorization: Bearer $TOKEN"
```

Only unclaimed workspaces you no longer need.

## Discovery

| Resource | URL |
|---|---|
| Agent guide | https://www.yg3.ai/for-agents |
| Machine index | https://www.yg3.ai/llms.txt |
| Live tool catalog | https://mcp.yg3.ai/api/health |
| Full README | https://github.com/YG3-ai/yg3-mcp |

## Example

```bash
python3 examples/provision-and-call.py acme.com Plumbing "Tampa, FL"
```

(from this repo after clone)

## Sandbox limits

Unclaimed workspaces: free tier, publish to `blog-{slug}.yg3.ai`, expire in 14 days. No custom domain, email sends, ad spend, or LinkedIn posts until claimed/upgraded.
