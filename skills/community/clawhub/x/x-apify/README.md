# X/Twitter Data Fetcher (Apify)

Fetch X/Twitter data from anywhere using Apify actors.

## Default actor

`apidojo~tweet-scraper` (Tweet Scraper V2). Store sheet: https://apify.com/apidojo/tweet-scraper

Checked against the Apify API on 2026-08-31: public, not deprecated, last code change 2026-08-31. 30-day public runs: 4,501,223 succeeded, 0 failed, 19,055 timed out, 245,137 aborted (94.5% succeeded). Cost: $0.0004 per tweet ($0.40 per 1,000 tweets), pay per event, all plan tiers.

The previous default `quacker~twitter-scraper` is deprecated and under maintenance. https://apify.com/quacker/twitter-scraper is a generic landing page, not an actor sheet.

Limits of the default actor (actor README, 2026-08-31):

- At least 50 tweets per query. This skill's `--max-results` default is 20; pass `--max-results 50` or higher.
- No single-tweet fetch and no conversation/reply scraping. `--url` does not match this actor; use `APIFY_ACTOR_ID=apidojo~twitter-scraper-lite` for that mode.
- Free-plan users: 5 runs per month, 10 items per run, and the actor README states they cannot call this actor via the API.

`scripts/config.py` defaults to this actor. `APIFY_ACTOR_ID` overrides it.

Raw tweet fields (`author.userName`, `createdAt`, `likeCount`, `retweetCount`, `replyCount`) differ from the old quacker schema (`user.screen_name`, `created_at`, `favorite_count`, `conversation_count`). The skill script maps both into a flat `{id, text, author, likes, ...}` object. See [SKILL.md](SKILL.md) for the field table.

## Features

- Tweet search by keywords, hashtags, mentions
- User timelines via profile URL
- Tweet-by-URL mode exists in the script; the default actor rejects single tweets and replies
- Local caching so repeat requests do not start a new actor run (1h for searches, 24h for profiles)
- Cache management: `--cache-stats`, `--clear-cache`, `--no-cache`
- JSON or human-readable summary output
- Python script, no Apify SDK

## Free Tier

Apify Free plan: $5 prepaid usage per month, no credit card. Unused credits do not roll over. At $0.40 per 1,000 tweets that is 12,500 tweets, subject to the actor's Free-plan run/item/API limits above.

[Sign up](https://apify.com/)

## Quick Start

```bash
# 1. Set your API token and actor
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN"
export APIFY_ACTOR_ID="apidojo~tweet-scraper"

# 2. Search tweets (50+ for the default actor)
python3 scripts/fetch_tweets.py --search "artificial intelligence" --max-results 50

# 3. Get user's tweets
python3 scripts/fetch_tweets.py --user "OpenAI" --max-results 50

# 4. Get specific tweet (needs APIFY_ACTOR_ID=apidojo~twitter-scraper-lite)
python3 scripts/fetch_tweets.py --url "https://x.com/user/status/123"
```

## Documentation

See [SKILL.md](SKILL.md) for setup, input/output schema, and usage examples.

## Links

- [Apify Free plan](https://apify.com/pricing): $5/month prepaid usage
- [Get API token](https://console.apify.com/account/integrations)
- [Tweet Scraper V2 actor](https://apify.com/apidojo/tweet-scraper)

## Requirements

- Python 3.6+
- `requests` library (`python3 -m pip install requests`)
- Apify API token

## Legal Notice

This skill accesses publicly available data via Apify. Users are responsible for compliance with local data protection laws (GDPR etc.) and X/Twitter's Terms of Service.

## License

MIT
