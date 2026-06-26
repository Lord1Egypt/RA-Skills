---
name: unifuncs-search
description: Use unifuncs-search for real-time web search. Use this skill when users want to search the web, find articles, look up information, get the latest news, discover resources, or ask to "search", "find", "look up", check "latest updates", "find related articles", or otherwise retrieve up-to-date information from the internet.
argument-hint: [query]
allowed-tools: Bash(python*:*)
---

# UniFuncs Real-Time Web Search Skill

A fast real-time web search service.

## First-Time Setup

1. Go to <https://unifuncs.com/account> to get your API key.
2. Set the environment variable: `export UNIFUNCS_API_KEY="sk-your-api-key"`

## When to Use

You need to find information on any topic.
You do not have a specific URL yet.

## Guidelines

- `query` supports full search engine syntax (such as `site:` filters and exact-match phrases in quotes). For years or months in `query`
- use the latest year by default unless the user explicitly specifies otherwise.
- use the `freshness` parameter only when strong recency is required.
- For market data queries (stock price, share price, index, etc.), set `useStockQuery` to `true`.
- When needed, combine with [unifuncs-reader](../unifuncs-reader/SKILL.md) to fetch detailed content from result URLs.

## Usage

```bash
python3 search.py "query"
```

## Options

```text
usage: search.py [-h] [--freshness {Day,Week,Month,Year}]
                 [--include-images] [--page PAGE] [--count COUNT]
                 [--format {json,markdown,md,text,txt}]
                 query

UniFuncs real-time web search API client

positional arguments:
  query                 Search query. Full search engine syntax is
                        supported (for example site filters and exact-
                        match with quotes).

options:
  -h, --help            show this help message and exit
  --freshness {Day,Week,Month,Year}
                        Result freshness filter. Use only when strong
                        recency is required.
  --include-images      Include image results (default: false).
  --page PAGE           Result page number (default: 1).
  --count COUNT         Results per page, range 1-50 (default: 10).
  --format {json,markdown,md,text,txt}
                        Output format (default: json).

Examples:
  search.py "today's gold price" --page 1 --count 5
```
