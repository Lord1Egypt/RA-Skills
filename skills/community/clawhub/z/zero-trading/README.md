# ZERO Trading Agent

## install

```bash
clawhub install zero-trading
```

That's it. MCP server auto-configured. 42 tools available. No config files. No API keys. No wallet needed for paper trading.

## what happens on install

1. OpenClaw reads `.mcp.json` — connects to `https://api.getzero.dev/mcp` via streamable-http
2. Gateway registers all ZERO tools (starts with 2, unlocks up to 42 as you use them)
3. SKILL.md injected into agent system prompt — agent knows how to trade
4. Sub-skills loaded for onboarding, strategy selection, risk management, etc.

## first interaction

Tell your agent: **"set me up on zero"**

The onboarding skill walks through:
1. verify engine connection
2. show the market (50 coins being watched)
3. run a live evaluation demo (9 layers on BTC)
4. deploy a paper momentum session
5. hand off with drive mode selection

## what your agent gets

**42 tools** (progressively unlocked):
- evaluate any coin through 9 intelligence layers
- heat maps, approaching signals, regime analysis
- session lifecycle (start, monitor, end, result cards)
- 9 strategies with different risk profiles
- progression system (score, streak, achievements, arena)
- diagnostic tools (circuit breaker, immune system, execution quality)

**8 sub-skills:**
- onboarding, strategy selection, market reading
- session management, risk management, operator communication
- competitive features, pattern recognition

## alternative install methods

### from source
```bash
openclaw plugins install ./scanner/skills/zero-trading
```

### manual
Drop the `zero-trading/` directory into `~/.openclaw/skills/` and restart the gateway.

## requirements

- OpenClaw agent with MCP support
- internet connection (engine runs at api.getzero.dev)
- no API key needed for paper trading
- no wallet needed for paper trading

## links

- engine: https://api.getzero.dev
- join page: https://api.getzero.dev/join
- skill: https://clawhub.ai/squaeragent/zero-trading
- source: https://github.com/squaeragent/getzero-os
