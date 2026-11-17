# Topical agent webhook payloads

Topical POSTs signed JSON to the agent webhook URL configured in the portal or via the `manage_agent_webhook` MCP tool.

## Headers

| Header | Purpose |
| --- | --- |
| `Authorization` | Optional `Bearer` token you configured |
| `Content-Type` | `application/json` |
| `X-Topical-Timestamp` | Unix timestamp for signature verification |
| `X-Topical-Signature` | HMAC-SHA256 of `{timestamp}.{body}` using the signing secret |

## `topic_breaking_news`

High-relevance global breaking news matched to a monitored topic.

```json
{
  "idempotencyKey": "topic_breaking_news:sub_abc:topic_xyz:bn_123",
  "type": "topic_breaking_news",
  "subscriptionId": "sub_abc",
  "topicId": "topic_xyz",
  "breakingNewsId": "bn_123",
  "title": "Anthropic filed for an IPO",
  "summary": "Anthropic submitted confidential IPO paperwork with the SEC.",
  "occurredAt": "2026-06-14T10:00:00.000Z",
  "sources": [{ "url": "https://example.com/ipo", "title": "SEC filing", "role": "primary" }],
  "relevanceScore": 88,
  "relevanceReason": "Matches IPO watchlist entities",
  "deliveredAt": "2026-06-15T16:53:49.000Z"
}
```

## `topic_briefing`

Scheduled briefing after a completed pipeline run.

```json
{
  "idempotencyKey": "topic_briefing:sub_abc:topic_xyz:run_456",
  "type": "topic_briefing",
  "subscriptionId": "sub_abc",
  "topicId": "topic_xyz",
  "name": "AI for software developers",
  "deliveredAt": "2026-06-15T16:53:49.000Z",
  "since": "2026-06-08T07:00:00.000Z",
  "markdown": "## Breaking news\n\n- **Cursor 3.0 shipped** …",
  "breakingNews": [],
  "signals": [],
  "trends": []
}
```

## Legacy type names

The OpenClaw transform (`topical-inbound.mjs`) still accepts older payloads for backward compatibility:

| Current | Legacy |
| --- | --- |
| `topic_briefing` | `topic_digest` (`events` instead of `breakingNews`) |
| `topic_breaking_news` | `topic_event` (`eventId` instead of `breakingNewsId`) |

## OpenClaw ingress URL

Point Topical at your gateway hook path, for example:

`https://<your-gateway-host>/hooks/topical-inbound`

Use the same bearer token as `hooks.token` in OpenClaw config (or configure Topical's outbound bearer token to match).
