---
name: threads-research
description: Researches public Threads (Meta) profiles, posts, replies, and search results via the Crawlora API, returning clean JSON. Use when the user wants a Threads profile's stats, a post's content/replies, a profile's recent posts, or a keyword search on Threads — instead of scraping the app.
---

# Threads research

Look up public Threads profiles, posts, and replies, and run keyword search
— all as normalized JSON from the Crawlora API, no app scraping or
unofficial client libraries.

## When to use this skill

- "What's <handle>'s profile / follower count on Threads?"
- "Pull this Threads post's text and replies."
- "What has <handle> posted recently on Threads?"
- "Search Threads for posts about <topic>."
- Competitor social-listening or brand-mention monitoring on Threads.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Profile** — `/threads/profile/{username}` for public profile metadata
   (bio, counts).
2. **Profile posts** — `/threads/profile/{username}/posts` for a profile's
   public posts, paginated via an opaque `cursor`.
3. **One post** — `/threads/post/{username}/{code}` for a single post's
   text, author, canonical URL, and preview image.
4. **Post replies** — `/threads/post/{username}/{code}/replies` for the
   public replies to that post.
5. **Search** — `/threads/search` for the public first page of Threads
   search results for a query.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Profile + posts:
scripts/crawlora.sh /threads/profile/zuck | jq '.'
scripts/crawlora.sh /threads/profile/zuck/posts | jq '.'

# Post + replies:
scripts/crawlora.sh /threads/post/zuck/C1abc2DEfGh | jq '.'
scripts/crawlora.sh /threads/post/zuck/C1abc2DEfGh/replies | jq '.'

# Search:
scripts/crawlora.sh /threads/search q="web scraping" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Threads
endpoint this skill uses.

## Examples

- **Profile snapshot:** `/threads/profile/{username}` for bio and follower
  counts, then `/threads/profile/{username}/posts` to see recent activity.
- **Post deep-dive:** `/threads/post/{username}/{code}` for a specific
  post's text, then `/threads/post/{username}/{code}/replies` to read what
  people are saying about it.
- **Keyword sweep:** `/threads/search` for a brand or topic name to gauge
  how much public conversation is happening on Threads right now.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public profiles/posts; no login, no private content.
  Respect Threads' terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Search has no continuation cursor** — `/threads/search` returns only the
  logged-out first page of results; there's no way to page deeper.
- **Reply pagination is opaque and sometimes absent** — `/threads/post/{username}/{code}/replies`
  will flag when Threads reports more replies exist but can withhold a
  usable cursor to fetch them.
- **Profile posts paginate via cursor** — pass the `cursor` from the
  previous `/threads/profile/{username}/posts` response to walk beyond the
  first page.
