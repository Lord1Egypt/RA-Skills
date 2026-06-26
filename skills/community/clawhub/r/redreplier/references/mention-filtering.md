# RedReplier Mention Filtering

How to slice the mention inbox with `GET /mentions` (and `GET /mentions/count`). Base URL: `https://ai.redreplier.com/ai-app/api/v1`. All params are query-string; repeat a key to pass an array.

## Default behavior (no params)

`GET /mentions` with no filters applies two implicit filters:

1. **Excludes `REJECTED`** mentions.
2. **Hides anything scoring below 30** (i.e. only `relevanceScore >= 30` OR not-yet-scored mentions are shown).

So the default view is "unreviewed/approved mentions that are at least moderately relevant" — the working lead inbox. To see the full firehose, add `includeLowRelevance=true` and/or an explicit `statuses` filter.

## Relevance score buckets

`relevanceScore` is an AI score from 0-100. `scoreBuckets` maps to ranges:

| Bucket | Range |
| --- | --- |
| `VERY_LOW` | `< 10` |
| `LOW` | `10 – 29` |
| `MEDIUM` | `30 – 49` |
| `HIGH` | `50 – 74` |
| `VERY_HIGH` | `>= 75` |

`scoreBuckets` is OR-combined. Note `LOW` and `VERY_LOW` are below the 30 default cutoff, so to actually see them you must also pass `includeLowRelevance=true` (or rely on the bucket filter, which overrides the cutoff when buckets are supplied).

```
# Best leads only
?scoreBuckets=VERY_HIGH&scoreBuckets=HIGH

# Everything low-quality (for auditing noise) — needs includeLowRelevance
?scoreBuckets=LOW&scoreBuckets=VERY_LOW&includeLowRelevance=true
```

## Status

`statuses` (OR-combined): `NEW`, `APPROVED`, `REJECTED`.

- Omitted → defaults to "not REJECTED".
- Pass an explicit list to override (e.g. include `REJECTED` to audit what was dismissed).

```
?statuses=NEW                 # unreviewed inbox
?statuses=APPROVED            # confirmed leads
?statuses=NEW&statuses=APPROVED
```

## Source

`sources` (OR-combined): `REDDIT_POST`, `REDDIT_COMMENT`, `TWITTER` (X), `BLUESKY`, `HACKERNEWS`.

```
?sources=REDDIT_POST                     # Reddit top-level posts only
?sources=REDDIT_COMMENT                  # Reddit comments only
?sources=TWITTER&sources=BLUESKY         # X and Bluesky posts
?sources=HACKERNEWS                      # Hacker News stories/comments
```

The `subreddit` field on a mention is only set for `REDDIT_POST` / `REDDIT_COMMENT`; it is `null` for X, Bluesky, and Hacker News.

## Keyword

`keywords` (OR-combined, case-insensitive exact match on the matched keyword): restrict to mentions matched by specific keywords.

```
?keywords=my%20product&keywords=competitor
```

## Website

`websiteId` (single UUID): restrict to one monitored website.

## Time window

`from` / `to` are ISO 8601 datetimes filtering on **ingestion time** (`ingestedAt`), not publish time.

```
?from=2026-05-23T00:00:00Z&to=2026-05-30T00:00:00Z
```

## Sort & pagination

- `sort`: `RELEVANCE` (default — highest score first, then most recent) or `RECENT` (newest first). Ties break on a stable internal key so offset pagination stays consistent.
- `limit`: 1-500 (default 50).
- `offset`: ≥ 0 (default 0).

`GET /mentions` returns `{ mentions, total, limit, offset }` — `total` is the full count for the filter, so paginate with `offset += limit` until `offset >= total`.

## Recipes

```
# Today's best unreviewed leads for one site, newest first
?websiteId=WID&statuses=NEW&scoreBuckets=HIGH&scoreBuckets=VERY_HIGH&sort=RECENT

# Count of unreviewed leads worth a human look
/mentions/count?statuses=NEW&scoreBuckets=HIGH&scoreBuckets=VERY_HIGH

# Comment-only mentions of a specific keyword in the last 24h
?sources=REDDIT_COMMENT&keywords=my%20product&from=2026-05-29T00:00:00Z

# Mentions from X, Bluesky, and Hacker News only (skip Reddit)
?sources=TWITTER&sources=BLUESKY&sources=HACKERNEWS

# Full firehose including noise (auditing the scorer)
?includeLowRelevance=true&statuses=NEW&statuses=APPROVED&statuses=REJECTED&limit=200
```
