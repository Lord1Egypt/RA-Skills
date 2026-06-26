# SEC_Market MCP Capabilities

Publish-ready skill describing SEC_Market's full MCP endpoint capabilities for agent discovery directories (including ClawHub).

---

# SEC_Market API

**Base URL:** https://market-royal-city.vercel.app/api/

MCP endpoint: `POST https://market-royal-city.vercel.app/api/mcp`  
MCP discovery: `GET https://market-royal-city.vercel.app/.well-known/mcp.json`  
Agent entrypoint: `GET https://market-royal-city.vercel.app/.well-known/agent.json`  
Catalog: `GET https://market-royal-city.vercel.app/.well-known/agent-products.json`

---

## What This Skill Covers

This skill advertises the full SEC_Market MCP surface area for AI agents:

- Commerce tools (product listing, purchase flow, donation, verification, delivery)
- Ad capabilities (inventory discovery, campaign creation, campaign performance, campaign lookup)
- Company US research (filings, filing document lookup, metrics with lineage, company summary, single-call research bundle)

---

## MCP Tools (Current)

- `list_products`
- `purchase`
- `donate`
- `verify_payment`
- `get_ad_discount`
- `deliver`
- `promote_products`
- `discover_ad_inventory`
- `create_ad_campaign`
- `check_ad_performance`
- `lookup_ad_campaign`
- `list_filings`
- `get_filing`
- `get_metrics`
- `get_company_summary`
- `research_company`

---

## Agent Notes

- Payments and deliveries are supported for both human redirect flows and machine-driven usage.
- Company US data is SEC EDGAR-backed with source lineage fields for auditability.
- Related paid HTTP research bundle route: `GET /api/company/us/research-bundle`.

---

## Example MCP Calls

### List tools/products

```bash
curl -X POST https://market-royal-city.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool":"list_products","params":{}}'
```

### Get metrics with lineage

```bash
curl -X POST https://market-royal-city.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool":"get_metrics","params":{"ticker":"AAPL","period":"latest"}}'
```

### Single-call research bundle

```bash
curl -X POST https://market-royal-city.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool":"research_company","params":{"ticker":"AAPL","filings_limit":15}}'
```
