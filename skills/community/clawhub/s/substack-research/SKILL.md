---
name: substack-research
description: Research Substack publications, writers, public posts, recommendations, categories, and Notes through Crawlora. Use to find newsletters, compare editorial coverage, inspect a publication archive, or sample public discussion and writer networks.
---

# Substack publication and Notes research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Find public newsletters and writers, then inspect bounded samples of their
published work and discussion. Use publication identity separately from writer
identity; one writer may contribute to multiple publications.

## Discover and follow returned identities

- Search publications or users with their respective tools. Publication detail
  requires either `publication` (subdomain/custom domain) or `publication_id`;
  supply one despite the schema marking both individually optional. Posts use a
  publication identifier plus a returned post slug, not a user handle alone.
- Discover categories before category browsing or leaderboards. Category IDs can
  be numeric or `podcast`; keep free/paid leaderboard scope explicit. Category
  pages are zero-based, while publication archives use `offset` and `limit`.
- Fetch publication posts, selected public post content, contributors, and
  recommendations only as relevant. Recommendations require the numeric
  publication ID; a recommendation or user connection does not establish a
  commercial relationship, endorsement of every article, or common ownership.
- Notes tabs return a paired tab ID and type (`base`, `secondary`, `category`).
  Preserve the pair. Follow `next_cursor` for Notes, replies, or restacks;
  small variable pages do not imply pagination has ended.
- User detail/activity/connections and Notes/replies/restacks use their own
  returned identifiers. Preserve which surface produced each engagement metric.

```sh
scripts/crawlora.sh /substack/search query="climate policy"
scripts/crawlora.sh /substack/categories
scripts/crawlora.sh /substack/notes/tabs
# Use a discovered publication and post slug, for example:
# scripts/crawlora.sh /substack/publication publication="$PUBLICATION"
# scripts/crawlora.sh /substack/publication/posts publication="$PUBLICATION" sort=new limit=10
# scripts/crawlora.sh /substack/post publication="$PUBLICATION" slug="$POST_SLUG"
```

## Interpret and deliver

Return a publication/writer shortlist or coverage brief with topic-fit evidence,
public excerpts, URLs, dates, collection time, and sample size. Distinguish a
paid-content preview from the full article and leave unavailable text unknown.
A public feed is a snapshot, not the signed-in user's personalised feed.
Leaderboard positions, follower counts, or reactions are not audited subscriber
revenue or representative opinion. Attribute claims to their authors and separate
coverage observations from inference. Do not subscribe, comment, message writers,
or follow accounts unless the user requests those actions.
