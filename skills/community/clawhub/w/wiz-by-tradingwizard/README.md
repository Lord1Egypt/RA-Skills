# Wiz by TradingWizard for OpenClaw

Add current market intelligence and TradingWizard bot context to OpenClaw.

## Install from ClawHub

```bash
openclaw skills install @HugoRS00/wiz-by-tradingwizard
```

Then connect the public MCP server:

```bash
openclaw mcp set tradingwizard '{"url":"https://www.tradingwizard.ai/api/mcp","transport":"streamable-http"}'
openclaw mcp probe tradingwizard --json
openclaw mcp reload
```

Public tools work without a TradingWizard account. See `SETUP.md` for optional OAuth and private account tools.

## What OpenClaw gets

- Market summary with Fear & Greed, VIX, US 10-year yield, regime, and freshness
- Current prices and the `/markets` dataset
- Public Market Track events with significance and short explanations
- Market movers and bot consensus
- Public global bots and ranked opportunities
- Bot Fund performance
- Optional private tools that follow the connected Free, Pro, or Ultimate plan

Wiz supports market research and paper trading only. It does not execute real-money trades.

- Website: https://www.tradingwizard.ai/mcp?client=openclaw#connect
- Documentation: https://www.tradingwizard.ai/docs/mcp
- Privacy: https://www.tradingwizard.ai/policy
- Support: https://www.tradingwizard.ai/support
