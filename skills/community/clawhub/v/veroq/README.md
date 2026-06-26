# veroq

**Verified AI. One function call.** Stop shipping hallucinations.

Shield any LLM output — every claim extracted, fact-checked against live evidence, corrected if wrong. Private knowledge base, 5-agent verified swarm, 1,061+ tickers, 260 sources, self-hosted Docker option.

## Install

```
openclaw install veroq
```

## Hero Commands

**`/ask`** — Ask any question. Get a verified, sourced answer with trade signals, reasoning, and follow-ups.

```
/ask What's happening with NVDA?
/ask How is the market doing today?
/ask Compare AAPL and MSFT
```

**`/verify`** — Fact-check any claim. Returns verdict + evidence chain + confidence score.

```
/verify NVIDIA revenue grew 200% last quarter
/verify Bitcoin hit an all-time high in March 2026
```

## All Commands (32)

**Shield & Verify:** `/ask`, `/verify`

**Intelligence:** `/news`, `/brief`, `/search`, `/trending`, `/forecast`, `/entities`, `/trending-entities`, `/events`, `/historical`, `/similar`, `/clusters`, `/data`, `/timeline`, `/web-search`, `/crawl`

**Trading:** `/price`, `/ticker`, `/ticker-score`, `/technicals`, `/candles`, `/screener`, `/backtest`, `/correlation`, `/alerts`, `/market-movers`, `/sectors`, `/portfolio`, `/events-calendar`, `/ipo`

**Reports:** `/report` (quick/full/deep AI analysis)

**Social:** `/social`, `/social-trending`

**Alternative Assets:** `/crypto`, `/defi`, `/economy`

## Beyond Commands

- **Verified Swarm** — 5-agent pipeline with auto-verification at every step
- **Agent Memory** — persistent per-agent knowledge that gets smarter over time
- **Private Knowledge Base** — upload your docs, Shield verifies against them first
- **Self-hosted Shield** — `docker run veroq/shield` — your VPC, your LLM, your data
- **62 MCP tools** — [veroq-mcp](https://www.npmjs.com/package/veroq-mcp)
- **8 SDKs** — Python, TypeScript, LangChain, CrewAI, Vercel AI, n8n, Haystack, CLI

## Links

- [VeroQ](https://veroq.ai)
- [Shield](https://github.com/veroq-ai/shield)
- [Self-Hosted](https://github.com/veroq-ai/veroq-self-hosted)
- [API Reference](https://veroq.ai/api-reference)
- [GitHub](https://github.com/veroq-ai)
