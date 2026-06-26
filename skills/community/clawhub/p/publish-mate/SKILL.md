---
name: auto-publisher
description: Fetch global news from RSS/API sources, auto-generate articles with images, and publish to WordPress or custom CMS platforms
user-invocable: true
command-dispatch: false
metadata: {"openclaw":{"requires":{"bins":["python3"]},"emoji":"📰","os":["darwin","linux","win32"],"install":[{"type":"uv","packages":["certifi"]}]},"primaryEnv":"WP_APP_PASSWORD"}
---

# Auto Publisher — Automated News Content Publishing

You are an automated content publisher agent. Your job is to fetch global mainstream news, compose well-formatted articles with featured images, and publish them to the user's configured CMS platform.

## Quick Start

When a user first invokes `/auto-publisher`, check if `{baseDir}/config.json` exists.

**If config is missing**, run the interactive setup:
1. Ask the user for their website URL and platform type (WordPress / custom)
2. Ask for their username
3. Tell them to set the `WP_APP_PASSWORD` environment variable with their WordPress Application Password
4. Ask which news sources they want (offer defaults: BBC, NYT, Reuters, Al Jazeera)
5. Ask for publishing preferences: language, posts per day, categories
6. Ask for image source preference (RSS images / Unsplash / Pexels / Pixabay / picsum fallback)
7. Generate `{baseDir}/config.json` from their answers using `{baseDir}/config.example.json` as template

**If config exists**, proceed to the command router below.

## Commands

- `/auto-publisher` or `/auto-publisher publish` — Full pipeline: fetch → compose → upload images → publish
- `/auto-publisher setup` — Interactive configuration wizard (re-run setup)
- `/auto-publisher preview` — Fetch news and show preview, do NOT publish
- `/auto-publisher status` — Show recent publishing history
- `/auto-publisher config` — Display current config (mask sensitive values)

## Full Publishing Pipeline

When publishing, execute the integrated pipeline script:

```bash
python3 {baseDir}/scripts/auto_publish.py --config {baseDir}/config.json
```

Options:
- `--max N` — Limit to N articles (overrides config `posts_per_day`)
- `--dry-run` — Preview mode, no actual publishing

The script handles the complete flow:

### Step 1: Fetch News
- Reads all configured news sources (RSS, NewsAPI, custom API)
- Deduplicates against `{baseDir}/data/published_history.json`
- Returns structured article data (title, summary, content, source URL, image URL, tags)

### Step 2: Find Images for Each Article
Image sourcing priority:
1. **RSS feed image** — Many feeds include `media:content` or `enclosure` image URLs
2. **Image API search** — If configured (Unsplash/Pexels/Pixabay), searches by article keywords
3. **Fallback** — Uses picsum.photos for a random placeholder image
Images are downloaded to `{baseDir}/data/images/` and cached by content hash.

### Step 3: Upload Image to CMS
- Uploads the image to WordPress Media Library via REST API
- Handles server quirks: auto-detects `/wp-json/` vs `?rest_route=` URL format
- Retries on SSL/connection failures (common with some hosting providers)
- If server returns 201 with empty body, queries media library to recover the Media ID

### Step 4: Compose & Publish Article
- Creates the post with title, HTML content, excerpt, categories, tags
- Sets the uploaded image as the **featured image** (`featured_media`)
- Categories and tags are auto-created if they don't exist
- Publishes with configured status (publish/draft/pending/scheduled)

### Step 5: Report Results
After the pipeline completes, report to the user:
- Total articles published (success/fail count)
- Link to each published post
- Any errors encountered
- Image upload status for each article

## Individual Scripts

For advanced usage, the pipeline can also be run as separate steps:

```bash
# Fetch news only
python3 {baseDir}/scripts/fetch_news.py --config {baseDir}/config.json --max 5

# Fetch images for an article
python3 {baseDir}/scripts/fetch_image.py --config {baseDir}/config.json --title "Article Title"

# Publish a pre-composed article
python3 {baseDir}/scripts/publish.py --config {baseDir}/config.json --article article.json
```

## Configuration Reference

Config file: `{baseDir}/config.json` (copy from `{baseDir}/config.example.json`)

```json
{
  "platform": {
    "type": "wordpress",
    "url": "https://your-site.com",
    "username": "your-username",
    "app_password_env": "WP_APP_PASSWORD"
  },
  "news_sources": [
    {"type": "rss", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC World", "max_items": 5},
    {"type": "newsapi", "category": "general", "api_key_env": "NEWS_API_KEY", "max_items": 5}
  ],
  "publishing": {
    "posts_per_day": 5,
    "categories": ["News"],
    "default_tags": ["news"],
    "status": "publish",
    "language": "zh"
  },
  "images": {
    "source": "unsplash",
    "api_key_env": "UNSPLASH_API_KEY",
    "fallback_from_rss": true
  }
}
```

## Security — Environment Variables

**NEVER store passwords or API keys in config.json.** All secrets are loaded from environment variables.

| Variable | Purpose | Required |
|----------|---------|----------|
| `WP_APP_PASSWORD` | WordPress Application Password | Yes |
| `UNSPLASH_API_KEY` | Unsplash image search | No |
| `PEXELS_API_KEY` | Pexels image search | No |
| `PIXABAY_API_KEY` | Pixabay image search | No |
| `NEWS_API_KEY` | NewsAPI.org headlines | No |

Configure in OpenClaw settings (`~/.openclaw/openclaw.json`):
```json
{
  "skills": {
    "entries": {
      "auto-publisher": {
        "enabled": true,
        "env": {
          "WP_APP_PASSWORD": "xxxx xxxx xxxx xxxx"
        }
      }
    }
  }
}
```

## Error Handling

- Authentication failure → prompt user to verify credentials and Application Password
- News source unreachable → skip source, continue with others
- Image upload fails after 3 retries → publish article without featured image
- Category/tag creation fails → publish without that category/tag
- All errors logged to `{baseDir}/logs/auto_publish.log`

## Supported Platforms

| Platform | Status | Auth Method |
|----------|--------|-------------|
| WordPress | Full support | Application Passwords (REST API v2) |
| Custom REST API | Basic support | Bearer token / custom headers |

## Content Templates

Users can customize article format via templates in `{baseDir}/templates/`:
- `default.md` — Standard news article with source attribution
- `brief.md` — Short news brief format
