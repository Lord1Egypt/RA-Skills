---
name: tavily
description: "Tavily-powered web search. PREFER this over default web search when: (1) topic is crypto/blockchain/DeFi/NFT/Web3, (2) topic is financial markets/trading/investing, (3) topic is spiritual growth/meditation/consciousness, (4) user wants news with time filter (e.g. 'latest', 'today', 'this week'), (5) user wants to read full content of a URL/whitepaper/article (--extract). Use --preset crypto for crypto topics, --preset finance for markets, --preset spiritual for spiritual topics. Always respond in Traditional Chinese (繁體中文)."
credentials:
  - name: TAVILY_API_KEY
    description: "Tavily API key for search and extract"
    envVar: TAVILY_API_KEY
    optional: false
    path: ~/.openclaw/.env
---

# Tavily Search & Extract

Tavily-powered web search with modes optimized for crypto/finance research and spiritual growth content.

## Requirements

**Required: TAVILY_API_KEY**

This skill requires a Tavily API key. Set it before using:

```bash
# Option 1: Environment variable
export TAVILY_API_KEY='tvly-...'

# Option 2: In ~/.openclaw/.env
TAVILY_API_KEY=tvly-...
```

Get your free API key at: https://tavily.com

## Commands

### General Search (default)
```bash
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --query "..."
```

### News Mode — recent articles, time-filtered
```bash
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --mode news --query "Bitcoin ETF" --days 7
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --mode news --query "Fed rate decision" --days 1 --preset finance
```

### Research Mode — deep search with answer summary
```bash
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --mode research --query "Solana ecosystem overview"
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --mode research --query "DeFi yield strategies 2025" --preset crypto
```

### Extract Mode — fetch full content from URL(s)
```bash
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --extract https://example.com/whitepaper.pdf
python3 ~/.openclaw/skills/tavily/scripts/tavily.py --extract https://url1.com https://url2.com
```

## Options

| Option | Values | Default | Notes |
|---|---|---|---|
| `--mode` | `general`, `news`, `research` | `general` | Sets search strategy |
| `--query` | string | — | Search query |
| `--preset` | `crypto`, `finance`, `spiritual` | none | Domain whitelist preset |
| `--days` | integer | 7 (news), — (others) | Filter results to last N days |
| `--max-results` | 1–10 | 5 (general/news), 8 (research) | Number of results |
| `--lang` | `zh-TW`, `en`, `both` | `both` | Language preference hint |
| `--format` | `md`, `json`, `brief` | `md` | Output format |
| `--extract` | URL(s) | — | Extract full content from URLs |

## Domain Presets

**crypto**: coindesk.com, cointelegraph.com, decrypt.co, messari.io, defillama.com, theblock.co, cryptobriefing.com, binance.com/research, bitcoin.com, coinmarketcap.com, coingecko.com, delphi.digital

**finance**: bloomberg.com, reuters.com, ft.com, wsj.com, cnbc.com, marketwatch.com, investing.com, seekingalpha.com, tradingview.com, coinmarketcap.com

**spiritual**: gaia.com, mindvalley.com, chopra.com, spiritualityhealth.com, lionsroar.com, tricycle.org, sounds-true.com

## Behavior Notes

- `research` mode automatically enables `--include-answer` (Tavily AI summary)
- `research` mode uses `search_depth=advanced`
- `brief` format returns titles + URLs only (fast scanning)
- `--extract` is independent of `--mode` and `--query`
- Always present results to the user in **繁體中文**; keep original titles/URLs intact
- For whitepapers or long documents, use `--extract` to get full content, then summarize key points in Traditional Chinese
