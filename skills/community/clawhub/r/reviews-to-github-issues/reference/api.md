# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", "next_cursor", … } }`; errors carry `error.hint`.

| MCP tool | REST call |
|---|---|
| `get_app` | `GET /apps/{app}` |
| `get_reviews` | `GET /apps/{app}/reviews?country=us&rating=1-3&since=YYYY-MM-DD&limit=100` (next page: `&cursor=<meta.next_cursor>`) |
| `get_job` | `GET /jobs/{id}` (free) |

```bash
APP=com.spotify.music
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" "https://api.appgoat.ai/v1/apps/$APP/reviews" \
  -d country=us -d rating=1-3 -d since=2026-10-15 -d limit=100 \
  | jq -r '.data[] | "\(.rating)★ v\(.version) \(.created_at) review:\(.review_id) \(.body[0:200])"'
```

Review fields: `review_id`, `country`, `rating`, `title`, `body`, `version`, `thumbs_up`, `reply`,
`replied_at`, `created_at`, and the AI tags `sentiment` (positive|neutral|negative), `intent` (bug|crash|feature_request|pricing|ux|praise|spam|other), `severity` (0–3), `topic`, `confidence` (null until a review is tagged). `author` is present
but must not be copied into issues.
