# rune-ext-zalo

> Rune L4 Skill | extension


# @rune/zalo

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Zalo is Vietnam's dominant messaging platform (~75M users) but its developer ecosystem has critical gaps: no Node.js SDK, zero webhook handling in official SDKs, undocumented rate limits, and confusing dual-token OAuth2 flows. This pack provides production-ready guidance for two tracks:

**Track A — Official Account API** (production-safe): OAuth2 PKCE, 8 message types, webhook server, token lifecycle, and MCP server blueprint for AI agent integration. Use this for business chatbots, customer support automation, and notification systems.

**Track B — Personal Account via zca-js** (unofficial, risk-gated): QR login, personal/group messaging, media handling. Use this for personal bots, group utilities, and rapid prototyping before committing to OA.

Both tracks share a rate limiting skill — the #1 cause of account bans.

## Best Fit

- Vietnamese dev teams building Zalo OA chatbots or customer support automation
- AI agent projects that need Zalo as a communication channel (MCP server pattern)
- Personal automation: group bots, notification forwarders, quick prototypes
- Projects migrating from unofficial to official Zalo API

## Not a Fit

- Facebook Messenger, Telegram, or Discord bots — different APIs entirely
- ZaloPay payment integration (separate API surface, not covered here)
- Zalo Mini App development (JSAPI bridge, not OA/personal messaging)

## Triggers

- Auto-trigger: when `zalo`, `zca-js`, `@anthropic-ai/sdk` + Zalo context detected
- `/rune zalo-oa` — Official Account setup and messaging
- `/rune zalo-personal` — Personal account automation
- `/rune zalo-mcp` — MCP server for AI agent ↔ Zalo
- `/rune zalo-rate` — Rate limiting and anti-ban strategies
- Called by `cook` (L1) when Zalo integration task detected
- Called by `mcp-builder` (L2) when building Zalo MCP server

## Skills Included

| Skill | Model | Track | Description |
|-------|-------|-------|-------------|
| [zalo-oa-setup](skills/zalo-oa-setup.md) | sonnet | A | OAuth2 PKCE flow, dual token management (User vs OA), app registration, appsecret_proof signing, token auto-refresh middleware. |
| [zalo-oa-messaging](skills/zalo-oa-messaging.md) | sonnet | A | All 8 OA message types (text, image, file, sticker, list, template, transaction, promotion), follower management, broadcast with demographic targeting. |
| [zalo-oa-webhook](skills/zalo-oa-webhook.md) | sonnet | A | Webhook server setup, event routing, signature verification, retry handling, event type catalog, Express/Fastify/Hono patterns. |
| [zalo-oa-mcp](skills/zalo-oa-mcp.md) | sonnet | A | MCP server blueprint — tools for read/send/broadcast, webhook-to-MCP bridge, credential storage, AI agent conversation loop. |
| [zalo-personal-setup](skills/zalo-personal-setup.md) | sonnet | B | zca-js setup, QR login flow, credential persistence, session management, WebSocket listener, keepAlive, anti-detection baseline. |
| [zalo-personal-messaging](skills/zalo-personal-messaging.md) | sonnet | B | Personal/group messaging, media (image/video/voice/sticker), reactions, group management (create, members, settings), mention gating, message buffer. |
| [zalo-rate-guard](skills/zalo-rate-guard.md) | sonnet | Shared | Rate limiting patterns for both tracks — token bucket per endpoint, exponential backoff, queue management, quota monitoring, anti-ban strategies. |

## Risk Gate — Track B (Personal Account)

<HARD-GATE>
Track B skills use unofficial reverse-engineered APIs via zca-js.
Before ANY Track B implementation, the developer MUST acknowledge:

1. **ToS violation**: Personal account automation violates Zalo's Terms of Service
2. **Ban risk**: Account can be suspended without warning
3. **Single-session**: Cannot run bot + personal Zalo simultaneously on same account
4. **API instability**: Zalo can break the internal API at any time without notice
5. **No support**: Zalo will not help with issues caused by unofficial API usage

Track B is for: personal projects, prototypes, group utilities.
Track B is NOT for: production business systems, customer-facing bots, high-volume messaging.

For production use → Track A (Official Account API).
</HARD-GATE>

## Connections

```
Calls → mcp-builder (L2): zalo-oa-mcp uses mcp-builder patterns for server scaffolding
Calls → sentinel (L2): credential handling triggers security review
Calls → rate-guard (shared): all messaging skills call rate-guard before API calls
Calls → verification (L3): verify webhook server is running and receiving events
Called By ← cook (L1): when Zalo integration task detected in project
Called By ← scaffold (L1): when bootstrapping a Zalo bot project
Called By ← mcp-builder (L2): when building Zalo-specific MCP server
```

## Tech Stack

| Component | Recommended | Alternatives |
|-----------|-------------|--------------|
| Runtime | Node.js 20+ | Bun, Deno |
| OA HTTP client | undici / fetch | axios |
| Personal API | zca-js | none (only option) |
| Webhook server | Hono | Express, Fastify |
| MCP framework | @anthropic-ai/sdk | custom |
| Queue (rate limit) | p-queue | bottleneck, bull |
| Validation | zod | joi |

## Constraints

1. All skills MUST reference Zalo OA API v3 (not deprecated v2)
2. Track B skills MUST display HARD-GATE risk disclaimer before execution
3. Rate limiting MUST be implemented before any messaging — no fire-and-forget
4. Credentials (tokens, cookies, secrets) MUST never be logged or committed
5. Webhook signature verification MUST NOT be skipped — even in development

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| OAuth2 access token expires (1h) without auto-refresh causing silent API failures | HIGH | Implement token refresh middleware that intercepts 401 responses and retries with new token before propagating errors |
| zca-js session lost when running personal bot and Zalo app simultaneously on same account | HIGH | Use a dedicated account for bot automation — single-session limit is non-negotiable on Track B |
| Webhook signature verification skipped in development, then deployed to production unsigned | HIGH | Always validate `X-Zalo-Signature` header from first commit — skip in dev only via explicit `SKIP_WEBHOOK_VERIFY=true` env flag |
| Rate limit hit causes account ban with no warning (HTTP 429 mishandled as transient error) | HIGH | Implement token bucket per endpoint; treat sustained 429s as ban-risk signal and back off for 60+ seconds |

## References

| Reference | Trigger |
|-----------|---------|
| [VietQR & Banking](references/vietqr-banking.md) | Payment, bank transfer, QR code patterns detected |
| [Conversation Management](references/conversation-management.md) | Polls, auto-reply, mute/archive, advanced messaging |
| [MCP Production](references/mcp-production.md) | MCP server deployment, cursor pagination, pm2 setup |
| [Multi-Account & Proxy](references/multi-account-proxy.md) | Multi-account setup, proxy configuration, VPS deployment |
| [Listen Mode](references/listen-mode.md) | WebSocket listener, real-time events, webhook forwarding |
| [Eval Scenarios](references/eval-scenarios.md) | Quality gate — 24 test scenarios (functional + security) |

## Credits

This pack was originally inspired by and incorporates patterns from:

- **[zalo-agent-cli](https://github.com/PhucMPham/zalo-agent-cli)** by PhucMPham (MIT) — CLI tool for Zalo automation, 90+ commands, MCP server, VietQR banking integration
- **[openzalo](https://github.com/darkamenosa/openzalo)** by darkamenosa — OpenClaw channel plugin for Zalo personal accounts via openzca CLI
- **[zca-js](https://github.com/RFS-ADRENO/zca-js)** — Unofficial Zalo client library (reverse-engineered API)

## Done When

- OA OAuth2 flow working with auto-refresh
- All 8 message types documented with request/response examples
- Webhook server receiving and routing events correctly
- MCP server operational: agent can read and send Zalo messages
- Rate limiting active on all outbound API calls
- Track B: QR login + personal/group messaging working with risk gate shown

# zalo-oa-mcp

MCP server blueprint that bridges AI agents (Claude) with Zalo OA — enabling the use case "AI agent chats via Zalo".

#### Architecture

```
User sends message via Zalo
  → Zalo webhook POST to your server
  → Webhook handler verifies signature, stores in message queue
  → MCP server exposes tools:
      zalo_read_messages  — poll queue for new messages
      zalo_send_message   — send reply via OA API
      zalo_get_profile    — fetch user info (cached)
      zalo_list_followers — list OA followers
      zalo_send_broadcast — broadcast with targeting (confirm-gated)
  → AI agent (Claude) calls these tools in a conversation loop
  → Agent processes message, decides response
  → Calls zalo_send_message to reply
  → User receives reply in Zalo
```

Webhook server and MCP server run in the **same Node.js process** — no IPC overhead, shared in-memory queue.

#### MCP Tool Definitions

**1. zalo_read_messages** — query, auto-approve

```json
{
  "name": "zalo_read_messages",
  "description": "Poll the webhook queue for new Zalo OA messages. Returns messages received since last read.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "limit": { "type": "number", "default": 10, "description": "Max messages to return" },
      "since_timestamp": { "type": "number", "description": "Unix ms — only return messages after this time" }
    }
  }
}
```

Returns: `{ messages: [{ user_id, user_name, text, attachments, timestamp, msg_id }] }`

**2. zalo_send_message** — mutation, confirm before send

```json
{
  "name": "zalo_send_message",
  "description": "Send a message to a Zalo OA follower. Requires confirmation before execution.",
  "inputSchema": {
    "type": "object",
    "required": ["user_id", "text"],
    "properties": {
      "user_id": { "type": "string", "description": "OA-scoped user ID" },
      "text": { "type": "string", "description": "Message text (max 2000 chars)" },
      "message_type": { "type": "string", "enum": ["text", "image", "template"], "default": "text" },
      "attachment_id": { "type": "string", "description": "Required when message_type is image" }
    }
  }
}
```

Returns: `{ success: true, msg_id: "..." }` or `{ success: false, error: "..." }`

**3. zalo_get_profile** — query, auto-approve, 1-hour TTL cache

```json
{
  "name": "zalo_get_profile",
  "description": "Get Zalo user profile. Cached for 1 hour to avoid repeated API calls.",
  "inputSchema": {
    "type": "object",
    "required": ["user_id"],
    "properties": {
      "user_id": { "type": "string" }
    }
  }
}
```

Returns: `{ display_name, avatar, user_id, is_follower }`

**4. zalo_list_followers** — query, auto-approve

```json
{
  "name": "zalo_list_followers",
  "description": "List OA followers with pagination.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "offset": { "type": "number", "default": 0 },
      "count": { "type": "number", "default": 50, "maximum": 50 }
    }
  }
}
```

Returns: `{ followers: [{ user_id, display_name }], total }`

**5. zalo_send_broadcast** — mutation, ALWAYS confirm with preview

```json
{
  "name": "zalo_send_broadcast",
  "description": "Broadcast message to all followers or filtered segment. Always shows preview before sending.",
  "inputSchema": {
    "type": "object",
    "required": ["text"],
    "properties": {
      "text": { "type": "string" },
      "target": {
        "type": "object",
        "properties": {
          "gender": { "type": "string", "enum": ["male", "female"] },
          "age_range": { "type": "object", "properties": { "min": { "type": "number" }, "max": { "type": "number" } } },
          "city": { "type": "string" }
        }
      }
    }
  }
}
```

Returns: `{ success: true, sent_count: 1240 }` — always preview target before sending.

#### MCP Server Implementation

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js'
import { Hono } from 'hono'
import { serve } from '@hono/node-server'

// ── Message Queue (webhook → MCP bridge) ──────────────────────────────────
const MAX_QUEUE = 1000
const messageQueue: ZaloMessage[] = []

function enqueue(msg: ZaloMessage): void {
  messageQueue.push(msg)
  if (messageQueue.length > MAX_QUEUE) messageQueue.shift() // drop oldest
}

// ── Profile Cache (1-hour TTL) ─────────────────────────────────────────────
const profileCache = new Map<string, { data: ZaloProfile; expiry: number }>()

async function getCachedProfile(userId: string): Promise<ZaloProfile> {
  const cached = profileCache.get(userId)
  if (cached && Date.now() < cached.expiry) return cached.data
  const data = await fetchOAProfile(userId)
  profileCache.set(userId, { data, expiry: Date.now() + 3_600_000 })
  return data
}

// ── MCP Server ─────────────────────────────────────────────────────────────
const server = new Server(
  { name: 'zalo-oa-mcp', version: '1.0.0' },
  { capabilities: { tools: {} } }
)

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: 'zalo_read_messages', description: '...', inputSchema: { /* as above */ } },
    { name: 'zalo_send_message',  description: '...', inputSchema: { /* as above */ } },
    { name: 'zalo_get_profile',   description: '...', inputSchema: { /* as above */ } },
    { name: 'zalo_list_followers',description: '...', inputSchema: { /* as above */ } },
    { name: 'zalo_send_broadcast',description: '...', inputSchema: { /* as above */ } },
  ]
}))

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params

  switch (name) {
    case 'zalo_read_messages': {
      const { limit = 10, since_timestamp } = args as { limit?: number; since_timestamp?: number }
      const msgs = since_timestamp
        ? messageQueue.filter(m => m.timestamp > since_timestamp).slice(-limit)
        : messageQueue.slice(-limit)
      return { content: [{ type: 'text', text: JSON.stringify({ messages: msgs }) }] }
    }

    case 'zalo_send_message': {
      const { user_id, text, message_type = 'text', attachment_id } = args as SendMessageArgs
      const result = await sendOAMessage({ user_id, text, message_type, attachment_id })
      return { content: [{ type: 'text', text: JSON.stringify(result) }] }
    }

    case 'zalo_get_profile': {
      const profile = await getCachedProfile((args as { user_id: string }).user_id)
      return { content: [{ type: 'text', text: JSON.stringify(profile) }] }
    }

    case 'zalo_list_followers': {
      const { offset = 0, count = 50 } = args as { offset?: number; count?: number }
      const result = await listOAFollowers(offset, Math.min(count, 50))
      return { content: [{ type: 'text', text: JSON.stringify(result) }] }
    }

    case 'zalo_send_broadcast': {
      // Confirmation preview MUST be shown before sending
      const { text, target } = args as BroadcastArgs
      const preview = `BROADCAST PREVIEW:\nText: "${text}"\nTarget: ${JSON.stringify(target ?? 'all followers')}\nConfirm?`
      return { content: [{ type: 'text', text: preview }] }
      // On confirmed re-call with confirmed: true, execute sendOABroadcast()
    }

    default:
      throw new Error(`Unknown tool: ${name}`)
  }
})

// ── Webhook Server (same process) ──────────────────────────────────────────
const app = new Hono()

app.post('/webhook/zalo', async (c) => {
  const signature = c.req.header('X-ZEvent-Signature') ?? ''
  const body = await c.req.text()

  if (!verifySignature(body, signature)) return c.json({ error: 'Invalid signature' }, 403)

  const event = JSON.parse(body)
  c.executionCtx?.waitUntil(handleWebhookEvent(event))
  return c.json({ received: true })
})

async function handleWebhookEvent(event: ZaloEvent): Promise<void> {
  if (event.event_name !== 'user_send_text') return // extend as needed
  const profile = await getCachedProfile(event.sender.id).catch(() => null)
  enqueue({
    user_id: event.sender.id,
    user_name: profile?.display_name ?? event.sender.id,
    text: event.message.text,
    attachments: event.message.attachments ?? [],
    timestamp: event.timestamp,
    msg_id: event.message.msg_id,
  })
}

// ── Boot both in same process ───────────────────────────────────────────────
serve({ fetch: app.fetch, port: 3000 })
const transport = new StdioServerTransport()
await server.connect(transport)
```

#### Credential Management

Store credentials in `~/.zalo-mcp/credentials.json` — never commit this file.

```json
{
  "oa_token": "OA_ACCESS_TOKEN",
  "oa_secret_key": "OA_SECRET_KEY_FOR_WEBHOOK",
  "refresh_token": "REFRESH_TOKEN",
  "expires_at": 1712345678000
}
```

MCP server reads on startup and auto-refreshes before expiry. Never expose tokens via MCP tool responses.

```typescript
import { readFileSync, writeFileSync } from 'fs'
import { homedir } from 'os'
import { join } from 'path'

const CREDS_PATH = join(homedir(), '.zalo-mcp', 'credentials.json')

function loadCredentials(): ZaloCredentials {
  const raw = readFileSync(CREDS_PATH, 'utf-8')
  return JSON.parse(raw) as ZaloCredentials
}
```

#### Conversation Loop (Agent Side)

```typescript
// Claude agent system prompt excerpt
const systemPrompt = `
You are a Zalo OA customer support agent.
- Call zalo_read_messages to get new messages from users
- Call zalo_get_profile to personalize responses
- Reply via zalo_send_message — ALWAYS confirm before sending
- You cannot reply to users who haven't messaged in the last 7 days (OA API constraint)
- Keep replies concise — Zalo UI shows ~160 chars before truncation on mobile
`
```

#### Tool Safety Classification

| Tool | Class | Approval |
|------|-------|----------|
| `zalo_read_messages` | query | auto-approve |
| `zalo_get_profile` | query | auto-approve |
| `zalo_list_followers` | query | auto-approve |
| `zalo_send_message` | mutation | confirm before send |
| `zalo_send_broadcast` | mutation | ALWAYS confirm — shows preview |

Rate limiting: call `zalo-rate-guard` before `zalo_send_message` and `zalo_send_broadcast`. See [@rune/zalo rate guard skill](zalo-rate-guard.md).

#### Sharp Edges

- **Queue overflow**: Queue caps at 1000 messages, drops oldest. If agent polls infrequently in high-traffic OA, messages are lost. Use Redis `LPUSH/LTRIM` in production.
- **7-day CS window**: OA API rejects sends to users who haven't initiated contact in 7 days. Agent must check `timestamp` before attempting reply — surface this as a graceful error, not a crash.
- **Rate limiting is mandatory**: `zalo_send_message` must go through `zalo-rate-guard` — OA bans are silent and permanent.
- **user_id is OA-scoped**: The same Zalo user has different IDs per OA. Cache `display_name` via `zalo_get_profile` to humanize logs and agent context.
- **Single process, not microservices**: Webhook and MCP server share the same queue in-memory. Splitting into separate processes requires a Redis or HTTP bridge — adds latency and operational overhead with no benefit at typical OA traffic volumes.
- **Broadcast confirmation is non-negotiable**: `zalo_send_broadcast` without preview risks mass-spamming followers. Always return preview on first call; only execute on explicit re-call with `confirmed: true`.

---

# zalo-oa-messaging

Send any of the 8 Zalo OA message types, manage followers, and run broadcast campaigns via the v3 Official Account API.

## Base Config

```
Base URL : https://openapi.zalo.me/v3.0/oa
Upload   : https://openapi.zalo.me/v2.0/oa  (intentional version mismatch)
Auth     : Authorization: Bearer {oa_access_token}
Content  : Content-Type: application/json
Endpoint : POST /message/cs  (all 8 CS message types)
```

## Step 1 — Identify the Message Type

| # | Type | Use Case | Constraint |
|---|------|----------|------------|
| 1 | Text | Simple reply, notification | 2000 char limit |
| 2 | Image | Product photo, banner | attachment_id from upload |
| 3 | File | PDF, invoice, document | attachment_id from upload |
| 4 | Sticker | Friendly interaction | sticker_id from catalog |
| 5 | List | Menu, product listing | max 10 items |
| 6 | Template | CTA with buttons | max 5 buttons |
| 7 | Transaction | Order/shipping update | pre-approved template required |
| 8 | Promotion | Marketing campaign | approved template + quota |

**All CS messages**: only sendable within 7 days of user's last interaction with the OA.

---

## Step 2 — Send the Right Payload

### Type 1 — Text Message

```http
POST https://openapi.zalo.me/v3.0/oa/message/cs
Authorization: Bearer {oa_access_token}

{
  "recipient": { "user_id": "4337842264521611405" },
  "message": { "text": "Xin chào! Chúng tôi có thể giúp gì cho bạn?" }
}
```

Response (success):
```json
{ "error": 0, "message": "Success", "data": { "message_id": "oaMsgId.567890" } }
```

---

### Type 2 — Image Message

Upload first (v2.0 endpoint), then send:

```http
POST https://openapi.zalo.me/v2.0/oa/upload/image
Authorization: Bearer {oa_access_token}
Content-Type: multipart/form-data

file=@banner.jpg   (max 1MB)
```

```json
{ "error": 0, "data": { "attachment_id": "f8d5a7e1-2b3c-4d5e-8f9a-1b2c3d4e5f6a" } }
```

Then send:

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "media",
        "elements": [{
          "media_type": "image",
          "attachment_id": "f8d5a7e1-2b3c-4d5e-8f9a-1b2c3d4e5f6a"
        }]
      }
    }
  }
}
```

---

### Type 3 — File Message

```http
POST https://openapi.zalo.me/v2.0/oa/upload/file
Authorization: Bearer {oa_access_token}
Content-Type: multipart/form-data

file=@invoice.pdf   (max 5MB)
```

```json
{ "error": 0, "data": { "attachment_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890" } }
```

Send payload same shape as image but `"media_type": "file"`.

---

### Type 4 — Sticker Message

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "media",
        "elements": [{ "media_type": "sticker", "attachment_id": "87521" }]
      }
    }
  }
}
```

Sticker IDs: fetch from Zalo sticker catalog. Common IDs: 87521 (thumbs up), 87522 (heart), 87523 (smile).

---

### Type 5 — List Message

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "list",
        "elements": [
          {
            "title": "Sản phẩm A",
            "subtitle": "Giá: 299.000đ",
            "image_url": "https://cdn.example.com/product-a.jpg",
            "default_action": { "type": "oa.open.url", "url": "https://example.com/product-a" }
          },
          {
            "title": "Sản phẩm B",
            "subtitle": "Giá: 199.000đ",
            "image_url": "https://cdn.example.com/product-b.jpg",
            "default_action": { "type": "oa.open.url", "url": "https://example.com/product-b" }
          }
        ],
        "buttons": [{
          "title": "Xem tất cả sản phẩm",
          "type": "oa.open.url",
          "payload": { "url": "https://example.com/products" }
        }]
      }
    }
  }
}
```

Limits: max 10 elements, max 5 buttons at bottom.

---

### Type 6 — Template Message (Button Template)

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "button",
        "text": "Chọn hành động bạn muốn thực hiện:",
        "buttons": [
          {
            "title": "Xem đơn hàng",
            "type": "oa.open.url",
            "payload": { "url": "https://example.com/orders" }
          },
          {
            "title": "Gọi hỗ trợ",
            "type": "oa.open.phone",
            "payload": { "phone_code": "0901234567" }
          },
          {
            "title": "Theo dõi vận chuyển",
            "type": "oa.query.show",
            "payload": { "content": "TRACK_ORDER_12345" }
          }
        ]
      }
    }
  }
}
```

Button types: `oa.open.url`, `oa.open.phone`, `oa.query.show` (postback), `oa.open.sms`.

---

### Type 7 — Transaction Message

Requires a pre-approved template from Zalo OA portal. Cannot send arbitrary content.

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "transaction_order",
        "language": "VI",
        "elements": [{
          "attachment_id": "approved-template-id-from-zalo",
          "type": "banner"
        }],
        "parameters": {
          "order_id": "ORD-2026-001234",
          "order_status": "Đã giao hàng",
          "delivery_date": "15/03/2026",
          "tracking_url": "https://example.com/track/ORD-2026-001234"
        }
      }
    }
  }
}
```

Template must match an approved template ID. Parameter keys defined by the template.

---

### Type 8 — Promotion Message

Requires approved template + sufficient broadcast quota.

```json
{
  "recipient": { "user_id": "4337842264521611405" },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "promotion",
        "language": "VI",
        "elements": [{
          "attachment_id": "approved-promo-banner-id",
          "type": "banner"
        }],
        "parameters": {
          "coupon_code": "SALE30",
          "discount": "30%",
          "expiry": "31/03/2026"
        }
      }
    }
  }
}
```

---

## Step 3 — Long Text Chunking

Text limit is 2000 chars. Chunk before sending:

```typescript
function chunkMessage(text: string, limit = 2000): string[] {
  if (text.length <= limit) return [text]
  const chunks: string[] = []
  let remaining = text
  while (remaining.length > 0) {
    if (remaining.length <= limit) { chunks.push(remaining); break }
    let splitAt = remaining.lastIndexOf('\n', limit)
    if (splitAt === -1) splitAt = remaining.lastIndexOf(' ', limit)
    if (splitAt === -1) splitAt = limit
    chunks.push(remaining.slice(0, splitAt))
    remaining = remaining.slice(splitAt).trimStart()
  }
  return chunks
}

// Send each chunk with delay to respect rate limits
for (const chunk of chunkMessage(longText)) {
  await sendTextMessage(userId, chunk)
  await new Promise(r => setTimeout(r, 300))
}
```

---

## Step 4 — Follower Management

### List Followers

```http
GET https://openapi.zalo.me/v3.0/oa/user/getlist?offset=0&count=50
Authorization: Bearer {oa_access_token}
```

```json
{
  "error": 0,
  "data": {
    "users": [
      { "user_id": "4337842264521611405", "display_name": "Nguyen Van A", "followed_date": 1709827200 }
    ],
    "total": 1250,
    "offset": 0,
    "count": 50
  }
}
```

Paginate: increment `offset` by `count` until `offset >= total`.

### User Profile

```http
GET https://openapi.zalo.me/v3.0/oa/user/detail?user_id=4337842264521611405
Authorization: Bearer {oa_access_token}
```

```json
{
  "error": 0,
  "data": {
    "user_id": "4337842264521611405",
    "display_name": "Nguyen Van A",
    "birth_date": 0,
    "gender": 1,
    "phone": "",
    "city": "Ho Chi Minh City",
    "district": "",
    "tags_and_notes_info": { "tag_names": ["VIP", "Repeat-buyer"] }
  }
}
```

Note: `user_id` is OA-scoped — same person has a different `user_id` for each OA they follow.

### Tag Management

```http
POST https://openapi.zalo.me/v3.0/oa/tag/tagfollower
Authorization: Bearer {oa_access_token}

{ "user_id": "4337842264521611405", "tag_name": "VIP" }
```

```http
POST https://openapi.zalo.me/v3.0/oa/tag/rmfollowerfromtag
Authorization: Bearer {oa_access_token}

{ "user_id": "4337842264521611405", "tag_name": "VIP" }
```

---

## Step 5 — Broadcast

```http
POST https://openapi.zalo.me/v3.0/oa/message/promotion
Authorization: Bearer {oa_access_token}

{
  "recipient": {
    "target": {
      "gender": 1,
      "ages": ["18-25", "26-35"],
      "cities": ["Ho Chi Minh City", "Ha Noi"],
      "platforms": ["iOS", "Android"],
      "telcos": ["Viettel", "Mobifone"]
    }
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "promotion",
        "language": "VI",
        "elements": [{ "attachment_id": "approved-promo-banner-id", "type": "banner" }],
        "parameters": { "coupon_code": "SUMMER30", "discount": "30%" }
      }
    }
  }
}
```

Response includes estimated reach count before send is confirmed. Quota resets monthly.

---

## Sharp Edges

- **7-day CS window** — `error: 12` means the user hasn't interacted in 7 days. Cannot bypass. Solution: use Transaction or Promotion templates (pre-approved) which ignore the window.
- **Version mismatch is intentional** — upload endpoints stay on `v2.0`, message send is `v3.0`. Do not "fix" this.
- **OA-scoped user_id** — never assume the same physical person has the same `user_id` across different OAs. Always store per-OA.
- **Template approval lag** — Transaction/Promotion templates take 1-5 business days to approve. Plan ahead; cannot substitute with CS messages after approval delay.
- **Image 1MB / File 5MB hard limits** — compress images server-side before upload. Zalo returns `error: 201` for oversized files.
- **Broadcast quota** — based on follower count × OA verification tier. Track monthly usage; `error: 133` = quota exceeded.
- **Button limit 5** — template messages silently drop buttons beyond index 4. Always validate `buttons.length <= 5` before sending.

## Error Codes Quick Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 0 | Success | — |
| 12 | Outside 7-day CS window | Use approved template type |
| 14 | Invalid access token | Refresh token, retry |
| 107 | Invalid recipient | Verify user_id is OA-scoped and valid |
| 133 | Broadcast quota exceeded | Wait for monthly reset |
| 201 | File size exceeded | Compress/split before upload |
| 216 | Template not approved | Submit template for Zalo review |

---

# zalo-oa-setup

#### Purpose

Zalo's OAuth2 system has two completely separate token hierarchies — User tokens and OA tokens — that are not interchangeable. Most developers fail because they conflate the two or skip PKCE entirely. This skill walks through app registration, implements PKCE code challenge generation, builds a token auto-refresh middleware, and secures every API call with appsecret_proof signing.

#### Workflow

**Step 1 — App registration at developers.zalo.me**

Navigate to https://developers.zalo.me → Create App → note `app_id` and `secret_key`. Under "Official Account", bind your OA to the app. Configure redirect URI (must be HTTPS in production; `http://localhost:PORT/callback` for dev). Set webhook URL if receiving events. Add `app_id` and `secret_key` to `.env` — never commit them.

```
ZALO_APP_ID=your_app_id
ZALO_APP_SECRET=your_secret_key
ZALO_REDIRECT_URI=https://yourapp.com/auth/zalo/callback
ZALO_OA_ID=your_oa_id
```

**Step 2 — Decide which token track you need**

| Track | Endpoint prefix | Use case |
|-------|----------------|----------|
| User OAuth2 | `oauth.zaloapp.com/v4/permission` | Log in users, read user profile |
| OA OAuth2 | `oauth.zaloapp.com/v4/oa/permission` | Send messages, manage followers, all bot operations |

Most bots only need the OA track. If you only build a chatbot, skip User OAuth2 entirely.

**Step 3 — Generate PKCE pair**

PKCE prevents auth-code interception. Store `code_verifier` in session/memory between the redirect and the callback — it must survive that round-trip.

```typescript
import crypto from 'crypto'

export function generateCodeVerifier(): string {
  // 32 random bytes → base64url = 43-char verifier (RFC 7636 compliant)
  return crypto.randomBytes(32).toString('base64url')
}

export function generateCodeChallenge(verifier: string): string {
  return crypto.createHash('sha256').update(verifier).digest('base64url')
}
```

**Step 4 — Build the authorization URL**

```typescript
import { generateCodeVerifier, generateCodeChallenge } from './pkce'

interface AuthUrlResult {
  url: string
  codeVerifier: string // store in session — needed for token exchange
  state: string
}

export function buildOaAuthUrl(appId: string, redirectUri: string): AuthUrlResult {
  const codeVerifier = generateCodeVerifier()
  const codeChallenge = generateCodeChallenge(codeVerifier)
  const state = crypto.randomBytes(16).toString('hex') // CSRF protection

  const params = new URLSearchParams({
    app_id: appId,
    redirect_uri: redirectUri,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
    state,
  })

  return {
    url: `https://oauth.zaloapp.com/v4/oa/permission?${params}`,
    codeVerifier,
    state,
  }
}
```

**Step 5 — Exchange auth code for tokens (callback handler)**

```typescript
import { z } from 'zod'

const TokenResponseSchema = z.object({
  access_token: z.string(),
  refresh_token: z.string(),
  expires_in: z.number(), // seconds
})

export async function exchangeOaCode(
  code: string,
  codeVerifier: string,
  appId: string,
  appSecret: string,
): Promise<z.infer<typeof TokenResponseSchema>> {
  const res = await fetch('https://oauth.zaloapp.com/v4/oa/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'secret_key': appSecret },
    body: new URLSearchParams({
      app_id: appId,
      code,
      code_verifier: codeVerifier,
      grant_type: 'authorization_code',
    }),
  })

  if (!res.ok) throw new Error(`Token exchange failed: ${res.status} ${await res.text()}`)
  return TokenResponseSchema.parse(await res.json())
}
```

**Step 6 — Token store with auto-refresh middleware**

OA access_token expires in ~24h. Never make an API call without first verifying the token is still valid. When refreshing, Zalo returns a NEW refresh_token — the old one is invalidated immediately.

```typescript
import fs from 'fs/promises'
import path from 'path'
import os from 'os'

const CREDENTIALS_PATH = path.join(os.homedir(), '.zalo-mcp', 'credentials.json')
const REFRESH_BUFFER_MS = 5 * 60 * 1000 // refresh if <5 min remaining

export interface ZaloTokenStore {
  oa_access_token: string
  oa_refresh_token: string
  oa_expires_at: number  // Unix timestamp ms
  user_access_token?: string
  user_refresh_token?: string
  user_expires_at?: number
}

export async function loadTokens(): Promise<ZaloTokenStore> {
  const raw = await fs.readFile(CREDENTIALS_PATH, 'utf-8')
  return JSON.parse(raw) as ZaloTokenStore
}

export async function saveTokens(tokens: ZaloTokenStore): Promise<void> {
  await fs.mkdir(path.dirname(CREDENTIALS_PATH), { recursive: true })
  await fs.writeFile(CREDENTIALS_PATH, JSON.stringify(tokens, null, 2), { mode: 0o600 })
}

async function refreshOaToken(
  refreshToken: string,
  appId: string,
  appSecret: string,
): Promise<{ access_token: string; refresh_token: string; expires_in: number }> {
  const res = await fetch('https://oauth.zaloapp.com/v4/oa/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'secret_key': appSecret },
    body: new URLSearchParams({
      app_id: appId,
      refresh_token: refreshToken,
      grant_type: 'refresh_token',
    }),
  })

  if (!res.ok) throw new Error(`Token refresh failed: ${res.status} ${await res.text()}`)
  return res.json()
}

export async function getValidOaToken(appId: string, appSecret: string): Promise<string> {
  const store = await loadTokens()
  const now = Date.now()

  if (store.oa_expires_at - now > REFRESH_BUFFER_MS) {
    return store.oa_access_token // still fresh
  }

  // Token expired or expiring soon — refresh
  const refreshed = await refreshOaToken(store.oa_refresh_token, appId, appSecret)
  const updated: ZaloTokenStore = {
    ...store,
    oa_access_token: refreshed.access_token,
    oa_refresh_token: refreshed.refresh_token, // rotate — old token is now dead
    oa_expires_at: now + refreshed.expires_in * 1000,
  }
  await saveTokens(updated)
  return updated.oa_access_token
}
```

**Step 7 — appsecret_proof signing for server-side calls**

appsecret_proof is an HMAC-SHA256 of the access_token keyed with app_secret. It binds a token to your server — even if a token leaks, it cannot be replayed without the secret.

```typescript
import crypto from 'crypto'

export function generateAppSecretProof(accessToken: string, appSecret: string): string {
  return crypto.createHmac('sha256', appSecret).update(accessToken).digest('hex')
}

// Usage: attach to every OA API call
export async function oaApiCall(
  endpoint: string,
  body: Record<string, unknown>,
  appId: string,
  appSecret: string,
): Promise<unknown> {
  const accessToken = await getValidOaToken(appId, appSecret)
  const proof = generateAppSecretProof(accessToken, appSecret)

  const res = await fetch(`https://openapi.zalo.me/v3.0/oa/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'access_token': accessToken,
      'X-Appsecret-Proof': proof,
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) throw new Error(`OA API ${endpoint} failed: ${res.status} ${await res.text()}`)
  return res.json()
}
```

#### Sharp Edges

| Failure | Symptom | Fix |
|---------|---------|-----|
| Using User token for OA API | `error_code: 216` or permission denied | Check token source — OA APIs require OA track token, not user track |
| Lost `code_verifier` between redirect and callback | `invalid_grant` on token exchange | Store verifier in server-side session (not cookie) before redirecting |
| Redirect URI mismatch | `redirect_uri does not match` | URI must EXACTLY match registered value — trailing slash, protocol, and port all matter |
| Not rotating refresh token | Refresh silently fails after first use | Always write the NEW `refresh_token` from refresh response back to store |
| `appsecret_proof` missing on server calls | Token accepted but flagged; future calls blocked | Add `X-Appsecret-Proof` header on ALL server-side API calls, not just some |
| `secret_key` sent from browser | Secret exposure in network tab | `secret_key` header and appsecret_proof are server-side only — never from browser JS |
| Credentials file world-readable | Token leak on shared host | `chmod 600 ~/.zalo-mcp/credentials.json` — enforced by `saveTokens` above |

---

# zalo-oa-webhook

Set up and handle Zalo OA webhook server — signature verification, event routing, idempotency, and tunnel for local development.

#### Workflow

**Step 1 — Register webhook at Zalo Developer Portal**
Go to [developers.zalo.me](https://developers.zalo.me) → select App → **App Settings → Webhook**. Enter your HTTPS endpoint URL (e.g., `https://your-domain.com/webhook/zalo`). Zalo sends `POST` requests to this URL for every OA event. The URL must be HTTPS — no plain HTTP. For local dev, use ngrok: `ngrok http 3000` and paste the `https://` tunnel URL. Remember to update the URL when the tunnel restarts.

**Step 2 — Verify signature on every request (CRITICAL)**
Every request from Zalo includes `X-ZEvent-Signature` header — HMAC-SHA256 of the raw request body, signed with your **OA Secret Key** (not the App Secret — different keys). Verify before processing. Use `crypto.timingSafeEqual` to prevent timing attacks. Reject with 403 if invalid.

```typescript
import crypto from 'crypto'

function verifyWebhookSignature(
  body: string,
  signature: string,
  oaSecretKey: string
): boolean {
  const computed = crypto
    .createHmac('sha256', oaSecretKey)
    .update(body)
    .digest('hex')
  return crypto.timingSafeEqual(
    Buffer.from(computed, 'hex'),
    Buffer.from(signature, 'hex')
  )
}
```

NEVER skip verification — even in development. NEVER use `===` string compare (timing leak).

**Step 3 — Respond within 5 seconds**
Zalo expects `200 OK` within 5 seconds or it marks the delivery failed and retries up to 3 times. Acknowledge immediately, then process asynchronously:

```typescript
// Return 200 first, then process
return c.json({ received: true })  // respond immediately
await queue.push(event)            // async processing
```

**Step 4 — Implement idempotency**
Retries cause duplicate events. Use `msg_id` (present on message events) to deduplicate. Check before processing, mark as processed after:

```typescript
const processedIds = new Set<string>() // or Redis for production

async function idempotentHandle(event: ZaloEvent): Promise<void> {
  const id = event.message?.msg_id ?? `${event.event_name}:${event.timestamp}`
  if (processedIds.has(id)) return
  processedIds.add(id)
  await routeEvent(event)
}
```

**Step 5 — Route events by event_name**

| event_name | Trigger | Key payload fields |
|---|---|---|
| `user_send_text` | User sends text | `sender.id`, `message.text`, `message.msg_id` |
| `user_send_image` | User sends image | `sender.id`, `message.attachments[].payload.url` |
| `user_send_file` | User sends file | `sender.id`, `message.attachments[]` |
| `user_send_sticker` | User sends sticker | `sender.id`, `message.attachments[]` |
| `user_send_location` | User sends location | `sender.id`, `message.attachments[].payload.coordinates` |
| `follow` | User follows OA | `follower.id` |
| `unfollow` | User unfollows OA | `follower.id` |
| `user_click_button` | User clicks button | `sender.id`, `message.text` (button payload) |
| `oa_send_text` | OA message delivered | — |

Note: naming is inconsistent — messages use `user_send_*` prefix, follow/unfollow do not.

#### Server Implementations

**Hono (recommended — edge-ready)**

```typescript
import { Hono } from 'hono'
import { serve } from '@hono/node-server'
import crypto from 'crypto'

const OA_SECRET_KEY = process.env.ZALO_OA_SECRET_KEY!
const app = new Hono()

app.post('/webhook/zalo', async (c) => {
  const signature = c.req.header('X-ZEvent-Signature') ?? ''
  const body = await c.req.text() // raw body — MUST use text(), not json()

  if (!verifyWebhookSignature(body, signature, OA_SECRET_KEY)) {
    return c.json({ error: 'Invalid signature' }, 403)
  }

  const event: ZaloEvent = JSON.parse(body)
  c.executionCtx?.waitUntil(idempotentHandle(event)) // non-blocking
  return c.json({ received: true })
})

async function routeEvent(event: ZaloEvent): Promise<void> {
  switch (event.event_name) {
    case 'user_send_text':    return handleTextMessage(event)
    case 'user_send_image':   return handleImageMessage(event)
    case 'user_send_file':    return handleFileMessage(event)
    case 'user_send_location': return handleLocation(event)
    case 'follow':            return handleFollow(event)
    case 'unfollow':          return handleUnfollow(event)
    case 'user_click_button': return handleButtonClick(event)
    default: console.warn('Unhandled Zalo event:', event.event_name)
  }
}

serve({ fetch: app.fetch, port: 3000 })
```

**Express**

```typescript
import express from 'express'

const app = express()

// MUST use raw body parser — not express.json() — to preserve signature input
app.post('/webhook/zalo', express.raw({ type: 'application/json' }), async (req, res) => {
  const signature = req.headers['x-zevent-signature'] as string ?? ''
  const body = req.body.toString()

  if (!verifyWebhookSignature(body, signature, OA_SECRET_KEY)) {
    return res.status(403).json({ error: 'Invalid signature' })
  }

  const event: ZaloEvent = JSON.parse(body)
  res.json({ received: true }) // respond first
  idempotentHandle(event).catch(console.error) // then process
})
```

**Fastify**

```typescript
import Fastify from 'fastify'

const fastify = Fastify()

fastify.addContentTypeParser('application/json', { parseAs: 'string' }, (req, body, done) => {
  done(null, body) // keep raw string for signature verification
})

fastify.post('/webhook/zalo', async (request, reply) => {
  const signature = request.headers['x-zevent-signature'] as string ?? ''
  const body = request.body as string

  if (!verifyWebhookSignature(body, signature, OA_SECRET_KEY)) {
    return reply.status(403).send({ error: 'Invalid signature' })
  }

  const event: ZaloEvent = JSON.parse(body)
  reply.send({ received: true })
  idempotentHandle(event).catch(console.error)
})
```

#### Local Development Tunnel

```bash
# ngrok (most common)
ngrok http 3000
# → copy https://xxxx.ngrok.io → paste to Zalo Developer Portal

# cloudflared (free, no account needed for temp tunnels)
cloudflare tunnel --url http://localhost:3000
```

Update webhook URL in Zalo portal every time the tunnel restarts. Use a stable subdomain (`ngrok http --subdomain=myapp 3000`) with a paid ngrok account to avoid this.

#### Sharp Edges

- **5-second timeout**: If your handler takes longer, Zalo marks it failed and retries. Always return 200 immediately, process async.
- **Wrong secret key**: Signature uses **OA Secret Key** from OA Management → Settings, NOT the App Secret Key from Developer Portal. Different keys, same name confusion.
- **Raw body required**: Parse body as raw string before verification. Using `express.json()` or Hono's `.json()` before verification will break the HMAC because the body gets re-serialized.
- **Inconsistent event naming**: `user_send_text` but just `follow` — not `user_follow`. Handle both patterns in your router.
- **HTTPS required**: Zalo rejects plain HTTP webhook URLs. ngrok/cloudflared tunnels provide HTTPS automatically.
- **msg_id deduplication is mandatory in production**: Zalo retries on non-200 (up to 3x), and network issues can cause duplicate deliveries. A Redis-backed `SETNX msg_id EX 86400` is the production-safe pattern.

---

# zalo-personal-messaging

> ⚠️ Track B (unofficial). See zalo-personal-setup for full risk disclaimer.
> This skill assumes you have completed zalo-personal-setup and have an active API instance.

## Overview

Send messages, media, and reactions to Zalo personal accounts and groups via zca-js. Covers 1:1 DMs, group messaging, mention-gated bot patterns, and context buffering.

---

## Direct Messages (1:1)

```typescript
// Send text
await api.sendMessage('Hello!', threadId, 'User')

// Send image (local file path — download first if URL)
await api.sendMessage({
  body: 'Check this image',
  attachments: [imagePath]
}, threadId, 'User')

// Chunk long messages (2000-char limit applies to DMs too)
async function sendLong(text: string, threadId: string, type: 'User' | 'Group') {
  const chunks = text.match(/.{1,1900}/gs) ?? [text]
  for (const chunk of chunks) {
    await api.sendMessage(chunk, threadId, type)
  }
}
```

---

## Group Messaging

```typescript
// Send to group
await api.sendMessage('Hello group!', groupId, 'Group')

// Send with mention
await api.sendMessage({
  body: '@John check this',
  mentions: [{ pos: 0, len: 5, uid: johnUserId }]
}, groupId, 'Group')

// Group management
await api.createGroup('Bot Test Group', [userId1, userId2]) // min 3 members incl. self
await api.addGroupMembers(groupId, [newMemberId])
await api.removeGroupMembers(groupId, [memberId])
await api.changeGroupName(groupId, 'New Name')
```

---

## Media Types

| Type | Notes |
|------|-------|
| Text | 2000-char limit — chunk if needed |
| Image | Local file path only — download URL first |
| Video | Local file path |
| Voice | Local file path |
| Sticker | By sticker ID — IDs undocumented, capture from received msgs |
| File | Local file path |
| Contact card | User ID reference |
| Link | Auto-generates preview |

---

## Reactions

```typescript
// React to a message (11 types)
await api.sendReaction(messageId, threadId, '❤️', 'User')

// Available: ❤️ 😆 😮 😢 😠 👍 👎 ✊ 🎉 😏 🥰
```

---

## Mention Gating Pattern

For group bots — only process when @mentioned, buffer other messages for context:

```typescript
function isMentioned(msg: GroupMessage, botId: string): boolean {
  return msg.data.mentions?.some(m => m.uid === botId) ?? false
}

listener.on('group_message', async (msg) => {
  if (!isMentioned(msg, BOT_USER_ID)) {
    messageBuffer.push(msg) // buffer for context
    return
  }
  // Bot was mentioned — process with buffered context
  const context = messageBuffer.getRecent(msg.threadId, 20)
  const response = await processWithContext(msg, context)
  await api.sendMessage(response, msg.threadId, 'Group')
})
```

> Use `msg.data.mentions` array — never parse `@` from message text (unreliable).

---

## Message Buffer

Buffer recent group messages per thread for context injection:

```typescript
class MessageBuffer {
  private buffer: Map<string, Message[]> = new Map()
  private maxPerThread = 50

  push(msg: Message) {
    const threadId = msg.threadId
    const msgs = this.buffer.get(threadId) ?? []
    msgs.push(msg)
    if (msgs.length > this.maxPerThread) msgs.shift() // cap to avoid unbounded growth
    this.buffer.set(threadId, msgs)
  }

  getRecent(threadId: string, count: number): Message[] {
    return (this.buffer.get(threadId) ?? []).slice(-count)
  }
}
```

---

## Name Cache

Resolve user IDs to display names with TTL to avoid API hammering:

```typescript
class NameCache {
  private cache = new Map<string, { name: string; expiresAt: number }>()
  private ttl = 60 * 60 * 1000 // 1 hour

  async resolve(userId: string, api: ZaloApi): Promise<string> {
    const cached = this.cache.get(userId)
    if (cached && cached.expiresAt > Date.now()) return cached.name
    try {
      const profile = await api.getUserInfo(userId)
      const name = profile.displayName || 'Unknown'
      this.cache.set(userId, { name, expiresAt: Date.now() + this.ttl })
      return name
    } catch {
      return 'Unknown'
    }
  }
}
```

---

## Event Listeners

```typescript
// DM and group events are SEPARATE — wire both
listener.on('message', async (msg) => {
  // 1:1 personal messages
  const senderId = msg.data.uidFrom
  await handleDM(msg, senderId)
})

listener.on('group_message', async (msg) => {
  // Group messages — includes mention data
  const senderId = msg.data.uidFrom
  await handleGroup(msg, senderId)
})
```

---

## Sharp Edges

- **Separate events**: `message` (DM) vs `group_message` (group) — missing one = silent drop
- **Mention detection**: check `msg.data.mentions` array, not text `@` parsing
- **2000-char limit**: applies to both DM and group — always chunk
- **Image upload**: local file path only — download remote URLs before sending
- **Sticker IDs**: undocumented — sniff from received sticker messages to build your own map
- **Group create**: minimum 3 members including self — 2-member call throws
- **Buffer cap**: always set `maxPerThread` — unbounded growth crashes long-running bots
- **Name cache TTL**: don't skip — `getUserInfo` rate-limited aggressively on personal accounts

---

# zalo-personal-setup

## Purpose

Bootstrap a personal Zalo account automation using zca-js — the community-maintained reverse-engineered client. Handles first-time QR login, credential persistence, WebSocket listener setup, and session restore on subsequent runs.

<HARD-GATE>
This skill uses UNOFFICIAL reverse-engineered APIs via zca-js.
BEFORE proceeding, acknowledge ALL risks:
1. ToS VIOLATION — Zalo can ban your account without warning
2. SINGLE SESSION — cannot use Zalo mobile/web simultaneously
3. API INSTABILITY — Zalo can break internal APIs anytime
4. NO SUPPORT — Zalo will not help with issues from unofficial usage
5. NOT FOR PRODUCTION — personal projects and prototypes ONLY

If building for business/production → use Track A (zalo-oa-setup) instead.
</HARD-GATE>

## Step 1 — Install Dependency

```bash
npm install zca-js
# zca-js: https://github.com/RFS-ADRENO/zca-js (359★, 202 forks)
```

Minimum Node.js: 18+. TypeScript users add `@types/node` if not already present.

## Step 2 — QR Login (First Run)

```typescript
import { Zalo } from 'zca-js'

const zalo = new Zalo()

// First-time login: QR code
const api = await zalo.loginQR()
// Terminal displays QR → scan with Zalo mobile app
// Returns API instance with full access

// Save credentials for next time
const credentials = {
  imei: api.getImei(),         // generated device ID
  cookie: api.getCookie(),      // session cookies
  userAgent: api.getUserAgent() // browser fingerprint
}
await saveCredentials(credentials)
```

QR code expires in ~60 seconds — scan quickly. After scan, zca-js completes handshake and returns a live API instance.

## Step 3 — Credential Persistence

```typescript
import { readFile, writeFile, chmod } from 'fs/promises'
import { join } from 'path'
import { homedir } from 'os'

const CRED_PATH = join(homedir(), '.zalo-personal', 'credentials.json')

async function saveCredentials(creds: ZaloCredentials): Promise<void> {
  await writeFile(CRED_PATH, JSON.stringify(creds, null, 2))
  await chmod(CRED_PATH, 0o600) // owner-only read/write
}

async function loadCredentials(): Promise<ZaloCredentials | null> {
  try {
    return JSON.parse(await readFile(CRED_PATH, 'utf-8'))
  } catch { return null }
}
```

Store at `~/.zalo-personal/credentials.json` — outside the project repo. Never commit credentials to git. Add `.zalo-personal/` to `.gitignore`.

## Step 4 — Session Restore (Subsequent Runs)

```typescript
const creds = await loadCredentials()

const api = creds
  ? await zalo.login({
      imei: creds.imei,
      cookie: creds.cookie,
      userAgent: creds.userAgent
    })
  : await zalo.loginQR() // fall back to QR if no saved creds

// Always re-persist after login — cookies may have refreshed
await saveCredentials({
  imei: api.getImei(),
  cookie: api.getCookie(),
  userAgent: api.getUserAgent()
})
```

## Step 5 — WebSocket Listener

```typescript
const listener = api.listener
await listener.start({ retryOnClose: true })

listener.on('message', (msg) => {
  // Handle incoming DMs
  console.log(`[DM] ${msg.data.content}`)
})

listener.on('group_message', (msg) => {
  // Group messages arrive on separate event
  console.log(`[Group] ${msg.data.content}`)
})

// keepAlive is automatic via zca-js — no manual ping needed
```

`retryOnClose: true` enables automatic reconnect using the retry schedule provided by Zalo's server.

## Session Management Notes

| Concept | Detail |
|---------|--------|
| IMEI | Deterministic UUID from userAgent — acts as device fingerprint. Must stay consistent across restarts. |
| Cookies | Auto-refreshed on keepAlive. Always re-persist after each session start. |
| DuplicateConnection (3000) | Another session opened — this one closes. Cannot run bot + Zalo mobile simultaneously. |
| Reconnect | Handled by zca-js via server retry schedule. No manual logic needed. |

## Anti-Detection Baseline

- Use consistent `userAgent` across sessions — don't randomize on each run
- Don't send messages too fast (see `zalo-rate-guard` for throttle patterns)
- Avoid running during unusual hours (3–6 AM local time)
- Keep sessions long-lived — frequent login/logout is suspicious
- Never change profile info programmatically

## Sharp Edges

- Cookie refresh happens on keepAlive — **MUST** persist updated cookies after every session start, not just first login
- IMEI must stay consistent — changing it looks like a new device to Zalo's backend
- If Zalo mobile is active on same account, bot receives `DuplicateConnection` kick immediately
- zca-js depends on Zalo's internal undocumented API — breaks without warning on Zalo updates
- No official rate limits documented — err heavily on the side of caution

## Mesh Links

- `zalo-oa-setup` — Track A (official OA API) if this use case grows to production
- `zalo-rate-guard` — rate limiting and message throttle for personal bots
- `zalo-personal-messaging` — send/reply DMs and group messages once session is live

---

# zalo-rate-guard

Shared rate limiting layer for both Track A (OA API) and Track B (Personal via zca-js).
Zalo has **undocumented rate limits** — no official RPM/QPM numbers published.
Exceeding limits: throttled (429) → warned → OA suspended / account banned.
Neither `zalo-php-sdk`, `zalo-java-sdk`, nor `zca-js` implement any rate limiting.
This skill fills that gap.

---

## Estimated Safe Limits

**Track A — OA API:**

| Endpoint | Safe RPM | Burst | Notes |
|----------|----------|-------|-------|
| Send CS message | 200 | 10 | Per OA, includes all message types |
| Send broadcast | 50 | 5 | Monthly quota based on follower count |
| Get user profile | 300 | 20 | Cacheable — use name cache |
| Get follower list | 100 | 10 | Paginated, cache results |
| Upload media | 60 | 5 | Large payloads, slower |
| Global | 500 | 30 | Total across all endpoints |

**Track B — Personal (zca-js):**

| Action | Safe RPM | Burst | Notes |
|--------|----------|-------|-------|
| Send message (DM) | 30 | 5 | Much lower than OA — personal account |
| Send message (group) | 20 | 3 | Groups are more scrutinized |
| Friend operations | 10 | 2 | Add/remove friend is very sensitive |
| Profile lookups | 60 | 10 | Less sensitive, still cache |
| Global | 100 | 15 | Err on side of caution |

---

## Token Bucket Implementation

```typescript
import PQueue from 'p-queue'

interface RateLimitConfig {
  rpm: number        // requests per minute
  burst: number      // max concurrent
  retryAfter: number // ms to wait on 429
}

const LIMITS: Record<string, RateLimitConfig> = {
  'oa:send_message':   { rpm: 200, burst: 10, retryAfter: 5000 },
  'oa:broadcast':      { rpm: 50,  burst: 5,  retryAfter: 10000 },
  'oa:get_profile':    { rpm: 300, burst: 20, retryAfter: 3000 },
  'oa:upload':         { rpm: 60,  burst: 5,  retryAfter: 5000 },
  'personal:send_dm':  { rpm: 30,  burst: 5,  retryAfter: 10000 },
  'personal:send_grp': { rpm: 20,  burst: 3,  retryAfter: 15000 },
  'personal:friend':   { rpm: 10,  burst: 2,  retryAfter: 30000 },
}

export class ZaloRateLimiter {
  private queues = new Map<string, PQueue>()

  constructor() {
    for (const [key, config] of Object.entries(LIMITS)) {
      this.queues.set(key, new PQueue({
        concurrency: config.burst,
        intervalCap: config.rpm,
        interval: 60_000, // per minute window
      }))
    }
  }

  async execute<T>(endpoint: string, fn: () => Promise<T>): Promise<T> {
    const queue = this.queues.get(endpoint)
    if (!queue) throw new Error(`Unknown endpoint: ${endpoint}`)
    return queue.add(fn) as Promise<T>
  }

  queueSize(endpoint: string): number {
    return this.queues.get(endpoint)?.size ?? 0
  }

  pending(endpoint: string): number {
    return this.queues.get(endpoint)?.pending ?? 0
  }
}
```

---

## Exponential Backoff on 429

```typescript
export async function withBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error: any) {
      const isRateLimit = error?.status === 429 || error?.error_code === 429
      if (!isRateLimit || attempt === maxRetries) throw error
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000
      console.warn(`[zalo-rate-guard] Rate limited. Retry ${attempt + 1}/${maxRetries} in ${Math.round(delay)}ms`)
      await new Promise(r => setTimeout(r, delay))
    }
  }
  throw new Error('Unreachable')
}
```

---

## Quota Monitoring (OA Broadcast)

Broadcast quota is a **hard monthly limit** — exceeding it silently drops messages, no error returned.

```typescript
interface QuotaTracker {
  monthly_limit: number  // based on follower count + OA level
  used: number
  resets_at: Date        // 1st of each month
}

export function canBroadcast(tracker: QuotaTracker, recipientCount: number): boolean {
  const remaining = tracker.monthly_limit - tracker.used
  if (recipientCount > remaining) {
    console.error(
      `[zalo-rate-guard] Broadcast quota insufficient: need ${recipientCount}, have ${remaining}/${tracker.monthly_limit}`
    )
    return false
  }
  return true
}

export function trackBroadcastUsed(tracker: QuotaTracker, sent: number): QuotaTracker {
  return { ...tracker, used: tracker.used + sent }
}
```

---

## Integration Pattern

```typescript
// Singleton — shared across the app
export const limiter = new ZaloRateLimiter()

// Track A: OA message send with rate limiting
export async function sendOaMessage(userId: string, text: string) {
  return limiter.execute('oa:send_message', () =>
    withBackoff(() =>
      oaApiCall('/message/cs', {
        recipient: { user_id: userId },
        message: { text },
      })
    )
  )
}

// Track B: Personal DM with rate limiting + human jitter
export async function sendPersonalMessage(threadId: string, text: string) {
  const jitter = 500 + Math.random() * 1500 // 500–2000ms
  await new Promise(r => setTimeout(r, jitter))
  return limiter.execute('personal:send_dm', () =>
    withBackoff(() => api.sendMessage(text, threadId, 'User'))
  )
}

// Track B: Friend operation — highest-risk, extra jitter
export async function addFriend(userId: string) {
  const jitter = 2000 + Math.random() * 3000 // 2–5s
  await new Promise(r => setTimeout(r, jitter))
  return limiter.execute('personal:friend', () =>
    withBackoff(() => api.sendFriendRequest(userId), 2, 5000)
  )
}
```

---

## Anti-Ban Strategies

**Track A (OA):**
1. Stay under safe RPM limits (table above)
2. Exponential backoff on ALL 429 responses — never retry immediately
3. Cache user profiles — avoid repeated lookups for the same user
4. Spread broadcasts over time — don't burst the entire follower list at once
5. Monitor quota before each broadcast batch — stop before hitting monthly limit
6. Use `appsecret_proof` on all requests — proves you're the legitimate app owner

**Track B (Personal):**
1. Much lower limits than OA — personal accounts are watched more closely
2. Add human-like jitter: 500–2000ms random delay between messages (not optional)
3. Avoid 3–6 AM (VN timezone) — traffic at those hours flags automated activity
4. Never change profile info programmatically — triggers manual review
5. Friend operations are highest-risk — max 10 RPM, prefer lower in practice
6. Keep sessions long-lived — repeated login/logout is a strong ban signal
7. Use a consistent device fingerprint (`userAgent` + `IMEI`) per account
8. On `DuplicateConnection` (error 3000): wait 30s before reconnecting, never spam reconnects

---

## Sharp Edges

- Rate limits are **estimated** — Zalo does not publish official numbers; treat all figures as conservative targets
- `p-queue` `intervalCap` applies per window, not per request — test behavior under burst
- 429 without backoff = accelerating toward ban, not slowing down
- Broadcast quota overflow **silently drops messages** — no 429, no error, just lost sends
- Stale cached profile data is acceptable; hitting rate limits for fresh data is not
- Personal account friend operations are the single highest-risk action — handle with care
- Human jitter for personal track is a survival strategy, not a nice-to-have

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)