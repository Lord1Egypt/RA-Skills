# Find Trending Content

Check today's trends and explore trending videos.

## User Prompt

"What's trending on social media today?"

## Agent Steps

1. Get today's trends:
```bash
curl "https://api.virlo.ai/v1/trends/digest?limit=10" \
  -H "Authorization: Bearer {api_key}"
```

2. Present trend names and descriptions to the user.

3. Get top viral videos:
```bash
curl "https://api.virlo.ai/v1/videos/digest?limit=10" \
  -H "Authorization: Bearer {api_key}"
```

4. Show top hashtags:
```bash
curl "https://api.virlo.ai/v1/hashtags?start_date={today_minus_7}&end_date={today}&limit=10&order_by=views&sort=desc" \
  -H "Authorization: Bearer {api_key}"
```

5. If the user is interested in a specific trend, offer to run a Full Niche Analysis with Orbit.

## Total Cost

$0.25 for trends + $0.25 for videos + $0.05 for hashtags = $0.55 total.
