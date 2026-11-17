# Analytics & Feedback Loop

## Performance Tracking

### PosteAhora Analytics API

PosteAhora returns per-post analytics directly. Each published post's remote platform ID (e.g. its TikTok video ID) is stored internally, so you never have to match videos by hand — just call the analytics endpoint and read the numbers per post.

**Analytics** (per-post views, likes, comments, shares, reach — plus summary totals):
```
GET https://api.posteahora.com/functions/v1/api/analytics?period=7d&platform=tiktok
Authorization: Bearer pah_live_...
```

Query params:
- `period` — `7d`, `30d`, `90d`, or `all`
- `platform` — optional filter (`tiktok`, `instagram`, `youtube`, etc.); omit for all connected accounts

Response:
```json
{
  "period": "7d",
  "summary": {
    "totals": { "views": 20000, "likes": 6709, "comments": 148, "shares": 119, "reach": 18400 },
    "byPlatform": { "tiktok": { "views": 20000, "likes": 6709, "comments": 148, "shares": 119 } }
  },
  "posts": [
    {
      "postId": "post-abc",
      "caption": "boyfriend said flat looks like catalogue",
      "platform": "tiktok",
      "views": 15000,
      "likes": 450,
      "comments": 23,
      "shares": 89,
      "reach": 13800
    }
  ]
}
```

The `posts` array gives you exactly what you need for the feedback loop: one row per post with its view/like/comment/share counts. No release-ID matching, no reconciliation step — PosteAhora already knows which remote video belongs to which post.

**List posts** (to see what has been published or is scheduled):
```
GET https://api.posteahora.com/functions/v1/api/posts?status=published&limit=50
Authorization: Bearer pah_live_...
```

CLI equivalents (`npm i -g @posteahora/cli`):
```
posteahora analytics --period 7d --platform tiktok
posteahora posts --status published --limit 50
```

Note: per-post metrics can take a few hours to populate after a post goes live (platforms like TikTok update engagement counts on a delay). If a freshly published post shows zeros, re-pull `/analytics` later in the day rather than treating it as a failure.

### RevenueCat Integration (Optional)

If the user has RevenueCat, track conversions from TikTok:
- Downloads → Trial starts → Paid conversions
- UTM parameters in App Store link
- Compare conversion spikes with post timing

## The Feedback Loop

### After Every Post (24h)
Record in `hook-performance.json`:
```json
{
  "posts": [
    {
      "date": "2026-02-15",
      "hook": "boyfriend said flat looks like catalogue",
      "hookCategory": "person-conflict-ai",
      "views": 15000,
      "likes": 450,
      "comments": 23,
      "saves": 89,
      "postId": "posteahora-post-id",
      "appCategory": "home"
    }
  ]
}
```

### Weekly Review
1. Sort posts by views
2. Identify top 3 hooks → create variations
3. Identify bottom 3 hooks → drop or radically change
4. Check if any hook CATEGORY consistently wins
5. Update prompt templates with learnings

### Decision Rules

| Views | Action |
|-------|--------|
| 50K+ | DOUBLE DOWN — make 3 variations immediately |
| 10K-50K | Good — keep in rotation, test tweaks |
| 1K-10K | Okay — try 1 more variation before dropping |
| <1K (twice) | DROP — radically different approach needed |

### What to Vary When Iterating
- **Same hook, different person:** "landlord" → "mum" → "boyfriend"
- **Same structure, different room/feature:** bedroom → kitchen → bathroom
- **Same images, different text:** proven images can be reused with new hooks
- **Same hook, different time:** morning vs evening posting

## Conversion Tracking

### Funnel
```
Views → Profile Visits → Link Clicks → App Store → Download → Trial → Paid
```

### Benchmarks
- 1% conversion (views → download) = average
- 1.5-3% = good
- 3%+ = great

### Attribution Tips
- Track download spikes within 24h of viral post
- Use unique UTM links per campaign if possible
- RevenueCat `$attribution` for source tracking
- Compare weekly MRR growth with weekly view totals

## Daily Analytics Cron

Set up a cron job to run every morning before the first post (e.g. 7:00 AM user's timezone):

```
Task: node scripts/daily-report.js --config tiktok-marketing/config.json --days 3
Output: tiktok-marketing/reports/YYYY-MM-DD.md
```

The daily report:
1. Fetches per-post analytics from PosteAhora (`GET /analytics?period=7d`) covering the last 3 days of posts
2. Reads each post's views, likes, comments, shares, and reach straight from the `posts` array
3. If RevenueCat is connected, pulls conversion events (trials, purchases) in the same window
4. Cross-references: maps conversion timestamps to post publish times (24-72h attribution window)
5. Applies the diagnostic framework:
   - High views + High conversions → SCALE (make variations)
   - High views + Low conversions → FIX CTA (hook works, downstream is broken)
   - Low views + High conversions → FIX HOOKS (content converts, needs more eyeballs)
   - Low views + Low conversions → FULL RESET (try radically different approach)
6. Suggests 3-5 new hooks based on what's working
7. Updates `hook-performance.json` with latest data
8. Messages the user with a summary

### Why 3 Days?
- TikTok posts peak at 24-48 hours (not instant like Twitter)
- Conversion attribution takes up to 72 hours (user sees post → downloads → trials → pays)
- 3-day window captures the full lifecycle of each post

### RevenueCat Integration
When connected, the daily report pulls:
- **Trial starts** within 24-72h of each post → maps to which hooks drive installs
- **Paid conversions** (initial purchase + trial converted) → maps to which CTAs convert
- **Revenue** per period → tracks actual MRR impact of content

This is the difference between "this post got 50K views" (vanity) and "this post generated $47 in new subscriptions" (intelligence).
