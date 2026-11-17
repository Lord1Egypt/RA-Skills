# Hashtag Deep-Dive

Analyze everything happening around a specific hashtag: posting velocity, top creators, co-occurring tags, sounds, and AI-detected creative trends.

## User Prompt

"What's going on with #glassskin on TikTok right now? Is it still growing?"

## Agent Steps

1. Start the hashtag lookup with trend analysis (the leading `#` is optional: URL-encode it as `%23` or just drop it):
```bash
curl "https://api.virlo.ai/v1/satellite/hashtags/tiktok/glassskin?trend_analysis=true" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
Returns `{ job_id, status }` immediately. Repeating the same lookup within 6 hours returns the cached run for free (`cached: true`).

2. Poll every 10-15 seconds. A default TikTok lookup takes about 15 seconds (about a minute on YouTube or Instagram); trend analysis takes a few minutes (plan for ~5):
```bash
curl "https://api.virlo.ai/v1/satellite/hashtags/status/{job_id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

3. Answer "is it still growing?" from `stats.velocity`: compare `last_4w_avg_videos_per_week` vs `prior_4w_avg_videos_per_week` and read `is_accelerating`.

4. Present `trends[]`: each trend carries `time_windows[]` computed mechanically from real publish dates, plus `resurged` and `momentum`: when each creative pattern fired, whether it came back, and whether the comeback was stronger or weaker.

5. Mine the expansion signals: `stats.related_hashtags` (20 co-occurring tags) as adjacent-tag candidates, `stats.top_sounds` as audio picks proven inside this tag, and `stats.top_creators` for collab or vetting targets.

6. Save the `run_id` from the completed payload (it equals the `job_id`). `GET /v1/satellite/runs/:run_id` re-reads the full result for free, forever, even after the 24-hour status check expires.

## Total Cost

$1.00 with `trend_analysis=true` ($0.50 base + $0.50 trend surcharge). The surcharge is refunded when no trends come out, for example when fewer than 10 videos turn up, and a lookup that fails is refunded in full; the result or failed status shows `credits_refunded`. $0.50 for a basic lookup without trends.
