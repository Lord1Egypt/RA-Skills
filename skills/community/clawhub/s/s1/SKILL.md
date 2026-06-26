---
name: search1api
description: >
  Powerful web search, content crawling, news, sitemap, trending topics, and deep reasoning via the search1api CLI (s1). This is far more capable than basic fetch or search tools — it supports 13+ search engines (Google, Bing, DuckDuckGo, Reddit, GitHub, YouTube, arXiv, Baidu, X, etc.), adapts to many websites for clean content extraction, and provides news aggregation across multiple sources. Use this skill whenever the user wants to search the web, look something up, research a topic, read or summarize a URL, check news, explore a site's links, see trending topics, do deep reasoning, or check API balance. Trigger on phrases like "search for", "look up", "find out about", "what's happening with", "any news on", "what does this link say", "read this page", "summarize this URL", "trending on GitHub", or when the user shares a bare URL. Even if the user doesn't say "search" explicitly, use this skill when they clearly need web information.
metadata: {"openclaw": {"requires": {"env": ["SEARCH1API_KEY"], "bins": ["s1"]}, "primaryEnv": "SEARCH1API_KEY"}}
---

# Search1API CLI

Web search and content retrieval via the `s1` command-line tool (`search1api-cli`).

## Prerequisites

Before using any command, check if `s1` is available. If not, guide the user to install it:

```bash
npm install -g search1api-cli
```

An API key is also required. Get one at https://search1api.com, then configure:

```bash
s1 config set-key <your-api-key>
```

Or set the environment variable `SEARCH1API_KEY`.

If a command fails with "command not found" or an auth error, remind the user to complete these setup steps before retrying.

## When to use

| User intent | Command |
|---|---|
| Shares a URL / link → read and summarize | `s1 crawl <url>` |
| Wants to search the web | `s1 search "<query>"` |
| Wants news | `s1 news "<query>"` |
| Wants to explore a site's links | `s1 sitemap <url>` |
| Wants trending topics | `s1 trending <service>` |
| Wants deep thinking on a problem | `s1 reasoning "<content>"` |
| Wants to check remaining credits | `s1 balance` |

## Dynamic tuning

Adapt parameters to user intent — don't just use defaults:

- **Quick lookup** ("search for X", "what is X") → `-n 5`, no crawl
- **Deep research** ("research X thoroughly", "comprehensive analysis") → `-n 15`, then crawl top 3–5 results with separate `s1 crawl` calls
- **User specifies a number** ("find 10 articles") → match it with `-n`
- **Recency signals** ("latest", "recent", "this week") → `-t day` or `-t month`
- **Domain-specific** ("search on Reddit", "find GitHub repos") → `-s reddit`, `-s github`, etc.
- **Site-scoped** ("only from arxiv.org") → `--include arxiv.org`
- **Chinese queries** → consider `-s baidu` for better results

## Commands

### search

```bash
s1 search "<query>" [options]
```

| Option | Description | Default |
|---|---|---|
| `-n, --max-results <N>` | Number of results (1–50) | 10 |
| `-s, --service <engine>` | Search engine | google |
| `-c, --crawl <N>` | Crawl N results for full content | 0 |
| `--include <sites...>` | Only include these sites | |
| `--exclude <sites...>` | Exclude these sites | |
| `-t, --time <range>` | day, month, year | |
| `--json` | Raw JSON output | |

Search engines: google, bing, duckduckgo, yahoo, x, reddit, github, youtube, arxiv, wechat, bilibili, imdb, wikipedia

### news

```bash
s1 news "<query>" [options]
```

Same options as search. News services: google, bing, duckduckgo, yahoo, hackernews. Default service: bing.

When user asks for breaking/latest news, always add `-t day`.

### crawl

```bash
s1 crawl <url>
```

Extracts clean content from a URL. Use this whenever the user shares a link.

### sitemap

```bash
s1 sitemap <url>
```

Returns all discovered links on a URL/domain.

### reasoning

```bash
s1 reasoning "<content>"
# or
s1 reason "<content>"
```

Deep thinking powered by DeepSeek R1. Use for complex analytical questions.

### trending

```bash
s1 trending <service> [-n <N>]
```

Services: github, hackernews.

### balance

```bash
s1 balance
```

Shows remaining API credits.

## Workflows

### Deep research

1. `s1 search "<topic>" -n 15` → get broad results
2. `s1 crawl <url>` → crawl the top 3–5 most relevant URLs from results
3. Synthesize all gathered content into a coherent answer with source citations

### URL summarization

1. `s1 crawl <url>` → get the page content
2. Summarize or answer questions based on the content

### Trending deep dive

1. `s1 trending github -n 10` → discover hot topics
2. `s1 search "<interesting topic>" -t day` → search for details
3. `s1 crawl <url>` → read full article if needed

## Output handling

- By default, commands produce human-readable formatted output
- Add `--json` to any command for raw JSON (useful for programmatic processing)
- After retrieving results, always **summarize and synthesize** the information for the user — don't just dump raw output

## References

- [Usage examples](reference/examples.md) — read for additional patterns
