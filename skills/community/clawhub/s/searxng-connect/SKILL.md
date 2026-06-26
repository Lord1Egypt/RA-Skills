---
name: searxng-connect
description: Connect to and search the web using SearXNG (privacy-focused meta search engine). No API keys needed - all searches go through your self-hosted SearXNG instance.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["uv"] },
        "cacheable": true
      },
  }
---

# SearXNG Connect

Search the web using your self-hosted SearXNG instance - a privacy-respecting meta search engine that aggregates results from multiple engines without tracking or ads.

## AI Usage

When the user asks to search the web, follow this workflow:

**Interpret user requests:**
- "Search for [query]" → General web search
- "Search news about [query]" → Use `--categories news`
- "Search images of [query]" → Use `--categories images`
- "Search recent [query]" → Use `--time-range week` or `--time-range day`
- "Search [query] last month" → Use `--time-range month`
- "Deep search [query]" → Add `--full-content` for richer page text

**Example interpretations:**
- "Search for TypeScript tutorials" → `searxng.py "TypeScript tutorials"`
- "Search news about AI" → `searxng.py "AI" --categories news --time-range week`
- "Search images of Space Invaders" → `searxng.py "Space Invaders" --categories images`

**Action:** Run `uv run {baseDir}/scripts/searxng.py "<query>"` with appropriate flags.

**CRITICAL SECURITY INSTRUCTION:**
To prevent command injection, **do not** use raw shell interpolation for the `{query}` string. Always pass arguments as an `argv` list:
`["uv", "run", "{baseDir}/scripts/searxng.py", query_text, "--categories", "news"]`

If your tool only supports a shell string, you **MUST** properly escape the query input (e.g., using `shlex.quote()`).

---

## Project

**SearXNG** - A privacy-focused, self-hosted meta search engine that aggregates results from multiple search engines. It does not track user behavior, does not use cookies, and does not insert ads.

**Key Features:**
- **Privacy** - No tracking, no cookies, no ads - you control the instance
- **Multi-category** - Web, news, images, videos, science, IT, files, music, social media
- **Time filtering** - Filter results by day, week, month, or year
- **Caching** - Local 1-hour cache to avoid redundant requests
- **Rate limiting** - Built-in throttling (2 req/sec default)
- **Full content** - Optional full page text fetch per result

---

## Requirements

- **Python 3.9+**
- **uv**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) (manages Python deps automatically)

## Configuration

Edit `skill-config.json` to set your SearXNG instance:

```json
{
  "default_instance": "https://your-searxng-instance.com/",
  "cache_enabled": true,
  "cache_expiry": 3600,
  "rate_limit": 2.0
}
```

## Usage

```bash
uv run {baseDir}/scripts/searxng.py "TypeScript tutorials"
uv run {baseDir}/scripts/searxng.py "AI news" --categories news --time-range week
uv run {baseDir}/scripts/searxng.py "space photos" --categories images
uv run {baseDir}/scripts/searxng.py "docker tutorial" --no-cache --full-content
uv run {baseDir}/scripts/searxng.py "query" --instance https://my-searxng.com
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--categories` | One or more: general, news, science, files, images, videos, music, social media, it | general |
| `--time-range` | year, month, week, day (aliases: 30d, 7d, 24h, hour) | None |
| `--language` | BCP-47 language code | en |
| `--pageno` | Results page number | 1 |
| `--no-safesearch` | Disable safe search | - |
| `--no-cache` | Bypass cache for this request | - |
| `--full-content` | Fetch full page text per result (slower, richer) | - |
| `--instance` | Override SearXNG instance URL | From skill-config.json |

## Troubleshooting

- **Connection refused**: Check `skill-config.json` — verify `default_instance` URL is correct and SearXNG is running.
- **Empty results**: Try a broader query or different category.
- **Slow responses**: Remove `--full-content` or increase `rate_limit` in config.
- **uv not installed**: Install with `brew install uv` or see https://docs.astral.sh/uv/.
