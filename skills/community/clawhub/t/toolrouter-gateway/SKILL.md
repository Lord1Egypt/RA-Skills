---
name: toolrouter-gateway
description: "Unified access to 150+ tools via ToolRouter API. Dynamically exposes research, security scanning, video production, web extraction, and more as native OpenClaw tools. Caching, usage tracking, and MCP transport included."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$49/mo"
tags: ["toolrouter", "gateway", "proxy", "mcp", "automation"]
tools:
  - name: toolrouter_discovery
    description: "Search ToolRouter's catalog of 150+ tools. Returns matching tools with descriptions and schemas."
    input_schema:
      type: object
      properties:
        query:
          type: string
        category:
          type: string
        limit:
          type: integer
          default: 20
      required: []
    permission: read_only
  - name: toolrouter_status
    description: "Get gateway status: API connectivity, cache age, usage stats"
    input_schema:
      type: object
      properties: {}
      required: []
    permission: read_only
---

# ToolRouter Gateway

One skill to rule them all. ToolRouter provides 150+ tools (competitor research, vulnerability scanning, video generation, web scraping, etc.). This skill makes them feel like native OpenClaw tools.

## How It Works

1. **Discovery** — Fetches ToolRouter's tool catalog (cached 24h)
2. **Dynamic Tools** — Each ToolRouter tool becomes `toolrouter_<slug>` in your registry
3. **Proxy** — All calls go to `https://api.toolrouter.com/mcp` with your API key
4. **Caching** — Responses cached by input hash (TTL configurable)
5. **Usage Tracking** — Counts calls per tool, shows in status

## Prerequisites

- ToolRouter API key (get at https://toolrouter.com — auto-provisioned on first use)
- Set environment variable: `TOOLROUTER_API_KEY=your_key`

## Tools

### toolrouter_discovery

Search the catalog:

```json
{
  "query": "competitor",
  "category": "research",
  "limit": 10
}
```

Returns list of available tools with:
- `slug` — use in tool name (`toolrouter_<slug>`)
- `name`, `description`
- `input_schema` — JSONSchema for the tool
- `category`, `pricing` (cost per call)

### toolrouter_status

```json
{}
```

Returns:
```json
{
  "api_connected": true,
  "cache_age_minutes": 12,
  "total_calls": 147,
  "calls_today": 23,
  "enabled_tools": 42,
  "errors_last_24h": 0
}
```

### Dynamic Tools (examples)

Once catalog is fetched, you can call any ToolRouter tool:

```python
# Competitor research
tool("toolrouter-gateway", "toolrouter_competitor_research", {
  "url": "https://example.com",
  "depth": "full"
})

# Vulnerability scan
tool("toolrouter-gateway", "toolrouter_security_scan", {
  "target": "https://myapp.com",
  "checks": ["cve", "misconfig"]
})

# Video generation
tool("toolrouter-gateway", "toolrouter_video_from_brief", {
  "brief": "30s product demo for OpenClaw Memory Stack",
  "style": "modern"
})
```

Tool names are derived from ToolRouter slugs (replace hyphens with underscores, add `toolrouter_` prefix). The `toolrouter_discovery` tool tells you which slugs exist.

## Configuration

Optional `toolrouter-gateway-config.json`:

```json
{
  "api_url": "https://api.toolrouter.com/mcp",
  "cache_ttl_minutes": 1440,
  "usage_log_file": "memory/toolrouter-usage.jsonl",
  "enable_caching": true,
  "timeout_seconds": 60
}
```

## Caching

- Cache key: SHA256 of tool name + input JSON
- Stored in `memory/toolrouter-cache.jsonl`
- Reduces cost and improves speed for repeated calls
- Can be cleared manually if needed

## Usage Tracking

All calls logged to `memory/toolrouter-usage.jsonl`:
```json
{"timestamp":"2026-04-01T17:40:00Z","tool":"competitor_research","input_hash":"abc123","cost":0.005}
```

`toolrouter_status` aggregates these.

## Error Handling

- API down → returns cached response if available, else error
- Rate limits → exponential backoff retry (3 attempts)
- Invalid tool → `discovery` tool will reflect removal from catalog

## MCP Integration

The gateway can also run as an MCP server (experimental):

```bash
# Start MCP server (stdio)
toolrouter-gateway --mcp
```

Other MCP clients can then connect and use all ToolRouter tools as MCP resources.

## Pricing

$49/month. Includes:
- Unlimited tool calls (you pay ToolRouter usage separately; most tools cost fractions of a cent)
- Caching reduces your ToolRouter bill
- Usage analytics
- Priority support

You need your own ToolRouter API key (free tier available).

## FAQ

**Q: Do I pay per ToolRouter call?**  
A: Yes, ToolRouter charges per call (typically $0.001–$0.05). Our caching minimizes costs.

**Q: Can I add my own tools to ToolRouter?**  
A: ToolRouter is a separate service; contact them for custom integrations.

**Q: What if a tool is flaky?**  
A: Check `toolrouter_status` for error rates. Cache helps smooth failures.

**Q: Is there a free trial?**  
A: Not yet. But ToolRouter has a free tier with limited calls.

---

*Inspired by ClawHub's toolrouter skill, extended with caching, usage tracking, and native tool manifests.*
