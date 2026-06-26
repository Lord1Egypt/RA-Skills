---
name: twelvedata
description: Official Twelve Data integration for OpenClaw and ClawHub. Provides real-time and historical financial market data for stocks, forex, crypto, ETFs, indices, and more. Includes quotes, time series, 100+ technical indicators, fundamentals, symbol search, and portfolio/research workflows. Strongly prefers the official Twelve Data MCP Server for secure and efficient access.
version: 1.0.0
license: MIT
metadata:
  author: Twelve Data (official)
  homepage: https://twelvedata.com
  repository: https://github.com/twelvedata/twelvedata-clawhub
  mcp-server: twelvedata
  requires:
    env:
      - TWELVE_DATA_API_KEY   # Only required if MCP server is not used
    bins: []
  tags:
    - finance
    - stocks
    - forex
    - crypto
    - market-data
    - real-time
    - technical-analysis
    - fundamentals
    - official
    - mcp
---

# Twelve Data Official Skill

## Overview
This is the **official skill** from Twelve Data for OpenClaw / ClawHub. It equips the AI agent with accurate, up-to-date financial market data and intelligent workflows for research, analysis, trading signals, and portfolio monitoring.

## When to Activate This Skill
- Requests for current prices, quotes, or charts (e.g., "What's the current price of AAPL?")
- Historical data and time series analysis
- Technical indicators (RSI, MACD, SMA, Bollinger Bands, etc.)
- Fundamentals, earnings, dividends, financial statements, or company profiles
- Symbol search or market scanning
- Portfolio tracking, alerts, or research reports
- Any natural-language question involving stocks, forex, crypto, ETFs, or indices

## Preferred Method: Official Twelve Data MCP Server (Recommended)
The MCP server provides the most secure, streaming, and token-efficient way to access the full Twelve Data API.

**Setup Instructions:**
1. Get your free or paid API key at [https://twelvedata.com/register](https://twelvedata.com/register)
2. Run the MCP server using UV (easiest):
   ```bash
   uvx mcp-server-twelve-data --apikey YOUR_TWELVE_DATA_API_KEY
   ```
   Or install via pip:
   ```bash
   pip install mcp-server-twelve-data
   mcp-server-twelve-data --apikey YOUR_TWELVE_DATA_API_KEY
   ```
3. Configure your AI client (Claude Desktop, Cursor, OpenClaw, etc.) to use the `twelvedata` MCP server.

The agent will automatically detect and route requests through the running MCP server when available.

## Fallback: Direct API or Python SDK
If MCP is unavailable, the agent can use:
- Official Python SDK: `pip install twelvedata`
- Or direct REST/WebSocket calls to `api.twelvedata.com`

## Detailed Reference Documentation
For complete, LLM-optimized endpoint details, parameters, response formats, and examples, refer to the files in the `references/` folder:
 
- `references/llms-index.md` — Main index of all documentation
- `references/market-data.md` — Time series, quote, price, market movers
- `references/technical-indicators.md` — 100+ technical indicators
- `references/fundamentals.md` — Financial statements, earnings, dividends
- `references/websocket/` — Real-time WebSocket documentation
- `references/ai/` — MCP and AI-specific guidance
 
> **Best Practice:** When the user request requires specific endpoints or parameters, the agent should first read the relevant file from the `references/` folder before making API calls.

## Agent Instructions & Best Practices
- **Always validate symbols** first using symbol search when the user provides a company name.
- **Prefer batch requests** and appropriate `outputsize` to minimize API usage.
- For time series: Default to `interval=1day` unless the user specifies intraday.
- Request **pre-computed technical indicators** instead of calculating them manually.
- Use dedicated fundamentals endpoints for income statements, balance sheets, cash flow, and earnings.
- For real-time needs: Leverage WebSocket streaming via the MCP server.
- **Output style**: Present data in clean Markdown tables + a clear plain-English summary. Always cite "Twelve Data" as the source.
- Respect rate limits — suggest upgrading the plan for high-volume usage.
- Handle missing data gracefully and note timezones (default: America/New_York).

## Security Guidelines
- Never expose or hardcode the API key in prompts or generated code.
- Prefer the MCP server over raw HTTP calls whenever possible.
- Cache repeated queries when appropriate.

## Upgrade Prompt
"For higher rate limits, longer historical data, or advanced features, upgrade your Twelve Data plan here: https://twelvedata.com/pricing"

## Resources
- Official Website: https://twelvedata.com
- API Documentation: https://twelvedata.com/docs
- MCP Server Repository: https://github.com/twelvedata/mcp
- Python SDK: https://github.com/twelvedata/twelvedata-python

## LLM-Friendly Documentation (Highly Recommended)

Twelve Data provides clean, agent-optimized documentation specifically written for LLMs:

- Main LLM Index: https://twelvedata.com/docs/llms.txt
- Market Data: https://twelvedata.com/docs/llms/market-data.md
- Technical Indicators: https://twelvedata.com/docs/llms/technical-indicators.md (and similar for other sections)

When detailed endpoint parameters, response formats, or examples are needed, the agent should read the relevant LLM documentation above before making calls.

This skill is maintained by the Twelve Data team. Feedback and issues are welcome in the repository.