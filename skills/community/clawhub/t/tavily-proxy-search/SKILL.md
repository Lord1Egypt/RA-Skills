---
name: tavily-proxy-search
description: Search the web through a self-hosted TavilyProxyManager instance using Bearer master-key authentication while preserving the familiar tavily-search parameter style. Use when the user wants Tavily-style web search, source gathering, quick research, or result summaries through a self-hosted proxy instead of the official Tavily API.
---

# Tavily Proxy Search

Use the bundled script to search the web through an existing TavilyProxyManager `/search` endpoint.

This skill does not deploy TavilyProxyManager. It only sends authenticated search requests to a TavilyProxyManager instance that is already running. Project: https://github.com/xuncv/TavilyProxyManager

## Requirements

Provide credentials via either:
- environment variable: `TAVILY_PROXY_MASTER_KEY`
- `~/.openclaw/.env` line: `TAVILY_PROXY_MASTER_KEY=...`

Optional:
- environment variable: `TAVILY_PROXY_URL`
- `~/.openclaw/.env` line: `TAVILY_PROXY_URL=...`
- default URL: `http://127.0.0.1:8080/search`

Minimal example:

```bash
export TAVILY_PROXY_URL="http://127.0.0.1:8080/search"
export TAVILY_PROXY_MASTER_KEY="your-master-key"
```

## Commands

Run from the OpenClaw workspace:

```bash
# raw JSON (default)
python3 {baseDir}/scripts/tavily_proxy_search.py --query "..." --max-results 5

# include short answer (if available)
python3 {baseDir}/scripts/tavily_proxy_search.py --query "..." --max-results 5 --include-answer

# stable schema (closer to web_search): {query, results:[{title,url,snippet}], answer?}
python3 {baseDir}/scripts/tavily_proxy_search.py --query "..." --max-results 5 --format brave

# human-readable Markdown list
python3 {baseDir}/scripts/tavily_proxy_search.py --query "..." --max-results 5 --format md
```

## Output

### raw (default)
- JSON: `query`, optional `answer`, `results: [{title,url,content}]`

### brave
- JSON: `query`, optional `answer`, `results: [{title,url,snippet}]`

### md
- A compact Markdown list with title/url/snippet.

## Common failures

- `Missing TAVILY_PROXY_MASTER_KEY`
  - Cause: the proxy master key is not configured.
  - Fix: set `TAVILY_PROXY_MASTER_KEY` in the environment or `~/.openclaw/.env`.

- `Tavily proxy returned HTTP 401`
  - Cause: the Bearer master key is wrong, expired, or the endpoint expects a different auth setup.
  - Fix: verify the master key and confirm the target really is a TavilyProxyManager `/search` endpoint.

- `Tavily proxy request failed`
  - Cause: the proxy URL is unreachable, refused, timed out, or DNS failed.
  - Fix: verify `TAVILY_PROXY_URL`, container status, reverse proxy, and network reachability.

- `Tavily proxy returned non-JSON`
  - Cause: the configured URL is not the correct `/search` API endpoint, or an upstream proxy returned HTML/error text.
  - Fix: point `TAVILY_PROXY_URL` to the real TavilyProxyManager `/search` endpoint.

## Notes

- Keep `max-results` small by default (3–5) to reduce token and reading load.
- Authentication is handled with `Authorization: Bearer <TAVILY_PROXY_MASTER_KEY>`.
- Do not send `TAVILY_API_KEY` in the JSON body for this skill.
- Preserve the familiar parameter style: `--query`, `--max-results`, `--include-answer`, `--search-depth`, `--format`.
- `advanced` search depth depends on the capabilities of the deployed TavilyProxyManager instance and its upstream search configuration.
