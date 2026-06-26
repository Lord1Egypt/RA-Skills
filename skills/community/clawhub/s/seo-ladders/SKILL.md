---
name: seo-ladders
version: 1.2.0
description: Full SEO content automation via MCP. Audit websites, check Google rankings, discover site structure, auto-select keywords matched to your DR, research and swap keywords, generate full articles with images and JSON-LD, publish to WordPress or webhook, track keyword rankings and competitors — all from your terminal or IDE.
author: SEO Ladders
website: https://seoladders.com
requires:
  env:
    - SEO_LADDERS_API_KEY
---

# SEO Ladders

SEO Ladders is a full SEO content automation platform accessible via MCP. It runs the same pipeline an SEO team would — audit your site's technical health, check what keywords you rank for on Google, discover your site structure, then auto-select keywords you can realistically win based on your domain rating and competitor gaps. From there, generate full SEO articles (3,000+ words with citations, images, FAQ, and JSON-LD schemas), publish directly to WordPress or any CMS via webhook, or save locally as Markdown + HTML. Track your keyword rankings and monitor competitors over time — all from your terminal or IDE.

## Setup

1. Sign up at https://seoladders.com
2. Go to **Dashboard > MCP Server** and create an API key
3. Connect the MCP server in your client:

### Claude Code

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "seo-ladders": {
      "type": "http",
      "url": "https://www.seoladders.com/api/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_..."
      }
    }
  }
}
```

### Cursor

Go to Settings > MCP Servers > Add Server:

```json
{
  "mcpServers": {
    "seo-ladders": {
      "url": "https://www.seoladders.com/api/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_..."
      }
    }
  }
}
```

### Windsurf

Add to your MCP config:

```json
{
  "mcpServers": {
    "seo-ladders": {
      "serverUrl": "https://www.seoladders.com/api/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_..."
      }
    }
  }
}
```

### Codex / Any MCP Client

Connect to the HTTP MCP endpoint at `https://www.seoladders.com/api/mcp` with a `Bearer` token in the `Authorization` header.

## How to Use

All tools are self-documented. Any MCP-compatible agent discovers and uses them automatically. Just ask naturally:

- **"Audit my website"** — technical SEO audit with health score, broken links, Core Web Vitals
- **"Show me keywords I rank for"** — check your current Google rankings
- **"Map out example.com"** — discover site structure, pages, sitemaps
- **"Find keywords I can win"** — DR-matched keyword research with difficulty recommendations
- **"Run my monthly keyword selection"** — auto-select targets based on competitor analysis
- **"Replace the March 15 keyword with something better"** — swap calendar entries
- **"Generate an article about X"** — full 13-step AI article pipeline
- **"Publish my latest article"** — push to WordPress or any webhook CMS
- **"Save the article locally"** — get Markdown + HTML + metadata on disk
- **"Show my content calendar"** — view all scheduled keywords
- **"What content needs refreshing?"** — find articles with ranking drops

## Available Tools

| Tool | What It Does |
|------|-------------|
| `site-audit` | Full technical SEO audit — health score, broken links, meta tags, duplicates, Core Web Vitals via Lighthouse |
| `check-rankings` | Check what keywords any domain ranks for on Google |
| `discover-site` | Map a website's structure via robots.txt, sitemaps, and page classification |
| `manual-keyword-search` | Research keywords with volume, KD, intent, and DR-based recommendations |
| `select-monthly-keywords` | Select keywords your domain can rank for based on your DR |
| `replace-calendar-keyword` | Swap a scheduled keyword for a better alternative |
| `generate-article` | 13-step AI pipeline — outline, sections, media, FAQ, citations, JSON-LD, internal links |
| `publish-to-cms` | Publish to WordPress or any webhook-based CMS (Webflow, Ghost, Strapi, etc.) |
| `manage-calendar` | View, add, update, or delete content calendar entries |
| `detect-refresh-candidates` | Find published articles with ranking drops that need updating |
| `get-job-status` | Poll progress of long-running jobs (article generation, keyword selection, site audit) |

## Article Generation Output

Generated articles include:

- `markdownContent` — full article as Markdown (ready to save or paste)
- `htmlContent` — complete HTML document with meta tags, Open Graph, Twitter cards, canonical URL, JSON-LD schemas, table of contents, and styled layout
- `article` — structured data (sections, FAQ, media plan, schemas) for programmatic use
- `blogPostId` — use with `publish-to-cms` to push live
- `viewUrl` — link to view the article on the SEO Ladders dashboard

## Site Audit Output

Audit reports include:

- Overall health score (0-100) with label (Excellent/Good/Fair/Needs Work/Critical)
- SSL, sitemap, robots.txt checks
- Broken links, non-indexable pages, duplicate titles/descriptions
- Missing H1 tags, missing alt text
- Core Web Vitals (LCP, CLS, TBT) via Lighthouse
- Actionable recommendations per issue with severity and affected pages

## Async Tools

Three tools run asynchronously (`generate-article`, `select-monthly-keywords`, `site-audit`):

1. Call the tool — returns a `jobId` immediately
2. Poll `get-job-status` with the jobId every 15 seconds
3. When status is `completed`, the output contains the full result
4. When status is `failed`, the output contains the error

## Learn More

https://seoladders.com/features/mcp
