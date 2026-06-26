---
name: x-interact
description: Interact with X.com (Twitter) via Tavily web search and extraction. Search tweets, extract content from linked URLs, monitor accounts and topics. Requires Tavily API key (free tier works).
---

# X.com Interact via Tavily

Tavily is configured as an MCP server and provides the interface for X.com content through search indexing.

## Prerequisites

- **Tavily API key** — free at [tavily.io](https://tavily.io)
- **mcporter** — OpenClaw skill for MCP tool calling

## Setup Tavily MCP

```bash
mcporter config add tavily https://mcp.tavily.com/mcp/?tavilyApiKey=<YOUR_KEY>
```

## Core Operations

### Search X.com

```bash
# Search for a user's tweets
mcporter call tavily.tavily_search query="from:username keyword" max_results=5

# Search tweets by keyword
mcporter call tavily.tavily_search query="keyword site:x.com" max_results=10

# Search for a specific tweet or thread
mcporter call tavily.tavily_search query="site:x.com username tweet context" max_results=3
```

### Extract Content from Linked URLs

```bash
# Extract from a news article or blog linked in a tweet
mcporter call tavily.tavily_extract urls='["https://example.com/article"]'
```

### Deep Research on a Topic

```bash
# Full research with Tavily (search + extract combined)
mcporter call tavily.tavily_research query="topic name" search_depth="basic" max_results=5
```

## Notes

- X.com blocks direct extraction (403). Use `tavily_search` to find tweet content via search index, or ask Z to paste tweet text.
- Tavily search indexes X.com profiles, tweet URLs, and threads.
- Combine Tavily search for finding tweets + Tavily extract for diving into linked articles.
- Rate limit: 20 requests/minute on Tavily free tier.

## Example Workflow

1. **Find tweets:** `mcporter call tavily.tavily_search query="from:vitalikbuterin ethereum" max_results=5`
2. **Get thread context:** `mcporter call tavily.tavily_search query="site:x.com vitalikbuterin tweet_thread" max_results=3`
3. **Extract linked article:** `mcporter call tavily.tavily_extract urls='["https://example.com/linked-article"]'`

## Rate Limits

- Tavily free tier: 20 requests/minute, 1000 requests/month
- No rate limits on GeckoTerminal/DeFiLlama when used alongside
