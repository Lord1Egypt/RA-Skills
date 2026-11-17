# Find Trending Content

Check today's Topic Trends (what people are talking about right now, by region: shows, celebrities, memes, sports, news; each topic has a `category`) and explore trending videos. For the video formats creators are copying, use Content Trends instead (see `find-a-format-to-copy.md`).

## User Prompt

"What's trending on social media today?"

## Agent Steps

1. Get today's Topic Trends (`/v1/topic-trends/today`; one daily list of 15 to 20 topics):
```bash
curl "https://api.virlo.ai/v1/topic-trends/today" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
If the user asks about a specific country, pass `region` (`us`, `gb`, `au`, `sg`; default is `global`, the worldwide feed):
```bash
curl "https://api.virlo.ai/v1/topic-trends/today?region=gb" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
`GET /v1/topic-trends/regions` (free) lists the currently available region codes: more are added over time.

If the user asks what's *emerging* or *about to take off* (rather than the full daily list), use the momentum-ranked emerging endpoint ($0.25): composable with `region`:
```bash
curl "https://api.virlo.ai/v1/topic-trends/emerging?region=gb&limit=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
It returns only `new`/`rising` trends sorted by momentum heat (each with `status`, `momentum_score`, `views_per_hour`): ideal for "what's emerging in the UK right now". It costs $0.25 per call and is rate-limited per plan.

If the user wants pop culture without politics, add `exclude_category=politics,news`:
```bash
curl "https://api.virlo.ai/v1/topic-trends/today?region=au&exclude_category=politics,news" \n  -H "Authorization: Bearer $VIRLO_API_KEY"
```

2. Present topic names, categories and descriptions to the user.

3. Get the most-viewed videos published in the last 48 hours ($0.25 whatever the limit, max 100):
```bash
curl "https://api.virlo.ai/v1/videos/digest?limit=10" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

4. Show top hashtags:
```bash
curl "https://api.virlo.ai/v1/hashtags?start_date={today_minus_7}&end_date={today}&limit=10&order_by=views&sort=desc" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

5. If the user is interested in a specific trend, offer to run a Full Niche Analysis: a one-shot agent (`POST /v1/agents` with `is_recurring: false`) seeded with the trend keywords.

## Total Cost

$0.25 for Topic Trends + $0.25 for videos + $0.05 for hashtags = $0.55 total.
