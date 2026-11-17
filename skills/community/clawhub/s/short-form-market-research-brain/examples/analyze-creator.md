# Creator Deep Dive

Analyze a specific creator's profile, stats, and content performance.

## User Prompt

"Analyze the TikTok creator @hatimsshorts"

## Agent Steps

1. Start creator lookup:
```bash
curl "https://api.virlo.ai/v1/satellite/creator/tiktok/hatimsshorts?include=videos,outliers&max_videos=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

2. Poll every 10-15 seconds until completed (usually 15-40 seconds). The result is also saved as a run whose `run_id` equals the `job_id`, so `GET /v1/satellite/runs/{job_id}` re-reads it free later:
```bash
curl "https://api.virlo.ai/v1/satellite/creator/status/{job_id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

3. Present profile stats: followers, engagement rate, posting frequency.

4. Highlight outlier videos with high outlier_ratio: these are the creator's breakout hits.

5. Optionally analyze the top outlier video:
```bash
curl -X POST https://api.virlo.ai/v1/satellite/video-outlier \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@hatimsshorts/video/7618009747375017219", "platform": "tiktok"}'
```

## Total Cost

$0.50 for creator lookup + $0.50 per video outlier analysis. A creator lookup that fails (for example, a handle that doesn't exist) is refunded in full; a video outlier check is not.
