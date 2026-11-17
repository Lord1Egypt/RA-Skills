# Connect Wiz to OpenClaw

The skill teaches OpenClaw how to use Wiz. The MCP connection supplies the live tools.

## Public market tools

Run once:

```bash
openclaw mcp set tradingwizard '{"url":"https://www.tradingwizard.ai/api/mcp","transport":"streamable-http"}'
openclaw mcp probe tradingwizard --json
openclaw mcp reload
```

The probe should list ten public, read-only tools. No TradingWizard account or API key is required.

## Optional private account tools

Only connect an account when private TradingWizard features are needed:

```bash
openclaw mcp configure tradingwizard --auth oauth --oauth-scope 'tw:mcp:read tw:mcp:paper.write'
openclaw mcp login tradingwizard
```

OpenClaw stores the resulting OAuth credentials. Available tools follow the connected Free, Pro, or Ultimate plan. Access tokens never appear in tool results.

## Verify in chat

Ask:

```text
Use Wiz to brief me on Fear & Greed, VIX, the US 10Y, market movers, global bots, and Bot Fund performance.
```

Documentation: https://www.tradingwizard.ai/docs/mcp
