---
name: tiktok-creator-research
description: Vet public TikTok creators through live profile, post, video, comment, and user-search endpoints in Crawlora. Use for TikTok-only creator research and shortlists; use influencer-discovery for cross-platform campaign sourcing.
---

# TikTok creator research

Build a current, evidence-backed view of public TikTok creators. Keep identity,
content fit, posting activity, and engagement observations separate from claims
about audience demographics, authenticity, or partnership history.

## Setup and requests

Set `CRAWLORA_API_KEY` to a key from [crawlora.net](https://crawlora.net), then
run the helper bundled with this skill. It sends `x-api-key` to
`https://api.crawlora.net/api/v1`; keep the key in the environment. Read
[`reference/endpoints.md`](reference/endpoints.md) for exact parameters.

```sh
Set `CRAWLORA_API_KEY` in the environment before running the helper.
scripts/crawlora.sh /tiktok/profile/username | jq '.'
scripts/crawlora.sh /tiktok/search/user keyword="running coach" | jq '.'
```

Check both the Crawlora envelope and any nested upstream application code before
using a response. Keep the key only in `CRAWLORA_API_KEY`.

## Workflow

1. Translate the brief into topic, geography, follower range if available,
   creator count, recency window, content-fit criteria, and any disqualifiers.
   Ask only for missing details that would change the shortlist.
2. Discover handles with `/tiktok/search/user` when needed. Search results are
   candidate evidence, not a verified identity or complete creator directory.
3. Refresh each candidate with `/tiktok/profile/{handler}` using the handle
   without `@`. Capture the returned stable user id, `uniqueId`, nickname,
   verification flag, bio, `secUid`, follower count, heart count, and video
   count. A missing/deleted/banned handle is not a successful refresh.
4. For recent or popular content, pass the profile's returned `user.secUid`
   exactly to `/tiktok/posts`. Do not substitute the numeric user id, nickname,
   or handle. Use `sort_type=0` for latest, `1` for popular, or `2` for oldest;
   take a bounded, consistent sample and follow its cursor only as needed.
5. Use `/tiktok/post/{id}` to enrich selected videos. Use `/tiktok/comments`
   with the video's `aweme_id` to sample top-level comments when engagement
   quality matters. Comments are a sample, not a complete sentiment census.
6. Rank candidates only against the user's stated criteria. Deduplicate by
   stable creator or video id and preserve the refresh time for every row.

## Interpretation

- A profile's follower count, likes, views, and verification status are public
  profile signals. None proves audience authenticity, demographic composition,
  location of followers, or conversion potential.
- Bio keywords and a small post sample show candidate content fit, not sustained
  niche ownership. Record sample size and dates before describing cadence or
  consistency.
- If calculating engagement, state the formula, numerator fields, denominator,
  sample size, and dates. Do not replace unavailable metrics with zero or rank
  creators on incomparable windows.
- Public contacts may be unavailable. Do not guess email addresses or hidden
  contact information; do not send outreach unless the user separately asks.
- Link identities across platforms only when a public profile link or other
  direct evidence establishes the match. Similar handles are not proof.
- If a live refresh fails, a candidate can remain in a clearly labeled
  unrefreshed/candidate state; it must not silently become a current observation.

## Output and reliability

Return the requested shortlist with handle, stable creator id, profile URL,
topic-fit evidence, follower/video counts, verification status, refresh time,
sampled video URLs, metric definitions, and unknowns. Include a brief reason for
each inclusion and disclose the discovery and sampling limits.

Use bounded profile, post, detail, and comment calls. On `429`, back off; retry
one transient `5xx` when useful. Stop on `401`/`403` and report the access
limitation. Preserve a partial shortlist when only some refreshes succeed, and
inspect application-level `code` before treating `data` as valid.
