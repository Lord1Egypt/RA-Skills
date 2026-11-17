# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", "next_cursor", … } }`; errors are
`{ "error": { "code", "message", "hint", "approve_url"? } }` - read `hint`.

| MCP tool | REST call |
|---|---|
| `list_connections` | `GET /connections` (free) |
| `read_connection` what=reviews | `GET /connections/{id}/reviews?app={app}&unanswered=true&limit=100` (next page: `&cursor=<meta.next_cursor>`) |
| `get_reviews` | `GET /apps/{app}/reviews?rating=1-3&intent=bug,crash&limit=100` |
| `propose_action` | `POST /actions` `{"type":"review.reply","connection":"con_…","dry_run":true,"source":"playbook:reply-to-every-review","params":{"app":"…","review_id":"…","text":"…"}}` (free) |
| `apply_action` | `POST /actions/{id}/approve` `{}` or `{"force":true}` (1 credit when applied) |
| `reject_action` | `POST /actions/{id}/reject` `{"reason":"…"}` (free) |
| `get_action` | `GET /actions/{id}` (free) |

```bash
CON=con_x8Hq2mXc0aLpQwRtYb APP=1234567890
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" "https://api.appgoat.ai/v1/connections/$CON/reviews" \
  -d app=$APP -d unanswered=true -d limit=100 \
  | jq -r '.data[] | "\(.rating)★ \(.created_at[0:10]) \(.id) \(.body[0:160])"'

curl -s -H "x-api-key: $APPGOAT_API_KEY" -H "content-type: application/json" \
  https://api.appgoat.ai/v1/actions -d @- <<JSON | jq '.data | {id, status, diff, guardrail}'
{"type":"review.reply","connection":"$CON","dry_run":true,"source":"playbook:reply-to-every-review",
 "params":{"app":"$APP","review_id":"<id>","text":"Thanks for the detailed report! …"}}
JSON
```

Approve outcomes: `200` with `status` `applied` or `pending_approval` (`approve_url`), `403
forbidden` (a person approves at `error.approve_url`), `409 conflict` with `error.diff` when someone
replied since the dry run.
