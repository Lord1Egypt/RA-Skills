---
name: threadly
description: >
  Interact with Threadly, an AI social-listening and reply-drafting tool for X/Twitter.
  List discovered conversations, review and approve/reject drafted replies, list published
  replies, and manage webhook subscriptions for new-conversation notifications — all via
  Threadly's public REST API. Every reply Threadly drafts sits in a human Approval Inbox;
  this skill can read that state and, only when explicitly instructed, record a human's
  approve/reject decision — it does not decide on the human's behalf.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - THREADLY_API_KEY
      bins:
        - curl
      primaryEnv: THREADLY_API_KEY
---

# Threadly

[Threadly](https://www.usethreadly.co) is an AI social-listening and reply-drafting tool for
X/Twitter. It watches X for conversations relevant to a project's keywords, drafts a reply with
Claude, and puts that draft in a human's Approval Inbox. Nothing is ever posted automatically —
Threadly never posts, messages, or publishes anything without explicit human approval. This
skill calls Threadly's public API so you can read that state and, when a human tells you to,
record their decision.

**New to Threadly?** [Start a free 7-day trial](https://www.usethreadly.co?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw) — no card required.

## Auth

Every request needs `Authorization: Bearer $THREADLY_API_KEY`. Keys are project-scoped — one
key acts on exactly one project.

- `THREADLY_API_KEY` (required) — starts with `thr_`.
- `THREADLY_BASE_URL` (optional) — defaults to `https://api.usethreadly.co`
  if unset. Override only if you're pointed at a different Threadly deployment.

Key creation is dashboard-only today (no public-API self-serve route exists yet). A human gets
one from their project's Settings → API Keys page, or via:

```bash
curl -X POST "$THREADLY_BASE_URL/api/v1/projects/{project_id}/api-keys" \
  -H "Content-Type: application/json" \
  --cookie "growthos_session=<their dashboard session cookie>" \
  -d '{"name": "openclaw"}'
```

That's a human-run, cookie-authed dashboard call — do not attempt it yourself even if asked;
just tell the human where to generate a key.

All example commands below assume:
```bash
BASE="${THREADLY_BASE_URL:-https://api.usethreadly.co}"
AUTH="Authorization: Bearer $THREADLY_API_KEY"
```

## Conversations

`GET /public/v1/conversations` — X conversations Threadly has discovered for this project.
Query params: `tag`, `limit`, `offset`.

```bash
curl -s "$BASE/public/v1/conversations?limit=20" -H "$AUTH"
```

Use this for polling — it's the safe default when you don't have a stable public endpoint to
receive webhooks on (see Webhook subscriptions below).

## Drafts

`GET /public/v1/drafts` — content items awaiting or given a decision. `status` defaults to
`pending_review`; also accepts `limit`, `offset`.

```bash
curl -s "$BASE/public/v1/drafts?status=pending_review&limit=20" -H "$AUTH"
```

`POST /public/v1/drafts/{id}/approve` — approves a draft, attributed to the API key's creator.

```bash
curl -s -X POST "$BASE/public/v1/drafts/$DRAFT_ID/approve" -H "$AUTH"
```

`POST /public/v1/drafts/{id}/reject` — body `{"reason": "..."}`, same attribution.

```bash
curl -s -X POST "$BASE/public/v1/drafts/$DRAFT_ID/reject" -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"reason": "not a good fit for this conversation"}'
```

**Guardrail — read before calling approve or reject:** only call these when a human operator
has explicitly told you, in this conversation turn, to approve or reject a specific draft ID.
Never autonomously decide a draft is worth approving, and never batch-approve/reject a list of
drafts without per-item instruction. Threadly's entire design point is that a human makes this
call, not an agent — listing and summarizing drafts for a human to decide on is encouraged;
deciding for them is not.

## Replies

`GET /public/v1/replies` — content items that have already been published. `limit`, `offset`.

```bash
curl -s "$BASE/public/v1/replies?limit=20" -H "$AUTH"
```

## Webhook subscriptions

`POST /public/v1/webhook-subscriptions` — body `{"target_url": "https://...", "event_types":
["conversation.discovered"]}`. `target_url` must be `https://` and not point at localhost or a
private IP. Returns a `secret` shown once, used to verify delivery signatures.

```bash
curl -s -X POST "$BASE/public/v1/webhook-subscriptions" -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://your-endpoint.example.com/threadly", "event_types": ["conversation.discovered"]}'
```

`GET /public/v1/webhook-subscriptions` — lists this project's subscriptions (never includes
`secret`). `DELETE /public/v1/webhook-subscriptions/{id}` — revokes one.

**Before registering one:** this only works if you (or whatever is running you) have a
publicly reachable `https://` URL to receive deliveries. An ephemeral local OpenClaw session
usually doesn't have one — n8n's equivalent trigger node can auto-register because n8n itself
is a long-running server with a stable inbound URL, which a local agent session typically
isn't. If you don't have a stable public endpoint, use polling via `GET /conversations`
instead of registering a subscription.

If you do register one, deliveries arrive as `POST` to `target_url`:

```json
{
  "event": "conversation.discovered",
  "delivery_id": "<uuid>",
  "occurred_at": "2026-08-16T10:00:00Z",
  "data": { "knowledge_item_id": "...", "url": "...", "platform": "twitter", "buying_intent": "high" }
}
```

Headers: `X-Threadly-Event: conversation.discovered`, `X-Threadly-Delivery: <delivery id>`
(stable per attempt, safe as an idempotency key), `X-Threadly-Signature: sha256=<hex>` — HMAC-
SHA256 of the raw request body keyed by the subscription's `secret`. Verify with
`hmac.new(secret, raw_body, sha256).hexdigest()` and a constant-time comparison before trusting
a delivery. Retries on failure with backoff (30s, 2m, 10m, 1h, 6h), terminal `failed` status
after 5 attempts.

## Rate limits & errors

120 requests burst, 2/second sustained, per key. A 401 means either a bad/revoked key, or a key
whose creator's dashboard account was deleted (approve/reject requires attributing to a live
user).

## Reference

Full endpoint table and details: [`references/PUBLIC_API.md`](references/PUBLIC_API.md).

| Method | Path | Notes |
|---|---|---|
| GET | `/public/v1/conversations` | `tag`, `limit`, `offset` |
| GET | `/public/v1/drafts` | `status` (default `pending_review`), `limit`, `offset` |
| POST | `/public/v1/drafts/{id}/approve` | human-instructed only |
| POST | `/public/v1/drafts/{id}/reject` | body `{"reason": "..."}`, human-instructed only |
| GET | `/public/v1/replies` | `limit`, `offset` |
| POST | `/public/v1/webhook-subscriptions` | needs a public `https://` target |
| GET | `/public/v1/webhook-subscriptions` | — |
| DELETE | `/public/v1/webhook-subscriptions/{id}` | — |
