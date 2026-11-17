# Changelog

## [1.1.0] - 2026-08-31

### Changed
- Removed `package.json`. It declared an npm package that was never published and had no `main`, dependencies, or scripts. ClawHub CLI 0.22+ refuses to publish any folder containing a `package.json` as a skill.
- Documented `apidojo~tweet-scraper` as the default actor. Apify API check on 2026-08-31: public, not deprecated, $0.40 per 1,000 tweets, 4,501,223 / 4,765,415 succeeded public runs in 30 days (0 failed).
- Replaced the `quacker~twitter-scraper` store link with https://apify.com/apidojo/tweet-scraper. The quacker URL is a generic landing page; the actor is deprecated and under maintenance (6,746 failed of 31,025 public runs in 30 days).
- Documented apidojo input (`searchTerms`, `startUrls`, `maxItems`) and output (`author.userName`, `createdAt`, `likeCount`, `retweetCount`, `replyCount`) versus the old quacker schema.
- Documented actor limits: 50-tweet minimum, no single-tweet or reply scraping, Free-plan API restriction. `--url` needs `apidojo~twitter-scraper-lite`.
- Switched the `scripts/config.py` default actor from `kaitoeasyapi` (`CJdippxWmn9uRfooo`) to `apidojo~tweet-scraper`. The payloads in `fetch_tweets.py` (`searchTerms`, `startUrls`, `maxItems`) are apidojo's input schema; kaitoeasyapi takes a different one and returned nothing for them.
- Raised `DEFAULT_MAX_RESULTS` from 20 to 50. The actor rejects runs below 50 items, so the old default failed on every unqualified search.

## [1.0.6] - 2026-03-04

### Fixed
- Switched default actor from deprecated `quacker~twitter-scraper` to `kaitoeasyapi` ($0.25/1000 tweets, 32M runs)
- Updated tweet field mapping for new actor schema (`author.userName`, `createdAt`, `likeCount`, `retweetCount`, `replyCount`)
- Search now returns real results (~20 tweets) vs 0 with old actor

## [1.0.5] - 2026-03-03

### Changed
- Synced version metadata and retained recent output/path safety fixes.


## [1.0.1] - 2026-02-11

### Fixed

- Switched default actor from `apidojo~tweet-scraper` (returning `{"noResults": true}`) to `quacker~twitter-scraper`
- Updated actor input payloads to match `quacker~twitter-scraper` API:
  - Search: `searchTerms` + `maxItems`
  - User: `startUrls` + `maxItems`
  - URL: `startUrls` + `maxItems`
- Updated tweet field mapping to match actor response shape:
  - `id_str` → `id`
  - `text` → `text`
  - `user.screen_name` → `author`
  - `user.name` → `author_name`
  - `created_at` → `created_at`
  - `favorite_count` → `likes`
  - `conversation_count` → `replies`
  - `retweets` set to `0` (field not provided by actor)
- URL generation now consistently builds `https://x.com/{screen_name}/status/{id_str}` when missing
- Updated docs/config metadata to reference `quacker~twitter-scraper`

## [1.0.0] - 2026-02-11

### Added

- **Tweet Search** - Search tweets by keywords, hashtags, mentions
- **User Profiles** - Get tweets from a specific user
- **Tweet Details** - Get a specific tweet + replies by URL
- **Local Caching** - Save API costs with local file cache
  - Search results: 1 hour TTL
  - User profiles: 24 hours TTL
  - Specific tweets: 24 hours TTL
- **Cache Management**
  - `--cache-stats` - View cache statistics
  - `--clear-cache` - Delete all cached results
  - `--no-cache` - Bypass cache for fresh fetch
- **Output Formats**
  - `--format json` - Structured JSON output
  - `--format summary` - Human-readable summary
- **Safety Features**
  - Bearer token auth (not in query string)
  - Query sanitization (control chars, length limits)
  - No hardcoded paths or personal data

### Technical

- Uses `apidojo~tweet-scraper` (Tweet Scraper V2) actor
- Supports `--max-results` to limit results (default 20)
- Supports `--output` to save to file
