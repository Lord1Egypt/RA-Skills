# Workflow: Pull analytics for recent posts

Use this when the user wants engagement metrics — likes, comments, shares, impressions — across their published posts.

## Step 1: List recently published posts

```bash
curl -sS "https://viralnote.app/api/v1/posts?status=published&limit=20" \
  -H "x-api-key: $VIRALNOTE_API_KEY"
```

Each post in the response has metadata: `id`, `caption`, `platforms`, `publishedAt`, and per-platform results in `platformResults[]` (each containing `platform`, `externalId`, `url`, and `metrics` if collected).

## Step 2: Inspect metrics per platform

The shape of `metrics` varies by platform but typically includes:

```json
{
  "impressions": 12345,
  "reach": 9876,
  "likes": 200,
  "comments": 14,
  "shares": 7,
  "engagementRate": 0.018,
  "fetchedAt": "2026-05-18T02:00:00.000Z"
}
```

If a post's `platformResults[i].metrics` is `null` or absent, metrics haven't been collected yet (collection runs periodically). Mention this to the user — don't pretend the post got zero engagement.

## Step 3: Aggregate intelligently

If the user asks "what's been working" or "best posts," sort by a meaningful metric (often `engagementRate`, which normalizes for reach). Report 3-5 top posts with the actual numbers — not just titles. Cite the platform alongside (a top X post and a top Instagram post are different beasts).

## Step 4: Useful queries

- "Best posts on Instagram in the last 30 days":
  ```bash
  curl -sS "https://viralnote.app/api/v1/posts?status=published&platforms=instagram&since=2026-04-18" \
    -H "x-api-key: $VIRALNOTE_API_KEY"
  ```
- "Recent failures":
  ```bash
  curl -sS "https://viralnote.app/api/v1/posts?status=failed&limit=20" \
    -H "x-api-key: $VIRALNOTE_API_KEY"
  ```
  The `error` field on each post explains what went wrong (token expired, platform rejected, etc.).

## What this skill does NOT do

- Doesn't fetch metrics live from social platforms. ViralNote's backend pulls metrics on its own schedule; you read what's already collected.
- Doesn't compare to other accounts or industry benchmarks. The API only knows about this user's posts.
- Doesn't post recommendations. If asked "what should I post next," that's an LLM judgment call from the data — be honest that you're inferring.
