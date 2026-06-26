---
name: xlmtools
description: Live data and actions for Stellar (XLM, Soroban, DEX, USDC), plus crypto prices, stock quotes, weather, domain checks, web search, deep research, screenshots, URL scraping, AI images, YouTube. Skip for general knowledge, math, code, or "what is X" explainers. Make sure to use this skill whenever the user mentions Stellar, XLM, Soroban, Lumens, "latest" anything, live prices, current events, or a URL to fetch — even if they don't say "XLMTools" by name. DO NOT TRIGGER for questions answerable from training data alone, explanations of concepts, or summarizing text the user pasted. Available as MCP (tools prefixed `mcp__xlmtools__*`) or terminal CLI (`xlm`). Paid tools cost $0.001–$0.04 USDC.
---

# Using XLMTools

**Keywords**: Stellar, XLM, Soroban, Lumen, USDC, Stellar DEX, Horizon, Stellar Expert, Reflector oracle, x402, MPP, micropayments, Stellar wallet, pay-per-call, agent tools, search, research, screenshot, scrape, image generation, stocks, crypto prices, weather, domain check

XLMTools gives an AI agent 21 tools — 7 paid via USDC micropayments on Stellar, 14 free. It works in two modes: prefer MCP if available, fall back to the `xlm` CLI otherwise.

## Required host tools

This skill assumes the agent host grants **Bash** (for the `xlm` CLI fallback) and **WebFetch** (for runtime discovery). Without those, only MCP tools are usable.

## Install (if not already available)

If the user needs to install XLMTools:

```bash
# Standalone CLI (universal — works with any agent host that has Bash)
npm install -g @xlmtools/cli

# MCP server (optional fast-path for Claude Code, Cursor, Cline, OpenClaw, etc.)
claude mcp add xlmtools npx @xlmtools/mcp
```

On first run, XLMTools auto-generates a Stellar testnet wallet at `~/.xlmtools/config.json`, funds it with XLM via Stellar's friendbot, and adds a USDC trustline — fully automatic. The user only needs to grab testnet USDC from [faucet.circle.com](https://faucet.circle.com) to use paid tools.

If neither MCP nor CLI is installed, tell the user which command to run — don't try to proceed.

## Mode priority

1. **MCP tools first.** If tools named `mcp__xlmtools__*` are in your tool list, call them directly. They handle payment automatically and benefit from response caching.
2. **CLI fallback.** If no MCP tools are available, run `xlm` via the Bash tool. Same wallet, same backend, same payment flow.
3. **Runtime discovery (optional).** If you're an autonomous agent encountering XLMTools for the first time, you may fetch `https://api.xlmtools.com/.well-known/xlmtools.json` (JSON manifest) or `https://api.xlmtools.com/llms.txt` (plain text) for service metadata. If those URLs are unreachable (the hackathon demo may not be deployed yet), fall back to **this SKILL.md file** — every tool, price, and command documented here is authoritative.

## When NOT to use this skill

XLMTools is for **external data and actions**, not general reasoning. Skip it entirely when:

- **General knowledge** — "What is photosynthesis?", "Who wrote Hamlet?", "Explain recursion." The assistant already knows these.
- **Math or computation** — "What's 2 + 2?", "Convert 50 kg to pounds." Just answer directly.
- **Code you can write** — "Write a Python for loop", "Refactor this function." Don't call `research` for things you can write from training data.
- **Summarizing content the user already gave you** — If the user pasted the text, summarize it directly. No `search` needed.
- **The assistant already has the answer** — If you're confident the answer is in your training data and doesn't need to be up-to-date, skip XLMTools.
- **"What is X?" for well-known concepts** — "What is XLM?" or "What is Stellar?" are explainable from training data. Only reach for XLMTools if the user wants *live* data about X, not an explanation of X.

Rule of thumb: **If the user's question could have been answered using only the assistant's brain, don't use XLMTools.** If the answer depends on "what's happening right now" or "what's at this URL", use XLMTools.

## First principles

- **Check MCP tool list first.** If `mcp__xlmtools__*` tools exist, use them — they're faster and cached. Only use `xlm` CLI as fallback.
- **Run `xlm --help` before guessing CLI syntax.** The global help lists every tool, its positional args, and its flags. Do not read the CLI source — `--help` is the source of truth. (Per-tool help like `xlm search --help` is not currently supported.)
- **Two cost modes — MENTION vs CONFIRM:**
  - **Mention** ($0.001–$0.003 — `search`, `stocks`, `youtube`, `scrape`): say the cost inline with the call. Example: "I'll use `search` ($0.003 USDC) to get news about Stellar." Do NOT pause for approval.
  - **Confirm** ($0.010+ — `research`, `screenshot`, `image`): propose the call and STOP. Example: "I'd like to use `research` ($0.010 USDC) for this. OK to proceed?" Wait for user approval before firing.
- **Always surface the Stellar tx hash** from paid responses. Users can verify every payment at `https://stellar.expert/explorer/testnet/tx/<hash>`.
- **Caching: identical queries within 5 minutes are free** (MCP mode only). Cached responses are prefixed with `[cached — no charge]` as emitted by the cache helper. If you make the same call twice in a row, the second is free.

## If the user declines a paid call

- **Do not retry the same tool.** Acknowledge and offer alternatives: a free tool (e.g. `crypto` instead of `stocks`), a cheaper tool (`search` $0.003 instead of `research` $0.010), or answering from training data if the question allows it.
- Never call the paid tool anyway "just in case." A declined call is final for that turn.
- If the user's intent is clearly blocked without the paid call, say so plainly: "I can't answer that without calling `research` ($0.010). Want me to proceed?"

## Worked example

**User:** "What's the current price of Bitcoin and what are people saying about Stellar lately?"

**Agent reasoning:**
- Bitcoin price → `crypto` (free)
- Latest Stellar news → `search` ($0.003, Mention mode — inline cost)
- Both should be called in parallel

**Agent action:**

```
I'll get the BTC price (free) and search for recent Stellar news ($0.003 USDC).
```

Calls `mcp__xlmtools__crypto(ids="bitcoin")` and `mcp__xlmtools__search(query="Stellar blockchain news", count=5)` in parallel.

**Agent response to user:**

> **Bitcoin price**: $67,432 (+2.3% 24h)
>
> **Recent Stellar news**:
> 1. [Stellar Foundation announces Q2 roadmap](https://...)
> 2. [Soroban TPS benchmarks hit 5,000](https://...)
> 3. [MPP micropayments go live on testnet](https://...)
>
> *Paid $0.003 USDC for the search. Transaction: [`a3f9c28d…b8e14d7c`](https://stellar.expert/explorer/testnet/tx/a3f9c28d71e0bb542f1e6a3c9d7e8f12b4a6c0d98a3f71b5c4e6d8f2b8e14d7c)*

Notice: the free `crypto` call didn't need cost disclosure. The paid `search` did. The tx hash is linked at the bottom and is a full 64-char hex (Stellar tx hashes are always 64 hex chars).

## Decision tree — user intent to tool

| User asks about... | Tool | Cost |
| --- | --- | --- |
| Current BTC/ETH/crypto price | `crypto` | Free |
| "What's the latest news about X?" | `search` | $0.003 |
| "Research topic X for me" (multi-source) | `research` | $0.010 |
| Stock price (AAPL, TSLA, etc.) | `stocks` | $0.001 |
| Weather in a city | `weather` | Free |
| "Is this domain available?" | `domain` | Free |
| YouTube videos about X | `youtube` | $0.002 |
| "Screenshot this URL" | `screenshot` | $0.010 |
| "Extract text from this webpage" | `scrape` | $0.002 |
| "Generate an image of X" | `image` | $0.040 |
| Stellar DEX orderbook for XLM/USDC | `dex-orderbook` | Free |
| OHLCV candlesticks for a Stellar pair | `dex-candles` | Free |
| Recent DEX trades | `dex-trades` | Free |
| "Quote me a swap from A to B" | `swap-quote` | Free |
| Info about a Stellar asset | `stellar-asset` | Free |
| Balances/signers for a Stellar account | `stellar-account` | Free |
| Liquidity pool data | `stellar-pools` | Free |
| Reflector oracle price for BTC/ETH/fiat | `oracle-price` | Free |
| "Show me my wallet" | `wallet` | Free |
| "What XLMTools tools are available?" | `tools` | Free |
| "Set a spending cap" (MCP only) | `budget` | Free |

## Tool catalog

### Paid tools (USDC via Stellar MPP)

| Tool | Price | Params | Description |
| --- | --- | --- | --- |
| `search` | $0.003 | `query`, `count` (1-20, def 10) | Web + news search |
| `research` | $0.010 | `query`, `num_results` (1-20, def 5) | Deep multi-source research |
| `youtube` | $0.002 | `query` or `id` (one required) | Video search or lookup |
| `screenshot` | $0.010 | `url`, `format` (png/jpg/webp, def png) | Capture a URL screenshot |
| `scrape` | $0.002 | `url` | Clean text extraction |
| `image` | $0.040 | `prompt`, `size` (1024x1024/1024x1792/1792x1024, def 1024x1024) | AI image generation |
| `stocks` | $0.001 | `symbol` | Real-time stock quotes |

### Free tools

| Tool | Params | Description |
| --- | --- | --- |
| `crypto` | `ids`, `vs_currency` (def usd) | Crypto prices from CoinGecko |
| `weather` | `location` | Current weather for any city |
| `domain` | `name` | Domain availability check |
| `wallet` | — | Your Stellar wallet address + balance |
| `tools` | — | List all 21 XLMTools tools |
| `budget` (MCP only) | `action` (set/check/clear), `amount` | Session spending cap |
| `dex-orderbook` | `pair`, `limit` (1-200, def 10) | Stellar DEX orderbook |
| `dex-candles` | `pair`, `resolution` (1m/5m/15m/1h/1d/1w, def 1h), `limit` (1-200, def 20) | OHLCV candles |
| `dex-trades` | `pair`, `limit` (1-200, def 10), `trade_type` (all/orderbook/liquidity_pool, def all) | Recent DEX trades |
| `swap-quote` | `from`, `to`, `amount`, `mode` (send/receive, def send) | Best swap path |
| `stellar-asset` | `asset` | Asset supply, trustlines |
| `stellar-account` | `address` | Account balances and signers |
| `stellar-pools` | `asset` (optional), `limit` (1-200, def 10) | Liquidity pool data |
| `oracle-price` | `asset`, `feed` (crypto/fiat/dex, def crypto) | Reflector oracle price |

## CLI invocation examples

When MCP is unavailable, use `xlm` via Bash:

```bash
# Free tools
xlm crypto bitcoin,ethereum,stellar
xlm weather Lagos
xlm wallet
xlm oracle-price BTC
xlm dex-orderbook XLM/USDC --limit 5

# Paid tools
xlm search "Stellar MPP micropayments" --count 5
xlm stocks AAPL
xlm research "Soroban smart contracts" --num-results 3
xlm image "a stingray gliding over a coral reef at dusk" --size 1024x1024

# Help
xlm --help
```

Output is JSON. Pipe to `jq` for filtering:

```bash
xlm crypto bitcoin | jq '.bitcoin.usd'
```

## Payment receipts

Every paid response ends with a line like:

```
---
Payment: $0.003 USDC · tx/a3f9c28d71e0... · stellar testnet
```

The `tx_hash` is a real 64-character Stellar transaction hash. Users can verify any call at `https://stellar.expert/explorer/testnet/tx/<hash>`. **Always surface the tx hash to the user** when showing results from a paid tool.

## Budget management

The `budget` tool is **MCP-only**. In MCP mode, call `mcp__xlmtools__budget` with:

- `action: "set"` + `amount: 2.00` — cap spending at $2 for the session
- `action: "check"` — see remaining balance
- `action: "clear"` — remove the cap

**Scoping:**
- **MCP mode**: budget is session-scoped. The cap persists until the MCP server restarts. Cached responses never count against it.
- **CLI mode**: budget is not implemented. Because each `xlm` invocation is a fresh process, a per-call cap has no meaning there. If you need a cap in CLI mode, track spend externally by parsing the tx hash footer of each response.

## Working agreement (non-negotiable)

These are the hard rules. If you are about to break one, stop and reconsider.

1. **Mention the cost inline** for $0.001–$0.003 tools. **Confirm and wait** for $0.01+ tools (`research`, `screenshot`, `image`). Never skip either.
2. **Always surface the Stellar tx hash** in the response after a paid call. Users must be able to verify the payment on-chain.
3. **Always prefer the cheapest sufficient tool.** `crypto` (free) before `stocks` ($0.001). `search` ($0.003) before `research` ($0.010) unless the user explicitly wants a deep dive.
4. **Never retry a declined paid call.** If the user says no, offer an alternative or answer from training data. Do not call the tool anyway.
5. **Never batch multiple paid calls** without re-confirming. Each paid call is an independent spend decision.
6. **Never call paid tools for things answerable from training data.** See "When NOT to use this skill" above.
7. **Check MCP tool list before shelling out to CLI.** `mcp__xlmtools__*` tools exist? Use them. They're cached.
8. **Respect the budget.** If `mcp__xlmtools__budget` reports a low cap, pause and ask the user before continuing.

## Subagent caveat

If you delegate work to a forked subagent (e.g. via `context: fork`), **this skill does not automatically travel with it**. The subagent may call paid tools without the cost-confirmation rules above. Either preload this skill into the subagent explicitly, or handle paid calls from the parent context only.

## What to tell the user after a paid call

Good response pattern:

> Here's what I found about [topic] from XLMTools search:
>
> [results...]
>
> *Paid $0.003 USDC. Transaction: [`a3f9c28d…`](https://stellar.expert/explorer/testnet/tx/<full-64-char-hash>)*

Include the transaction link so the user can verify the payment on-chain.

## Troubleshooting

**"Command not found: xlm"** — User needs to install: `npm install -g @xlmtools/cli`

**"Account not found" / payment errors** — Wallet needs funding. Direct user to `https://faucet.circle.com` for testnet USDC. XLM is auto-funded via friendbot on first wallet creation — but if the wallet already exists and is out of XLM, it won't re-fund. In that case, ask the user to visit `https://lab.stellar.org/account/fund` manually.

**"Unknown tool: budget" (in CLI mode)** — The CLI doesn't implement `budget`. Budget is MCP-only. Use an MCP-compatible host, or track spend externally.

**"Budget limit reached"** — Only appears in MCP mode. Ask user to either clear the budget (`mcp__xlmtools__budget` with `action: "clear"`) or raise the cap (`action: "set"` with a higher `amount`).

**MCP tools not appearing** — User may need to install XLMTools as an MCP server: `claude mcp add xlmtools npx @xlmtools/mcp`. Fall back to CLI mode in the meantime if `xlm` is installed.

**API server unreachable** — XLMTools tools require the API server to be running. If every call hangs or times out, the API is either down or unreachable. Report to the user and stop retrying.

**"Is this site up / accessible?"** — There's no dedicated uptime tool. Closest approximation: `domain` (checks if DNS resolves) or `scrape` (fails loudly if the site is down, returns content if it's up). Note: `domain` does WHOIS availability, not HTTP reachability — a registered domain could still be offline.
