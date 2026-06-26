# Set Up Niche Monitoring

Create automated recurring searches for a topic.

## User Prompt

"Set up weekly monitoring for TikTok Shop strategies"

## Agent Steps

1. Create Comet configuration:
```bash
curl -X POST https://api.virlo.ai/v1/comet \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TikTok Shop Strategies",
    "keywords": ["TikTok Shop success", "TikTok Shop strategies", "TikTok Shop tips", "TikTok Shop sellers", "TikTok Shop marketing"],
    "platforms": ["youtube", "tiktok", "instagram"],
    "cadence": "weekly",
    "time_range": "this_month",
    "min_views": 0,
    "is_active": true,
    "meta_ads_enabled": true
  }'
```

2. Confirm the configuration was created and share the next_run_at time.

3. To check results after a run:
```bash
curl "https://api.virlo.ai/v1/comet/{comet_id}/videos?limit=20&order_by=views&sort=desc" \
  -H "Authorization: Bearer {api_key}"
```

## Total Cost

$0.50 to create. Retrieval of results is always free.
