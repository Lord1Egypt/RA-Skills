# Full Niche Analysis

Search for a topic across all platforms, get an AI intelligence report, explore videos and creators. Uses the unified `/v1/agents` API in one-shot mode (`is_recurring: false`).

## User Prompt

"Research the jeep wrangler modification niche across all platforms"

## Agent Steps

1. Draft keywords from a one-sentence intent (free, creates nothing). It returns 7 to 12 keywords plus `exclude_keywords`; drop any exclude word that belongs to the niche itself:
```bash
curl -X POST https://api.virlo.ai/v1/agents/suggest-keywords \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "intent": "Find what content and mods win in the jeep wrangler niche, not dealership ads" }'
```

2. Create a one-time agent (`POST /v1/agents` with `is_recurring: false`) with the SAME intent and the suggested keywords ($0.50, charged at creation):
```bash
curl -X POST https://api.virlo.ai/v1/agents \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "is_recurring": false,
    "intent": "Find what content and mods win in the jeep wrangler niche, not dealership ads",
    "name": "Jeep Wrangler Mods Research",
    "keywords": ["jeep wrangler mods", "jeep wrangler accessories", "jeep wrangler lift kit", "jeep wrangler build", "jeep wrangler off road upgrades", "jeep wrangler interior mods", "jeep wrangler wheels and tires"],
    "platforms": ["youtube", "tiktok", "instagram"],
    "meta_ads_enabled": true
  }'
```

3. Poll every 30-60 seconds until `finalized: true`. Half of runs finish collecting in under ~8 minutes and 9 in 10 within ~20, with the AI report a few minutes later; a broad run with ads can take up to 45 min. Don't loop tightly, never hard-timeout, and treat `partial_failure` as a usable terminal state:
```bash
curl https://api.virlo.ai/v1/agents/{id} \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

4. Get the AI intelligence report:
```bash
curl "https://api.virlo.ai/v1/agents/{id}/analysis/latest" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

5. Get top videos. Apply any view/date filters here at read time (free), since collection is system-managed and broad:
```bash
curl "https://api.virlo.ai/v1/agents/{id}/videos?limit=20&order_by=views&sort=desc&min_views=100000&start_date=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

6. Find rising creators (rank by `weighted_score`, not raw `outlier_ratio`, which is the default sort):
```bash
curl "https://api.virlo.ai/v1/agents/{id}/creators/outliers?limit=10&order_by=weighted_score&sort=desc" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

## Total Cost

$0.50 for the one-shot agent ($1.50 with `data_intelligence_enabled: true`). Keyword suggestions and all retrieval are free.

> **Legacy note:** `POST /v1/orbit` + `GET /v1/orbit/:orbit_id/…` still respond but are deprecated; don't build on them. An existing `orbit_id` is a valid agent id, so the `/v1/agents/:id/…` read paths above work for old searches too.
