# Find a Content Trend to Copy

Find repeatable video formats creators are copying right now, pick the ones that suit the user, and turn one into a plan.

## User Prompt

"I run a skincare brand. What video format should we copy on TikTok this week?"

## Agent Steps

1. List live Content Trends that suit a consumer brand on TikTok ($0.25). Content Trends (`/v1/content-trends`) are video formats creators copy; Topic Trends (`/v1/topic-trends`) are subjects people talk about, so use `/v1/content-trends` here:
```bash
curl "https://api.virlo.ai/v1/content-trends?client_fit=consumer_brand&platform=tiktok&brand_safety=safe&limit=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
The default sort puts live trends first, with the most creators in the last 7 days on top. Each item has `name`, `recipe`, `lifecycle`, `creators_7d`, `creators_prev_7d`, `client_fit.consumer_brand` (`fit` and `how`) and 3 `examples`. Unknown query params return a 400 (not charged).

If the user wants to get in early, narrow to young formats:
```bash
curl "https://api.virlo.ai/v1/content-trends?lifecycle=new,rising&client_fit=consumer_brand&platform=tiktok&limit=20" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

2. Shortlist 3-5 content trends. Prefer `lifecycle` `new` or `rising`, a `creators_7d` that is clearly above `creators_prev_7d`, and `client_fit.consumer_brand.fit` of `yes`. Skip `fading` ones unless the user asks for them. Present each with its `recipe` and the `how` line for a consumer brand.

3. When the user picks one, open it for all examples and the 30-day series ($0.05):
```bash
curl "https://api.virlo.ai/v1/content-trends/{id}" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```
If it returns 404 with `merged_into` in the error body, the trend was merged into another one: request that id instead.

4. Explain the format: `constant_part` is what stays the same, `swapped_part` is what each creator swaps in. Link 2-3 examples with `verified_fit: true` (they pass the recipe check) and `is_paid: false` (paid examples are ads, listed last, and prove nothing about organic spread). When reading `series`, ignore dips on days marked `partial: true`: the last 7 days are still being counted.

5. Draft the brand's own version: keep `constant_part` and fill `swapped_part` with the user's product. If they want opening lines too, pull trending skincare hooks ($0.25):
```bash
curl "https://api.virlo.ai/v1/hooks/trending?platform=tiktok&category=beauty&days=7&limit=10" \
  -H "Authorization: Bearer $VIRLO_API_KEY"
```

## Total Cost

$0.25 for the list + $0.05 per content trend opened (+ $0.25 if you pull hooks). One list and one trend = $0.30.
