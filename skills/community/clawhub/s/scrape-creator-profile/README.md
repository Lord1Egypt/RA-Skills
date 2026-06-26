# scrape-creator-profile

Extract structured data from creator profiles on YouTube, Instagram, TikTok, Twitter/X, LinkedIn, Twitch, Substack, GitHub, and Patreon.

## What it does

- Resolves a creator handle or URL to a profile page
- Fetches and parses the profile using web_fetch, browser mode, or Apify fallback
- Returns a normalized JSON object with followers, bio, stats, recent content, and links
- Supports multi-profile comparison as a Markdown table or CSV export

## Platforms supported

YouTube · Instagram · TikTok · Twitter/X · LinkedIn · Twitch · Substack · GitHub · Patreon

## Install

```bash
clawhub install your-username/scrape-creator-profile
```

## Optional env vars

| Variable | Purpose |
|---|---|
| `APIFY_API_TOKEN` | Enables Apify fallback for heavily-blocked platforms |
| `CREATOR_SCRAPE_DELAY_MS` | Delay between requests in ms (default: 1500) |

## License

MIT-0
