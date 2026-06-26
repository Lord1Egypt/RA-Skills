---
name: proxy4agent
description: Residential proxy for AI agents — fetch any URL through 2M+ real IPs, bypass anti-bot, geo-target, sticky sessions.
version: 1.6.2
metadata:
  openclaw:
    requires:
      anyBins: [node, npx]
    primaryEnv: NOVADA_PROXY_USER
    always: false
    homepage: https://github.com/Goldentrii/proxy4agent
    os: [macos, linux, windows]
    install:
      - kind: node
        formula: bestproxy4agents@1.6.2
        bins: [bestproxy4agents]
---

# Proxy4Agent

Residential proxy MCP server for AI agents. Route HTTP requests through 2M+ real home devices to bypass anti-bot systems, geo-target by country or city, and maintain sticky sessions.

**npm package:** `bestproxy4agents` | **GitHub:** [Goldentrii/proxy4agent](https://github.com/Goldentrii/proxy4agent)

## Setup

You only need credentials for ONE provider. Novada is the default and recommended provider.

### Option 1: Novada (recommended)

```bash
claude mcp add proxy4agent \
  -e NOVADA_PROXY_USER=your_username \
  -e NOVADA_PROXY_PASS=your_password \
  -- npx -y bestproxy4agents
```

Get credentials: [novada.com](https://www.novada.com) → Dashboard → Residential Proxies (30 seconds, no credit card).

### Option 2: Any HTTP proxy

```bash
claude mcp add proxy4agent \
  -e PROXY_URL="http://user:pass@host:port" \
  -- npx -y bestproxy4agents
```

Works with BrightData, Smartproxy, Oxylabs, IPRoyal, or any standard HTTP proxy. Encode targeting in the URL per your provider's format.

### Optional additional credentials

These are NOT required. Only set them if you need the specific feature:

- `NOVADA_API_KEY` — enables `agentproxy_search` (Google search via Novada Scraper API)
- `NOVADA_BROWSER_WS` — enables `agentproxy_render` (JS rendering via Novada Browser API)

## Privacy note

All HTTP requests are routed through your chosen proxy provider's residential network. Do not send sensitive internal URLs, API keys, or personally identifiable information through the proxy. The proxy provider can see request URLs and response content in transit. Use only for public web content.

## Tools

### agentproxy_fetch
Fetch any URL through a residential proxy. Works on Amazon, LinkedIn, Cloudflare-protected sites.

```
agentproxy_fetch(url="https://example.com", country="US", city="newyork", format="markdown")
```

Parameters: `url` (required), `country`, `city`, `session_id`, `format` (markdown/raw), `timeout` (1-120s).

### agentproxy_session
Sticky session — same IP across multiple requests. Use for login flows, paginated scraping.

```
agentproxy_session(session_id="job001", url="https://example.com/page/1")
agentproxy_session(session_id="job001", url="https://example.com/page/2")
```

### agentproxy_search
Structured Google search. Returns titles, URLs, descriptions as clean JSON.

```
agentproxy_search(query="residential proxy for AI", num=5, country="us")
```

Requires: `NOVADA_API_KEY` (optional — only if you need search)

### agentproxy_render
Render JS-heavy pages with real Chromium (SPAs, React/Vue apps).

```
agentproxy_render(url="https://react.dev", wait_for=".main-content", format="markdown")
```

Requires: `NOVADA_BROWSER_WS` (optional — only if you need JS rendering)

### agentproxy_status
Check proxy network health. No credentials needed.

## When to use proxy4agent

- Target site blocks your agent (403, captcha, Cloudflare challenge)
- Need content from a specific country or city
- Multi-step workflow requires same IP (login + scrape)
- JS-heavy page returns blank without a real browser
- Need structured search results without HTML parsing
