---
name: skillfully
description: Use Skillfully APIs from an AI runtime to authenticate, create a tracked skill, and retrieve feedback.
---

# Skillfully API skill

Use this skill to onboard and manage Skillfully from a non-browser AI runtime.

Set this once:

```bash
BASE_URL="https://www.skillfully.sh"
```

## 1) Login via API code

Call `POST /login` to start login.

```bash
curl -X POST "$BASE_URL/login" \
  -H "content-type: application/json" \
  -d '{"email":"agent@example.com"}'
```

The response indicates a code was sent. `email` must be reachable by Skillfully's email delivery webhook.

## 2) Verify code and get bearer token

Call `POST /login_confirm` with the code from email.

```bash
curl -X POST "$BASE_URL/login_confirm" \
  -H "content-type: application/json" \
  -d '{"email":"agent@example.com","code":"123456"}'
```

Response shape:

```json
{
  "token_type": "Bearer",
  "access_token": "<jwt-like-token>",
  "token_prefix": "a1b2c3d4",
  "user_id": "api_user_123",
  "token_expires_at": 1745000000000
}
```

Use `access_token` for every authenticated endpoint with:

```bash
Authorization: Bearer <access_token>
```

## 3) Create a tracked skill and receive the suggested snippet

Call `POST /skills` with name and optional description.

```bash
curl -X POST "$BASE_URL/skills" \
  -H "authorization: Bearer <access_token>" \
  -H "content-type: application/json" \
  -d '{"name":"Code Reviewer","description":"Collect feedback after each run"}'
```

Response shape:

```json
{
  "id": "<record-id>",
  "skill_id": "sk_xxxxxx",
  "name": "Code Reviewer",
  "description": "Collect feedback after each run",
  "feedback_url": "https://www.skillfully.sh/feedback/sk_xxxxxx",
  "snippet": "# Skillfully feedback (required)\n...\nhttps://www.skillfully.sh/feedback/sk_xxxxxx",
  "created_at": 1745000000000
}
```

Paste `snippet` into the agent skill you maintain (typically `SKILL.md`).

## 4) Retrieve feedback for one skill

Call `GET /feedback/<skill_id>` with optional query filters:

- `rating=positive|negative|neutral` (optional)
- `sort=asc|desc` (optional, default `desc`)
- `limit=1..100` (optional, default `20`)
- `cursor=<createdAt:id>` (optional, required for stable pagination)

```bash
curl -X GET "$BASE_URL/feedback/sk_xxxxxx?rating=positive&sort=desc&limit=25" \
  -H "authorization: Bearer <access_token>"
```

Paginated responses include:

```json
{
  "items": [],
  "sort": "desc",
  "limit": 25,
  "rating": "positive",
  "cursor": null,
  "hasMore": true,
  "nextCursor": "1739999999000:feedback-record-id"
}
```

Use `nextCursor` as the `cursor` query arg for the next call:

```bash
curl -X GET "$BASE_URL/feedback/sk_xxxxxx?sort=desc&cursor=1739999999000:feedback-record-id" \
  -H "authorization: Bearer <access_token>"
```
