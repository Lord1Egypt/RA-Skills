---
name: social-analytics-report
description: Report on social media performance from Auto Poster AI. Shows top and weak posts, engagement totals, follower growth and what to post next. Use when the user asks how their posts, accounts or a platform are doing, or wants a weekly or monthly social report.
---

# Social analytics report

Uses `autoposter_get_analytics`, `autoposter_list_accounts` and `autoposter_list_posts`.

## Workflow

1. **Set the range.** Dates are `YYYY-MM-DD`, at most 90 days. Default is the last 14 days. If the user said "last month", resolve it to dates and state them.
2. **Account level.** `autoposter_get_analytics` with `level: "accounts"` and `from`/`to`. Gives followers, reach, impressions and engagement per account, with a daily series.
3. **Post level.** `level: "posts"` (default). Use `platform` or `accountIds` to narrow, `limit` up to 50. Totals cover all matches even when the list is cut.
4. **One post.** Pass `postId` from `autoposter_list_posts`.
5. **Write the report:**
   - Headline numbers and change over the period.
   - Top 3 and bottom 3 posts with the metric that explains why.
   - One pattern (format, time, topic, platform) the data supports.
   - Two or three concrete next posts to try.

## Rules

- Data syncs periodically. Posts from the last day or so may show no metrics. Say so, do not treat them as failures.
- Compare like with like: same platform, similar length of time live.
- Small numbers are noise. If a post has a handful of impressions, do not draw conclusions from it.
- Only state what the returned data shows. If a metric is missing for a platform, say it is not available.
- Offer to schedule the suggested posts with `schedule-social-posts`; do not schedule unasked.
