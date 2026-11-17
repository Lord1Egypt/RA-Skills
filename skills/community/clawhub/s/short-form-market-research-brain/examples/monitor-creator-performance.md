# Monitor Creator Performance

Track a creator over time, collect metric snapshots, and get AI analysis reports. Each tracking cycle collects metrics AND generates an AI report as one bundled operation.

## User Prompt

"Start tracking @khaby.lame on TikTok every 12 hours"

## Agent Steps

1. Start tracking the creator (initial cycle starts immediately and usually finishes in 1-2 minutes; the $0.25 is refunded if the creator can't be found). Add `collection_depth` to also back-fill older posts (and per-post sound) right away: `standard` (up to 50 videos, +$0.50), `deep` (up to 200, +$1.00), or `full` (up to 500, +$2.00). It is refunded if the collection finds no posts or fails.
```bash
curl -X POST https://api.virlo.ai/v1/tracking/creators \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "tiktok",
    "handle": "khaby.lame",
    "scrape_cadence": "twelve_hours",
    "collection_depth": "deep"
  }'
```

2. Check the creator's current data. The main scrape finishes fast, but secondary jobs (AI report, audience snapshot) may still be running: rely on `finalized: true`, not `status`. While `finalized` is `false`, `pending_jobs[]` lists each in-flight job with its `poll_url` and `retry_after_seconds`; any `null` fields just mean "not computed yet," not "no data":
```bash
curl https://api.virlo.ai/v1/tracking/creators/{id} \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

3. After a few cycles, review growth snapshots. You get the most recent `limit` snapshots (default 30) in the date range, listed oldest first:
```bash
curl "https://api.virlo.ai/v1/tracking/creators/{id}/snapshots?start_date={today_minus_30}&limit=365" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

4. Read the latest AI report (generated automatically on every cycle):
```bash
curl https://api.virlo.ai/v1/tracking/creators/{id}/report \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

5. Enumerate the creator's collected posts with per-post metrics, outlier flags, and the per-post `sound` object. `sound.external_id` is the platform-native sound id (TikTok music/clip id, Instagram audio id; `null` for YouTube) a music catalog matches against: filter or group posts by it to see which tracks a creator uses:
```bash
curl "https://api.virlo.ai/v1/tracking/creators/{id}/posts?sort=views_desc&limit=50" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

6. Deepen the post history on demand at any time: `standard` (the default, up to 50 videos), `deep` (up to 200), or `full` (up to 500). It populates per-post sound for TikTok/Instagram always, YouTube on deep/full. If the creator's last tracking cycle failed, this returns 409 "Tracking unhealthy" before charging; fix the handle or resume tracking first, or add `"force": true` when the failure was transient:
```bash
curl -X POST https://api.virlo.ai/v1/tracking/creators/{id}/posts/collect \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "depth": "deep" }'
```

7. Adjust cadence or pause tracking:
```bash
curl -X PATCH https://api.virlo.ai/v1/tracking/creators/{id} \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "scrape_cadence": "daily" }'
```

## Total Cost

$0.25 per tracking cycle, including the initial cycle when you start tracking. Later cycles are charged only when they succeed. An optional initial `collection_depth` adds $0.50/$1.00/$2.00 (standard/deep/full), and on-demand `posts/collect` costs the same by depth; both are charged when the request is accepted and refunded in full if the collection finds no posts or fails. All GET, PATCH, and DELETE endpoints are free.
