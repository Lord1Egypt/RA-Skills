# Threadly public API reference

The full reference for the API this skill calls. Adapted from Threadly's own
`docs/api/PUBLIC_API.md` — also consumed by the
[n8n community node](https://github.com/thumbflipcontact-ops/n8n-nodes-threadly), a separate,
independently maintained client of the same surface.

## Auth

Every route below requires `Authorization: Bearer <api_key>`. Keys are project-scoped (one
key acts on exactly one project) and generated from the dashboard API — no public-API UI
exists for this yet:

```
POST   /api/v1/projects/{project_id}/api-keys      { "name": "..." }  -> { full_key, ... } (shown once)
GET    /api/v1/projects/{project_id}/api-keys
POST   /api/v1/projects/{project_id}/api-keys/{id}/revoke
```

Rate limit: 120 requests burst, 2/second sustained, per key.

## Endpoints

All under `/public/v1`:

| Method | Path | Notes |
|---|---|---|
| GET | `/conversations` | X conversations Threadly has discovered. `tag`, `limit`, `offset` query params. |
| GET | `/drafts` | Content items awaiting/given a decision. `status` (default `pending_review`), `limit`, `offset`. |
| POST | `/drafts/{id}/approve` | Approves a draft. Attributed to the API key's creator (`created_by_user_id`) — a key whose creator's account was deleted is rejected with 401. |
| POST | `/drafts/{id}/reject` | Body: `{"reason": "..."}`. Same attribution as approve. |
| GET | `/replies` | Content items already published. `limit`, `offset`. |
| POST | `/webhook-subscriptions` | Body: `{"target_url": "https://...", "event_types": ["conversation.discovered"]}`. `target_url` must be `https://` and not point at localhost/a private IP. Returns a `secret` shown once, used to verify delivery signatures. |
| GET | `/webhook-subscriptions` | Lists this project's subscriptions (never includes `secret`). |
| DELETE | `/webhook-subscriptions/{id}` | Revokes a subscription. |

## Webhook delivery

`conversation.discovered` fires whenever Threadly discovers a new lead. Delivered as `POST` to
your `target_url`:

```json
{
  "event": "conversation.discovered",
  "delivery_id": "<uuid>",
  "occurred_at": "2026-08-16T10:00:00Z",
  "data": { "knowledge_item_id": "...", "url": "...", "platform": "twitter", "buying_intent": "high" }
}
```

Headers:

- `X-Threadly-Event: conversation.discovered`
- `X-Threadly-Delivery: <delivery id>` — stable per delivery attempt, safe to use as an
  idempotency key
- `X-Threadly-Signature: sha256=<hex>` — HMAC-SHA256 of the raw request body, keyed by the
  subscription's `secret`. Verify with `hmac.new(secret, raw_body, sha256).hexdigest()` and a
  constant-time comparison.

Retries on failure with backoff (30s, 2m, 10m, 1h, 6h), terminal `failed` status after 5
attempts. No retry-triggered duplicate deliveries — one row per (subscription, event) pair.

## What's out of scope for now

- Additional webhook events beyond `conversation.discovered`.
- Zapier/Make integrations — same underlying API, not yet built.
- Any dashboard UI for managing API keys or webhook subscriptions — API-only for now.
