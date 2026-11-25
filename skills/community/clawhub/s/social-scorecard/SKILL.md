---
name: social-scorecard
description: Score and compare 2 to 6 Facebook pages and Instagram accounts side by side - audience size, posting rhythm, engagement per post and per 1,000 followers, format mix and best posts - from public data via SocialAPIs. Use when the user wants to benchmark a brand against competitors, see how their page is doing, compare accounts before a partnership, or produce a monthly social performance table.
---

# Social scorecard

A fair, numbers-first comparison of social accounts: same time window, same metrics, normalized for audience size so a 5k-follower shop can be compared with a 2M-follower brand.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_page` and `instagram_profile`.

## Ask first (only what's missing)

- The accounts: Facebook page URLs and/or Instagram usernames (2 to 6). Mark which one is the user's.
- Window: default last 30 days (or the last 20 posts for accounts that post rarely).

## Budget

Per Facebook page: 1 (details) + ceil(posts / 3) for posts (limit 9 = 3 credits per call), about 6 to 10 credits for 30 days. Per Instagram account: 1 (details) + 1 (user id) + 1 to 3 (posts) + 1 to 2 (reels), about 5 to 7. Five accounts is roughly 30 to 45 credits; say so before starting.

## Steps

### Facebook pages
1. `/facebook/pages/details?link=…`: name, category, `followers_count`. Add `exact_followers_count=true` (5 credits) only if the user needs exact numbers for small differences.
2. `/facebook/pages/posts?link=…&limit=9&after_time=<window start ISO>`, follow `end_cursor` to the window start.
3. Per post: reactions (`reactions.total_reaction_count`), comments and shares (`details.comments_count`, `details.share_count`, strings), format (`values.is_media`: Photo, Video, none = text/link).
4. For reels views, `/facebook/pages/reels?link=…` (1 credit per page of results).

### Instagram accounts
1. `/instagram/profile/details?username=…`: followers, posts count, verified.
2. `/instagram/profile/posts?username=…`, follow `end_cursor` to the window start: likes, comments, type (photo, video, carousel).
3. `/instagram/user/id?username=…` then `/instagram/profile/reels?user_id=<long user_id>` for play counts (use the long `user_id`, not `pk`).

### Metrics (per account, same window)
- **Posts per week**
- **Median engagement per post** (reactions/likes + comments + shares). Use the median: one viral post shouldn't decide the table.
- **Engagement per 1,000 followers** = median engagement / followers × 1000. This is the fair comparison column.
- **Format mix** (% photo / video or reel / carousel / text) and **median engagement by format**
- **Reel median plays** (where available)
- **Best post** in the window (highest engagement), with link

## Output

```
## Scorecard, <window>

| Account | Platform | Followers | Posts/wk | Median eng./post | Per 1k followers | Top format | Reel median plays |
|---|---|---|---|---|---|---|---|

### Takeaways
- Who wins on engagement per 1k, and what they do differently (format, rhythm)
- Where the user's account stands; the 2 or 3 changes most likely to help, each tied to evidence in the table

### Best posts
| Account | Post (first line) | Engagement | Format | Link |
```

Facebook and Instagram numbers aren't directly comparable (likes vs reactions, different reach); compare within a platform, and say it when the table mixes both.

## Limits

- Public counts only: no reach, saves, or click data.
- Follower counts on Facebook are rounded ("2.1M") unless `exact_followers_count=true`.
- Short windows on rarely-posting accounts give noisy numbers; switch to "last 20 posts" and say so.
