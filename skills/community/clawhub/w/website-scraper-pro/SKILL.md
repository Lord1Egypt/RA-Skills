---
name: website-scraper-pro
description: "Run a local script to scrape a single web page into clean markdown or deterministic JSON with Crawl4AI. Use when: user needs direct page retrieval from a URL, JS-aware single-page scraping, or deterministic query-focused narrowing without internal AI processing. Invoke by reading this SKILL.md then running: uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py <URL>"
homepage: https://github.com/unclecode/crawl4ai
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["uv"]}}}
---

# Skill: Website Scraper Pro

## When to use
- The user wants the content of a single web page from a specific URL.
- The user wants clean markdown extracted from an article, docs page, blog post, or landing page.
- The user wants a JS-aware scrape for a page that depends on client-side rendering.
- The user wants deterministic query-focused narrowing of one page without using an AI model inside the skill.
- The user wants structured JSON output with markdown, title, links, and metadata.

## When NOT to use
- The user wants a broad web search across multiple sources.
- The user wants a site-wide crawl, recursive crawl, or multi-page extraction workflow.
- The user wants AI summarization, synthesis, or answer generation inside the scraper itself.
- The user wants authenticated browser automation or interactive form submission.

## Commands

### Scrape a page to markdown

```bash
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py <URL>
```

### Scrape a JS-heavy page

```bash
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py <URL> --js
```

### Scrape a page and narrow by query

```bash
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py <URL> --query "<TEXT>"
```

### Return deterministic JSON

```bash
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py <URL> --format json
```

### Examples

```bash
# Default markdown scrape
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py https://example.com

# JS-aware scrape
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py https://example.com --js

# Query-focused retrieval
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py https://example.com --query "documentation examples"

# JSON output
uv run /root/.openclaw/workspace/skills/website-scraper-pro/src/main.py https://example.com --format json
```

## Output

- Default output is clean markdown for a single page.
- `--query` keeps the output deterministic and non-LLM.
- `--format json` returns deterministic JSON with fields such as `title`, `url`, `markdown`, `links`, and `metadata` when available.

## Notes

- This v1 does not use AI models internally. It is a deterministic retrieval tool only.
- The skill is single-page only. It does not do deep crawling, site maps, schema extraction, or RAG.
- `uv run` reads the inline `# /// script` dependency block in `main.py` and installs `crawl4ai` in an isolated environment.
- If browser setup is missing, run one-time setup commands such as:
  - `uv run --with crawl4ai crawl4ai-setup`
  - `uv run --with crawl4ai python -m playwright install chromium`
- Do NOT use web search for this workflow when a direct URL is available.
- Call `uv run src/main.py` directly as shown above.
