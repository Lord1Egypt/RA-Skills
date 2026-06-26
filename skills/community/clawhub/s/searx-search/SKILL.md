---
name: searx-search
description: Provides web search using free SearX instances from https://searx.space/. Trigger when a user asks to search the web or wants the latest AI news and global events. The skill fetches the list of public SearX instances, selects one, performs the query, and retries with up to two alternative instances if the request fails. Returns plain text search results only.
---

# SearX Search Skill

## Overview

Search the web via a free SearX instance. Use when a user requests "search ...", "最新 AI 新闻", or "全球大事". The skill returns plain text results without HTML.

## Execution

The `scripts/search_searx.sh` script takes a search query as its argument and performs the steps:

1. Download the JSON list of public instances from `https://searx.space/data/instances.json`.
2. Extract up to three reachable instance URLs.
3. For each instance (max 3 attempts):
   * Send a GET request to `<instance>/search?q=<query>&format=json`.
   * If the HTTP status is 200 and a non‑empty result is returned, output the titles and URLs of the first 5 results, one per line, then exit successfully.
   * If the request fails, continue with the next instance.
4. If all attempts fail, output `搜索失败，请稍后重试。`.

The script prints only plain text, suitable for direct user consumption.

## Usage

```bash
./scripts/search_searx.sh "最新 AI 新闻"
```

Will output something like:

```
Title 1 - https://example.com/...
Title 2 - https://example.org/...
```
