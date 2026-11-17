# Monitor a TikTok Genre / Scene

Stand up a recurring TikTok genre monitor and read its discovery signals: trending sounds, hashtag momentum, rising creators, and genre benchmarks. A "genre" is just a recurring agent (`POST /v1/agents` with `is_recurring: true`) with `platforms: ["tiktok"]` and genre keywords.

## User Prompt

"Track the progressive house scene on TikTok: what sounds and hashtags are blowing up, and which small creators are breaking out?"

## Agent Steps

1. Create the genre monitor. Use 7-12 specific multi-word keywords that all describe the SAME genre (synonyms/sub-scenes); `POST /v1/agents/suggest-keywords` (free) drafts them from the intent. Write multi-word tags as words: a leading `#` is stripped but tags are not split, so `#progressivehouse` searches `progressivehouse`, not `progressive house`.

```bash
curl -X POST https://api.virlo.ai/v1/agents \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "is_recurring": true,
    "intent": "Track the progressive house scene on TikTok: breakout sounds, hashtags, and small creators, not house cleaning or real estate",
    "name": "Progressive House Scene",
    "keywords": ["progressive house", "melodic house", "melodic techno", "afterhours set", "organic house", "progressive house dj set", "melodic house mix"],
    "platforms": ["tiktok"],
    "cadence": "weekly",
    "exclude_keywords": ["mortgage", "renovation", "cleaning"]
  }'
```

2. The first run starts immediately and is billed like every run. Poll every 30-60s until `finalized: true` (usually under 20 min; half of runs collect in under ~8). Don't loop tightly:

```bash
curl "https://api.virlo.ai/v1/agents/{id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

3. Read the discovery signals (all free):

```bash
# Sounds breaking out in the genre right now (momentum, not all-time)
curl "https://api.virlo.ai/v1/agents/{id}/sounds?sort=rising&limit=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"

# Hashtags gaining steam + the creators driving each
curl "https://api.virlo.ai/v1/agents/{id}/hashtags?sort=growth&limit=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"

# Rising creators, filtered to a seeding-friendly follower tier
curl "https://api.virlo.ai/v1/agents/{id}/creators/outliers?order_by=rising&follower_tier=micro" \
  -H "Authorization: Bearer $VIRLO_API_KEY"

# Genre norms: what "good" looks like per follower tier
curl "https://api.virlo.ai/v1/agents/{id}/benchmarks" \
  -H "Authorization: Bearer $VIRLO_API_KEY"

# Adjacent scenes to expand into (exploratory, beta)
curl "https://api.virlo.ai/v1/agents/{id}/affinity" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

4. (Optional) Catch a sound before it peaks across all of TikTok, and resolve a standout sound back to its real artist (for licensing / outreach):

```bash
# Platform-wide breakout sounds (early-momentum detector)
curl "https://api.virlo.ai/v1/sounds/breakout" \
  -H "Authorization: Bearer $VIRLO_API_KEY"

# Resolve a specific sound to its canonical artist
curl -G "https://api.virlo.ai/v1/sounds/{sound_id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY" \
  -d resolve=true
```

5. Summarize: the sound to ride this week, the hashtags heating up, the rising micro-creators to seed/collab with (and how they compare to the genre norm), and confirm the weekly monitor will keep this fresh, tuning its own keywords on autopilot (on by default, never removing the ones you set) as it learns the scene.

## Total Cost

Free to create the monitor; each weekly run is billed like a search ($0.50/run), starting with the first run. Every discovery read above is free. `/v1/sounds/breakout` is $0.25; a sound detail read is $0.05, and `?resolve=true` adds $0.10 only the first time that sound is resolved.

> **Legacy note:** the old `POST /v1/comet` + `/v1/comet/:id/…` reads still respond but are deprecated; don't build on them.
