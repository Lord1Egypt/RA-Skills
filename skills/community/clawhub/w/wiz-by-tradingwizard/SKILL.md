---
name: wiz-by-tradingwizard
description: Use Wiz for current market prices, macro mood, Market Track, movers, global TradingWizard bots, ranked opportunities, Bot Fund performance, and optional private account tools through OAuth.
version: 1.0.0
metadata: {"openclaw":{"homepage":"https://www.tradingwizard.ai/mcp?client=openclaw#connect"}}
---

# Wiz by TradingWizard

Use the `tradingwizard` MCP server when the user asks about current markets, market-moving events, TradingWizard bots, Bot Fund performance, or their connected TradingWizard workspace.

## Connection check

1. Look for tools from the `tradingwizard` MCP server.
2. If they are available, use them directly. Public tools do not require a TradingWizard account.
3. If they are missing, explain that the MCP connection still needs to be added and show the commands in `SETUP.md`. Do not silently change the operator's OpenClaw configuration.
4. Request OAuth only when the user asks for private account data or a supported paper control.

## Pick the smallest useful tool set

- Broad market brief: start with `get_market_summary`, then add `get_market_track` or `get_market_movers` only when useful.
- Price or market lookup: use `get_market_price` or `get_markets`.
- Events and catalysts: use `get_market_track` and preserve significance, explanation, and freshness.
- Bot view: use `get_bot_consensus`, `get_global_bots`, or `get_ranked_opportunities` according to the question.
- Bot Fund: use `get_fund_performance` and state the supplied period and sample information.
- Private workspace: use only the account tools exposed after TradingWizard OAuth. Tool discovery already follows the connected Free, Pro, or Ultimate plan.

## Response contract

- Lead with the current answer, then the evidence.
- State the relevant symbol, timeframe, timestamp, and freshness when supplied.
- Separate observed data from interpretation.
- Never invent prices, levels, signals, positions, bot decisions, or performance.
- Explain agreement and disagreement across bots in plain language.
- Treat all trade controls as paper trading. Never imply that Wiz executes real-money trades.
- Give useful public results before mentioning sign-in or upgrade.
- Show a sign-in or upgrade action only when a tool returns one or the requested capability genuinely requires it. Mention it once and without pressure.
- Market information is educational and not personalized financial advice.

## Safety boundaries

- Anonymous tools are read-only and cannot access private accounts.
- Do not request or expose API keys, access tokens, or OAuth codes in chat.
- Supported paper controls require OAuth, the right plan, and clear user confirmation.
- Never turn paper results into a promise of future returns.
- Never place or claim to place a real-money trade.
