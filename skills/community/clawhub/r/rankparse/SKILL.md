# RankParse SEO API

RankParse gives you live SEO data — backlinks, domain authority, tech stack, competitor overlap, and 20+ other signals — for any domain or URL. No subscription. Credits from $0.009/call.

## When to use this skill

Use RankParse when the user is doing SEO work:

- **Link building** — finding prospects, auditing competitors' backlinks, spotting link gaps
- **Competitor research** — comparing DA scores, top pages, referring domains across sites
- **Site audits** — checking tech stack, page metadata, crawl history, status codes
- **Content strategy** — finding which pages earn the most links in a niche
- **Prospecting** — discovering similar domains or shared linkers for outreach lists

## Common SEO workflows

### Competitor link gap analysis
Find domains linking to competitors but not to you — ranked by authority for outreach prioritization.
1. `get_backlinks` for your domain
2. `get_backlinks` for each competitor
3. `get_domain_overlap` across all targets
4. `get_domain_authority` on gap domains to prioritize

*Prompt: "Find link-building opportunities I'm missing vs stripe.com and shopify.com"*

### Domain authority comparison
Benchmark a site against competitors before a pitch, acquisition, or partnership.
1. `get_domain_authority` for each domain

*Prompt: "Compare the DA of linear.app, height.app, and plane.so"*

### Backlink profile audit
Understand the quality and anchor text distribution of a site's inbound links.
1. `get_referring_domains` — unique linking domains
2. `get_anchor_text` — anchor text distribution, flag over-optimized anchors
3. `get_backlinks` — top individual links with source pages

*Prompt: "Audit the backlink profile of example.com — flag anything that looks spammy"*

### Top pages by link equity
Find what content earns the most links in a niche to inform your content strategy.
1. `get_top_pages` for competitor domains

*Prompt: "What pages on vercel.com attract the most backlinks?"*

### Outreach list building
Build a targeted list of prospects to contact for guest posts or link placements.
1. `get_similar_domains` — sites with overlapping link profiles
2. `get_link_intersect` — domains already linking to multiple competitors
3. `get_domain_authority` — filter by DA threshold

*Prompt: "Build me a list of 20 sites similar to smashingmagazine.com with DA over 50"*

### Site technical audit
Quickly check a site's tech stack, page signals, and crawl health.
1. `get_tech_stack` — CMS, analytics, CDN, frameworks
2. `get_page_meta` — title, description, canonical, OG tags
3. `get_crawl_history` — first seen, last crawled

*Prompt: "What tech stack and CMS is competitor.com running?"*

## Setup

```
RANKPARSE_API_KEY=rp_your_key_here
```

Get a free key with 100 credits at https://rankparse.com/signup.

## MCP server

```json
{
  "mcpServers": {
    "rankparse": {
      "url": "https://mcp.rankparse.com/mcp",
      "headers": {
        "X-API-Key": "${RANKPARSE_API_KEY}"
      }
    }
  }
}
```

## Available tools

| Tool | What it does | Credits |
|---|---|---|
| `get_domain_authority` | DA score, referring domains, registered date, popularity rank | 1 |
| `get_backlinks` | Inbound links with anchor text and source pages | 2 |
| `get_referring_domains` | Unique domains linking to target | 2 |
| `get_anchor_text` | Anchor text distribution | 2 |
| `get_top_pages` | Pages with most inbound links | 2 |
| `get_outbound_links` | External links from a domain | 2 |
| `get_domain_rank` | Rank metrics and scores | 2 |
| `get_site_explorer` | Full domain overview | 10 |
| `get_page_meta` | Title, description, canonical, OG tags | 2 |
| `get_tech_stack` | Detected technologies | 2 |
| `get_url_index` | Indexed URLs for a domain | 2 |
| `get_crawl_history` | Crawl timestamps | 2 |
| `get_status_codes` | HTTP status distribution | 2 |
| `get_content_types` | Content type breakdown | 2 |
| `get_language` | Language distribution | 2 |
| `get_domain_overlap` | Domains linking to multiple targets | 5 |
| `get_link_intersect` | Shared linkers between two domains | 5 |
| `get_similar_domains` | Domains similar to target | 5 |

## Pricing

Credits never expire. Packs start at $9 for 1,000 credits (~1,000 DA lookups or ~500 backlink queries).
