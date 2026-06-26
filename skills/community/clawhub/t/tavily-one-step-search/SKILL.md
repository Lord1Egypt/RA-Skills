---
name: tavily-search
description: "联网搜索, 网页搜索, 实时联网, 一键配置。让 OpenClaw 用 Tavily 实现实时搜索（含免费额度）。One-step install + guided key setup. Guide: github.com/plabzzxx/openclaw-tavily-search"
---

# Tavily Search Toolkit (V2)

This skill provides a single Node CLI with subcommands:

- `search` — web search with filters and multiple output formats
- `extract` — fetch clean content from one or more URLs
- `crawl` — crawl a site with extraction controls
- `map` — discover and map site URLs

## Requirements

Set `TAVILY_API_KEY` via one of:

- env var: `TAVILY_API_KEY=...`
- `~/.openclaw/.env` line: `TAVILY_API_KEY=...`

## Quick examples

```bash
# 1) Search (Brave-like structure)
node {baseDir}/scripts/tavily_search.mjs search \
  --query "OpenClaw multi-agent" --max-results 5 --format brave

# 2) Search with domain filters
node {baseDir}/scripts/tavily_search.mjs search \
  --query "周大福" \
  --include-domains ctf.com.cn,ctfmall.com,chowtaifook.com \
  --format brave

# 3) Extract specific URLs
node {baseDir}/scripts/tavily_search.mjs extract \
  --urls https://docs.openclaw.ai,https://docs.tavily.com \
  --content-format markdown --format md

# 4) Crawl docs site
node {baseDir}/scripts/tavily_search.mjs crawl \
  --url docs.tavily.com --max-depth 2 --limit 30 --format md

# 5) Map a site structure
node {baseDir}/scripts/tavily_search.mjs map \
  --url docs.openclaw.ai --max-depth 2 --limit 40 --format md
```

## Proxy controls

- Inherit system proxy env by default (`HTTP_PROXY` / `HTTPS_PROXY`)
- Force proxy: `--proxy http://127.0.0.1:7890`
- Disable proxy: `--no-proxy`

## Notes

- Keep `max-results` small (3–5) for chat tasks.
- Use `search --format brave` for stable downstream parsing.
- Use `extract/crawl/map` only when search snippets are insufficient.
