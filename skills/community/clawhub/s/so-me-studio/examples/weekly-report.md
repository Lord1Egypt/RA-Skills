# Example — Assemble a weekly performance digest

> **User:** "Give me last week's numbers across all my accounts and pick the top 3 posts."

**Agent's reasoning:**
1. List all connected accounts via `accounts:list`.
2. For each, fetch 7-day platform analytics via `analytics:platform <accountId> --days 7`.
3. List published posts in the last 7 days via `posts:list --status POSTED` filtered by date.
4. For each, fetch `analytics:post <postId>` and rank by an engagement score (likes + 3×comments + 5×shares).
5. Format a digest the user can paste into Slack/Notion.

**Agent execution:**

```bash
# 1. Connected accounts
so-me accounts:list

# 2. Platform metrics per account (loop)
for acct in $(so-me accounts:list | jq -r '.data[].id'); do
  so-me analytics:platform "$acct" --days 7
done

# 3. Posts published in the last 7 days
so-me posts:list --status POSTED --start-date 2026-04-18 --end-date 2026-04-25

# 4. Post-level analytics (loop)
for post in $(so-me posts:list --status POSTED ... | jq -r '.data[].id'); do
  so-me analytics:post "$post"
done
```

**Reply to user:**

> **Week of Apr 18 – Apr 25**
>
> | Account | Platform | Reach | Engagement | Followers Δ |
> |---|---|---|---|---|
> | @yourbrand | Twitter | 24.3k | 5.1% | +127 |
> | yourbrand-page | LinkedIn | 8.9k | 7.3% | +44 |
> | yourbrand-ig | Instagram | 12.1k | 4.0% | +88 |
>
> **Top 3 posts:**
> 1. "Friday launch teaser" (Twitter, p_01H…) — 1.2k likes, 84 RTs, 18 replies
> 2. "Q2 retrospective thread" (LinkedIn, p_02J…) — 612 reactions, 43 comments
> 3. "Behind-the-scenes Reel" (Instagram, p_03K…) — 4.5k views, 312 likes
>
> Want me to schedule a recycle of the top performer for next Tuesday?

## Notes for the agent

- Analytics endpoints are platform-specific. The shorthand `analytics:platform` resolves the right per-platform endpoint based on the account's platform.
- Date filtering on `posts:list` uses ISO 8601 dates without time.
- Don't blindly trust your math — when in doubt, surface raw API numbers and let the user reconcile.
