# webcrawlerapi skill

Scrape a single page or crawl a full website using [WebCrawlerAPI](https://webcrawlerapi.com/).

## What it does

- **Scrape** — fetches a single URL and returns its content as markdown (synchronous)
- **Crawl** — crawls an entire website, saves all pages as markdown files (asynchronous, with polling)

## When it triggers

This skill is invoked when you ask Claude to:
- Fetch page content or get markdown from a URL
- Scrape a specific page
- Crawl a website or domain
- Do a web search or web fetch

## Requirements

Set the API key before use:

```bash
export WEBCRAWLERAPI_API_KEY="your_api_key"
```

Get a key at [dash.webcrawlerapi.com/access](https://dash.webcrawlerapi.com/access).

## Output

- **Scrape**: markdown content returned directly in the conversation
- **Crawl**: files saved to `.webcrawlerapi/<hostname>/` in the current working directory

## Skill file

[SKILL.md](./SKILL.md) — full instructions used by the Claude Code agent.
