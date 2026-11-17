---
name: social-media-research
description: Researches public profiles, posts, trends, and Facebook Marketplace listings across Instagram, TikTok, Threads, Bluesky, X, Pinterest, LinkedIn, Facebook, Reddit, Bilibili, and Patreon through the Crawlora API. It also supports explicitly requested Reddit buying-intent lead discovery. Use for public social listening, or a clearly requested listings/lead search; avoid sensitive targeting.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Social media research

Look up public profiles, posts, and engagement, run keyword/hashtag search,
and track trending topics across eleven social platforms — all as normalized
JSON from the Crawlora API, no app scraping or unofficial client libraries.

## Tool scope and data flow

The optional shell helper is the only command this skill asks to run. It makes
GET requests only to the documented, allowlisted Crawlora routes. When invoked,
it reads `CRAWLORA_API_KEY` and sends it as an `x-api-key` header over HTTPS to
`api.crawlora.net`; it does not send the key to social platforms. It briefly
writes a mode-600 curl config under `TMPDIR` and removes it when the command
exits. It does not inspect other environment variables, enumerate files, install
software, or run with elevated privileges. Search terms, public handles, URLs,
and other requested targets are sent to Crawlora; do not submit confidential
investigations or sensitive personal data.

The Facebook Marketplace route returns public listings, not social posts. The
Reddit leads route ranks public posts for product/service buying intent; use it
only for an explicit lead-discovery request, disclose the post-level scoring,
and do not infer sensitive traits or target people for high-impact decisions.

## When to use this skill

- "What's <handle>'s profile / follower count / recent posts on <platform>?"
- "Pull this post's engagement (likes, comments, shares)."
- "Search <platform> for posts about <topic/hashtag>."
- "What's trending on <platform> right now?"
- Competitor social-listening, influencer research, or brand-mention monitoring.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Pick the platform, then the job:

1. **Profile** — `/instagram/profile/{username}`, `/tiktok/profile/{handler}`,
   `/threads/profile/{username}`, `/bluesky/profile`, `/x/profile/{username}`,
   `/pinterest/user/{username}`, `/linkedin/company/{id}`,
   `/facebook/{page}`, `/reddit/user/{username}/posts`.
2. **Posts / feed** — `/instagram/reels/{id}`, `/tiktok/posts`,
   `/threads/profile/{username}/posts`, `/bluesky/author-feed`,
   `/x/profile/{username}/posts`, `/pinterest/user/{username}/pins`,
   `/reddit/subreddit/{subreddit}/posts`.
3. **One post/pin/pin detail** — `/instagram/post/{id}/{post_id}`,
   `/tiktok/post/{id}`, `/threads/post/{username}/{code}` (+ `/replies`),
   `/bluesky/post-thread`, `/x/post/{id}`, `/pinterest/pin/{id}`,
   `/reddit/post/{id}` (+ `/reddit/comments/{id}`).
4. **Search & discovery** — `/tiktok/search`, `/tiktok/search_hashtag`,
   `/bluesky/search-actors`, `/pinterest/search`, `/reddit/search`,
   `/facebook/marketplace/search` (listings, not social posts), plus Bilibili
   and Patreon's public discovery endpoints listed in the reference.
5. **Trending** — `/tiktok/trending`, `/tiktok/creative-center/hashtags`,
   `/bluesky/trending-topics`, `/reddit/trends`, `/reddit/subreddits/posts`
   (multi-subreddit hot feed).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Profile + posts:
scripts/crawlora.sh /tiktok/profile/nasa | jq '.'
scripts/crawlora.sh /reddit/user/spez/posts | jq '.'

# Search:
scripts/crawlora.sh /tiktok/search keyword="ai agents" | jq '.'
scripts/crawlora.sh /reddit/search q="web scraping" | jq '.'

# Trending:
scripts/crawlora.sh /tiktok/trending | jq '.'
scripts/crawlora.sh /bluesky/trending-topics | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Instagram,
TikTok, Threads, Bluesky, X, Pinterest, LinkedIn, Facebook, Reddit, Bilibili,
and Patreon endpoint this skill uses.

## Examples

- **Competitor social audit:** pull profile + recent posts on each platform
  a competitor is active on, compare follower counts and post cadence.
- **Brand-mention sweep:** `/reddit/search`, `/tiktok/search`, and
  `/pinterest/search` for the same brand/product name, aggregate volume and
  sentiment cues from captions/comments.
- **Influencer vetting:** profile + recent posts to check follower count,
  engagement rate (likes/comments per post), and posting consistency before
  a partnership.
- **Trending-topic scan:** `/tiktok/trending` + `/bluesky/trending-topics` +
  `/reddit/trends` for a same-day cross-platform snapshot.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profiles/posts; no login, no private content.
  Respect each platform's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Coverage varies by platform**: X and Instagram expose a narrower public
  surface (profile + recent posts) than TikTok or Reddit (full search +
  trending); check `reference/endpoints.md` before assuming an endpoint exists.
- List endpoints are cursor- or page-paginated — follow the returned cursor
  to walk beyond the first page.
