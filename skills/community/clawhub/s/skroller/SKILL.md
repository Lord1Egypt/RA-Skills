---
name: skroller
description: Automated social media content collection and analysis across platforms (Twitter/X, Instagram, TikTok, Reddit, LinkedIn, YouTube, Product Hunt, Medium, GitHub, Pinterest). Use when you need to: (1) scrape public posts programmatically, (2) analyze content by keywords or filters, (3) monitor brand mentions or trends for research, (4) curate content for personal analysis, (5) archive publicly available information, or (6) generate digests from scraped feeds. Always comply with platform ToS and applicable privacy laws.
---

# Skroller - Social Media Content collection

Automate the collection and analysis of publicly available social media content. This skill handles content collection, filtering, and export with compliance safeguards.

## ⚖️ Legal & Compliance Requirements

**Before using this skill:**
1. **Review Platform ToS** - Each platform has different rules about automated access
2. **Check robots.txt** - Respect disallowed paths
3. **Rate Limiting** - Stay within platform rate limits to avoid service disruption
4. **Privacy Laws** - GDPR, CCPA, and other regulations apply to personal data
5. **Permitted Use** - Research, personal analysis, competitive intelligence (where allowed)
6. **Prohibited Use** - Spam, harassment, data resale, manipulation, bypassing auth

**Data Protection:**
- Anonymize personal data when storing
- Honor deletion requests (GDPR Art. 17)
- Limit retention to necessary periods
- Document lawful basis for processing
- Do not scrape sensitive personal data

## Core Capabilities

- **Content collection** - Gather publicly available posts from platforms
- **Data extraction** - Pull text, timestamps, engagement metrics, author info
- **Smart filtering** - Filter by keywords, hashtags, date ranges, engagement thresholds
- **Deduplication** - Track seen posts to avoid duplicates across sessions
- **Export formats** - JSON, CSV, Markdown, or direct to note apps (Bear/Obsidian)
- **Rate limiting** - Respect platform constraints and avoid service disruption

## Platform Support

| Platform | Approach | Notes |
|----------|----------|-------|
| Twitter/X | Browser automation | Use Playwright; handle login if needed |
| Instagram | Browser automation | Rate-limited; use sparingly |
| TikTok | Browser automation | Heavy JS; may need longer waits |
| Reddit | API + browser | Prefer API where possible |
| LinkedIn | Browser automation | Login required for most content |
| YouTube | API + browser | Comments via browser, videos via API |
| Product Hunt | Browser automation | Product discovery, launches |
| Medium | Browser automation | Articles, blog posts |
| GitHub | Browser automation | Issues, discussions, repos |
| Pinterest | Browser automation | Visual content, pins |

## Quick Start

### Basic Scroll and Extract

```bash
# Scroll Twitter feed, extract 50 posts about "AI"
node scripts/skroller.js --platform twitter --query "AI" --limit 50 --output posts.json
```

### Monitor Brand Mentions

```bash
# Monitor Reddit for brand mentions, export to Markdown
node scripts/skroller.js --platform reddit --query "mybrand" --format markdown --output mentions.md
```

### Competitive Research

```bash
# Scroll competitor Instagram, capture top posts by engagement
node scripts/skroller.js --platform instagram --profile @competitor --min-likes 1000 --output competitor-posts.json
```

## Scripts

### `scripts/skroller.js` - Main scrolling engine

JavaScript script using Playwright for browser automation.

```bash
# Using npm scripts (recommended)
npm run scroll -- --platform twitter --query "AI" --limit 50 --output posts.json

# Direct execution
node scripts/skroller.js --platform twitter --query "AI" --limit 50 --output posts.json
```

**Options:**
- `--platform` - Target platform (required): twitter, reddit, instagram, tiktok, linkedin, youtube, producthunt, medium, github, pinterest
- `--query` - Search keyword/hashtag
- `--profile` - Specific profile to scroll
- `--limit` - Max posts to scrape (default: 50)
- `--min-likes` - Filter by minimum engagement
- `--format` - Output format: json, csv, markdown (default: json)
- `--output` - Output file path
- `--screenshot` - Capture screenshots for debugging
- `--dedupe` - Skip previously seen posts

### `scripts/feed-digest.js` - Generate digests

Creates summary digests from exported post data.

```bash
npm run digest -- --input posts.json --output digest.md
# or: node scripts/feed-digest.js --input posts.json --output digest.md
```

### `scripts/export-to-notes.js` - Unified note app exporter

Exports scraped posts to multiple note applications with a single command.

**Supported apps:** Bear, Obsidian, Notion, Apple Notes, Evernote, OneNote, Google Keep, Roam Research, Logseq, Anytype

```bash
# Using npm scripts (recommended)
npm run export -- --input posts.json --app obsidian --vault ~/Documents/Obsidian

# Direct execution
node scripts/export-to-notes.js --input posts.json --app bear --tags "ai,research"
node scripts/export-to-notes.js --input posts.json --app notion --api-key $NOTION_TOKEN
node scripts/export-to-notes.js --input posts.json --app apple-notes
node scripts/export-to-notes.js --input posts.json --app evernote --output export.enex
node scripts/export-to-notes.js --input posts.json --app one-note --access-token $MS_TOKEN
node scripts/export-to-notes.js --input posts.json --app keep --output keep.html
node scripts/export-to-notes.js --input posts.json --app roam --output roam.md
node scripts/export-to-notes.js --input posts.json --app logseq --vault ~/Documents/Logseq
node scripts/export-to-notes.js --input posts.json --app anytype --output anytype.md
node scripts/export-to-notes.js --input posts.json --app obsidian --dry-run
```

**Configuration:** Set defaults in `.skroller-config.json`:
```json
{
  "export": {
    "defaultApp": "obsidian",
    "vault": "~/Documents/Obsidian",
    "folder": "Skroller",
    "notionDatabaseId": "<db-id>"
  }
}
```

**Requirements by app:**
- **Bear:** grizzly CLI (`go install github.com/tylerwince/grizzly/cmd/grizzly@latest`)
- **Obsidian:** Vault path
- **Notion:** API key (create at notion.so)
- **Apple Notes:** macOS with Notes app
- **Evernote:** Manual ENEX import
- **OneNote:** Microsoft Graph access token
- **Google Keep:** Manual HTML import
- **Roam Research:** Markdown import (drag MDL file into Roam)
- **Logseq:** Vault path (writes to pages/ folder)
- **Anytype:** Markdown import (use Anytype Import feature)

## Configuration

### `.skroller-config.json`

Store default settings:

```json
{
  "defaultLimit": 50,
  "scrollDelayMs": 1500,
  "userAgent": "Mozilla/5.0 ...",
  "platforms": {
    "twitter": {
      "loginRequired": false,
      "rateLimit": "100 requests/hour"
    },
    "instagram": {
      "loginRequired": true,
      "rateLimit": "50 requests/hour"
    }
  },
  "export": {
    "defaultFormat": "json",
    "includeImages": true,
    "includeMetrics": true
  }
}
```

### Authentication

Some platforms require login. Store credentials securely:

```bash
# For platforms requiring auth, set environment variables
export SKROLLR_TWITTER_COOKIE="<auth cookie>"
export SKROLLR_INSTAGRAM_USER="<username>"
export SKROLLR_INSTAGRAM_PASS="<password>"
```

**Security note:** Never commit auth files. Use `.env` with `.gitignore`.

## Output Structure

### JSON Output (default)

```json
{
  "platform": "twitter",
  "query": "AI",
  "scrapedAt": "2026-03-14T20:30:00Z",
  "posts": [
    {
      "id": "1234567890",
      "author": "@username",
      "text": "Post content here...",
      "timestamp": "2026-03-14T18:00:00Z",
      "likes": 150,
      "retweets": 42,
      "replies": 12,
      "url": "https://twitter.com/...",
      "media": ["image1.jpg"],
      "hashtags": ["#AI", "#ML"]
    }
  ]
}
```

### Markdown Output

```markdown
## Twitter Posts: "AI" (2026-03-14)

### @username - 150 likes
Post content here...

[View post](https://twitter.com/...)

---
```

## Filtering Strategies

### Keyword Matching
- Exact match: `"exact phrase"`
- Boolean: `AI AND (startup OR venture)`
- Exclude: `AI -crypto`

### Engagement Thresholds
- Filter low-quality: `--min-likes 100`
- Viral content: `--min-shares 500`

### Time Windows
- Recent only: `--date-from 2026-03-14`
- Historical: `--date-from 2026-01-01 --date-to 2026-01-31`

## Best Practices

### Rate Limiting
- Add delays between scrolls: `--delay 2000`
- Respect platform limits (see config)
- Use proxies for high-volume scraping

### Content Quality
- Filter by engagement to find signal
- Dedupe across sessions
- Export with timestamps for freshness tracking

### Ethics & Compliance
- Check platform ToS before scraping
- Don't scrape personal data at scale
- Use for research/curation, not spam

## Troubleshooting

### Scroll stops early
- Increase `--limit` or check for login requirements
- Some platforms detect automation; add random delays

### Missing content
- Some platforms lazy-load; increase scroll delay
- Try `--screenshot` to debug what's visible

### Rate limited
- Reduce frequency; use `--delay`
- Check platform-specific rate limits in config

## Integration with Other Skills

- **bear-notes**: Export via `export-to-notes.js --app bear`
- **obsidian**: Export via `export-to-notes.js --app obsidian`
- **notion**: Export via `export-to-notes.js --app notion`
- **github**: Create issues from scraped feedback/mentions

```bash
# Scroll and export to Obsidian in one command
node scripts/skroller.js --platform twitter --query "AI" --limit 20 --output ai.json && \
  node scripts/export-to-notes.js --input ai.json --app obsidian --vault ~/Documents/Obsidian

# Scroll and export to Notion
node scripts/skroller.js --platform reddit --query "startups" --limit 30 --output startups.json && \
  node scripts/export-to-notes.js --input startups.json --app notion --api-key $NOTION_TOKEN

# Use npm scripts for cleaner commands
npm run scroll -- --platform twitter --query "tech" --limit 25 --output tech.json
npm run export -- --input tech.json --app bear --tags "tech,research"
```

## See Also

- `references/platform-details.md` - Platform-specific selectors and quirks
- `references/rate-limits.md` - Rate limit guidelines per platform
- `assets/selector-cheatsheet.md` - CSS selectors for each platform
