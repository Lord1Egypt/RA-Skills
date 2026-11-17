# Set Up Niche Monitoring

Create an automated recurring search for a topic. Uses the unified `/v1/agents` API in recurring mode (`is_recurring: true`).

## User Prompt

"Set up weekly monitoring for TikTok Shop strategies"

## Agent Steps

1. Create a recurring agent (`POST /v1/agents` with `is_recurring: true`). Aim for 7-12 specific keywords; `POST /v1/agents/suggest-keywords` (free) drafts them from the intent:
```bash
curl -X POST https://api.virlo.ai/v1/agents \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "is_recurring": true,
    "intent": "track what is working for TikTok Shop sellers week over week",
    "name": "TikTok Shop Strategies",
    "keywords": ["TikTok Shop success", "TikTok Shop strategies", "TikTok Shop tips", "TikTok Shop sellers", "TikTok Shop marketing"],
    "platforms": ["youtube", "tiktok", "instagram"],
    "cadence": "weekly",
    "meta_ads_enabled": true
  }'
```

2. Confirm the agent was created and share the next run time. Creating a recurring agent is **free**; you're billed $0.50 per run, starting with the first run, which begins right away.

3. Poll every 30-60s until `finalized: true` (usually under 20 min; half of runs collect in under ~8), then check results:
```bash
curl "https://api.virlo.ai/v1/agents/{id}/videos?limit=20&order_by=views&sort=desc" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

4. Nothing to approve: autopilot is on by default. After each run it rewords searches and adds keywords to keep finding new videos, and it never removes the keywords you set or adds charges. To see what it changed and why, read the activity log:
```bash
curl "https://api.virlo.ai/v1/agents/{id}/activity" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
If the user wants the configuration frozen exactly as set, turn autopilot off (free):
```bash
curl -X PUT "https://api.virlo.ai/v1/agents/{id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "autopilot": false }'
```

## Total Cost

Free to create. Each recurring run is billed like a search ($0.50/run, or +$1.00/run with `data_intelligence_enabled`). Retrieval of results is always free.

> **Legacy note:** `POST /v1/comet` still responds but is deprecated; don't build on it. An existing `comet_id` is a valid agent id.
