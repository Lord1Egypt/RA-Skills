---
name: searxng-web-search
description: >
  Search the web using a self-hosted SearXNG metasearch engine. Use when the user asks
  to search the web, find information online, look up recent news, research a topic,
  or needs current data from the internet. Also use when the agent needs to gather
  external context to answer a question. Requires a running SearXNG instance with
  JSON API enabled.
license: Apache-2.0
compatibility: >
  Requires Python 3.9+, requests library, and a running SearXNG instance with
  format: [html, json] enabled in settings.yml. Network access to the SearXNG endpoint.
metadata:
  author: timeplus-io
  version: "1.0.0"
  tags: search web searxng metasearch privacy
  category: web
---

# SearXNG Web Search

Privacy-respecting web search skill powered by SearXNG, a free metasearch engine
that aggregates results from 243+ search services without tracking users.

Rewritten from PulseBot's built-in web search skill to use SearXNG as the backend,
packaged as a standalone agentskills.io skill.

## Prerequisites

1. A running SearXNG instance (self-hosted or accessible endpoint)
2. JSON format must be enabled in your SearXNG `settings.yml`:

```yaml
search:
  formats:
    - html
    - json
```

3. Python `requests` library installed

## Configuration

The skill uses environment variables for configuration:

| Variable | Default | Description |
|---|---|---|
| `SEARXNG_BASE_URL` | `http://localhost:8080` | SearXNG instance URL |
| `SEARXNG_MAX_RESULTS` | `10` | Maximum results to return |
| `SEARXNG_LANGUAGE` | `all` | Default search language (e.g. `en`, `zh`, `all`) |
| `SEARXNG_SAFESEARCH` | `0` | Safe search level: 0=off, 1=moderate, 2=strict |
| `SEARXNG_TIMEOUT` | `15` | Request timeout in seconds |
| `SEARXNG_CATEGORIES` | `general` | Default categories (comma-separated) |

## Usage

Run the search script:

```bash
python scripts/searxng_search.py "your search query"
```

With options:

```bash
python scripts/searxng_search.py "latest AI news" \
  --categories news \
  --language en \
  --time-range day \
  --max-results 5
```

### Output Format

The script outputs JSON to stdout with the following structure:

```json
{
  "query": "search query",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Text snippet from the page...",
      "engines": ["google", "bing"],
      "score": 9.0,
      "category": "general",
      "published_date": "2025-01-01T00:00:00"
    }
  ],
  "suggestions": ["related query 1", "related query 2"],
  "answers": ["direct answer if available"],
  "total_results": 10,
  "error": null
}
```

If an error occurs, `results` will be empty and `error` will contain the message.

### As a Python Module

You can also import and use the search function directly:

```python
from scripts.searxng_search import SearXNGSearchTool

tool = SearXNGSearchTool(base_url="http://localhost:8080")
results = tool.search("quantum computing", categories="science,it", max_results=5)

for r in results["results"]:
    print(f"[{r['title']}]({r['url']})")
    print(f"  {r['snippet']}")
```

## Integration with PulseBot

To register this skill in PulseBot, place it under `skills/` and PulseBot
will discover it via SKILL.md frontmatter. The Python script can also be
called as a tool function by wrapping it:

```python
from skills.searxng_web_search.scripts.searxng_search import SearXNGSearchTool

tool = SearXNGSearchTool()

def web_search(query: str, categories: str = "general", max_results: int = 10) -> str:
    """Search the web using SearXNG. Returns JSON results."""
    result = tool.search(query, categories=categories, max_results=max_results)
    return json.dumps(result, indent=2)
```

## Edge Cases

- If SearXNG is unreachable, the script returns a structured error with `error` field set
- If no results are found, `results` is an empty list (not an error)
- Some engines may be unresponsive; check `unresponsive_engines` in verbose mode
- Rate-limited public instances may return 429; prefer self-hosted instances
- Queries with special characters are URL-encoded automatically

## SearXNG Setup (Quick Start)

For details on deploying SearXNG, see [references/REFERENCE.md](references/REFERENCE.md).

```bash
docker run -d --name searxng -p 8080:8080 \
  -v "$(pwd)/searxng:/etc/searxng" \
  searxng/searxng:latest
```

Then edit `/etc/searxng/settings.yml` to add `json` to `search.formats`.
