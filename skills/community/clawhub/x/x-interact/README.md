# X.com Interact via Tavily

Search X.com (Twitter) content using Tavily's web search and extraction capabilities. Requires Tavily API key (free tier works).

## Install

```bash
# Clone the repo
git clone https://github.com/0x-wzw/x-interact.git ~/.openclaw/skills/x-interact

# Or install via ClawHub (when published)
clawhub install x-interact
```

## Configure

```bash
# Add Tavily MCP server via mcporter
mcporter config add tavily https://mcp.tavily.com/mcp/?tavilyApiKey=<YOUR_KEY>
```

Get a free API key at [tavily.io](https://tavily.io).

## Quick Start

```bash
# Search for a user's tweets
mcporter call tavily.tavily_search query="from:vitalikbuterin ethereum" max_results=5

# Search tweets by keyword
mcporter call tavily.tavily_search query="DeFi yield farming site:x.com" max_results=10

# Extract content from a linked article
mcporter call tavily.tavily_extract urls='["https://example.com/article"]'
```

## How It Works

X.com blocks direct extraction (403). Tavily provides search-index access to tweets, profiles, and threads. Use `tavily_search` to find content, then extract linked articles with `tavily_extract`.

## Rate Limits

- Tavily free tier: 20 requests/minute, 1000 requests/month

## Skills

This skill is part of the 0x-wzw agent swarm. Related skills:

- **[swarm-workflow-protocol](https://github.com/0x-wzw/swarm-workflow-protocol)** — Multi-agent orchestration
- **[defi-analyst](https://github.com/0x-wzw/defi-analyst)** — DeFi research and analysis

## License

MIT
