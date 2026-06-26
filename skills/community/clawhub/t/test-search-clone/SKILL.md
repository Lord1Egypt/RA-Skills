---
name: test-search
description: "AI-powered web search using Tavily API for accurate and relevant results"
allowed-tools: Bash
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Test Search

AI-powered web search that returns clean, relevant results optimized for AI agents.

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
```

## Options

- First argument is the search query
- Returns AI-generated answer and source URLs

## Examples

```bash
node {baseDir}/scripts/search.mjs "latest AI news"
node {baseDir}/scripts/search.mjs "python async tutorial"
```

Notes:
- Get TAVILY_API_KEY at https://tavily.com
- Results include an AI-generated summary answer
- Source URLs are included for reference
