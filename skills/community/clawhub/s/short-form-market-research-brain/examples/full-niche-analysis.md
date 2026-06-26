# Full Niche Analysis

Search for a topic across all platforms, get an AI intelligence report, explore videos and creators.

## User Prompt

"Research the jeep wrangler modification niche across all platforms"

## Agent Steps

1. Queue Orbit search:
```bash
curl -X POST https://api.virlo.ai/v1/orbit \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jeep Wrangler Mods Research",
    "keywords": ["jeep wrangler mods", "jeep wrangler accessories", "jeep upgrades"],
    "time_period": "this_month",
    "platforms": ["youtube", "tiktok", "instagram"],
    "enable_meta_ads": true,
    "min_views": 1000
  }'
```

2. Poll every 30 seconds until status is "completed":
```bash
curl https://api.virlo.ai/v1/orbit/{orbit_id} \
  -H "Authorization: Bearer {api_key}"
```

3. Get the AI intelligence report:
```bash
curl "https://api.virlo.ai/v1/orbit/{orbit_id}/analysis/latest" \
  -H "Authorization: Bearer {api_key}"
```

4. Get top videos:
```bash
curl "https://api.virlo.ai/v1/orbit/{orbit_id}/videos?limit=20&order_by=views&sort=desc" \
  -H "Authorization: Bearer {api_key}"
```

5. Find rising creators:
```bash
curl "https://api.virlo.ai/v1/orbit/{orbit_id}/creators/outliers?limit=10&order_by=outlier_ratio&sort=desc" \
  -H "Authorization: Bearer {api_key}"
```

## Total Cost

$0.50 for the Orbit search. All retrieval is free.
